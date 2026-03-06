import pandas as pd
import snowflake.connector
from sqlalchemy import create_engine
import yaml
import os
# Replace the path to your profiles.yml
with open("C:/Users/Dell/.dbt/profiles.yml", "r") as file:
    data = yaml.safe_load(file)

# Snowflake credentials
user = data[ 'ecommerce_dbt']['outputs']['dev']['user']
password = data[ 'ecommerce_dbt']['outputs']['dev']['password']
account = data[ 'ecommerce_dbt']['outputs']['dev']['account']

warehouse = "COMPUTE_WH"
database = "ECOMMERCE_DB"
schema = "RAW"

# Create connection
conn = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)

engine = create_engine(
    f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}"
)

print("Connected to Snowflake")

# Path to the dataset folder
folder_path = "C:/Users/Dell/Desktop/Datasets/Brazilian E-Commerce Public Dataset by Olist"
# Chunk size (number of rows per batch)
chunk_size = 100_000

for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        if file_name=="olist_customers_dataset.csv":
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            table_name = os.path.splitext(file_name)[0].lower()  # Snowflake-friendly table name
            
            print(f"Uploading {file_name} ({df.shape[0]} rows) to table '{table_name}' in chunks of {chunk_size}...")
            
            # Upload in chunks
            for i in range(0, len(df), chunk_size):
                df_chunk = df.iloc[i:i+chunk_size]
                df_chunk.to_sql(
                    table_name,
                    engine,
                    index=False,
                    if_exists="append"  # append chunk by chunk
                )
                print(f"Chunk {i // chunk_size + 1} uploaded")
            
            print(f"{file_name} uploaded successfully!\n")
