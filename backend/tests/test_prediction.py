import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import json

client = TestClient(app)

def test_health():
    """Test health endpoint"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data

def test_predict_success():
    """Test prediction with valid input"""
    request_data = {
        "location": "Mumbai",
        "carpet_area_sqft": 1200.0,
        "floor_num": 3,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "North"
    }
    
    response = client.post("/api/v1/predict", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "predicted_price" in data
    assert isinstance(data["predicted_price"], float)
    assert data["predicted_price"] > 0

def test_predict_invalid_furnishing():
    """Test prediction with invalid furnishing value"""
    request_data = {
        "location": "Mumbai",
        "carpet_area_sqft": 1200.0,
        "floor_num": 3,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Invalid Value",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "North"
    }
    
    response = client.post("/api/v1/predict", json=request_data)
    assert response.status_code == 422  # Validation error

def test_predict_negative_area():
    """Test prediction with negative carpet area"""
    request_data = {
        "location": "Mumbai",
        "carpet_area_sqft": -100.0,
        "floor_num": 3,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "North"
    }
    
    response = client.post("/api/v1/predict", json=request_data)
    assert response.status_code == 422  # Validation error

def test_predict_unknown_location():
    """Test prediction with location not in training set (should map to 'Other')"""
    request_data = {
        "location": "UnknownCity123",
        "carpet_area_sqft": 1200.0,
        "floor_num": 3,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Furnished",
        "transaction": "Resale",
        "ownership": "Freehold",
        "facing": "North"
    }
    
    response = client.post("/api/v1/predict", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "predicted_price" in data

def test_predict_missing_field():
    """Test prediction with missing required field"""
    request_data = {
        "location": "Mumbai",
        "carpet_area_sqft": 1200.0,
        "floor_num": 3,
        "bathroom": 2,
        "balcony": 1,
        "furnishing": "Furnished",
        "transaction": "Resale"
        # ownership is missing
    }
    
    response = client.post("/api/v1/predict", json=request_data)
    assert response.status_code == 422  # Validation error

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data