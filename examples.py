"""
Example usage scenarios for the Data Cleaning Pipeline
"""

from src.data_cleaner import DataCleaner
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# EXAMPLE: Simple Basic Cleaning

def basic_cleaning():
    print("Basic Cleaning")
    cleaner = DataCleaner('data/raw_data.csv')
    cleaner.load_data()
    cleaner.remove_duplicates()
    cleaner.handle_missing_values(strategy='drop')
    cleaner.save_cleaned_data('data/cleaned.csv')
    report = cleaner.generate_report()
    print(f"\nCleaned dataset shape: {report['cleaned_shape']}")

def main():
    print("DATA CLEANING PIPELINE")
    basic_cleaning()
if __name__ == "__main__":
    main()
