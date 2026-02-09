"""
Schemas Pydantic pour validation des donnees.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class HouseFeatures(BaseModel):
    """Features d'une maison pour prediction."""
    
    MedInc: float = Field(..., ge=0, description="Median income (en 10k$)")
    HouseAge: float = Field(..., ge=0, le=100, description="Age median des maisons (annees)")
    AveRooms: float = Field(..., ge=0, description="Nombre moyen de pieces")
    AveBedrms: float = Field(..., ge=0, description="Nombre moyen de chambres")
    Population: float = Field(..., ge=0, description="Population du quartier")
    AveOccup: float = Field(..., ge=0, description="Nombre moyen d'occupants")
    Latitude: float = Field(..., ge=32, le=42, description="Latitude")
    Longitude: float = Field(..., ge=-125, le=-114, description="Longitude")
    
    class Config:
        json_schema_extra = {
            "example": {
                "MedInc": 8.3,
                "HouseAge": 41.0,
                "AveRooms": 6.98,
                "AveBedrms": 1.02,
                "Population": 322.0,
                "AveOccup": 2.55,
                "Latitude": 37.88,
                "Longitude": -122.23
            }
        }

class PredictionResponse(BaseModel):
    """Reponse de prediction."""
    
    predicted_price: float = Field(..., description="Prix predit (en 100k$)")
    predicted_price_formatted: str = Field(..., description="Prix formate")
    confidence: Optional[str] = Field(None, description="Niveau de confiance")
    features_used: Dict[str, float] = Field(..., description="Features utilisees")
    
class ModelInfo(BaseModel):
    """Informations sur le modele."""
    
    model_name: str
    model_type: str
    version: str
    metrics: Dict[str, float]
    n_features: int
    features: List[str]

class HealthResponse(BaseModel):
    """Reponse health check."""
    
    status: str
    model_loaded: bool
    timestamp: str