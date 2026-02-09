"""
API FastAPI pour la prediction de prix immobiliers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import des routers (imports relatifs)
from endpoints import router

# Créer l'application FastAPI
app = FastAPI(
    title="Real Estate Price Predictor API",
    description="API de prediction de prix immobiliers avec ML",
    version="1.0.0"
)

# CORS (pour permettre les appels depuis un frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod, limiter aux domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(router)

# Route racine
@app.get("/")
def root():
    """Page d'accueil de l'API."""
    return {
        "message": "Welcome to Real Estate Price Predictor API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)