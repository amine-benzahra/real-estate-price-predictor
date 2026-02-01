"""
Module pour les requêtes MongoDB courantes.

Ce module fournit des fonctions prêtes à l'emploi pour
effectuer des requêtes fréquentes sur la collection properties.
"""
from typing import List, Dict, Any, Optional
from pymongo.collection import Collection


def find_expensive_properties(
    collection: Collection,
    price_threshold: float = 5.0,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Trouve les propriétés au-dessus d'un certain prix.
    
    Args:
        collection: Collection MongoDB
        price_threshold: Prix minimum (en centaines de milliers $)
        limit: Nombre maximum de résultats
    
    Returns:
        list: Liste de documents
    """
    query = {"MedHouseVal": {"$gt": price_threshold}}
    projection = {
        "MedInc": 1,
        "MedHouseVal": 1,
        "Latitude": 1,
        "Longitude": 1,
        "price_category": 1
    }
    
    return list(collection.find(query, projection).limit(limit))


def get_properties_by_price_category(
    collection: Collection,
    category: str
) -> int:
    """
    Compte les propriétés dans une catégorie de prix.
    
    Args:
        collection: Collection MongoDB
        category: 'low', 'medium', ou 'high'
    
    Returns:
        int: Nombre de propriétés
    """
    return collection.count_documents({"price_category": category})


def get_average_price_by_category(
    collection: Collection
) -> List[Dict[str, Any]]:
    """
    Calcule le prix moyen par catégorie.
    
    Args:
        collection: Collection MongoDB
    
    Returns:
        list: Liste avec stats par catégorie
    """
    pipeline = [
        {
            "$group": {
                "_id": "$price_category",
                "count": {"$sum": 1},
                "avg_price": {"$avg": "$MedHouseVal"},
                "avg_income": {"$avg": "$MedInc"},
                "avg_rooms": {"$avg": "$AveRooms"}
            }
        },
        {
            "$sort": {"_id": 1}
        }
    ]
    
    return list(collection.aggregate(pipeline))


def get_top_expensive_zones(
    collection: Collection,
    top_n: int = 10
) -> List[Dict[str, Any]]:
    """
    Trouve les zones géographiques les plus chères.
    
    Args:
        collection: Collection MongoDB
        top_n: Nombre de zones à retourner
    
    Returns:
        list: Top zones avec prix moyen
    """
    pipeline = [
        {
            "$project": {
                "lat_zone": {"$round": ["$Latitude", 0]},
                "lon_zone": {"$round": ["$Longitude", 0]},
                "MedHouseVal": 1
            }
        },
        {
            "$group": {
                "_id": {
                    "lat": "$lat_zone",
                    "lon": "$lon_zone"
                },
                "avg_price": {"$avg": "$MedHouseVal"},
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gt": 100}
            }
        },
        {
            "$sort": {"avg_price": -1}
        },
        {
            "$limit": top_n
        }
    ]
    
    return list(collection.aggregate(pipeline))


def search_properties_by_criteria(
    collection: Collection,
    min_income: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rooms: Optional[float] = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """
    Recherche de propriétés selon plusieurs critères.
    
    Args:
        collection: Collection MongoDB
        min_income: Revenu minimum
        max_price: Prix maximum
        min_rooms: Nombre minimum de pièces
        limit: Nombre maximum de résultats
    
    Returns:
        list: Propriétés matchant les critères
    """
    query = {}
    
    if min_income is not None:
        query["MedInc"] = {"$gte": min_income}
    
    if max_price is not None:
        query["MedHouseVal"] = {"$lte": max_price}
    
    if min_rooms is not None:
        query["AveRooms"] = {"$gte": min_rooms}
    
    return list(collection.find(query).limit(limit))


if __name__ == "__main__":
    # Test du module
    from src.database.mongodb import MongoDBConnection
    
    print("🧪 Test du module queries.py")
    print("=" * 60)
    
    mongo = MongoDBConnection()
    db = mongo.connect()
    
    if db:
        collection = db['properties']
        
        # Test 1
        print("\n📌 Test 1 : Propriétés chères")
        expensive = find_expensive_properties(collection, 5.0, 5)
        print(f"Trouvées : {len(expensive)}")
        
        # Test 2
        print("\n📌 Test 2 : Comptage par catégorie")
        for cat in ['low', 'medium', 'high']:
            count = get_properties_by_price_category(collection, cat)
            print(f"  {cat.capitalize()}: {count:,}")
        
        # Test 3
        print("\n📌 Test 3 : Prix moyen par catégorie")
        stats = get_average_price_by_category(collection)
        for stat in stats:
            print(f"  {stat['_id']}: ${stat['avg_price']*100:.0f}k")
        
        mongo.close()