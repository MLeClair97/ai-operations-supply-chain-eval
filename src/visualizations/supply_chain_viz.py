import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st


def create_logistics_performance_chart(df):
    """Create logistics partner performance comparison chart"""
    try:
        if 'Logistics Partner' not in df.columns or 'Delivery Status' not in df.columns:
            return None
        
        # Calculate performance metrics by logistics partner
        partner_stats = df.groupby('Logistics Partner').agg({
            'Delivery Status': [
                lambda x: (x == 'Delivered').sum(),
                lambda x: (x == 'Delayed').sum(),
                lambda x: (x == 'In Transit').sum(),
                lambda x: (x == 'Pending').sum(),
                'count'
            ]
        }).round(2)
        
        # Flatten column names
        partner_stats.columns = ['Delivered', 'Delayed', 'In_Transit', 'Pending', 'Total']
        partner_stats = partner_stats.reset_index()
        
        # Calculate percentages
        partner_stats['Delivered_Pct'] = (partner_stats['Delivered'] / partner_stats['Total'] * 100).round(1)
        partner_stats['Delayed_Pct'] = (partner_stats['Delayed'] / partner_stats['Total'] * 100).round(1)
        partner_stats['In_Transit_Pct'] = (partner_stats['In_Transit'] / partner_stats['Total'] * 100).round(1)
        partner_stats['Pending_Pct'] = (partner_stats['Pending'] / partner_stats['Total'] * 100).round(1)
        
        # Create stacked bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Delivered',
            x=partner_stats['Logistics Partner'],
            y=partner_stats['Delivered_Pct'],
            marker_color='#2E8B57',
            text=partner_stats['Delivered_Pct'].astype(str) + '%',
            textposition='inside'
        ))
        
        fig.add_trace(go.Bar(
            name='In Transit',
            x=partner_stats['Logistics Partner'],
            y=partner_stats['In_Transit_Pct'],
            marker_color='#4682B4',
            text=partner_stats['In_Transit_Pct'].astype(str) + '%',
            textposition='inside'
        ))
        
        fig.add_trace(go.Bar(
            name='Pending',
            x=partner_stats['Logistics Partner'],
            y=partner_stats['Pending_Pct'],
            marker_color='#FFD700',
            text=partner_stats['Pending_Pct'].astype(str) + '%',
            textposition='inside'
        ))
        
        fig.add_trace(go.Bar(
            name='Delayed',
            x=partner_stats['Logistics Partner'],
            y=partner_stats['Delayed_Pct'],
            marker_color='#DC143C',
            text=partner_stats['Delayed_Pct'].astype(str) + '%',
            textposition='inside'
        ))
        
        fig.update_layout(
            title='Logistics Partner Performance Comparison',
            xaxis_title='Logistics Partner',
            yaxis_title='Percentage of Orders',
            barmode='stack',
            height=400,
            showlegend=True,
            template='plotly_dark'
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Error creating logistics performance chart: {str(e)}")
        return None

def create_risk_heatmap(df):
    """Create risk assessment heatmap by supplier and logistics partner"""
    try:
        if not all(col in df.columns for col in ['Supplier', 'Logistics Partner', 'Delivery Status']):
            return None
        
        # Create pivot table for risk analysis
        risk_matrix = df.groupby(['Supplier', 'Logistics Partner']).agg({
            'Delivery Status': lambda x: (x == 'Delayed').mean() * 100,
            'Total Cost': 'sum'
        }).round(1)
        
        risk_matrix.columns = ['Delay_Rate', 'Total_Cost']
        risk_matrix = risk_matrix.reset_index()
        
        # Create pivot for heatmap
        heatmap_data = risk_matrix.pivot(
            index='Supplier', 
            columns='Logistics Partner', 
            values='Delay_Rate'
        ).fillna(0)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn_r',  # Red-Yellow-Green reversed (red = bad)
            text=heatmap_data.values,
            texttemplate="%{text:.1f}%",
            textfont={"size": 10},
            colorbar=dict(title="Delay Rate %")
        ))
        
        fig.update_layout(
            title='Risk Heatmap: Delay Rate by Supplier-Logistics Partner',
            xaxis_title='Logistics Partner',
            yaxis_title='Supplier',
            height=400,
            template='plotly_dark'
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Error creating risk heatmap: {str(e)}")
        return None

def create_shipping_method_analysis(df):
    """Analyze performance by shipping method"""
    try:
        if not all(col in df.columns for col in ['Shipping Method', 'Delivery Status', 'Total Cost']):
            return None
        
        # Calculate metrics by shipping method
        shipping_stats = df.groupby('Shipping Method').agg({
            'Delivery Status': [
                lambda x: (x == 'Delayed').mean() * 100,
                'count'
            ],
            'Total Cost': ['mean', 'sum']
        }).round(2)
        
        shipping_stats.columns = ['Delay_Rate', 'Order_Count', 'Avg_Cost', 'Total_Cost']
        shipping_stats = shipping_stats.reset_index()
        
        # Create subplot with dual y-axis - REMOVE the subplot_titles parameter
        fig = make_subplots(
            specs=[[{"secondary_y": True}]]
            # Removed: subplot_titles=('Shipping Method Performance Analysis',)
        )
        
        # Add delay rate bars
        fig.add_trace(
            go.Bar(
                name='Delay Rate %',
                x=shipping_stats['Shipping Method'],
                y=shipping_stats['Delay_Rate'],
                marker_color='#DC143C',
                text=shipping_stats['Delay_Rate'].astype(str) + '%',
                textposition='inside',
                textfont=dict(size=12, color='white')
            ),
            secondary_y=False,
        )
        
        # Add average cost line
        fig.add_trace(
            go.Scatter(
                name='Avg Cost',
                x=shipping_stats['Shipping Method'],
                y=shipping_stats['Avg_Cost'],
                mode='lines+markers',
                line=dict(color='#4682B4', width=3),
                marker=dict(size=8)
            ),
            secondary_y=True,
        )
        
        # Update axis labels
        fig.update_xaxes(title_text="Shipping Method")
        fig.update_yaxes(title_text="Delay Rate (%)", secondary_y=False)
        fig.update_yaxes(title_text="Average Cost ($)", secondary_y=True)
        
        fig.update_layout(
            title='Shipping Method Performance Analysis',  # Add title here instead
            height=450,
            template='plotly_dark',
            showlegend=True,
            margin=dict(t=60, b=40, l=50, r=50)
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Error creating shipping method analysis: {str(e)}")
        return None

def create_cost_impact_donut(df):
    """Create donut chart showing cost impact of delays"""
    try:
        if not all(col in df.columns for col in ['Delivery Status', 'Total Cost']):
            return None
        
        # Calculate cost by delivery status
        cost_by_status = df.groupby('Delivery Status')['Total Cost'].sum().reset_index()
        
        # Create donut chart
        fig = go.Figure(data=[go.Pie(
            labels=cost_by_status['Delivery Status'],
            values=cost_by_status['Total Cost'],
            hole=.4,
            marker_colors=['#2E8B57', '#DC143C', '#4682B4', '#FFD700'],
            textinfo='label+percent+value',
            texttemplate='%{label}<br>%{percent}<br>$%{value:,.0f}'
        )])
        
        fig.update_layout(
            title='Cost Distribution by Delivery Status',
            height=400,
            template='plotly_dark',
            showlegend=True,
            annotations=[dict(text='Total Cost<br>Impact', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        
        return fig
    
    except Exception as e:
        st.error(f"Error creating cost impact chart: {str(e)}")
        return None

def create_delivery_performance_gauge(df):
    """Create a performance gauge showing overall delivery health"""
    try:
        if 'Delivery Status' not in df.columns:
            return None
        
        # Calculate performance metrics
        total_orders = len(df)
        delivered = len(df[df['Delivery Status'] == 'Delivered'])
        delayed = len(df[df['Delivery Status'] == 'Delayed'])
        in_transit = len(df[df['Delivery Status'] == 'In Transit'])
        pending = len(df[df['Delivery Status'] == 'Pending'])
        
        # Calculate performance score (delivered + in transit + pending = "on track")
        on_track = delivered + in_transit + pending
        performance_score = (on_track / total_orders * 100) if total_orders > 0 else 0
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = performance_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Overall Delivery Performance"},
            delta = {'reference': 80, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            template='plotly_dark',
            font={'color': "white"}
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating performance gauge: {str(e)}")
        return None

def create_delivery_status_summary(df):
    """Create a clean summary table of delivery status"""
    try:
        if not all(col in df.columns for col in ['Delivery Status', 'Total Cost']):
            return None
        
        # Calculate summary stats
        summary = df.groupby('Delivery Status').agg({
            'Total Cost': ['count', 'sum', 'mean'],
            'Delivery Date': ['min', 'max']
        }).round(2)
        
        # Flatten column names
        summary.columns = ['Orders', 'Total_Cost', 'Avg_Cost', 'Earliest_Date', 'Latest_Date']
        summary = summary.reset_index()
        
        # Calculate percentages
        total_orders = summary['Orders'].sum()
        summary['Percentage'] = (summary['Orders'] / total_orders * 100).round(1)
        
        # Add status icons
        status_icons = {
            'Delivered': '✅',
            'Delayed': '🔴',
            'In Transit': '🚛',
            'Pending': '📦'
        }
        summary['Status'] = summary['Delivery Status'].map(status_icons) + ' ' + summary['Delivery Status']
        
        # Create a nice display table
        display_df = summary[['Status', 'Orders', 'Percentage', 'Total_Cost', 'Avg_Cost']].copy()
        display_df.columns = ['Status', 'Orders', '%', 'Total Cost ($)', 'Avg Cost ($)']
        
        return display_df
        
    except Exception as e:
        st.error(f"Error creating delivery summary: {str(e)}")
        return None

def create_logistics_partner_comparison(df):
    """Create a simple bar chart comparing logistics partners"""
    try:
        if not all(col in df.columns for col in ['Logistics Partner', 'Delivery Status']):
            return None
        
        # Calculate delay rates by partner
        partner_performance = df.groupby('Logistics Partner').agg({
            'Delivery Status': [
                lambda x: len(x),
                lambda x: (x == 'Delayed').sum(),
                lambda x: (x == 'Delayed').mean() * 100
            ]
        }).round(1)
        
        partner_performance.columns = ['Total_Orders', 'Delayed_Orders', 'Delay_Rate']
        partner_performance = partner_performance.reset_index()
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=partner_performance['Logistics Partner'],
            y=partner_performance['Delay_Rate'],
            text=partner_performance['Delay_Rate'].astype(str) + '%',
            textposition='outside',
            marker_color=['#DC143C' if x > 25 else '#FFD700' if x > 15 else '#2E8B57' 
                         for x in partner_performance['Delay_Rate']],
            name='Delay Rate %'
        ))
        
        fig.update_layout(
            title='Logistics Partner Delay Rates',
            xaxis_title='Logistics Partner',
            yaxis_title='Delay Rate (%)',
            height=350,
            template='plotly_dark',
            showlegend=False
        )
        
        # Add threshold line
        fig.add_hline(y=20, line_dash="dash", line_color="orange", 
                     annotation_text="Target: <20%")
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating partner comparison: {str(e)}")
        return None

def create_cost_by_warehouse(df):
    """Create warehouse cost analysis"""
    try:
        if not all(col in df.columns for col in ['Warehouse Location', 'Total Cost', 'Delivery Status']):
            return None
        
        # Group by warehouse
        warehouse_stats = df.groupby('Warehouse Location').agg({
            'Total Cost': 'sum',
            'Delivery Status': ['count', lambda x: (x == 'Delayed').mean() * 100]
        }).round(1)
        
        warehouse_stats.columns = ['Total_Cost', 'Total_Orders', 'Delay_Rate']
        warehouse_stats = warehouse_stats.reset_index()
        
        # Create bubble chart (size = cost, color = delay rate)
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=warehouse_stats['Warehouse Location'],
            y=warehouse_stats['Total_Orders'],
            mode='markers',
            marker=dict(
                size=warehouse_stats['Total_Cost']/1000,  # Scale for visibility
                color=warehouse_stats['Delay_Rate'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Delay Rate %"),
                sizemode='diameter',
                sizeref=2,
                line=dict(width=2, color='white')
            ),
            text=[f"Warehouse: {w}<br>Orders: {o}<br>Cost: ${c:,.0f}<br>Delay Rate: {d:.1f}%" 
                  for w, o, c, d in zip(warehouse_stats['Warehouse Location'], 
                                       warehouse_stats['Total_Orders'],
                                       warehouse_stats['Total_Cost'],
                                       warehouse_stats['Delay_Rate'])],
            hovertemplate='%{text}<extra></extra>',
            name='Warehouses'
        ))
        
        fig.update_layout(
            title='Warehouse Performance Analysis',
            xaxis_title='Warehouse Location',
            yaxis_title='Number of Orders',
            height=350,
            template='plotly_dark'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating warehouse analysis: {str(e)}")
        return None
    
def create_performance_over_time(df):
    """Create a performance trend chart showing delivery success over time"""
    try:
        if not all(col in df.columns for col in ['Delivery Date', 'Delivery Status']):
            return None
        
        # Convert delivery date and create weekly periods
        df_copy = df.copy()
        df_copy['Delivery Date'] = pd.to_datetime(df_copy['Delivery Date'])
        df_copy['Week'] = df_copy['Delivery Date'].dt.to_period('W').dt.start_time
        
        # Calculate weekly performance metrics
        weekly_stats = df_copy.groupby('Week').agg({
            'Delivery Status': [
                lambda x: (x == 'Delivered').mean() * 100,  # Success rate
                lambda x: (x == 'Delayed').mean() * 100,    # Delay rate
                lambda x: (x == 'In Transit').mean() * 100, # In transit rate
                'count'  # Total orders
            ]
        }).round(1)
        
        weekly_stats.columns = ['Success_Rate', 'Delay_Rate', 'InTransit_Rate', 'Total_Orders']
        weekly_stats = weekly_stats.reset_index()
        
        # Create multi-line chart
        fig = go.Figure()
        
        # Success rate line (primary focus)
        fig.add_trace(go.Scatter(
            x=weekly_stats['Week'],
            y=weekly_stats['Success_Rate'],
            mode='lines+markers',
            name='Delivery Success Rate',
            line=dict(color='#2E8B57', width=3),
            marker=dict(size=8),
            hovertemplate='Week: %{x}<br>Success Rate: %{y:.1f}%<extra></extra>'
        ))
        
        # Delay rate line (problem indicator)
        fig.add_trace(go.Scatter(
            x=weekly_stats['Week'],
            y=weekly_stats['Delay_Rate'],
            mode='lines+markers',
            name='Delay Rate',
            line=dict(color='#DC143C', width=2, dash='dash'),
            marker=dict(size=6),
            hovertemplate='Week: %{x}<br>Delay Rate: %{y:.1f}%<extra></extra>'
        ))
        
        # Add target line for success rate
        fig.add_hline(
            y=80, 
            line_dash="dot", 
            line_color="orange",
            annotation_text="Target: 80% Success Rate",
            annotation_position="top right"
        )
        
        # Add annotations for significant changes
        if len(weekly_stats) > 1:
            # Find week with biggest improvement/decline
            success_changes = weekly_stats['Success_Rate'].diff()
            if not success_changes.empty:
                max_change_idx = success_changes.abs().idxmax()
                if pd.notna(success_changes.iloc[max_change_idx]):
                    change_week = weekly_stats.iloc[max_change_idx]
                    change_value = success_changes.iloc[max_change_idx]
                    
                    annotation_text = f"{'Improvement' if change_value > 0 else 'Decline'}: {abs(change_value):.1f}%"
                    fig.add_annotation(
                        x=change_week['Week'],
                        y=change_week['Success_Rate'],
                        text=annotation_text,
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor="white",
                        bgcolor="rgba(0,0,0,0.8)",
                        bordercolor="white",
                        borderwidth=1
                    )
        
        fig.update_layout(
            title='Delivery Performance Trends Over Time',
            xaxis_title='Week',
            yaxis_title='Performance Rate (%)',
            height=400,
            template='plotly_dark',
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Format x-axis to show dates nicely
        fig.update_xaxes(
            tickformat='%m/%d',
            tickangle=45
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating performance over time chart: {str(e)}")
        return None

def create_delivery_volume_trends(df):
    """Create a chart showing order volume and composition over time"""
    try:
        if not all(col in df.columns for col in ['Delivery Date', 'Delivery Status']):
            return None
        
        # Convert delivery date and create weekly periods
        df_copy = df.copy()
        df_copy['Delivery Date'] = pd.to_datetime(df_copy['Delivery Date'])
        df_copy['Week'] = df_copy['Delivery Date'].dt.to_period('W').dt.start_time
        
        # Calculate weekly volume by status
        weekly_volume = df_copy.groupby(['Week', 'Delivery Status']).size().reset_index(name='Count')
        
        # Create stacked area chart
        fig = px.area(
            weekly_volume,
            x='Week',
            y='Count',
            color='Delivery Status',
            title='Order Volume and Status Distribution Over Time',
            color_discrete_map={
                'Delivered': '#2E8B57',
                'Delayed': '#DC143C',
                'In Transit': '#4682B4',
                'Pending': '#FFD700'
            }
        )
        
        fig.update_layout(
            height=350,
            template='plotly_dark',
            xaxis_title='Week',
            yaxis_title='Number of Orders',
            hovermode='x unified'
        )
        
        # Format x-axis
        fig.update_xaxes(
            tickformat='%m/%d',
            tickangle=45
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating volume trends chart: {str(e)}")
        return None
    
# Add these functions to your supply_chain_viz.py file

def create_inventory_by_product_chart(df):
    """Create inventory analysis by product"""
    try:
        if not all(col in df.columns for col in ['Product', 'Quantity', 'Total Cost']):
            return None
        
        # Calculate inventory metrics by product
        inventory_stats = df.groupby('Product').agg({
            'Quantity': ['sum', 'count', 'mean'],
            'Total Cost': ['sum', 'mean'],
            'Unit Price': 'mean'
        }).round(2)
        
        inventory_stats.columns = ['Total_Qty', 'Order_Count', 'Avg_Qty', 'Total_Value', 'Avg_Value', 'Unit_Price']
        inventory_stats = inventory_stats.reset_index()
        
        # Create bubble chart: x=quantity, y=value, size=order_count
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=inventory_stats['Total_Qty'],
            y=inventory_stats['Total_Value'],
            mode='markers',
            marker=dict(
                size=inventory_stats['Order_Count'] * 8,  # Scale for visibility
                color=inventory_stats['Unit_Price'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Unit Price ($)"),
                line=dict(width=2, color='white'),
                sizemode='diameter',
                sizeref=2
            ),
            text=[f"Product: {p}<br>Quantity: {q}<br>Value: ${v:,.0f}<br>Orders: {o}<br>Unit Price: ${up:.2f}" 
                  for p, q, v, o, up in zip(inventory_stats['Product'], 
                                          inventory_stats['Total_Qty'],
                                          inventory_stats['Total_Value'],
                                          inventory_stats['Order_Count'],
                                          inventory_stats['Unit_Price'])],
            hovertemplate='%{text}<extra></extra>',
            name='Products'
        ))
        
        fig.update_layout(
            title='Product Inventory Analysis',
            xaxis_title='Total Quantity',
            yaxis_title='Total Inventory Value ($)',
            height=400,
            template='plotly_dark'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating inventory by product chart: {str(e)}")
        return None

def create_inventory_turnover_analysis(df):
    """Create inventory turnover analysis by warehouse"""
    try:
        if not all(col in df.columns for col in ['Warehouse Location', 'Quantity', 'Total Cost', 'Delivery Status']):
            return None
        
        # Calculate turnover metrics by warehouse
        warehouse_stats = df.groupby('Warehouse Location').agg({
            'Quantity': 'sum',
            'Total Cost': 'sum',
            'Delivery Status': ['count', lambda x: (x == 'Delivered').sum()]
        }).round(2)
        
        warehouse_stats.columns = ['Total_Quantity', 'Total_Value', 'Total_Orders', 'Delivered_Orders']
        warehouse_stats = warehouse_stats.reset_index()
        
        # Calculate metrics
        warehouse_stats['Turnover_Rate'] = (warehouse_stats['Delivered_Orders'] / warehouse_stats['Total_Orders'] * 100).round(1)
        warehouse_stats['Avg_Order_Size'] = (warehouse_stats['Total_Quantity'] / warehouse_stats['Total_Orders']).round(1)
        
        # Create the chart with manual x-positions for proper grouping
        fig = go.Figure()
        
        # Create custom x-positions for grouped bars
        x_positions = list(range(len(warehouse_stats)))
        x_labels = warehouse_stats['Warehouse Location'].tolist()
        
        # Add turnover rate bars (left side of each group)
        fig.add_trace(go.Bar(
            name='Turnover Rate (%)',
            x=[x - 0.2 for x in x_positions],  # Shift left
            y=warehouse_stats['Turnover_Rate'],
            width=0.35,  # Make bars narrower
            marker_color='#2E8B57',
            text=warehouse_stats['Turnover_Rate'].astype(str) + '%',
            textposition='outside',
            textfont=dict(size=12, color='white')
        ))
        
        # Add average order size bars (right side of each group)
        fig.add_trace(go.Bar(
            name='Avg Order Size',
            x=[x + 0.2 for x in x_positions],  # Shift right
            y=warehouse_stats['Avg_Order_Size'],
            width=0.35,  # Make bars narrower
            marker_color='#4682B4',
            text=warehouse_stats['Avg_Order_Size'].astype(str),
            textposition='outside',
            textfont=dict(size=12, color='white')
        ))
        
        fig.update_layout(
            title='Warehouse Inventory Turnover Analysis',
            xaxis_title='Warehouse Location',
            yaxis_title='Rate (%)',  # Single y-axis
            height=450,
            template='plotly_dark',
            bargap=0.6,  # Space between groups
            xaxis=dict(
                tickmode='array',
                tickvals=x_positions,
                ticktext=x_labels
            ),
            margin=dict(t=80, b=60, l=80, r=80)
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating turnover analysis: {str(e)}")
        return None

def create_reorder_point_recommendations(df):
    """Create reorder point recommendations based on demand patterns"""
    try:
        if not all(col in df.columns for col in ['Product', 'Quantity', 'Delivery Status']):
            return None
        
        # Calculate demand statistics by product
        demand_stats = df.groupby('Product').agg({
            'Quantity': ['mean', 'std', 'sum', 'count']
        }).round(2)
        
        demand_stats.columns = ['Avg_Demand', 'Demand_StdDev', 'Total_Demand', 'Order_Frequency']
        demand_stats = demand_stats.reset_index()
        
        # Calculate safety stock and reorder points
        demand_stats['Safety_Stock'] = (1.5 * demand_stats['Demand_StdDev']).round(0)
        demand_stats['Current_Stock'] = demand_stats['Avg_Demand'] * 2
        demand_stats['Reorder_Point'] = demand_stats['Current_Stock'] + demand_stats['Safety_Stock']
        
        # Reorder trigger level
        reorder_level = demand_stats['Avg_Demand'] + (demand_stats['Safety_Stock'] * 0.5)
        
        fig = go.Figure()
        
        # Current stock level
        fig.add_trace(go.Bar(
            name='Current Stock',
            x=demand_stats['Product'],
            y=demand_stats['Current_Stock'],
            marker_color='#4682B4'
        ))
        
        # Safety stock buffer
        fig.add_trace(go.Bar(
            name='Safety Stock Buffer',
            x=demand_stats['Product'],
            y=demand_stats['Safety_Stock'],
            marker_color='#FFD700'
        ))
        
        # Reorder point line with text labels
        fig.add_trace(go.Scatter(
            name='Reorder Trigger Level',
            x=demand_stats['Product'],
            y=reorder_level,
            mode='markers+lines+text',  # Added text mode
            line=dict(color='#DC143C', width=3, dash='dash'),
            marker=dict(size=10, color='#DC143C'),
            text=[f"{val:.0f}" for val in reorder_level],  # Add numerical values
            textposition="top center",  # Position text above points
            textfont=dict(color='#DC143C', size=12),
            hovertemplate='Product: %{x}<br>Reorder at: %{y:.0f} units<extra></extra>'  # Fixed hover
        ))
        
        fig.update_layout(
            title='Inventory Reorder Point Recommendations',
            xaxis_title='Product',
            yaxis_title='Inventory Quantity',
            height=450,  # Increased height for text labels
            template='plotly_dark',
            barmode='stack',
            margin=dict(t=80, b=60, l=60, r=60)  # Added margins for text space
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating reorder point recommendations: {str(e)}")
        return None

def create_inventory_summary_table(df):
    """Create inventory summary statistics table with improved ABC analysis"""
    try:
        if not all(col in df.columns for col in ['Product', 'Quantity', 'Total Cost', 'Unit Price']):
            return None
        
        # Calculate comprehensive inventory metrics
        inventory_summary = df.groupby('Product').agg({
            'Quantity': ['sum', 'mean', 'std'],
            'Total Cost': ['sum', 'mean'],
            'Unit Price': 'mean'
        }).round(2)
        
        inventory_summary.columns = ['Total_Qty', 'Avg_Order_Qty', 'Qty_Variance', 'Total_Value', 'Avg_Order_Value', 'Unit_Price']
        inventory_summary = inventory_summary.reset_index()
        
        # Calculate additional metrics
        inventory_summary['Inventory_Turns'] = (inventory_summary['Total_Qty'] / inventory_summary['Avg_Order_Qty']).round(1)
        inventory_summary['Value_Density'] = (inventory_summary['Total_Value'] / inventory_summary['Total_Qty']).round(2)
        
        # IMPROVED ABC Classification using weighted scoring
        # Normalize metrics to 0-1 scale for comparison
        inventory_summary['Value_Score'] = inventory_summary['Total_Value'] / inventory_summary['Total_Value'].max()
        inventory_summary['Turn_Score'] = inventory_summary['Inventory_Turns'] / inventory_summary['Inventory_Turns'].max()
        inventory_summary['Qty_Score'] = inventory_summary['Total_Qty'] / inventory_summary['Total_Qty'].max()
        
        # Combined score (60% value, 25% turnover, 15% quantity)
        inventory_summary['ABC_Score'] = (
            inventory_summary['Value_Score'] * 0.6 + 
            inventory_summary['Turn_Score'] * 0.25 + 
            inventory_summary['Qty_Score'] * 0.15
        )
        
        # Classify based on combined score
        inventory_summary = inventory_summary.sort_values('ABC_Score', ascending=False)
        total_items = len(inventory_summary)
        
        # A: Top 20%, B: Next 30%, C: Bottom 50%
        inventory_summary['ABC_Class'] = ['A'] * int(total_items * 0.2) + \
                                        ['B'] * int(total_items * 0.3) + \
                                        ['C'] * (total_items - int(total_items * 0.2) - int(total_items * 0.3))
        
        # Create display table
        display_df = inventory_summary[['Product', 'ABC_Class', 'Total_Qty', 'Total_Value', 'Unit_Price', 'Inventory_Turns', 'ABC_Score']].copy()
        display_df.columns = ['Product', 'ABC Class', 'Total Quantity', 'Total Value ($)', 'Unit Price ($)', 'Inventory Turns', 'Priority Score']
        
        # Round the priority score for display
        display_df['Priority Score'] = display_df['Priority Score'].round(3)
        
        return display_df
        
    except Exception as e:
        st.error(f"Error creating inventory summary table: {str(e)}")
        return None

def calculate_inventory_kpis(df):
    """Calculate key inventory management KPIs"""
    try:
        if df.empty:
            return {}
        
        total_inventory_value = df['Total Cost'].sum()
        total_quantity = df['Quantity'].sum()
        avg_unit_price = df['Unit Price'].mean()
        total_orders = len(df)
        
        # Calculate turnover rate
        delivered_orders = len(df[df['Delivery Status'] == 'Delivered'])
        turnover_rate = (delivered_orders / total_orders * 100) if total_orders > 0 else 0
        
        # Calculate inventory diversity
        unique_products = df['Product'].nunique()
        unique_suppliers = df['Supplier'].nunique()
        
        # Stock level distribution
        high_value_items = len(df[df['Total Cost'] > df['Total Cost'].quantile(0.8)])
        
        return {
            'total_inventory_value': total_inventory_value,
            'total_quantity': total_quantity,
            'avg_unit_price': avg_unit_price,
            'turnover_rate': turnover_rate,
            'unique_products': unique_products,
            'unique_suppliers': unique_suppliers,
            'high_value_items': high_value_items,
            'total_orders': total_orders
        }
        
    except Exception as e:
        st.error(f"Error calculating inventory KPIs: {str(e)}")
        return {}
    
# Add these functions to your supply_chain_viz.py file

def create_cost_breakdown_analysis(df):
    """Create cost breakdown analysis by different dimensions"""
    try:
        if not all(col in df.columns for col in ['Supplier', 'Product', 'Warehouse Location', 'Total Cost']):
            return None
        
        # Calculate cost breakdown by supplier
        supplier_costs = df.groupby('Supplier')['Total Cost'].sum().reset_index()
        supplier_costs = supplier_costs.sort_values('Total Cost', ascending=True)
        
        # Create horizontal bar chart for better readability
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=supplier_costs['Total Cost'],
            y=supplier_costs['Supplier'],
            orientation='h',
            marker_color='#2E8B57',
            text=[f"${cost:,.0f}" for cost in supplier_costs['Total Cost']],
            textposition='inside',  # Changed from 'outside' to 'inside'
            textfont=dict(size=12, color='white')  # Added font styling
        ))
        
        fig.update_layout(
            title='Cost Distribution by Supplier',
            xaxis_title='Total Cost ($)',
            yaxis_title='Supplier',
            height=400,
            template='plotly_dark',
            margin=dict(l=100, r=100, t=50, b=50)  # Increased right margin
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating cost breakdown analysis: {str(e)}")
        return None

def create_cost_efficiency_matrix(df):
    """Create cost efficiency matrix comparing unit costs across suppliers and products"""
    try:
        if not all(col in df.columns for col in ['Supplier', 'Product', 'Unit Price', 'Quantity']):
            return None
        
        # Calculate average unit price by supplier-product combination
        efficiency_matrix = df.groupby(['Supplier', 'Product']).agg({
            'Unit Price': 'mean',
            'Quantity': 'sum',
            'Total Cost': 'sum'
        }).round(2)
        
        efficiency_matrix = efficiency_matrix.reset_index()
        
        # Create pivot for heatmap
        price_matrix = efficiency_matrix.pivot(
            index='Product',
            columns='Supplier', 
            values='Unit Price'
        ).fillna(0)
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=price_matrix.values,
            x=price_matrix.columns,
            y=price_matrix.index,
            colorscale='RdYlGn_r',  # Red = expensive, Green = cheap
            text=price_matrix.values,
            texttemplate="$%{text:.0f}",
            textfont={"size": 12},
            colorbar=dict(title="Unit Price ($)")
        ))
        
        fig.update_layout(
            title='Unit Price Comparison: Supplier vs Product',
            xaxis_title='Supplier',
            yaxis_title='Product',
            height=400,
            template='plotly_dark'
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating cost efficiency matrix: {str(e)}")
        return None

def create_cost_savings_opportunities(df):
    """Identify and visualize potential cost savings opportunities"""
    try:
        if not all(col in df.columns for col in ['Supplier', 'Product', 'Unit Price', 'Quantity', 'Total Cost']):
            return None
        
        # Calculate cost savings opportunities by finding price differences
        product_costs = df.groupby(['Product', 'Supplier']).agg({
            'Unit Price': 'mean',
            'Quantity': 'sum',
            'Total Cost': 'sum'
        }).reset_index()
        
        # Find min and max prices for each product
        price_analysis = product_costs.groupby('Product').agg({
            'Unit Price': ['min', 'max', 'mean'],
            'Quantity': 'sum'
        }).round(2)
        
        price_analysis.columns = ['Min_Price', 'Max_Price', 'Avg_Price', 'Total_Quantity']
        price_analysis = price_analysis.reset_index()
        
        # Calculate potential savings
        price_analysis['Price_Spread'] = price_analysis['Max_Price'] - price_analysis['Min_Price']
        price_analysis['Potential_Savings'] = (price_analysis['Price_Spread'] * price_analysis['Total_Quantity'])
        price_analysis['Savings_Opportunity'] = price_analysis['Potential_Savings'] / (price_analysis['Avg_Price'] * price_analysis['Total_Quantity']) * 100
        
        # Create savings opportunity chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=price_analysis['Product'],
            y=price_analysis['Potential_Savings'],
            marker_color=['#DC143C' if x > price_analysis['Potential_Savings'].quantile(0.75) 
                         else '#FFD700' if x > price_analysis['Potential_Savings'].quantile(0.5)
                         else '#2E8B57' for x in price_analysis['Potential_Savings']],
            text=[f"${savings:,.0f}<br>({pct:.1f}%)" for savings, pct in 
                  zip(price_analysis['Potential_Savings'], price_analysis['Savings_Opportunity'])],
            textposition='inside',  # Changed from 'outside' to 'inside'
            textfont=dict(size=11, color='white')  # Added font styling
        ))
        
        fig.update_layout(
            title='Cost Savings Opportunities by Product',
            xaxis_title='Product',
            yaxis_title='Potential Annual Savings ($)',
            height=450,  # Increased height
            template='plotly_dark',
            showlegend=False,
            margin=dict(t=80, b=60, l=80, r=80)  # Increased margins
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating cost savings opportunities: {str(e)}")
        return None

def create_logistics_cost_analysis(df):
    """Analyze logistics costs by shipping method and partner"""
    try:
        if not all(col in df.columns for col in ['Shipping Method', 'Logistics Partner', 'Total Cost', 'Delivery Status']):
            return None
        
        # Calculate average cost per shipment by method and partner
        logistics_costs = df.groupby(['Shipping Method', 'Logistics Partner']).agg({
            'Total Cost': ['mean', 'sum', 'count'],
            'Delivery Status': lambda x: (x == 'Delayed').mean() * 100
        }).round(2)
        
        logistics_costs.columns = ['Avg_Cost', 'Total_Cost', 'Shipment_Count', 'Delay_Rate']
        logistics_costs = logistics_costs.reset_index()
        
        # Create bubble chart: x=avg cost, y=delay rate, size=shipment count
        fig = go.Figure()
        
        # Color by shipping method
        colors = {'Air': '#FF6B6B', 'Road': '#4ECDC4', 'Rail': '#45B7D1', 'Sea': '#96CEB4'}
        
        for method in logistics_costs['Shipping Method'].unique():
            method_data = logistics_costs[logistics_costs['Shipping Method'] == method]
            
            fig.add_trace(go.Scatter(
                x=method_data['Avg_Cost'],
                y=method_data['Delay_Rate'],
                mode='markers',
                marker=dict(
                    size=method_data['Shipment_Count'] * 3,
                    color=colors.get(method, '#888888'),
                    line=dict(width=2, color='white'),
                    sizemode='diameter'
                ),
                text=[f"Method: {method}<br>Partner: {partner}<br>Avg Cost: ${cost:.0f}<br>Delay Rate: {delay:.1f}%<br>Shipments: {count}"
                      for method, partner, cost, delay, count in zip(
                          method_data['Shipping Method'], method_data['Logistics Partner'],
                          method_data['Avg_Cost'], method_data['Delay_Rate'], method_data['Shipment_Count'])],
                hovertemplate='%{text}<extra></extra>',
                name=method
            ))
        
        fig.update_layout(
            title='Logistics Cost vs Performance Analysis',
            xaxis_title='Average Cost per Shipment ($)',
            yaxis_title='Delay Rate (%)',
            height=450,
            template='plotly_dark'
        )
        
        # Add quadrant lines
        avg_cost = logistics_costs['Avg_Cost'].mean()
        avg_delay = logistics_costs['Delay_Rate'].mean()
        
        fig.add_vline(x=avg_cost, line_dash="dash", line_color="gray", opacity=0.5)
        fig.add_hline(y=avg_delay, line_dash="dash", line_color="gray", opacity=0.5)
        
        return fig
        
    except Exception as e:
        st.error(f"Error creating logistics cost analysis: {str(e)}")
        return None

def calculate_cost_optimization_kpis(df):
    """Calculate key cost optimization KPIs"""
    try:
        if df.empty:
            return {}
        
        total_cost = df['Total Cost'].sum()
        avg_unit_cost = df['Unit Price'].mean()
        total_quantity = df['Quantity'].sum()
        cost_per_unit = total_cost / total_quantity if total_quantity > 0 else 0
        
        # Calculate cost distribution
        supplier_costs = df.groupby('Supplier')['Total Cost'].sum()
        top_supplier_pct = supplier_costs.max() / total_cost * 100
        
        # Calculate potential savings from price optimization
        product_analysis = df.groupby('Product').agg({
            'Unit Price': ['min', 'max'],
            'Quantity': 'sum'
        })
        
        potential_savings = 0
        for product in product_analysis.index:
            min_price = product_analysis.loc[product, ('Unit Price', 'min')]
            max_price = product_analysis.loc[product, ('Unit Price', 'max')]
            quantity = product_analysis.loc[product, ('Quantity', 'sum')]
            potential_savings += (max_price - min_price) * quantity
        
        savings_percentage = potential_savings / total_cost * 100 if total_cost > 0 else 0
        
        # Logistics cost efficiency
        delayed_cost = df[df['Delivery Status'] == 'Delayed']['Total Cost'].sum()
        delay_cost_impact = delayed_cost / total_cost * 100
        
        return {
            'total_cost': total_cost,
            'avg_unit_cost': avg_unit_cost,
            'cost_per_unit': cost_per_unit,
            'top_supplier_concentration': top_supplier_pct,
            'potential_savings': potential_savings,
            'savings_percentage': savings_percentage,
            'delay_cost_impact': delay_cost_impact,
            'total_quantity': total_quantity
        }
        
    except Exception as e:
        st.error(f"Error calculating cost optimization KPIs: {str(e)}")
        return {}

def generate_cost_optimization_recommendations(df):
    """Generate AI-powered cost optimization recommendations"""
    try:
        if df.empty:
            return []
        
        recommendations = []
        
        # Analyze supplier concentration
        supplier_costs = df.groupby('Supplier')['Total Cost'].sum().sort_values(ascending=False)
        total_cost = df['Total Cost'].sum()
        top_supplier_pct = supplier_costs.iloc[0] / total_cost * 100
        
        if top_supplier_pct > 40:
            recommendations.append(f"**Supplier Diversification**: {supplier_costs.index[0]} represents {top_supplier_pct:.1f}% of total costs. Consider diversifying suppliers to reduce concentration risk and increase negotiating power.")
        
        # Analyze price variations
        product_price_analysis = df.groupby('Product').agg({
            'Unit Price': ['min', 'max', 'std'],
            'Quantity': 'sum',
            'Total Cost': 'sum'
        })
        
        high_variation_products = []
        for product in product_price_analysis.index:
            price_std = product_price_analysis.loc[product, ('Unit Price', 'std')]
            price_mean = product_price_analysis.loc[product, ('Unit Price', 'min')]
            if price_std / price_mean > 0.15:  # High price variation
                high_variation_products.append(product)
        
        if high_variation_products:
            recommendations.append(f"**Price Standardization**: Products {', '.join(high_variation_products)} show high price variation. Negotiate standard pricing agreements to reduce cost volatility.")
        
        # Analyze logistics efficiency
        logistics_efficiency = df.groupby(['Shipping Method', 'Logistics Partner']).agg({
            'Total Cost': 'mean',
            'Delivery Status': lambda x: (x == 'Delayed').mean() * 100
        })
        
        inefficient_logistics = logistics_efficiency[
            (logistics_efficiency['Total Cost'] > logistics_efficiency['Total Cost'].quantile(0.75)) &
            (logistics_efficiency['Delivery Status'] > logistics_efficiency['Delivery Status'].quantile(0.75))
        ]
        
        if not inefficient_logistics.empty:
            recommendations.append(f"**Logistics Optimization**: Review high-cost, high-delay shipping combinations. Consider alternative logistics partners or shipping methods for better cost-performance balance.")
        
        # Volume-based recommendations
        low_volume_suppliers = df.groupby('Supplier')['Quantity'].sum().sort_values()
        if len(low_volume_suppliers) > 1:
            smallest_volumes = low_volume_suppliers.head(2)
            recommendations.append(f"**Volume Consolidation**: Consider consolidating low-volume suppliers ({', '.join(smallest_volumes.index)}) to achieve better volume discounts and reduce administrative costs.")
        
        return recommendations
        
    except Exception as e:
        st.error(f"Error generating cost optimization recommendations: {str(e)}")
        return []