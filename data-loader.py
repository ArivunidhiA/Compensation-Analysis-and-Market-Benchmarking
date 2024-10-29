import os
import requests
import pandas as pd
from pathlib import Path

class DataLoader:
    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
    def download_bls_data(self, year: int = 2023) -> pd.DataFrame:
        """
        Downloads Occupational Employment Statistics from BLS.
        Data source: https://www.bls.gov/oes/tables.htm
        """
        url = f"https://www.bls.gov/oes/special.requests/oesm{str(year)[-2:]}nat.zip"
        
        # Download and extract data
        file_path = self.data_dir / f"bls_data_{year}.csv"
        
        if not file_path.exists():
            response = requests.get(url)
            response.raise_for_status()
            
            with open(file_path, "wb") as f:
                f.write(response.content)
        
        return pd.read_csv(file_path)

    def download_h1b_data(self, year: int = 2023) -> pd.DataFrame:
        """
        Downloads H-1B visa salary data.
        Data source: https://www.dol.gov/agencies/eta/foreign-labor/performance
        """
        url = f"https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-1B_Disclosure_Data_FY{year}.xlsx"
        
        file_path = self.data_dir / f"h1b_data_{year}.xlsx"
        
        if not file_path.exists():
            response = requests.get(url)
            response.raise_for_status()
            
            with open(file_path, "wb") as f:
                f.write(response.content)
        
        return pd.read_excel(file_path)

    def load_and_combine_data(self, year: int = 2023) -> pd.DataFrame:
        """
        Loads and combines data from both sources.
        """
        bls_data = self.download_bls_data(year)
        h1b_data = self.download_h1b_data(year)
        
        # Perform initial cleaning and combining
        # This is a simplified version - you'll need to adapt based on the actual data structure
        combined_data = pd.concat([
            self.clean_bls_data(bls_data),
            self.clean_h1b_data(h1b_data)
        ], axis=0)
        
        return combined_data
    
    def clean_bls_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans BLS data to standardized format.
        """
        cleaned = df.copy()
        # Add cleaning steps based on actual data structure
        return cleaned
    
    def clean_h1b_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Cleans H-1B data to standardized format.
        """
        cleaned = df.copy()
        # Add cleaning steps based on actual data structure
        return cleaned

if __name__ == "__main__":
    loader = DataLoader()
    data = loader.load_and_combine_data()
    print(f"Successfully loaded {len(data)} records")
