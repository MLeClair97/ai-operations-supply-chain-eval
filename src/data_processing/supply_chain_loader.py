import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, Any

@st.cache_data
def load_supply_chain_data() -> pd.DataFrame:
    """Load and preprocess supply chain operations data"""
    try:
        # Load the CSV file
        df = pd.read_csv('data/Supply_Chain_Logistics_Dataset.csv')
        
        # Basic data cleaning (adapt based on actual column names)
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
def calculate_supply_chain_metrics(df):
    try:
        today = pd.Timestamp.now().normalize()  # Today at midnight
        
        # Basic counts
        basic_metrics = {
            'total_suppliers': df['Supplier'].nunique(),
            'total_products': df['Product'].nunique(),
            'total_warehouses': df['Warehouse Location'].nunique(),
            'total_logistics_partners': df['Logistics Partner'].nunique(),
            'total_cost': df['Total Cost'].sum()
        }
        
        # Enhanced delivery analysis
        if 'Delivery Date' in df.columns and 'Delivery Status' in df.columns:
            df['Delivery Date'] = pd.to_datetime(df['Delivery Date'])
            
            # Classify delivery performance
            conditions = [
                # Delivered items (actual performance)
                (df['Delivery Status'] == 'Delivered'),
                
                # In progress but on-track (expected delivery >= today)
                ((df['Delivery Status'].isin(['In Transit', 'Pending'])) & 
                 (df['Delivery Date'] >= today)),
                
                # Overdue (in progress but past expected delivery date)
                ((df['Delivery Status'].isin(['In Transit', 'Pending'])) & 
                 (df['Delivery Date'] < today)),
                
                # Explicitly delayed
                (df['Delivery Status'] == 'Delayed')
            ]
            
            choices = ['Delivered', 'On-Track', 'Overdue', 'Delayed']
            df['Performance_Category'] = pd.Series(
                pd.Categorical(
                    np.select(conditions, choices, default='Unknown'),
                    categories=['Delivered', 'On-Track', 'Overdue', 'Delayed', 'Unknown']
                )
            )
            
            # Calculate performance metrics
            total_orders = len(df)
            delivered_count = len(df[df['Performance_Category'] == 'Delivered'])
            on_track_count = len(df[df['Performance_Category'] == 'On-Track'])
            overdue_count = len(df[df['Performance_Category'] == 'Overdue'])
            delayed_count = len(df[df['Performance_Category'] == 'Delayed'])
            
            # Performance rates
            delivery_metrics = {
                'completed_delivery_rate': (delivered_count / total_orders * 100) if total_orders > 0 else 0,
                'on_track_rate': (on_track_count / total_orders * 100) if total_orders > 0 else 0,
                'overdue_rate': (overdue_count / total_orders * 100) if total_orders > 0 else 0,
                'delayed_rate': (delayed_count / total_orders * 100) if total_orders > 0 else 0,
                
                # Overall performance score (delivered + on-track)
                'overall_performance_rate': ((delivered_count + on_track_count) / total_orders * 100) if total_orders > 0 else 0,
                
                # Average delivery time for completed orders only
                'avg_delivery_time': df[df['Performance_Category'] == 'Delivered']['Delivery Date'].dt.day.mean() if delivered_count > 0 else 0
            }
        else:
            delivery_metrics = {
                'completed_delivery_rate': 0,
                'on_track_rate': 0,
                'overdue_rate': 0, 
                'delayed_rate': 0,
                'overall_performance_rate': 0,
                'avg_delivery_time': 0
            }
        
        # Combine all metrics
        metrics = {**basic_metrics, **delivery_metrics}
        return metrics
    
    except Exception as e:
        st.error(f"Error calculating metrics: {str(e)}")
        return {}

def get_supplier_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze supplier performance with logistics metrics"""
    try:
        if 'Supplier' not in df.columns:
            return pd.DataFrame()
        
        supplier_metrics = df.groupby('Supplier').agg({
            'Total Cost': ['sum', 'mean'],
            'Quantity': 'sum',
            'Unit Price': 'mean',
            'Delivery Status': lambda x: (x == 'Delivered').mean() * 100,  # On-time delivery rate
            'Logistics Partner': 'nunique',  # Number of logistics partners used
            'Shipping Method': lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else 'Unknown'  # Most used shipping method
        }).round(2)
        
        # Flatten column names
        supplier_metrics.columns = [
            'Total_Cost_Sum', 'Total_Cost_Mean', 'Total_Quantity', 'Avg_Unit_Price',
            'On_Time_Delivery_Rate', 'Logistics_Partners_Used', 'Primary_Shipping_Method'
        ]
        supplier_metrics = supplier_metrics.reset_index()
        
        # Add performance score (combination of cost and delivery performance)
        supplier_metrics['Performance_Score'] = (
            supplier_metrics['On_Time_Delivery_Rate'] * 0.6 +  # 60% weight on delivery
            (100 - (supplier_metrics['Total_Cost_Mean'] / supplier_metrics['Total_Cost_Mean'].max() * 100)) * 0.4  # 40% weight on cost efficiency
        ).round(1)
        
        return supplier_metrics.sort_values('Performance_Score', ascending=False)
    
    except Exception as e:
        st.error(f"Error analyzing suppliers: {str(e)}")
        return pd.DataFrame()
    
def get_logistics_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze logistics partner performance"""
    try:
        if 'Logistics Partner' not in df.columns:
            return pd.DataFrame()
        
        logistics_metrics = df.groupby('Logistics Partner').agg({
            'Delivery Status': [
                lambda x: (x == 'Delivered').mean() * 100,  # On-time rate
                lambda x: (x == 'Delayed').mean() * 100,    # Delay rate
                lambda x: (x == 'Pending').mean() * 100     # Pending rate
            ],
            'Total Cost': ['sum', 'mean'],
            'Shipping Method': lambda x: x.value_counts().index[0],  # Most used method
            'Supplier': 'nunique'  # Number of suppliers served
        }).round(2)
        
        # Flatten column names
        logistics_metrics.columns = [
            'Delivery_Rate', 'Delay_Rate', 'Pending_Rate',
            'Total_Cost_Sum', 'Avg_Cost', 'Primary_Method', 'Suppliers_Served'
        ]
        logistics_metrics = logistics_metrics.reset_index()
        
        # Calculate reliability score
        logistics_metrics['Reliability_Score'] = (
            logistics_metrics['Delivery_Rate'] - logistics_metrics['Delay_Rate']
        ).round(1)
        
        return logistics_metrics.sort_values('Reliability_Score', ascending=False)
    
    except Exception as e:
        st.error(f"Error analyzing logistics partners: {str(e)}")
        return pd.DataFrame()