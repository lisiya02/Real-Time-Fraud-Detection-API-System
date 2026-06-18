from pydantic import BaseModel, Field
from typing import Optional
import uuid


class TransactionInput(BaseModel):
    """Input schema for fraud prediction request."""

    # Original dataset features
    Time: float = Field(..., description="Seconds elapsed since first transaction")
    Amount: float = Field(..., ge=0, description="Transaction amount in USD")

    # PCA features from the ULB dataset
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float

    # Engineered business features
    Transaction_Hour: int = Field(..., ge=0, le=23,
                                  description="Hour of transaction (0-23)")
    Account_Age_Days: int = Field(..., ge=0,
                                  description="Age of account in days")
    Spending_Deviation: float = Field(..., ge=0,
                                      description="Deviation from normal spending pattern")
    Merchant_Risk_Score: float = Field(..., ge=0, le=1,
                                       description="Merchant risk score (0-1)")
    Device_Risk_Score: float = Field(..., ge=0, le=1,
                                     description="Device risk score (0-1)")

    class Config:
        json_schema_extra = {
            "example": {
                "Time": 406.0,
                "Amount": 149.62,
                "V1": -1.3598, "V2": -0.0728, "V3": 2.5363,
                "V4": 1.3782, "V5": -0.3383, "V6": 0.4624,
                "V7": 0.2396, "V8": 0.0987, "V9": 0.3638,
                "V10": 0.0908, "V11": -0.5516, "V12": -0.6178,
                "V13": -0.9914, "V14": -0.3111, "V15": 1.4681,
                "V16": -0.4704, "V17": 0.2080, "V18": 0.0258,
                "V19": 0.4040, "V20": 0.2514, "V21": -0.0183,
                "V22": 0.2778, "V23": -0.1105, "V24": 0.0669,
                "V25": 0.1285, "V26": -0.1891, "V27": 0.1336,
                "V28": -0.0211,
                "Transaction_Hour": 14,
                "Account_Age_Days": 365,
                "Spending_Deviation": 0.3,
                "Merchant_Risk_Score": 0.2,
                "Device_Risk_Score": 0.15
            }
        }


class FraudPredictionResponse(BaseModel):
    """Response schema for fraud prediction."""

    transaction_id: str = Field(description="Unique ID for this prediction")
    is_fraud: bool = Field(description="Whether transaction is predicted as fraud")
    fraud_probability: float = Field(description="Model confidence score (0-1)")
    risk_level: str = Field(description="LOW, MEDIUM, or HIGH risk")
    message: str = Field(description="Human readable decision explanation")


class HealthResponse(BaseModel):
    """Response schema for health check endpoint."""

    status: str
    app_name: str
    version: str