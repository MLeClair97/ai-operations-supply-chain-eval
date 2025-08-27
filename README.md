# AI Operations Intelligence Platform

**Live Demo**: [https://ai-operations-supply-chain-eval.streamlit.app/](https://ai-operations-supply-chain-eval.streamlit.app/)

An AI-powered supply chain operations analytics platform that transforms raw logistics data into actionable business intelligence. Built with Streamlit and integrated with AI analysis capabilities to provide executive-level insights for operations optimization.

## Features

### 📊 Operations Overview
- Real-time performance monitoring dashboard
- Key performance indicators across suppliers, products, warehouses
- Executive-level status indicators and risk assessment
- Comprehensive metrics tracking delivery performance and operational efficiency

### ⚠️ Supply Chain Risk Analysis
- AI-powered risk identification and root cause analysis
- Supplier performance comparison and reliability scoring
- Logistics partner delay rate analysis with recommendations
- Financial impact assessment of operational delays

### 📈 Performance Analytics
- Performance trends over time with historical analysis
- Delivery status monitoring and volume distribution
- Shipping method efficiency comparison
- Warehouse performance analysis and optimization insights

### 📦 Inventory Management
- Product inventory analysis with ABC classification methodology
- Warehouse turnover analysis and efficiency metrics
- AI-driven reorder point recommendations with safety stock calculations
- Comprehensive inventory summary with priority scoring

### 💰 Cost Optimization
- Cost breakdown analysis by supplier and product categories
- Unit price comparison matrix for supplier evaluation
- Cost savings opportunity identification with potential ROI
- Logistics performance vs cost efficiency analysis

### 🤖 AI Insights
- Comprehensive AI-powered business analysis across all operational areas
- Strategic recommendations with priority-based action plans
- Executive summary with key findings and critical issues
- ROI projections and implementation timeline guidance

## Technology Stack

- **Frontend**: Streamlit for interactive web application
- **Data Processing**: Pandas, NumPy for data manipulation and analysis
- **Visualizations**: Plotly for interactive charts and dashboards
- **AI Integration**: OpenAI API for intelligent insights generation
- **Deployment**: Streamlit Cloud for live demo hosting

## Project Structure

```
ai-operations-supply-chain-eval/
├── dashboard.py                    # Main Streamlit application
├── requirements.txt                # Python dependencies
├── data/
│   └── Supply_Chain_Logistics_Dataset.csv
├── src/
│   ├── ai_insights/
│   │   └── operations_analyzer.py  # AI risk analysis functions
│   ├── data_processing/
│   │   └── supply_chain_loader.py  # Data loading and metrics calculation
│   └── visualizations/
│       └── supply_chain_viz.py     # Chart creation functions
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Git

### Local Development
1. Clone the repository:
```bash
git clone https://github.com/MLeClair97/ai-operations-supply-chain-eval.git
cd ai-operations-supply-chain-eval
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run dashboard.py
```

4. Open your browser to `http://localhost:8501`

## Data Source

The platform uses a supply chain logistics dataset containing:
- **Products**: 5 different product categories (Widgets, Gadgets, Tools)
- **Suppliers**: 5 suppliers with varying performance metrics
- **Warehouses**: 3 distribution locations
- **Logistics Partners**: 5 different logistics companies
- **Shipping Methods**: Air, Road, Rail, Sea transportation options
- **Performance Tracking**: Delivery status, costs, and timing data

*Note: Delivery dates have been updated to current timeframes for realistic demo purposes.*

**Original Data Source**: [Kaggle Supply Chain Dataset](https://www.kaggle.com/datasets/discovertalent143/supply-chain-dataset)

## Key Insights & Business Value

### Operational Intelligence
- **32% of orders experience delays**, creating significant operational risk
- **FastTrans logistics partner shows 45.5% delay rate** vs FleetPro at 11.1%
- **$27,911 in delayed shipments** represents 38.5% of total operational costs
- **68% overall performance rate** indicates need for systematic improvements

### Cost Optimization Opportunities
- **15-20% potential cost savings** through supplier consolidation and pricing standardization
- **High price variation across products** suggests inconsistent procurement practices
- **Volume consolidation opportunities** with low-volume suppliers
- **Logistics efficiency improvements** could reduce both costs and delays

### Strategic Recommendations
1. **Immediate**: Address supplier performance issues (highest ROI opportunity)
2. **Short-term**: Standardize pricing across product categories
3. **Medium-term**: Implement predictive analytics for demand forecasting
4. **Long-term**: Diversify logistics partner portfolio to reduce delivery risk

## Architecture & Design

### Modular Code Organization
- **Separation of Concerns**: Data processing, AI analysis, and visualization components are isolated
- **Scalable Structure**: Easy to extend with additional analytics or data sources
- **Maintainable Codebase**: Clear function organization and consistent error handling

### User Experience Design
- **Progressive Information Architecture**: From high-level overview to detailed analysis
- **Executive-Friendly Interface**: Business-focused language and actionable insights
- **Mobile-Responsive Design**: Accessible across different device types
- **Intuitive Navigation**: Clear page structure with logical flow

## Performance & Scalability

### Current Capabilities
- **Real-time Analysis**: Processes 50+ logistics transactions instantly
- **Interactive Visualizations**: 15+ different chart types across 6 pages
- **AI Integration**: Generates contextual business insights in seconds
- **Multi-dimensional Analysis**: Supplier, product, warehouse, and logistics perspectives

### Scalability Considerations
- **Caching Strategy**: Streamlit caching for improved performance
- **Modular Functions**: Easy to adapt for larger datasets
- **Cloud Deployment**: Streamlit Cloud hosting with automatic scaling
- **API Ready**: Architecture supports future API integration

## Contributing

This is a portfolio demonstration project. For questions or collaboration opportunities:

- **LinkedIn**: [Connect with me: https://www.linkedin.com/in/melissaleclair97/](https://www.linkedin.com/in/melissaleclair97/)
- **Email**: [Contact for opportunities: melissaleclair97@gmail.com](mailto:melissaleclair97@gmail.com)
- **Portfolio**: [View other projects: https://share.streamlit.io/user/mleclair97](https://share.streamlit.io/user/mleclair97)

## License

This project is open source and available under the MIT License.

---

**Built as part of AI career transition portfolio demonstrating:**
- Full-stack application development
- AI integration and prompt engineering
- Business intelligence and data visualization
- Operations analytics and supply chain optimization
- Professional deployment and documentation