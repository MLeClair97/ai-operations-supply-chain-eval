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

# Business Metrics
print("=== KEY BUSINESS METRICS ===")
print(f"Unique Suppliers: {df['Supplier'].nunique()}")
print(f"Unique Products: {df['Product'].nunique()}")
print(f"Unique Warehouses: {df['Warehouse Location'].nunique()}")
print(f"Unique Logistics Partners: {df['Logistics Partner'].nunique()}")
print(f"Total Cost: ${df['Total Cost'].sum():,.2f}")

# Performance Analysis
delivery_status = df['Delivery Status'].value_counts()
print("=== DELIVERY PERFORMANCE ===")
for status, count in delivery_status.items():
    pct = count / len(df) * 100
    print(f"{status}: {count} orders ({pct:.1f}%)")