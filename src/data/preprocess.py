# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import RobustScaler
# from src.features.engineering import add_engineered_features

# class DataPreprocessor:
#     def __init__(self, target_name='MedHouseVal'):
#         self.target_name = target_name
#         self.scaler = RobustScaler()
#         self.feature_names = None
    
#     def fit_transform(self, df, test_size=0.2, random_state=42):
#         print("Feature Engineering...")
#         df_processed = add_engineered_features(df)
        
#         print("Cap outliers...")
#         for col in ['AveRooms', 'AveBedrms', 'Population', 'AveOccup']:
#             if col in df_processed.columns:
#                 lower = df_processed[col].quantile(0.01)
#                 upper = df_processed[col].quantile(0.99)
#                 df_processed[col] = df_processed[col].clip(lower, upper)
        
#         X = df_processed.drop(columns=[self.target_name])
#         y = df_processed[self.target_name]
#         self.feature_names = X.columns.tolist()
        
#         print("Train/Test Split...")
#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
#         print("Scaling...")
#         self.scaler.fit(X_train)
#         X_train_scaled = pd.DataFrame(self.scaler.transform(X_train), columns=X_train.columns, index=X_train.index)
#         X_test_scaled = pd.DataFrame(self.scaler.transform(X_test), columns=X_test.columns, index=X_test.index)
        
#         print(f"Done! Train: {X_train_scaled.shape[0]}, Test: {X_test_scaled.shape[0]}")
#         return X_train_scaled, X_test_scaled, y_train, y_test
    
#     def get_feature_names(self):
#         return self.feature_names

# if __name__ == "__main__":
#     import sys
#     import os
#     sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
#     from src.data.load_data import load_california_housing_data
    
#     print("Test preprocess")
#     df = load_california_housing_data()
#     preprocessor = DataPreprocessor()
#     X_train, X_test, y_train, y_test = preprocessor.fit_transform(df)
#     print(f"X_train: {X_train.shape}")
#     print("OK!")

"""Module pour le preprocessing."""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from src.features.engineering import add_engineered_features


class OutlierHandler:
    def __init__(self, method='iqr', threshold=1.5, cap_percentiles=(1, 99)):
        self.method = method
        self.threshold = threshold
        self.cap_percentiles = cap_percentiles
    
    def cap_outliers(self, df, columns, inplace=False):
        if not inplace:
            df = df.copy()
        lower_pct, upper_pct = self.cap_percentiles
        for col in columns:
            if col in df.columns:
                lower_bound = df[col].quantile(lower_pct / 100)
                upper_bound = df[col].quantile(upper_pct / 100)
                df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        return df


class DataPreprocessor:
    def __init__(self, target_name='MedHouseVal'):
        self.target_name = target_name
        self.scaler = RobustScaler()
        self.outlier_handler = OutlierHandler()
        self.feature_names = None
        self._is_fitted = False
        self.cols_to_cap = ['AveRooms', 'AveBedrms', 'Population', 'AveOccup']
    
    def fit_transform(self, df, test_size=0.2, random_state=42):
        print("Feature Engineering...")
        df_processed = add_engineered_features(df, inplace=False)
        
        print("Gestion outliers...")
        df_processed = self.outlier_handler.cap_outliers(df_processed, columns=self.cols_to_cap)
        
        print("Separation features/target...")
        X = df_processed.drop(columns=[self.target_name])
        y = df_processed[self.target_name]
        self.feature_names = X.columns.tolist()
        
        print("Train/Test Split...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        print("Scaling...")
        self.scaler.fit(X_train)
        X_train_scaled = pd.DataFrame(self.scaler.transform(X_train), columns=X_train.columns, index=X_train.index)
        X_test_scaled = pd.DataFrame(self.scaler.transform(X_test), columns=X_test.columns, index=X_test.index)
        
        self._is_fitted = True
        print(f"Termine! Train: {X_train_scaled.shape[0]}, Test: {X_test_scaled.shape[0]}")
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def transform(self, df):
        """
        Transforme de nouvelles donnees (pour l'API).
        
        Args:
            df: DataFrame avec les features brutes
        
        Returns:
            DataFrame avec features transformees
        """
        if not self._is_fitted:
            raise RuntimeError("Le preprocessor doit etre fitte avec fit_transform() d'abord")
        
        # Feature engineering
        df_processed = add_engineered_features(df, inplace=False)
        
        # Cap outliers
        df_processed = self.outlier_handler.cap_outliers(df_processed, columns=self.cols_to_cap)
        
        # Supprimer target si presente
        if self.target_name in df_processed.columns:
            df_processed = df_processed.drop(columns=[self.target_name])
        
        # Verifier features
        missing = set(self.feature_names) - set(df_processed.columns)
        if missing:
            raise ValueError(f"Features manquantes: {missing}")
        
        # Reordonner colonnes
        df_processed = df_processed[self.feature_names]
        
        # Scaling
        df_scaled = pd.DataFrame(
            self.scaler.transform(df_processed),
            columns=self.feature_names,
            index=df_processed.index
        )
        
        return df_scaled
    
    def get_feature_names(self):
        return self.feature_names


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.data.load_data import load_california_housing_data
    
    print("Test preprocess")
    df = load_california_housing_data()
    preprocessor = DataPreprocessor()
    X_train, X_test, y_train, y_test = preprocessor.fit_transform(df)
    print(f"X_train: {X_train.shape}")
    print("OK!")