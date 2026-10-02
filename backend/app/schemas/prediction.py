from pydantic import BaseModel, Field, validator
from typing import Optional

class PredictionRequest(BaseModel):
    """Request schema for house price prediction"""
    
    carpet_area_sqft: float 
    floor_num: int
    Bathroom: int
    Balcony: int
    location_grouped: str
    Furnishing: str
    Transaction: str
    Ownership: str
    facing: str

    
    
    @validator('Furnishing')
    def validate_furnishing(cls, v):
        valid_values = ['Furnished', 'Semi-Furnished', 'Unfurnished']
        if v not in valid_values:
            raise ValueError(f'furnishing must be one of {valid_values}')
        return v
    
    @validator('Transaction')
    def validate_transaction(cls, v):
        valid_values = ['New Property', 'Resale']
        if v not in valid_values:
            raise ValueError(f'transaction must be one of {valid_values}')
        return v
    
    @validator('Ownership')
    def validate_ownership(cls, v):
        valid_values = ['Freehold', 'Leasehold', 'Co-operative Society']
        if v not in valid_values:
            raise ValueError(f'ownership must be one of {valid_values}')
        return v
    
    @validator('floor_num')
    def validate_floor(cls, v):
        if v < 0 or v > 50:
            raise ValueError('floor_num must be between 0 and 50')
        return v
    
    @validator('Bathroom')
    def validate_bathroom(cls, v):
        if v < 0 or v > 20:
            raise ValueError('bathroom must be between 0 and 20')
        return v
    
    @validator('Balcony')
    def validate_balcony(cls, v):
        if v < 0 or v > 20:
            raise ValueError('balcony must be between 0 and 20')
        return v

class PredictionResponse(BaseModel):
    """Response schema for house price prediction"""
    
    predicted_price: float = Field(..., description="Predicted house price in Indian Rupees", example=4500000.0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "predicted_price": 4500000.00
            }
        }