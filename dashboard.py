import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from src.data_processing.supply_chain_loader import (
    load_supply_chain_data, 
    calculate_supply_chain_metrics,
    get_supplier_performance
)
from src.ai_insights.operations_analyzer import generate_risk_analysis
from src.visualizations.supply_chain_viz import (
    create_logistics_performance_chart,
    create_risk_heatmap,
    create_shipping_method_analysis,
    create_cost_impact_donut,
    create_delivery_performance_gauge,
    create_delivery_status_summary,
    create_logistics_partner_comparison,
    create_cost_by_warehouse
)

# Page config
st.set_page_config(
    page_title="AI Operations Intelligence Platform",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (copy from your sales app and modify colors)
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🏭 AI Operations Intelligence Platform</h1>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return load_supply_chain_data()

# Sidebar navigation (adapt from your sales app)
with st.sidebar:
    st.header("🚀 Navigation")
    
    page = st.selectbox("Choose Analysis", [
        "📈 Operations Overview",
        "⚠️ Supply Chain Risk", 
        "📊 Performance Analytics",  
        "📦 Inventory Management",
        "💰 Cost Optimization",
        "🤖 AI Insights"
    ])
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    # Add quick metrics here

# Main content area
def main():
    df = load_data()
    debug_data_info(df) 
    
    if df.empty:
        st.error("No data loaded. Please check data file.")
        return
    
    if page == "📈 Operations Overview":
        show_operations_overview(df)
    elif page == "⚠️ Supply Chain Risk":
        show_supply_chain_risk(df)
    elif page == "📊 Performance Analytics": 
        show_performance_analytics(df)        
    elif page == "📦 Inventory Management":
        show_inventory_management(df)
    elif page == "💰 Cost Optimization":
        show_cost_optimization(df)
    elif page == "🤖 AI Insights":
        show_ai_insights(df)

def show_operations_overview(df):
    st.header("📈 Operations Overview")
    
    metrics = calculate_supply_chain_metrics(df)
    
    # First row - basic counts
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Suppliers", metrics.get('total_suppliers', 0))
    with col2:
        st.metric("Total Products", metrics.get('total_products', 0))
    with col3:
        st.metric("Total Warehouses", metrics.get('total_warehouses', 0))
    with col4:
        st.metric("Logistics Partners", metrics.get('total_logistics_partners', 0))
    
    # Second row - performance metrics
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        st.metric("Total Cost", f"${metrics.get('total_cost', 0):,.0f}")
    with col6:
        completed_rate = metrics.get('completed_delivery_rate', 0)
        st.metric("Completed Deliveries", f"{completed_rate:.1f}%")
    with col7:
        on_track_rate = metrics.get('on_track_rate', 0) 
        st.metric("On-Track Orders", f"{on_track_rate:.1f}%")
    with col8:
        overall_performance = metrics.get('overall_performance_rate', 0)
        if overall_performance > 80:
            st.metric("Overall Status", "🟢 Excellent", f"{overall_performance:.1f}%")
        elif overall_performance > 60:
            st.metric("Overall Status", "🟡 Good", f"{overall_performance:.1f}%")
        else:
            st.metric("Overall Status", "🔴 Needs Attention", f"{overall_performance:.1f}%")
    
    # Third row - problem areas
    col9, col10, col11, col12 = st.columns(4)
    with col9:
        overdue_rate = metrics.get('overdue_rate', 0)
        st.metric("⚠️ Overdue Orders", f"{overdue_rate:.1f}%")
    with col10:
        delayed_rate = metrics.get('delayed_rate', 0)
        st.metric("🔴 Delayed Orders", f"{delayed_rate:.1f}%")
    with col11:
        avg_delivery = metrics.get('avg_delivery_time', 0)
        st.metric("Avg Delivery Time", f"{avg_delivery:.1f} days")
    with col12:
        # Risk indicator
        risk_score = overdue_rate + delayed_rate
        if risk_score < 10:
            st.metric("Risk Level", "🟢 Low")
        elif risk_score < 25:
            st.metric("Risk Level", "🟡 Medium")
        else:
            st.metric("Risk Level", "🔴 High")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.8em; margin-top: 2rem;'>
        📊 Data: <a href='https://www.kaggle.com/datasets/discovertalent143/supply-chain-dataset' target='_blank'>Kaggle Supply Chain Dataset</a> (dates updated for demo)
        </div>
        """, 
        unsafe_allow_html=True
    )


def show_supply_chain_risk(df):
    """Display focused Supply Chain Risk Analysis"""
    
    st.header("⚠️ Supply Chain Risk Analysis")
    st.markdown("AI-powered risk identification and mitigation strategies")
    
    # AI Risk Analysis Section
    st.subheader("🤖 AI-Powered Risk Analysis")
    insights = generate_risk_analysis(df)
    for insight in insights:
        st.markdown(insight)
    
    # Recommended Actions Section
    st.subheader("📋 Recommended Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Immediate Actions:**
        • Review delayed shipments with logistics partners
        • Implement performance monitoring alerts  
        • Consider backup logistics options
        """)
    
    with col2:
        st.markdown("""
        **Strategic Improvements:**
        • Renegotiate contracts with underperforming partners
        • Diversify logistics partner portfolio
        • Implement predictive delay alerts
        """)
    
    st.markdown("---")
    
    # Risk Visualizations (focused on problems only)
    st.subheader("🔍 Risk Analysis")
    
    col3, col4 = st.columns(2)
    
    with col3:
        risk_heatmap = create_risk_heatmap(df)
        if risk_heatmap:
            st.plotly_chart(risk_heatmap, use_container_width=True)
    
    with col4:
        partner_chart = create_logistics_partner_comparison(df)
        if partner_chart:
            st.plotly_chart(partner_chart, use_container_width=True)
    
    # Risk Summary
    col5, col6 = st.columns(2)
    
    with col5:
        logistics_chart = create_logistics_performance_chart(df)
        if logistics_chart:
            st.plotly_chart(logistics_chart, use_container_width=True)
    
    with col6:
        cost_chart = create_cost_impact_donut(df)
        if cost_chart:
            st.plotly_chart(cost_chart, use_container_width=True)

