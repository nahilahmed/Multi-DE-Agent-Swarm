import pandas as pd
from sqlalchemy import create_engine

class LoaderAgent:
    def __init__(self):
        # Replace 'your_password_here' with your actual password
        self.engine = create_engine(
            "postgresql+psycopg2://nahilahmed:nahil757@localhost:5432/autogen_demo"
        )

    def load_data(self, cleaned_data):
        df = pd.read_json(cleaned_data)

        # Clean column names
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

        # Convert sale_date to string (YYYY-MM-DD)
        df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce').dt.date

        try:
            df.to_sql(
                "sales_data",
                con=self.engine,
                schema="sample_schema",
                if_exists="append",
                index=False
            )
            return "Data loaded successfully into sample_schema.sales_data in Postgres."
        except Exception as e:
            return f"Failed to load data: {str(e)}"