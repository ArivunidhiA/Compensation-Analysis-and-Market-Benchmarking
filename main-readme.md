# Compensation Analysis Dashboard

## Overview
This project provides a comprehensive compensation analysis and market benchmarking dashboard using publicly available salary data. It helps organizations make data-driven decisions about compensation by analyzing market trends, geographic differences, and job levels.

## Features
- Industry compensation benchmarking
- Geographic salary comparisons
- Job level analysis
- Trend forecasting
- Interactive visualization
- Scenario modeling

## Data Sources
1. [U.S. Bureau of Labor Statistics (BLS) Occupational Employment Statistics](https://www.bls.gov/oes/tables.htm)
2. [H-1B Visa Salary Data](https://www.dol.gov/agencies/eta/foreign-labor/performance)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/compensation-analysis.git
cd compensation-analysis

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download the required data
python src/data_loader.py

# Run the application
streamlit run app.py
```

## Usage
1. Navigate to `http://localhost:8501` after starting the application
2. Use the sidebar filters to select:
   - Job categories
   - Geographic regions
   - Experience levels
   - Industry sectors
3. Explore the various visualization tabs:
   - Market Benchmarks
   - Geographic Analysis
   - Trend Analysis
   - Scenario Modeling

## Project Structure
- `data/`: Contains data downloading and storage instructions
- `src/`: Source code for data processing and analysis
- `tests/`: Unit tests
- `app.py`: Main Streamlit application
- `requirements.txt`: Project dependencies

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
