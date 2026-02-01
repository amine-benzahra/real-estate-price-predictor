"""
Module pour charger les données California Housing.

Ce module fournit des fonctions pour charger et accéder
au dataset California Housing de scikit-learn.
"""
from sklearn.datasets import fetch_california_housing
import pandas as pd
from typing import List


def load_california_housing_data() -> pd.DataFrame:
    
    california = fetch_california_housing(as_frame=True)
    df = california.frame
    return df


def get_feature_names() -> List[str]:
    
    return [
        'MedInc',      # Median income in block group
        'HouseAge',    # Median house age in block group
        'AveRooms',    # Average number of rooms per household
        'AveBedrms',   # Average number of bedrooms per household
        'Population',  # Block group population
        'AveOccup',    # Average number of household members
        'Latitude',    # Block group latitude
        'Longitude'    # Block group longitude
    ]


def get_target_name() -> str:
    """
    Retourne le nom de la variable target (à prédire).
    
    """
    return 'MedHouseVal'


def get_feature_descriptions() -> dict:
    """
    Retourne les descriptions détaillées de chaque feature.
    
    Returns:
        dict: Dictionnaire {feature_name: description}
    """
    return {
        'MedInc': 'Median income in block group (in tens of thousands $)',
        'HouseAge': 'Median house age in block group (in years)',
        'AveRooms': 'Average number of rooms per household',
        'AveBedrms': 'Average number of bedrooms per household',
        'Population': 'Block group population',
        'AveOccup': 'Average number of household members',
        'Latitude': 'Block group latitude',
        'Longitude': 'Block group longitude',
        'MedHouseVal': 'Median house value (in hundreds of thousands $)'
    }


if __name__ == "__main__":
    # Test du module
    print(" Test du module load_data.py")
    print("=" * 60)
    
    # Charger les données
    df = load_california_housing_data()
    print(f"\n Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    
    # Afficher les features
    features = get_feature_names()
    print(f"\n Features ({len(features)}) :")
    for feature in features:
        print(f"  • {feature}")
    
    # Afficher la target
    target = get_target_name()
    print(f"\n Target : {target}")
    
    # Afficher les descriptions
    descriptions = get_feature_descriptions()
    print(f"\n Descriptions :")
    for name, desc in descriptions.items():
        print(f"  • {name}: {desc}")