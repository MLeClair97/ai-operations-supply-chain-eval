import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from src.data_processing.supply_chain_loader import (
    load_supply_chain_data, 
    calculate_supply_chain_metrics
)
from src.ai_insights.operations_analyzer import generate_risk_analysis
from src.visualizations.supply_chain_viz import (
    create_logistics_performance_chart,
    create_risk_heatmap,
    create_shipping_method_analysis,
    create_cost_impact_donut,
    create_delivery_status_summary,
    create_logistics_partner_comparison,
    create_cost_by_warehouse,
    create_performance_over_time, 
    create_delivery_volume_trends,
    create_inventory_by_product_chart,
    create_inventory_turnover_analysis,
    create_reorder_point_recommendations,
    create_inventory_summary_table,
    calculate_inventory_kpis,
    create_cost_breakdown_analysis,
    create_cost_efficiency_matrix,
    create_cost_savings_opportunities,
    create_logistics_performance_analysis,
    calculate_cost_optimization_kpis,
    generate_cost_optimization_recommendations,
    generate_comprehensive_ai_insights
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
    
    # Performance Insights at TOP (moved from bottom)
    st.subheader("💡 Key Performance Metrics")
    
    col1, col2, col3, col4 = st.columns(4)  # Use 4 columns for better spacing
    
    with col1:
        delivered_rate = len(df[df['Delivery Status'] == 'Delivered']) / len(df) * 100
        st.metric("Delivery Success Rate", f"{delivered_rate:.1f}%")
    
    with col2:
        avg_cost = df['Total Cost'].mean()
        st.metric("Average Order Cost", f"${avg_cost:,.0f}")
    
    with col3:
        best_method = df.groupby('Shipping Method')['Delivery Status'].apply(
            lambda x: (x == 'Delivered').mean()
        ).idxmax()
        st.metric("Best Shipping Method", best_method)
    
    with col4:
        # Add another useful metric
        total_orders = len(df)
        at_risk_orders = len(df[df['Delivery Status'].isin(['Delayed', 'Pending'])])
        st.metric("Orders Needing Attention", f"{at_risk_orders}/{total_orders}")
    
    st.markdown("---")
    
    # Performance Trends Section
    st.subheader("📈 Performance Trends")
    
    col5, col6 = st.columns([2, 1])
    
    with col5:
        performance_chart = create_performance_over_time(df)
        if performance_chart:
            st.plotly_chart(performance_chart, use_container_width=True)
    
    with col6:
        st.markdown("#### 📋 Delivery Status Summary")
        summary_table = create_delivery_status_summary(df)
        if summary_table is not None:
            st.dataframe(summary_table, use_container_width=True, hide_index=True)
    
    # Volume Trends
    volume_chart = create_delivery_volume_trends(df)
    if volume_chart:
        st.plotly_chart(volume_chart, use_container_width=True)
    
    # Detailed Analytics Section
    st.markdown("---")
    st.subheader("📈 Detailed Performance Analysis")
    
    col7, col8 = st.columns(2)
    
    with col7:
        shipping_chart = create_shipping_method_analysis(df)
        if shipping_chart:
            st.plotly_chart(shipping_chart, use_container_width=True)
    
    with col8:
        warehouse_chart = create_cost_by_warehouse(df)
        if warehouse_chart:
            st.plotly_chart(warehouse_chart, use_container_width=True)
        

def show_inventory_management(df):
    st.header("📦 Inventory Management")
    st.markdown("AI-powered inventory optimization and demand forecasting")
    
    # Calculate KPIs
    kpis = calculate_inventory_kpis(df)
    
    # KPI Row
    st.subheader("📊 Inventory Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Inventory Value", 
            f"${kpis.get('total_inventory_value', 0):,.0f}"
        )
    
    with col2:
        st.metric(
            "Total Units", 
            f"{kpis.get('total_quantity', 0):,.0f}"
        )
    
    with col3:
        st.metric(
            "Turnover Rate", 
            f"{kpis.get('turnover_rate', 0):.1f}%"
        )
    
    with col4:
        st.metric(
            "Product Lines", 
            f"{kpis.get('unique_products', 0)}"
        )
    
    st.markdown("---")
    
    # Inventory Analysis Charts
    st.subheader("📈 Inventory Analysis")
    
    col5, col6 = st.columns(2)
    
    with col5:
        product_chart = create_inventory_by_product_chart(df)
        if product_chart:
            st.plotly_chart(product_chart, use_container_width=True)
    
    with col6:
        turnover_chart = create_inventory_turnover_analysis(df)
        if turnover_chart:
            st.plotly_chart(turnover_chart, use_container_width=True)
    
    # Reorder Recommendations
    st.subheader("🎯 Reorder Point Recommendations")
    
    reorder_chart = create_reorder_point_recommendations(df)
    if reorder_chart:
        st.plotly_chart(reorder_chart, use_container_width=True)
    
    # Inventory Summary Table
    st.markdown("---")
    st.subheader("📋 Inventory Summary & ABC Analysis")
    
    st.markdown("""
                **ABC Classification Methodology:**
                Products are prioritized using a weighted scoring system that considers multiple factors:
                - **60% Total Value**: Higher-value inventory gets priority
                - **25% Inventory Turnover**: Items that move frequently are prioritized  
                - **15% Total Quantity**: Volume considerations for operational impact

                **Classifications:**
                - **Class A**: Top 20% - Critical items requiring close management and frequent monitoring
                - **Class B**: Next 30% - Important items with moderate management attention
                - **Class C**: Bottom 50% - Routine items suitable for automated reordering systems
                """)
    col7, col8 = st.columns([2, 1])
    
    with col7:
        summary_table = create_inventory_summary_table(df)
        if summary_table is not None:
            st.dataframe(summary_table, use_container_width=True, hide_index=True)
    
    with col8:
        st.markdown("#### 💡 Key Insights")
        if kpis:
            avg_price = kpis.get('avg_unit_price', 0)
            st.write(f"• Average unit price: ${avg_price:.2f}")
            
            high_value = kpis.get('high_value_items', 0)
            total = kpis.get('total_orders', 1)
            st.write(f"• High-value items: {high_value}/{total} ({high_value/total*100:.0f}%)")
            
            suppliers = kpis.get('unique_suppliers', 0)
            products = kpis.get('unique_products', 0)
            if products > 0:
                st.write(f"• Supplier diversity: {suppliers/products:.1f} suppliers per product")

def show_cost_optimization(df):
    st.header("💰 Cost Optimization")
    st.markdown("AI-powered cost analysis and savings opportunities identification")
    
    # Calculate cost KPIs
    cost_kpis = calculate_cost_optimization_kpis(df)
    
    # Cost Overview KPIs
    st.subheader("💵 Cost Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Spend", 
            f"${cost_kpis.get('total_cost', 0):,.0f}"
        )
    
    with col2:
        st.metric(
            "Average Unit Cost", 
            f"${cost_kpis.get('avg_unit_cost', 0):.2f}"
        )
    
    with col3:
        potential_savings = cost_kpis.get('potential_savings', 0)
        savings_pct = cost_kpis.get('savings_percentage', 0)
        st.metric(
            "Potential Savings",
            f"${potential_savings:,.0f}",
            f"{savings_pct:.1f}% opportunity"
        )
    
    with col4:
        delay_impact = cost_kpis.get('delay_cost_impact', 0)
        st.metric(
            "Delay Cost Impact",
            f"{delay_impact:.1f}%",
            "of total spend"
        )
    
    # AI Cost Optimization Recommendations
    st.markdown("---")
    st.subheader("🤖 AI Cost Optimization Recommendations")
    
    recommendations = generate_cost_optimization_recommendations(df)
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"{i}. {rec}")
    else:
        st.info("No specific cost optimization opportunities identified with current data.")
    
    # Cost Analysis Charts
    st.markdown("---")
    st.subheader("📊 Cost Analysis")
    
    col5, col6 = st.columns(2)
    
    with col5:
        breakdown_chart = create_cost_breakdown_analysis(df)
        if breakdown_chart:
            st.plotly_chart(breakdown_chart, use_container_width=True)
    
    with col6:
        efficiency_chart = create_cost_efficiency_matrix(df)
        if efficiency_chart:
            st.plotly_chart(efficiency_chart, use_container_width=True)
    
    # Savings Opportunities
    st.subheader("💡 Cost Savings Opportunities")
    
    savings_chart = create_cost_savings_opportunities(df)
    if savings_chart:
        st.plotly_chart(savings_chart, use_container_width=True)
    
    # Logistics Performance Analysis
    st.subheader("🚚 Logistics Performance Analysis")

    logistics_data = create_logistics_performance_analysis(df)
    if logistics_data is not None:
        st.markdown("**Logistics Partner Performance** (ranked by reliability)")
        st.dataframe(logistics_data, use_container_width=True, hide_index=True)
    
        st.markdown("""
                    **Reliability Score**: Delivery rate minus delay rate. Higher scores indicate more reliable service.
                    Note: Cost analysis not included since dataset contains material costs, not logistics fees.
                    """)
    
    # Cost Optimization Summary
    st.markdown("---")
    st.subheader("📋 Cost Optimization Summary")
    
    col7, col8 = st.columns(2)
    
    with col7:
        st.markdown("#### 🎯 Priority Actions")
        st.write("1. **Supplier Consolidation**: Focus on top 2-3 suppliers for volume discounts")
        st.write("2. **Price Standardization**: Negotiate consistent pricing across products")
        st.write("3. **Logistics Optimization**: Review shipping method cost-effectiveness")
        st.write("4. **Volume Leveraging**: Combine orders to achieve better rates")
    
    with col8:
        st.markdown("#### 📈 Expected Impact")
        if cost_kpis:
            total_cost = cost_kpis.get('total_cost', 0)
            potential = cost_kpis.get('potential_savings', 0)
            
            st.write(f"• **Current annual spend**: ${total_cost:,.0f}")
            st.write(f"• **Potential annual savings**: ${potential:,.0f}")
            if potential > 0:
                roi_months = 6  # Assume 6-month implementation
                st.write(f"• **ROI timeline**: {roi_months} months to implement")
                st.write(f"• **Monthly savings target**: ${potential/12:,.0f}")

