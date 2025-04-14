import pandas as pd
from io import StringIO
from datetime import datetime

class ValidatorAgent:
    def __init__(self):
        self.min_date = datetime(2020, 1, 1).timestamp() * 1000  # Convert to milliseconds Unix timestamp
        self.max_date = datetime.now().timestamp() * 1000  # Current time in milliseconds Unix timestamp

    def validate_data(self, cleaned_data):
        """Validate the cleaned data for business rules."""
        # Convert JSON string to DataFrame
        df = pd.read_json(StringIO(cleaned_data))
        
        validation_errors = []
        
        # Validate each row
        for index, row in df.iterrows():
            # Check if Product Name is not empty
            if pd.isna(row['Product Name']) or row['Product Name'].strip() == '':
                validation_errors.append(f"Row {index}: Product Name cannot be empty")
            
            # Check if Quantity is non-negative
            if row['Quantity'] < 0:
                validation_errors.append(f"Row {index}: Quantity cannot be negative")
            
            # Check if Price is non-negative
            if row['Price'] < 0:
                validation_errors.append(f"Row {index}: Price cannot be negative")
            
            # Check if Sale Date is within valid range
            if row['Sale Date'] < self.min_date:
                validation_errors.append(f"Row {index}: Sale Date cannot be before 2020-01-01")
            if row['Sale Date'] > self.max_date:
                validation_errors.append(f"Row {index}: Sale Date cannot be in the future")
        
        # Return validation results
        if validation_errors:
            return {
                "is_valid": False,
                "errors": validation_errors
            }
        else:
            return {
                "is_valid": True,
                "message": "All data is valid"
            }