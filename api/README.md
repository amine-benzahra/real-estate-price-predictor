# 🚀 Real Estate Price Predictor API

API REST pour prédire les prix immobiliers avec Machine Learning.

## 📋 Endpoints

### `GET /`
Page d'accueil de l'API avec liens vers la documentation.

### `GET /health`
Health check - vérifie que l'API et le modèle sont chargés.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-02-09T10:00:00"
}
```

### `GET /model-info`
Informations sur le modèle ML utilisé.

**Response:**
```json
{
  "model_name": "Gradient Boosting",
  "model_type": "GradientBoostingRegressor",
  "version": "2024-02-09",
  "metrics": {
    "test_r2": 0.8234,
    "test_mae": 0.3214
  },
  "n_features": 14
}
```

### `POST /predict`
Prédit le prix d'une maison.

**Request Body:**
```json
{
  "MedInc": 8.3,
  "HouseAge": 41.0,
  "AveRooms": 6.98,
  "AveBedrms": 1.02,
  "Population": 322.0,
  "AveOccup": 2.55,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

**Response:**
```json
{
  "predicted_price": 4.52,
  "predicted_price_formatted": "$452.00k",
  "confidence": "high",
  "features_used": {...}
}
```

### `POST /predict-batch`
Prédit les prix pour plusieurs maisons.

## 🚀 Lancement
```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Lancer l'API
cd api
python main.py
```

L'API sera accessible sur `http://localhost:8000`

## 📖 Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🧪 Tests
```bash
# Dans un terminal séparé
python test_api.py
```