def show_performance_analytics(df):
    """Display Performance Analytics page"""
    
    st.header("📊 Performance Analytics")
    st.markdown("Comprehensive performance monitoring and delivery analysis")
    
    # Performance Overview Section
    st.subheader("🎯 Overall Performance")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        gauge_chart = create_delivery_performance_gauge(df)
        if gauge_chart:
            st.plotly_chart(gauge_chart, use_container_width=True)
    
    with col2:
        st.markdown("#### 📋 Delivery Status Summary")
        summary_table = create_delivery_status_summary(df)
        if summary_table is not None:
            st.dataframe(summary_table, use_container_width=True, hide_index=True)
    
    # Detailed Analytics Section
    st.markdown("---")
    st.subheader("📈 Detailed Performance Analysis")
    
    col3, col4 = st.columns(2)
    
    with col3:
        shipping_chart = create_shipping_method_analysis(df)
        if shipping_chart:
            st.plotly_chart(shipping_chart, use_container_width=True)
    
    with col4:
        warehouse_chart = create_cost_by_warehouse(df)
        if warehouse_chart:
            st.plotly_chart(warehouse_chart, use_container_width=True)
    
    # Performance Insights
    st.markdown("---")
    st.subheader("💡 Performance Insights")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        delivered_rate = len(df[df['Delivery Status'] == 'Delivered']) / len(df) * 100
        st.metric("Delivery Success Rate", f"{delivered_rate:.1f}%")
    
    with col6:
        avg_cost = df['Total Cost'].mean()
        st.metric("Average Order Cost", f"${avg_cost:,.0f}")
    
    with col7:
        best_method = df.groupby('Shipping Method')['Delivery Status'].apply(
            lambda x: (x == 'Delivered').mean()
        ).idxmax()
        st.metric("Best Shipping Method", best_method)
        
# Placeholder functions for other pages
def show_inventory_management(df):
    st.header("📦 Inventory Management")
    st.info("Coming soon - Predictive inventory optimization")

def show_cost_optimization(df):
    st.header("💰 Cost Optimization")
    st.info("Coming soon - AI cost optimization recommendations")

def show_ai_insights(df):
    st.header("🤖 AI Insights")
    st.info("Coming soon - Natural language business insights")

def debug_data_info(df):
    st.sidebar.markdown("### 🔍 Debug Info")
    st.sidebar.write(f"Data loaded at: {datetime.now().strftime('%H:%M:%S')}")
    st.sidebar.write(f"Total rows: {len(df)}")
    
    if 'Delivery Date' in df.columns:
        st.sidebar.write(f"Date range: {df['Delivery Date'].min()} to {df['Delivery Date'].max()}")
        st.sidebar.write(f"Today: {pd.Timestamp.now().normalize()}")
    
    if 'Delivery Status' in df.columns:
        status_counts = df['Delivery Status'].value_counts()
        st.sidebar.write("**Original Status:**")
        for status, count in status_counts.items():
            st.sidebar.write(f"  {status}: {count}")
    
    # Show performance categories if available
    if 'Performance_Category' in df.columns:
        perf_counts = df['Performance_Category'].value_counts()
        st.sidebar.write("**Performance Categories:**")
        for category, count in perf_counts.items():
            st.sidebar.write(f"  {category}: {count}")


if __name__ == "__main__":
    main()
