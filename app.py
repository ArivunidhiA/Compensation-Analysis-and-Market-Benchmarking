import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.data_loader import DataLoader
from src.data_processor import DataProcessor

def main():
    st.set_page_config(page_title="Compensation Analysis Dashboard",
                      layout="wide")
    
    st.title("Compensation Analysis Dashboard")
    
    # Load data
    @st.cache_data
    def load_data():
        loader = DataLoader()
        return loader.load_and_combine_data()
    
    data = load_data()
    processor = DataProcessor(data)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    job_category = st.sidebar.selectbox(
        "Job Category",
        options=sorted(data['job_category'].unique())
    )
    
    location = st.sidebar.selectbox(
        "Location",
        options=['All'] + sorted(data['location'].unique())
    )
    
    experience_level = st.sidebar.selectbox(
        "Experience Level",
        options=['All'] + sorted(data['experience_level'].unique())
    )
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Market Benchmarks")
        benchmarks = processor.calculate_benchmarks(
            job_category,
            location if location != 'All' else None,
            experience_level if experience_level != 'All' else None
        )
        
        fig = go.Figure()
        fig.add_trace(go.Box(
            q1=[benchmarks['percentile_25']],
            median=[benchmarks['median']],
            q3=[benchmarks['percentile_75']],
            mean=[benchmarks['mean']],
            lowerfence=[benchmarks['percentile_25'] - 1.5 * (benchmarks['percentile_75'] - benchmarks['percentile_25'])],
            upperfence=[benchmarks['percentile_75'] + 1.5 * (benchmarks['percentile_75'] - benchmarks['percentile_25'])],
            name="Salary Distribution"
        ))
        st.plotly_chart(fig)
        
    with col2:
        st.subheader("Geographic Analysis")
        if location == 'All':
            top_locations = data['location'].value_counts().head(10).index
            geo_analysis = processor.analyze_geographic_differences(job_category, top_locations)
            
            fig = px.bar(geo_analysis,
                        x='location',
                        y='median',
                        error_y='std',
                        title=f"Median Salaries by Location - {job_category}")
            st.plotly_chart(fig)
            
    # Trend Analysis
    st.subheader("Salary Trends and Forecast")
    forecast, confidence = processor.create_forecast_model(job_category)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(len(forecast))),
        y=forecast,
        mode='lines',
        name='Forecast'
    ))
    fig.add_trace(go.Scatter(
        x=list(range(len(forecast))),
        y=forecast + confidence,
        mode='lines',
        line=dict(dash='dash'),
        name='Upper Bound'
    ))
    fig.add_trace(go.Scatter(
        x=list(range(len(forecast))),
        y=forecast - confidence,
        mode='lines',
        line=dict(dash='dash'),
        name='Lower Bound'
    ))
    st.plotly_chart(fig)
    
    # Scenario Analysis
    st.subheader("Scenario Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        current_salary = st.number_input("Current Salary", min_value=0, value=100000)
        target_location = st.selectbox("Target Location", options=sorted(data['location'].unique()))
        
    with col2:
        market_position = processor.calculate_market_position(
            current_salary,
            job_category,
            target_location
        )
        
        st.metric(
            "Market Position",
            f"{market_position:.1f}th percentile"
        )
        
        recommendation = "Above market" if market_position > 75 else \
                        "At market" if market_position > 25 else \
                        "Below market"
        
        st.info(f"Salary is {recommendation} for {job_category} in {target_location}")

if __name__ == "__main__":
    main()
