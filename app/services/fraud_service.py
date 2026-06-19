import joblib
import json
from sqlalchemy.orm import Session
from app.db.models import TransactionRecord
import numpy as np
import pandas as pd
import logging
import uuid
from typing import Optional
from pathlib import Path
from app.models.schemas import TransactionInput, FraudPredictionResponse

logger = logging.getLogger(__name__)

# Paths to saved artifacts
ARTIFACTS_PATH = Path(__file__).parent.parent / "ml" / "artifacts"


class FraudDetectionService:
    """Handles loading ML artifacts and running fraud predictions."""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self._load_artifacts()

    def _load_artifacts(self):
        """Load model, scaler, and feature columns from disk."""
        try:
            self.model = joblib.load(ARTIFACTS_PATH / "fraud_model.pkl")
            self.scaler = joblib.load(ARTIFACTS_PATH / "scaler.pkl")
            self.feature_columns = joblib.load(
                ARTIFACTS_PATH / "feature_columns.pkl"
            )
            logger.info("ML artifacts loaded successfully.")
        except FileNotFoundError as e:
            logger.error(f"Artifact not found: {e}")
            raise RuntimeError(f"Failed to load ML artifacts: {e}")

    def _get_risk_level(self, probability: float) -> str:
        """Convert fraud probability to business risk tier."""
        if probability < 0.3:
            return "LOW"
        elif probability < 0.7:
            return "MEDIUM"
        else:
            return "HIGH"

    def _get_message(self, is_fraud: bool, risk_level: str) -> str:
        """Generate human-readable decision message."""
        if not is_fraud:
            return f"Transaction approved. Risk level: {risk_level}."
        messages = {
            "MEDIUM": "Transaction flagged for review. Step-up verification required.",
            "HIGH": "Transaction blocked. High fraud probability detected."
        }
        return messages.get(risk_level, "Transaction flagged.")
    
    def _check_business_rules(self, transaction: TransactionInput) -> Optional[str]:
       """
           Apply deterministic business rules that should override or
           augment pure ML probability, based on known fraud patterns
           that may be underrepresented in training data.
       """
       if transaction.Amount == 0:
            return "Zero-amount transaction detected — possible card-testing fraud."
       return None

    def predict(
        self, transaction: TransactionInput, db: Session
    ) -> FraudPredictionResponse:
        """Run fraud prediction on a single transaction and persist the result."""
        try:
            # Convert input to DataFrame preserving exact column order
            input_dict = transaction.model_dump()
            input_df = pd.DataFrame([input_dict])[self.feature_columns]

            # Scale Time and Amount using the fitted scaler
            input_df[["Time", "Amount"]] = self.scaler.transform(
                input_df[["Time", "Amount"]]
            )

            # Get fraud probability for class 1 (fraud)
            fraud_probability = float(
                self.model.predict_proba(input_df)[0][1]
            )
            is_fraud = fraud_probability >= 0.5
            risk_level = self._get_risk_level(fraud_probability)

            # Apply business rules on top of ML prediction
            business_flag = self._check_business_rules(transaction)
            if business_flag:
                risk_level = "HIGH" if risk_level == "LOW" else risk_level
                logger.warning(f"Business rule triggered: {business_flag}")

            logger.info(
                f"Prediction complete. "
                f"fraud_probability={fraud_probability:.4f}, "
                f"is_fraud={is_fraud}"
            )

            message = self._get_message(is_fraud, risk_level)
            if business_flag:
                message = f"{message} Note: {business_flag}"

            transaction_id = str(uuid.uuid4())

            # Persist this prediction to the database for audit trail
            # and future retraining purposes
            record = TransactionRecord(
                transaction_id=transaction_id,
                amount=transaction.Amount,
                transaction_hour=transaction.Transaction_Hour,
                account_age_days=transaction.Account_Age_Days,
                raw_input=json.dumps(input_dict),
                fraud_probability=round(fraud_probability, 4),
                is_fraud=is_fraud,
                risk_level=risk_level,
                message=message,
            )
            db.add(record)
            db.commit()

            return FraudPredictionResponse(
                transaction_id=transaction_id,
                is_fraud=is_fraud,
                fraud_probability=round(fraud_probability, 4),
                risk_level=risk_level,
                message=message
            )

        except Exception as e:
            db.rollback()
            logger.error(f"Prediction failed: {e}")
            raise