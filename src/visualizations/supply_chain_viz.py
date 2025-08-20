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
        
        # Create subplot with dual y-axis
        fig = make_subplots(
            specs=[[{"secondary_y": True}]],
            subplot_titles=('Shipping Method Performance Analysis',)
        )
        
        # Add delay rate bars
        fig.add_trace(
            go.Bar(
                name='Delay Rate %',
                x=shipping_stats['Shipping Method'],
                y=shipping_stats['Delay_Rate'],
                marker_color='#DC143C',
                text=shipping_stats['Delay_Rate'].astype(str) + '%',
                textposition='auto'  # CHANGED: Better text positioning
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
            height=450,  # INCREASED HEIGHT
            template='plotly_dark',
            showlegend=True,
            margin=dict(t=80, b=60, l=60, r=60),  # ADDED MARGINS
            title_y=0.95
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
    
