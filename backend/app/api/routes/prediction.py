from fastapi import APIRouter, HTTPException, status
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.inference import predict_price
from app.services.preprocessing import preprocess_input
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict house price based on input features
    
    Args:
        request: PredictionRequest with all required features
        
    Returns:
        PredictionResponse with predicted price in rupees
    """
    try:
        logger.info(f"Received prediction request: {request.dict()}")
        
        # Convert request to DataFrame
        input_df = preprocess_input(request)
        
        # Get prediction
        predicted_price = predict_price(input_df)
        
        logger.info(f"Prediction successful: ₹{predicted_price:,.2f}")
        
        return PredictionResponse(predicted_price=predicted_price)
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {str(e)}"
        )

@router.get("/health")
async def health():
    """Health check endpoint"""
    from app.main import model
    return {
        "status": "ok",
        "model_loaded": model is not None
    }