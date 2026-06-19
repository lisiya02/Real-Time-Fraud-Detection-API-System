from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.db.database import Base


class TransactionRecord(Base):
    """
    Database table storing every transaction submitted for fraud
    prediction, along with the model's decision, for audit trail
    and future retraining purposes.
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)

    # Key input fields worth querying on directly
    amount = Column(Float, nullable=False)
    transaction_hour = Column(Integer, nullable=False)
    account_age_days = Column(Integer, nullable=False)

    # Full input payload, stored for completeness / audit / retraining
    raw_input = Column(Text, nullable=False)

    # Prediction results
    fraud_probability = Column(Float, nullable=False)
    is_fraud = Column(Boolean, nullable=False)
    risk_level = Column(String, nullable=False)
    message = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())