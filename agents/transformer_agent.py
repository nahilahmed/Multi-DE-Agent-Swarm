import pandas as pd
import json

class TransformerAgent:
    def __init__(self):
        pass

    def clean_data(self, raw_data):
        # Convert JSON string to DataFrame
        df = pd.read_json(raw_data)

        # Fill missing product name
        df["Product Name"] = df["Product Name"].fillna("Unknown")

        # Convert Quantity to numeric, invalid -> NaN -> 0
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce').fillna(0).astype(int)

        # Fill missing Price with 0
        df["Price"] = pd.to_numeric(df["Price"], errors='coerce').fillna(0)

        # Clean & standardize date
        df["Sale Date"] = pd.to_datetime(df["Sale Date"], errors='coerce')

        # Drop rows where Sale Date is invalid
        df = df.dropna(subset=["Sale Date"])

        return df.to_json(orient="records")