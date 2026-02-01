"""
Module pour gérer la connexion à MongoDB Atlas.

Ce module fournit une classe pour se connecter à MongoDB,
gérer les collections, et effectuer des opérations CRUD.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

"""
Module pour gérer la connexion à MongoDB Atlas.

Ce module fournit une classe pour se connecter à MongoDB,
gérer les collections, et effectuer des opérations CRUD.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any


class MongoDBConnection:
    """
    Gestionnaire de connexion MongoDB.
    
    Cette classe encapsule la logique de connexion à MongoDB Atlas
    et fournit des méthodes pour interagir avec la base de données.
    
    Attributes:
        mongodb_url (str): URL de connexion MongoDB
        db_name (str): Nom de la base de données
        client (MongoClient): Client MongoDB
        db (Database): Instance de la base de données
    
    Example:
        >>> mongo = MongoDBConnection()
        >>> db = mongo.connect()
        >>> collection = mongo.get_collection('properties')
        >>> count = collection.count_documents({})
        >>> mongo.close()
    """
    
    def __init__(self):
        """Initialise la configuration de connexion."""
        # Charger les variables d'environnement
        load_dotenv()
        
        self.mongodb_url = os.getenv("MONGODB_URL")
        self.db_name = os.getenv("MONGODB_DB_NAME", "real_estate")
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        
        # Vérifier que l'URL est définie
        if not self.mongodb_url:
            raise ValueError(
                "MONGODB_URL non trouvée. "
                "Vérifiez votre fichier .env"
            )
    
    def connect(self) -> Optional[Database]:
        """
        Établit la connexion à MongoDB Atlas.
        
        Returns:
            Database: Instance de la base de données si succès, None sinon
        
        Raises:
            ConnectionFailure: Si la connexion échoue
        """
        try:
            # Créer le client avec timeout
            self.client = MongoClient(
                self.mongodb_url,
                serverSelectionTimeoutMS=5000
            )
            
            # Tester la connexion
            self.client.admin.command('ping')
            
            # Sélectionner la base de données
            self.db = self.client[self.db_name]
            
            print(f" Connecté à MongoDB : {self.db_name}")
            return self.db
            
        except ServerSelectionTimeoutError:
            print(" Timeout : Impossible de se connecter à MongoDB")
            print(" Vérifiez votre connexion internet et votre IP dans MongoDB Atlas")
            return None
            
        except ConnectionFailure as e:
            print(f" Erreur de connexion MongoDB : {e}")
            return None
    
    def close(self):
        """Ferme la connexion MongoDB proprement."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            print(" Connexion MongoDB fermée")
    
    def get_collection(self, collection_name: str) -> Collection:
        """
        Retourne une collection MongoDB.
        
        Args:
            collection_name (str): Nom de la collection
        
        Returns:
            Collection: Collection MongoDB
        
        Example:
            >>> mongo = MongoDBConnection()
            >>> mongo.connect()
            >>> properties = mongo.get_collection('properties')
        """
        if self.db is None:
            self.connect()
        
        if self.db is None:
            raise ConnectionError("Impossible de se connecter à MongoDB")
        
        return self.db[collection_name]
    
    def list_collections(self) -> List[str]:
        """
        Liste toutes les collections de la base de données.
        
        Returns:
            list: Liste des noms de collections
        """
        if self.db is None:
            self.connect()
        
        if self.db is None:
            return []
        
        return self.db.list_collection_names()
    
    def drop_collection(self, collection_name: str) -> bool:
        """
        Supprime une collection complète.
        
        Args:
            collection_name (str): Nom de la collection à supprimer
        
        Returns:
            bool: True si succès, False sinon
        
        Warning:
            Cette opération est IRRÉVERSIBLE !
        """
        if self.db is None:
            self.connect()
        
        if self.db is None:
            return False
        
        try:
            self.db.drop_collection(collection_name)
            print(f" Collection '{collection_name}' supprimée")
            return True
        except Exception as e:
            print(f" Erreur lors de la suppression : {e}")
            return False
    
    def get_collection_stats(self, collection_name: str) -> Dict[str, Any]:
        """
        Retourne les statistiques d'une collection.
        
        Args:
            collection_name (str): Nom de la collection
        
        Returns:
            dict: Statistiques de la collection
        """
        collection = self.get_collection(collection_name)
        
        stats = {
            'name': collection_name,
            'count': collection.count_documents({}),
            'indexes': collection.list_indexes(),
        }
        
        return stats


# Context manager pour gérer automatiquement la connexion
class MongoDBContextManager:
    """
    Context manager pour gérer la connexion MongoDB automatiquement.
    
    Example:
        >>> with MongoDBContextManager() as db:
        ...     collection = db['properties']
        ...     count = collection.count_documents({})
        ...     print(f"Documents: {count}")
    """
    
    def __init__(self):
        self.mongo = MongoDBConnection()
    
    def __enter__(self):
        return self.mongo.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mongo.close()


if __name__ == "__main__":
    # Test du module
    print(" Test du module mongodb.py")
    print("=" * 60)
    
    # Test 1 : Connexion basique
    print("\n Test 1 : Connexion basique")
    mongo = MongoDBConnection()
    db = mongo.connect()
    
    if db is not None:
        print(f" Base de données : {mongo.db_name}")
        
        # Test 2 : Lister les collections
        print("\n Test 2 : Collections disponibles")
        collections = mongo.list_collections()
        print(f"Collections ({len(collections)}) : {collections}")
        
        # Test 3 : Obtenir une collection
        print("\n Test 3 : Accès à une collection")
        properties = mongo.get_collection('properties')
        count = properties.count_documents({})
        print(f"Documents dans 'properties' : {count:,}")
        
        # Test 4 : Stats de collection
        if count > 0:
            print("\n Test 4 : Statistiques")
            stats = mongo.get_collection_stats('properties')
            print(f"Collection : {stats['name']}")
            print(f"Documents : {stats['count']:,}")
    
    # Fermer la connexion
    mongo.close()
    
    # Test 5 : Context manager
    print("\n Test 5 : Context Manager")
    with MongoDBContextManager() as db:
        if db is not None:
            print(" Context manager fonctionne !")
            print(f"Collections : {db.list_collection_names()}")