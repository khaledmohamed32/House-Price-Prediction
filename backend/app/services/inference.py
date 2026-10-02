
import numpy as np
import pandas as pd

import logging

logger = logging.getLogger(__name__)

def predict_price(input_df: pd.DataFrame) -> float:
    """
    Make prediction using loaded model
    
    Args:
        input_df: DataFrame with preprocessed input features
        
    Returns:
        float: Predicted house price in rupees
    """
    from app.main import model
    if model is None:
        raise RuntimeError("Model not loaded")
    
    try:
        # Make prediction
        prediction = model.predict(input_df)
        
        # Ensure prediction is positive
        predicted_price = float(np.maximum(prediction[0], 0))
        
        return predicted_price
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise