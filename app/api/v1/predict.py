from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import TransactionInput, FraudPredictionResponse
from app.services.fraud_service import FraudDetectionService
from app.db.database import get_db
from app.core.security import verify_api_key
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
fraud_service = FraudDetectionService()


@router.post(
    "/predict",
    response_model=FraudPredictionResponse,
    summary="Predict transaction fraud",
    description="Accepts transaction details and returns fraud probability score. Requires a valid X-API-Key header.",
    dependencies=[Depends(verify_api_key)],
    responses={
        401: {
            "description": "Missing or invalid API key",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid API key."}
                }
            },
        },
        422: {
            "description": "Validation error in request body",
        },
        500: {
            "description": "Internal prediction failure",
        },
    },
)
async def predict_fraud(
    transaction: TransactionInput, db: Session = Depends(get_db)
) -> FraudPredictionResponse:
    """
    Fraud prediction endpoint. Requires a valid X-API-Key header.
    - Validates input via Pydantic schema
    - Runs ML inference via FraudDetectionService
    - Persists the prediction to the database
    - Returns fraud probability and risk level
    """
    try:
        result = fraud_service.predict(transaction, db)
        return result
    except Exception as e:
        logger.error(f"Prediction endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed.")