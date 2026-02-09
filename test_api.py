"""
Script pour tester l'API FastAPI.
"""

import requests
import json

# URL de l'API
BASE_URL = "http://localhost:8000"

def test_root():
    """Test de la route racine."""
    print("\n" + "="*60)
    print("TEST 1: Route racine (/)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    print(" Test réussi")

def test_health():
    """Test du health check."""
    print("\n" + "="*60)
    print("TEST 2: Health check (/health)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200
    assert response.json()['status'] in ['healthy', 'degraded']
    print(" Test réussi")

def test_model_info():
    """Test des infos du modèle."""
    print("\n" + "="*60)
    print("TEST 3: Model info (/model-info)")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/model-info")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Model: {data['model_name']}")
        print(f"Type: {data['model_type']}")
        print(f"R²: {data['metrics']['test_r2']:.4f}")
        print(" Test réussi")
    else:
        print(f" Warning: {response.status_code} - {response.text}")

def test_predict():
    """Test de prédiction."""
    print("\n" + "="*60)
    print("TEST 4: Prediction (/predict)")
    print("="*60)
    
    # Données de test
    house_data = {
        "MedInc": 8.3,
        "HouseAge": 41.0,
        "AveRooms": 6.98,
        "AveBedrms": 1.02,
        "Population": 322.0,
        "AveOccup": 2.55,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    
    response = requests.post(f"{BASE_URL}/predict", json=house_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Prix prédit: {data['predicted_price_formatted']}")
        print(f"Confiance: {data['confidence']}")
        print(" Test réussi")
    else:
        print(f" Erreur: {response.text}")
        assert False

def test_predict_batch():
    """Test de prédiction batch."""
    print("\n" + "="*60)
    print("TEST 5: Prediction batch (/predict-batch)")
    print("="*60)
    
    # Liste de maisons
    houses = [
        {
            "MedInc": 8.3,
            "HouseAge": 41.0,
            "AveRooms": 6.98,
            "AveBedrms": 1.02,
            "Population": 322.0,
            "AveOccup": 2.55,
            "Latitude": 37.88,
            "Longitude": -122.23
        },
        {
            "MedInc": 2.5,
            "HouseAge": 25.0,
            "AveRooms": 4.5,
            "AveBedrms": 1.0,
            "Population": 500.0,
            "AveOccup": 3.0,
            "Latitude": 34.05,
            "Longitude": -118.25
        }
    ]
    
    response = requests.post(f"{BASE_URL}/predict-batch", json=houses)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Nombre de prédictions: {data['count']}")
        for i, pred in enumerate(data['predictions'], 1):
            print(f"  {i}. {pred['predicted_price_formatted']}")
        print(" Test réussi")
    else:
        print(f" Erreur: {response.text}")

if __name__ == "__main__":
    print("\n TEST DE L'API FASTAPI")
    print("="*60)
    print("Assurez-vous que l'API tourne sur http://localhost:8000")
    print("="*60)
    
    try:
        test_root()
        test_health()
        test_model_info()
        test_predict()
        test_predict_batch()
        
        print("\n" + "="*60)
        print(" TOUS LES TESTS SONT PASSÉS !")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n ERREUR: Impossible de se connecter à l'API")
        print("Assurez-vous que l'API tourne avec: python api/main.py")
    
    except AssertionError as e:
        print(f"\n Test échoué: {e}")
    
    except Exception as e:
        print(f"\n Erreur inattendue: {e}")