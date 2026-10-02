import pandas as pd
import numpy as np
import json
import os
from app.core.config import settings
from app.schemas.prediction import PredictionRequest
import logging

logger = logging.getLogger(__name__)

# Load valid locations at module import
try:
    with open(settings.LOCATIONS_PATH, 'r') as f:
        VALID_LOCATIONS = set(json.load(f))
    logger.info(f"Loaded {len(VALID_LOCATIONS)} valid locations")
except FileNotFoundError:
    logger.warning(f"Locations file not found at {settings.LOCATIONS_PATH}")
    VALID_LOCATIONS = set()

def preprocess_input(request: PredictionRequest) -> pd.DataFrame:
    """
    Convert PredictionRequest to a DataFrame with proper column names
    and handle location mapping (unknown -> 'Other')
    
    Args:
        request: PredictionRequest object
        
    Returns:
        pd.DataFrame with columns matching training data
    """
    # Map location to 'Other' if not in valid locations
    location = request.location_grouped
    if VALID_LOCATIONS and location not in VALID_LOCATIONS:
        logger.info(f"Location '{location}' not in training set, mapping to 'Other'")
        location = 'Other'
    
    # Create DataFrame with exact column order used in training
    data = {
        'carpet_area_sqft': [request.carpet_area_sqft],
        'floor_num': [request.floor_num],
        'Bathroom': [request.Bathroom],
        'Balcony': [request.Balcony],
        'location_grouped': [location],
        'Furnishing': [request.Furnishing],
        'Transaction': [request.Transaction],
        'Ownership': [request.Ownership],
        'facing': [request.facing if request.facing else 'Unknown']
    }
    
    df = pd.DataFrame(data)
    
    # Ensure all columns are of correct type
    df['carpet_area_sqft'] = df['carpet_area_sqft'].astype(float)
    df['floor_num'] = df['floor_num'].astype(int)
    df['Bathroom'] = df['Bathroom'].astype(int)
    df['Balcony'] = df['Balcony'].astype(int)
    df['location_grouped'] = df['location_grouped'].astype(str)
    df['Furnishing'] = df['Furnishing'].astype(str)
    df['Transaction'] = df['Transaction'].astype(str)
    df['Ownership'] = df['Ownership'].astype(str)
    df['facing'] = df['facing'].astype(str)
    
    logger.debug(f"Preprocessed input DataFrame:\n{df}")
    
    return df

def get_valid_locations() -> list:
    """Get list of valid locations for frontend dropdown"""
    return sorted(list(VALID_LOCATIONS)) if VALID_LOCATIONS else []

def validate_input(request: PredictionRequest) -> tuple[bool, str]:
    """Additional validation beyond Pydantic"""
    # Check if location is valid (warning only)
    if request.location not in VALID_LOCATIONS:
        logger.warning(f"Location '{request.location_grouped}' not in training set")
    
    # Check for reasonable carpet area
    if request.carpet_area_sqft < 100 or request.carpet_area_sqft > 10000:
        return False, "Carpet area should be between 100 and 10,000 sqft"
    
    # Check for reasonable price per sqft (will be handled by model)
    return True, ""