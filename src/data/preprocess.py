import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from src.features.engineering import add_engineered_features

class DataPreprocessor:
    def __init__(self, target_name='MedHouseVal'):
        self.target_name = target_name
        self.scaler = RobustScaler()
        self.feature_names = None
    
    def fit_transform(self, df, test_size=0.2, random_state=42):
        print("Feature Engineering...")
        df_processed = add_engineered_features(df)
        
        print("Cap outliers...")
        for col in ['AveRooms', 'AveBedrms', 'Population', 'AveOccup']:
            if col in df_processed.columns:
                lower = df_processed[col].quantile(0.01)
                upper = df_processed[col].quantile(0.99)
                df_processed[col] = df_processed[col].clip(lower, upper)
        
        X = df_processed.drop(columns=[self.target_name])
        y = df_processed[self.target_name]
        self.feature_names = X.columns.tolist()
        
        print("Train/Test Split...")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        print("Scaling...")
        self.scaler.fit(X_train)
        X_train_scaled = pd.DataFrame(self.scaler.transform(X_train), columns=X_train.columns, index=X_train.index)
        X_test_scaled = pd.DataFrame(self.scaler.transform(X_test), columns=X_test.columns, index=X_test.index)
        
        print(f"Done! Train: {X_train_scaled.shape[0]}, Test: {X_test_scaled.shape[0]}")
        return X_train_scaled, X_test_scaled, y_train, y_test
    
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