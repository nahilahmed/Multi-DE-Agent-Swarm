import pandas as pd
import os

class FinderAgent:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        if not os.path.exists(self.file_path):
            return f"File not found at {self.file_path}"

        df = pd.read_csv(self.file_path)
        return df.to_json(orient="records")  # Passing as JSON string for now