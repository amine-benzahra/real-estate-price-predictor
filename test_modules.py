"""Test des modules."""

import sys
import os

# Ajouter le projet au path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("=" * 60)
print("TEST DES MODULES")
print("=" * 60)

# Test 1: Load data
print("\nTest 1: Load data")
try:
    from src.data.load_data import load_california_housing_data
    df = load_california_housing_data()
    print(f"✅ OK: {df.shape}")
except Exception as e:
    print(f"❌ ERREUR: {e}")

# Test 2: Engineering
print("\nTest 2: Engineering")
try:
    from src.features.engineering import add_engineered_features
    df_enhanced = add_engineered_features(df)
    print(f"✅ OK: {df_enhanced.shape}")
except Exception as e:
    print(f"❌ ERREUR: {e}")

# Test 3: Preprocess
print("\nTest 3: Preprocess")
try:
    from src.data.preprocess import DataPreprocessor
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.fit_transform(df)
    print(f"✅ OK: Train={X_train.shape}, Test={X_test.shape}")
except Exception as e:
    print(f"❌ ERREUR: {e}")

print("\n" + "=" * 60)
print("TERMINE!")
print("=" * 60)