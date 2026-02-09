"""
Endpoints de l'API.
"""

from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import pandas as pd
import numpy as np
import json
from pathlib import Path
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schemas import HouseFeatures, PredictionResponse, ModelInfo, HealthResponse
from dependencies import get_model, get_preprocessor

# Créer le router
router = APIRouter()

# Chemin vers les métadonnées
BASE_DIR = Path(__file__).resolve().parent.parent
METADATA_PATH = BASE_DIR / "models" / "model_metadata.json"


@router.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """
    Vérifie que l'API fonctionne.
    """
    try:
        model = get_model()
        preprocessor = get_preprocessor()
        model_loaded = model is not None and preprocessor is not None
    except Exception:
        model_loaded = False
    
    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        timestamp=datetime.now().isoformat()
    )


@router.get("/model-info", response_model=ModelInfo, tags=["Model"])
def get_model_info():
    """
    Retourne les informations sur le modèle.
    """
    try:
        # Charger les métadonnées
        if not METADATA_PATH.exists():
            raise HTTPException(status_code=404, detail="Métadonnées du modèle non trouvées")
        
        with open(METADATA_PATH, 'r') as f:
            metadata = json.load(f)
        
        return ModelInfo(
            model_name=metadata['model_name'],
            model_type=metadata['model_type'],
            version=metadata['training_date'][:10],
            metrics=metadata['metrics'],
            n_features=metadata['n_features'],
            features=metadata['features']
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des métadonnées: {str(e)}")


@router.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_price(
    house: HouseFeatures,
    model=Depends(get_model),
    preprocessor=Depends(get_preprocessor)
):
    """
    Prédit le prix d'une maison.
    
    Args:
        house: Caractéristiques de la maison
    
    Returns:
        PredictionResponse: Prix prédit et informations
    """
    try:
        # Convertir en DataFrame
        input_data = pd.DataFrame([house.model_dump()])
        
        # Preprocessing (feature engineering + scaling)
        processed_data = preprocessor.transform(input_data)
        
        # Prédiction
        prediction = model.predict(processed_data)[0]
        
        # Formater le prix
        price_in_thousands = prediction * 100  # Convertir en milliers
        formatted_price = f"${price_in_thousands:.2f}k"
        
        # Déterminer la confiance (basé sur la plage de prix)
        if prediction < 1.5:
            confidence = "high"
        elif prediction < 4.0:
            confidence = "medium"
        else:
            confidence = "low"
        
        return PredictionResponse(
            predicted_price=float(prediction),
            predicted_price_formatted=formatted_price,
            confidence=confidence,
            features_used=house.model_dump()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction: {str(e)}")


@router.post("/predict-batch", tags=["Prediction"])
def predict_batch(houses: list[HouseFeatures], model=Depends(get_model), preprocessor=Depends(get_preprocessor)):
    """
    Prédit les prix pour plusieurs maisons.
    
    Args:
        houses: Liste de caractéristiques de maisons
    
    Returns:
        list: Liste de prédictions
    """
    try:
        predictions = []
        
        for house in houses:
            # Convertir en DataFrame
            input_data = pd.DataFrame([house.model_dump()])
            
            # Preprocessing
            processed_data = preprocessor.transform(input_data)
            
            # Prédiction
            prediction = model.predict(processed_data)[0]
            
            # Formater
            price_in_thousands = prediction * 100
            formatted_price = f"${price_in_thousands:.2f}k"
            
            predictions.append({
                "predicted_price": float(prediction),
                "predicted_price_formatted": formatted_price,
                "features": house.model_dump()
            })
        
        return {
            "count": len(predictions),
            "predictions": predictions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction batch: {str(e)}")