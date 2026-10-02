from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import joblib
import os
import pandas as pd
from app.api.routes import prediction
from app.core.config import settings
from app.utils.logging_config import setup_logging
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global model variable
model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model at startup and clean up at shutdown"""
    global model
    
    # Startup: Load model
    model_path = settings.MODEL_PATH
    logger.info(f"Loading model from {model_path}")
    
    try:
        model = joblib.load(model_path)
        logger.info("Model loaded successfully")
        
        # Verify model works by making a test prediction
        test_df = pd.DataFrame({
            'carpet_area_sqft': [1000],
            'floor_num': [3],
            'Bathroom': [2],
            'Balcony': [1],
            'location_grouped': ['Other'],
            'Furnishing': ['Furnished'],
            'Transaction': ['Resale'],
            'Ownership': ['Freehold'],
            'facing': ['North']
        })
        test_pred = model.predict(test_df)
        logger.info(f"Test prediction successful: {test_pred[0]:.2f}")
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise
    
    yield
    
    # Shutdown: Clean up if needed
    logger.info("Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="House Price Prediction API",
    description="ML API for predicting house prices in India",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prediction.router, tags=["prediction"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "House Price Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "predict": "/api/predict"
        }
    }
