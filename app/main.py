from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import predict
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Real-time fraud detection API using machine learning.",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(
    predict.router,
    prefix=settings.API_V1_PREFIX,
    tags=["Fraud Detection"]
)


@app.get("/health", tags=["Health"])
async def health_check():
    """Verify the API is running."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
