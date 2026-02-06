import pandas as pd
import numpy as np

def add_engineered_features(df, inplace=False):
    if not inplace:
        df = df.copy()
    df['BedroomRatio'] = df['AveBedrms'] / df['AveRooms']
    df['RoomsPerPerson'] = df['AveRooms'] / df['AveOccup']
    df['PopulationDensity'] = df['Population'] / df['AveOccup']
    df['IncomeAge'] = df['MedInc'] * df['HouseAge']
    sf_lat, sf_lon = 37.7749, -122.4194
    df['DistanceToSF'] = np.sqrt((df['Latitude'] - sf_lat)**2 + (df['Longitude'] - sf_lon)**2)
    return df

def get_engineered_feature_names():
    return ['BedroomRatio', 'RoomsPerPerson', 'PopulationDensity', 'IncomeAge', 'DistanceToSF']

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from src.data.load_data import load_california_housing_data
    
    print("Test engineering")
    df = load_california_housing_data()
    print(f"Original: {df.shape}")
    df2 = add_engineered_features(df)
    print(f"Enhanced: {df2.shape}")
    print("OK!")