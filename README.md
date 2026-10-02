# House Price Prediction - End-to-End ML Web Application

An end-to-end machine learning application that predicts house prices in India using property features. The application includes a Jupyter notebook for data exploration and model training, a FastAPI backend serving the model, and a React frontend for user interaction.

## 📋 Overview

This project demonstrates a complete ML production pipeline:
1. **Data Processing**: Clean and preprocess real-world property listings from India
2. **Model Training**: Compare multiple regression models and export the best one
3. **API Service**: Serve predictions via FastAPI with proper validation
4. **Web Interface**: User-friendly React app for entering property details and viewing predictions

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   React         │────▶│   FastAPI       │────▶│   ML Model      │
│   Frontend      │     │   Backend       │     │   (Random Forest│
│   (Port 5173)   │◀────│   (Port 8000)   │◀────│   Regressor)    │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Jupyter Notebook → EDA → Feature Engineering → Model Training │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| **Backend** | FastAPI | 0.115.0+ |
| **ML Framework** | scikit-learn | 1.5.0+ |
| **Data Processing** | pandas, numpy | 2.0.0+ |
| **Visualization** | matplotlib, seaborn | 3.7.0+ |
| **Model Serialization** | joblib | 1.3.0+ |
| **Testing** | pytest, httpx | 8.0.0+ |
| **Environment** | Python 3.11+ | |


## 📊 Dataset

**Source**: [House Price Dataset by Juhi Bhojani](https://www.kaggle.com/datasets/juhibhojani/house-price)

- **Size**: 187,000 real property listings from India
- **Features**: Location, carpet area, floor, bathrooms, furnishing status, transaction type, ownership, facing, and more
- **Target**: Property price in Indian Rupees (₹)

### Download Instructions

#### Option A: Manual Download
1. Visit the [dataset page](https://www.kaggle.com/datasets/juhibhojani/house-price)
2. Click "Download" and unzip the file
3. Place `house_prices.csv` in `notebooks/data/`

#### Option B: Kaggle CLI (Recommended)
```bash
# Install Kaggle CLI
pip install kaggle

# Download and extract
kaggle datasets download -d juhibhojani/house-price -p notebooks/data --unzip
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.11+
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/khaledmohamed32/House-Price-Prediction.git
cd House-Price-Prediction
```

### 2. Generate the Model Files

#### ⚠️ IMPORTANT: The model file (house_price.pkl) are NOT included in the GitHub repository. You must generate them by running the Jupyter notebook:

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install notebook dependencies
pip install jupyter pandas numpy scikit-learn matplotlib seaborn joblib

# Navigate to notebooks folder and run the notebook
cd notebooks
jupyter notebook house_price_model.ipynb
```
#### The notebook will automatically:
1. Load and explore the dataset
2. Perform cleaning and feature engineering
3. Train and evaluate multiple models
4. Export the model to ../backend/models/house_price.pkl

### 3. Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Install dependencies
cd ../backend
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the API server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`


## 🔧 Environment Variables

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `MODEL_PATH` | Path to trained model file | `models/house_price.pkl` |
| `LOCATIONS_PATH` | Path to locations JSON | `models/locations.json` |
| `CORS_ORIGINS` | Allowed frontend origins | `["http://localhost:5173"]` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 📡 API Reference

### Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "ok",
  "model_loaded": true
}
```

### Predict Price
```http
POST /predict
```

**Request Body**:
```json
{
  "carpet_area_sqft": 1435.0, 
  "floor_num": 3.0, 
  "Bathroom": 3.0, 
  "Balcony": 3.0, 
  "location_grouped": "bangalore", 
  "Furnishing": "Semi-Furnished", 
  "Transaction": "Resale",
  "Ownership": "Freehold", 
  "facing": "East"
}
```

**Response**:
```json
{
  "predicted_price": 6300000.0
}
```

**Example curl**:
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "carpet_area_sqft": 1435.0, 
    "floor_num": 3.0, 
    "Bathroom": 3.0, 
    "Balcony": 3.0, 
    "location_grouped": "bangalore", 
    "Furnishing": "Semi-Furnished", 
    "Transaction": "Resale",
    "Ownership": "Freehold", 
    "facing": "East"
  }'
```

## 📈 Model Performance

### Best Model: Random Forest Regressor

After comparing multiple models, Random Forest Regressor performed best:

| Metric | Value |
|--------|-------|
| **R² Score** | 0.8993 |
| **MAE** | 1,084,901 |
| **RMSE** | 4,908,212 |

### Model Comparison

| Model | R² | MAE | RMSE |
|-------|-----|-----|------|
| **Random Forest (Winner)** | 0.8993 | 1,084,901 | 4,908,212 |
| Gradient Boosting | 0.8593 | 2,425,626 | 5,802,433 |
| Linear Regression | 0.6782 | 4,614,997 | 8,776,212 |

### Feature Engineering Highlights

1. **Price Parsing**: Converted "42 Lac", "1.2 Cr", etc. to numeric values
2. **Area Standardization**: Normalized all areas to sqft (1 sqm ≈ 10.764 sqft)
3. **Floor Extraction**: Parsed "3 out of 10" into floor number
4. **Categorical Encoding**: Grouped rare locations into "Other" category
5. **Outlier Removal**: Filtered properties outside 1st-99th percentile price-per-sqft



