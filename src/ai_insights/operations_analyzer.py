import streamlit as st
import pandas as pd
from src.data_processing.supply_chain_loader import (
    load_supply_chain_data,
    calculate_supply_chain_metrics,
    get_supplier_performance
)


def generate_risk_analysis(df):
    """Generate AI-powered risk analysis"""
    try:
        # Calculate risk factors
        total_orders = len(df)
        delayed_orders = len(df[df['Delivery Status'] == 'Delayed'])
        delayed_rate = (delayed_orders / total_orders * 100) if total_orders > 0 else 0
        
        # Analyze by logistics partner
        if 'Logistics Partner' in df.columns:
            partner_performance = df.groupby('Logistics Partner')['Delivery Status'].apply(
                lambda x: (x == 'Delayed').mean() * 100
            ).round(1)
            worst_partner = partner_performance.idxmax()
            worst_rate = partner_performance.max()
            best_partner = partner_performance.idxmin()
            best_rate = partner_performance.min()
        
        # Generate insights
        insights = []
        
        # Risk level explanation
        if delayed_rate > 25:
            insights.append(f"🔴 **HIGH RISK ALERT**: {delayed_rate:.1f}% of orders are delayed ({delayed_orders} out of {total_orders} orders)")
            insights.append(f"⚠️ **Root Cause**: {worst_partner} has {worst_rate:.1f}% delay rate vs {best_partner} at {best_rate:.1f}%")
            insights.append(f"💡 **Recommendation**: Consider shifting volume from {worst_partner} to {best_partner} to reduce delays")
        elif delayed_rate > 15:
            insights.append(f"🟡 **MEDIUM RISK**: {delayed_rate:.1f}% delay rate requires monitoring")
        else:
            insights.append(f"🟢 **LOW RISK**: {delayed_rate:.1f}% delay rate is within acceptable range")
        
        # Cost impact
        delayed_cost = df[df['Delivery Status'] == 'Delayed']['Total Cost'].sum()
        total_cost = df['Total Cost'].sum()
        cost_impact = (delayed_cost / total_cost * 100) if total_cost > 0 else 0
        
        insights.append(f"💰 **Financial Impact**: ${delayed_cost:,.0f} in delayed shipments ({cost_impact:.1f}% of total cost)")
        
        return insights
    
    except Exception as e:
        return [f"Error generating risk analysis: {str(e)}"]