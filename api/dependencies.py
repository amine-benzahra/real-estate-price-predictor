"""
Dependencies pour l'API.
"""

import joblib
import os
from typing import Tuple
from pathlib import Path

# Chemins vers les modèles
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

# Variables globales pour le modèle et preprocessor
_model = None
_preprocessor = None

def load_model_and_preprocessor() -> Tuple:
    """
    Charge le modele et le preprocessor.
    
    Returns:
        tuple: (model, preprocessor)
    """
    global _model, _preprocessor
    
    # Si déjà chargé, retourner
    if _model is not None and _preprocessor is not None:
        return _model, _preprocessor
    
    # Trouver le dernier modèle
    model_files = list(MODEL_DIR.glob("best_model_*.joblib"))
    
    if not model_files:
        raise FileNotFoundError("Aucun modele trouve dans models/")
    
    # Prendre le plus récent
    latest_model = max(model_files, key=os.path.getctime)
    
    # Charger le modèle
    _model = joblib.load(latest_model)
    print(f" Modele charge : {latest_model.name}")
    
    # Charger le preprocessor
    preprocessor_path = MODEL_DIR / "preprocessor.joblib"
    _preprocessor = joblib.load(preprocessor_path)
    print(f" Preprocessor charge")
    
    return _model, _preprocessor

def get_model():
    """Dependency pour obtenir le modele."""
    model, _ = load_model_and_preprocessor()
    return model

def get_preprocessor():
    """Dependency pour obtenir le preprocessor."""
    _, preprocessor = load_model_and_preprocessor()
    return preprocessor