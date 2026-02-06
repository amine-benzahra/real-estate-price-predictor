from sklearn.datasets import fetch_california_housing
import pandas as pd

def load_california_housing_data():
    california = fetch_california_housing(as_frame=True)
    return california.frame

def get_feature_names():
    return ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']

def get_target_name():
    return 'MedHouseVal'

if __name__ == "__main__":
    print("Test load_data")
    df = load_california_housing_data()
    print(f"Shape: {df.shape}")
    print("OK!")