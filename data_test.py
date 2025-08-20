import pandas as pd

# Load the supply chain dataset (correct relative path)
df = pd.read_csv(r'data\Supply_Chain_Logistics_Dataset.csv')
print(f"Dataset shape: {df.shape}")
print(df.head())

# Data Overview
print("=== DATASET OVERVIEW ===")
print(f"Total Records: {len(df)}")
print(f"Columns: {list(df.columns)}")
print(f"\\nData Types:")
print(df.dtypes)
print(f"\\nMissing Values:")
print(df.isnull().sum())