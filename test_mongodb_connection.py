# test_mongodb_connection.py
"""
Script simple pour tester la connexion à MongoDB Atlas.
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

def test_connection():
    """Teste la connexion à MongoDB."""
    try:
        # Récupérer l'URL depuis .env
        mongodb_url = os.getenv("MONGODB_URL")
        
        if not mongodb_url:
            print("❌ ERREUR : MONGODB_URL non trouvée dans .env")
            return
        
        print("🔄 Tentative de connexion à MongoDB...")
        
        # Créer le client MongoDB
        client = MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Tester la connexion
        client.admin.command('ping')
        
        print("✅ SUCCÈS : Connexion à MongoDB Atlas réussie !")
        
        # Afficher les bases de données existantes
        databases = client.list_database_names()
        print(f"📊 Bases de données disponibles : {databases}")
        
        # Fermer la connexion
        client.close()
        print("🔒 Connexion fermée.")
        
    except Exception as e:
        print(f"❌ ERREUR de connexion : {e}")
        print("\n💡 Vérifie :")
        print("  1. Que MONGODB_URL dans .env est correct")
        print("  2. Que ton mot de passe ne contient pas de caractères spéciaux non encodés")
        print("  3. Que ton IP est autorisée dans MongoDB Atlas")

if __name__ == "__main__":
    test_connection()