def show_ai_insights(df):
    st.header("🤖 AI Insights")
    st.markdown("Comprehensive AI-powered analysis and strategic recommendations")
    
    # Generate comprehensive insights
    insights = generate_comprehensive_ai_insights(df)
    
    if not insights:
        st.error("Unable to generate insights from current data.")
        return
    
    # Executive Summary
    st.subheader("📊 Executive Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Key Performance Indicators")
        total_orders = len(df)
        delivered_rate = len(df[df['Delivery Status'] == 'Delivered']) / total_orders * 100
        total_cost = df['Total Cost'].sum()
        
        st.write(f"• **Order Volume**: {total_orders} transactions analyzed")
        st.write(f"• **Delivery Performance**: {delivered_rate:.1f}% success rate")
        st.write(f"• **Total Value**: ${total_cost:,.0f} in operations")
        st.write(f"• **Risk Level**: {'High' if delivered_rate < 80 else 'Medium' if delivered_rate < 90 else 'Low'}")
    
    with col2:
        st.markdown("#### 🔍 Critical Findings")
        st.write(f"• {insights['operational']['key_finding']}")
        st.write(f"• {insights['supplier_risk']['key_finding']}")
        st.write(f"• {insights['cost_optimization']['key_finding']}")
    
    # Detailed Analysis by Area
    st.markdown("---")
    st.subheader("📈 Detailed AI Analysis")
    
    # Operational Performance
    with st.expander("🏭 Operational Performance Analysis", expanded=True):
        st.write(f"**Summary**: {insights['operational']['summary']}")
        st.write(f"**Key Finding**: {insights['operational']['key_finding']}")
        st.write(f"**Recommendation**: {insights['operational']['recommendation']}")
    
    # Supplier Risk
    with st.expander("⚠️ Supplier Risk Assessment"):
        st.write(f"**Summary**: {insights['supplier_risk']['summary']}")
        st.write(f"**Key Finding**: {insights['supplier_risk']['key_finding']}")
        st.write(f"**Recommendation**: {insights['supplier_risk']['recommendation']}")
    
    # Cost Optimization
    with st.expander("💰 Cost Optimization Opportunities"):
        st.write(f"**Summary**: {insights['cost_optimization']['summary']}")
        st.write(f"**Key Finding**: {insights['cost_optimization']['key_finding']}")
        st.write(f"**Recommendation**: {insights['cost_optimization']['recommendation']}")
    
    # Inventory Management
    with st.expander("📦 Inventory Management Insights"):
        st.write(f"**Summary**: {insights['inventory']['summary']}")
        st.write(f"**Key Finding**: {insights['inventory']['key_finding']}")
        st.write(f"**Recommendation**: {insights['inventory']['recommendation']}")
    
    # Strategic Recommendations
    st.markdown("---")
    st.subheader("🎯 Strategic Action Plan")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### Immediate Actions (Next 30 Days)")
        st.write(f"1. {insights['strategic']['priority_1']}")
        st.write(f"2. {insights['strategic']['priority_2']}")
    
    with col4:
        st.markdown("#### Strategic Initiatives (Next 90 Days)")
        st.write(f"3. {insights['strategic']['priority_3']}")
        st.write(f"4. {insights['strategic']['priority_4']}")
    
    # ROI Projection
    st.markdown("---")
    st.subheader("📊 Expected Business Impact")
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.metric("Potential Cost Savings", "15-20%", "of annual spend")
    
    with col6:
        st.metric("Delivery Improvement", "25-30%", "reduction in delays")
    
    with col7:
        st.metric("Implementation Timeline", "6 months", "full ROI realization")

def debug_data_info(df):
    with st.sidebar.expander("🔍 Debug Info", expanded=False):  # Collapsed by default
        st.write(f"Data loaded at: {datetime.now().strftime('%H:%M:%S')}")
        st.write(f"Total rows: {len(df)}")
        
        if 'Delivery Date' in df.columns:
            st.write(f"Date range: {df['Delivery Date'].min()} to {df['Delivery Date'].max()}")
            st.write(f"Today: {pd.Timestamp.now().normalize()}")
        
        if 'Delivery Status' in df.columns:
            status_counts = df['Delivery Status'].value_counts()
            st.write("**Original Status:**")
            for status, count in status_counts.items():
                st.write(f"  {status}: {count}")
    

if __name__ == "__main__":
    main()
