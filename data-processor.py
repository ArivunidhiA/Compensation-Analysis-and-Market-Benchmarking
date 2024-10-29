import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple

class DataProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.scaler = StandardScaler()
        
    def calculate_benchmarks(self, 
                           job_category: str,
                           location: str = None,
                           experience_level: str = None) -> Dict[str, float]:
        """
        Calculates salary benchmarks for given parameters.
        """
        mask = self.df['job_category'] == job_category
        
        if location:
            mask &= self.df['location'] == location
        if experience_level:
            mask &= self.df['experience_level'] == experience_level
            
        filtered_data = self.df[mask]['salary']
        
        return {
            'percentile_25': filtered_data.quantile(0.25),
            'median': filtered_data.median(),
            'percentile_75': filtered_data.quantile(0.75),
            'mean': filtered_data.mean(),
            'std': filtered_data.std()
        }
    
    def analyze_geographic_differences(self, 
                                    job_category: str,
                                    locations: List[str]) -> pd.DataFrame:
        """
        Analyzes salary differences across locations.
        """
        location_stats = []
        
        for location in locations:
            stats = self.calculate_benchmarks(job_category, location)
            stats['location'] = location
            location_stats.append(stats)
            
        return pd.DataFrame(location_stats)
    
    def create_forecast_model(self,
                            job_category: str,
                            years_ahead: int = 1) -> Tuple[List[float], List[float]]:
        """
        Creates a simple time-series forecast for salary trends.
        """
        historical_data = self.df[
            self.df['job_category'] == job_category
        ].groupby('year')['salary'].mean()
        
        # Simple linear regression for forecasting
        X = np.array(range(len(historical_data))).reshape(-1, 1)
        y = historical_data.values
        
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate forecast
        future_years = np.array(range(len(historical_data), 
                                    len(historical_data) + years_ahead)).reshape(-1, 1)
        forecast = model.predict(future_years)
        
        confidence_interval = np.std(y) * 1.96  # 95% confidence interval
        
        return forecast, confidence_interval
    
    def calculate_market_position(self,
                                salary: float,
                                job_category: str,
                                location: str = None) -> float:
        """
        Calculates market position percentile for a given salary.
        """
        mask = self.df['job_category'] == job_category
        if location:
            mask &= self.df['location'] == location
            
        market_data = self.df[mask]['salary']
        return percentileofscore(market_data, salary)

if __name__ == "__main__":
    # Test the processor with sample data
    from data_loader import DataLoader
    loader = DataLoader()
    data = loader.load_and_combine_data()
    processor = DataProcessor(data)
    
    # Run some test calculations
    print(processor.calculate_benchmarks("Software Engineer", "California"))
