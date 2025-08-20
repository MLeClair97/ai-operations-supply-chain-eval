import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any

@st.cache_data
def load_supply_chain_data() -> pd.DataFrame:
    """Load and preprocess supply chain operations data"""
    try:
        # Load the CSV file
        df = pd.read_csv('data/Supply_Chain_Operations_Dataset.csv')
        
        # Basic data cleaning (adapt based on your actual column names)
        df.columns = df.columns.str.strip()  # Remove whitespace
        
        # Convert date columns if they exist
        date_columns = [col for col in df.columns if 'date' in col.lower()]
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Convert numeric columns
        numeric_columns = [col for col in df.columns if 'price' in col.lower() or 'cost' in col.lower() or 'quantity' in col.lower()]
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def calculate_supply_chain_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate key supply chain KPIs"""
    try:
        metrics = {
            'total_suppliers': df['Supplier'].nunique() if 'Supplier' in df.columns else 0,
            'total_products': df['Product'].nunique() if 'Product' in df.columns else 0,
            'total_warehouses': df['Warehouse Location'].nunique() if 'Warehouse Location' in df.columns else 0,
            'avg_unit_price': df['Unit Price'].mean() if 'Unit Price' in df.columns else 0,
            'total_orders': len(df),
            'total_cost': df['Total Cost'].sum() if 'Total Cost' in df.columns else 0
        }
        return metrics
    
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return {}

def get_supplier_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze supplier performance metrics"""
    try:
        if 'Supplier' not in df.columns:
            return pd.DataFrame()
        
        supplier_metrics = df.groupby('Supplier').agg({
            'Total Cost': ['sum', 'mean'],
            'Quantity': 'sum',
            'Unit Price': 'mean'
        }).round(2)
        
        # Flatten column names
        supplier_metrics.columns = ['_'.join(col).strip() for col in supplier_metrics.columns]
        supplier_metrics = supplier_metrics.reset_index()
        
        return supplier_metrics
    
    except Exception as e:
        st.error(f"Error analyzing suppliers: {str(e)}")
        return pd.DataFrame()