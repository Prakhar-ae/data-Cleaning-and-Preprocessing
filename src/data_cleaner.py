"""
Data Cleaning and Preprocessing Pipeline
A comprehensive tool to clean and preprocess datasets for analysis
"""

import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Tuple, Dict
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self, filepath: str):
       
        self.filepath = filepath
        self.df = None
        self.original_df = None
        self.cleaning_report = {}
        
    def load_data(self) -> pd.DataFrame:
        try:
            self.df = pd.read_csv(self.filepath)
            self.original_df = self.df.copy()
            logger.info(f"Data loaded successfully. Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            sys.exit(1)
    
    def handle_missing_values(self, strategy: str = 'drop', fill_value=None) -> pd.DataFrame:
        missing_before = self.df.isnull().sum().sum()
        logger.info(f"Missing values before handling: {missing_before}")
        if strategy == 'drop':
            self.df = self.df.dropna()
        elif strategy == 'mean':
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                self.df[col].fillna(self.df[col].mean(), inplace=True)
            self.df = self.df.dropna()
        elif strategy == 'forward_fill':
            self.df = self.df.fillna(method='ffill')
        elif strategy == 'custom' and fill_value is not None:
            self.df = self.df.fillna(fill_value)
        missing_after = self.df.isnull().sum().sum()
        self.cleaning_report['missing_values'] = {
            'before': missing_before,
            'after': missing_after,
            'removed': missing_before - missing_after
        }
        logger.info(f"Missing values after handling: {missing_after}")
        return self.df
    
    def remove_duplicates(self, subset=None, keep='first') -> pd.DataFrame:
        duplicates_before = self.df.duplicated(subset=subset).sum()
        logger.info(f"Duplicate rows before removal: {duplicates_before}")
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        duplicates_after = self.df.duplicated(subset=subset).sum()
        self.cleaning_report['duplicates'] = {
            'before': duplicates_before,
            'after': duplicates_after,
            'removed': duplicates_before - duplicates_after
        }
        logger.info(f"Duplicate rows after removal: {duplicates_after}")
        return self.df
    
    def standardize_text(self) -> pd.DataFrame:
        logger.info("Standardizing text columns...")
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].str.strip()
            if 'email' not in col.lower():
                self.df[col] = self.df[col].str.title()
        logger.info("Text standardization completed")
        return self.df
    
    def fix_data_types(self, type_mapping: Dict = None) -> pd.DataFrame:
        logger.info("Fixing data types...")
        if type_mapping:
            for col, dtype in type_mapping.items():
                if col in self.df.columns:
                    try:
                        self.df[col] = self.df[col].astype(dtype)
                        logger.info(f"Converted {col} to {dtype}")
                    except Exception as e:
                        logger.warning(f"Could not convert {col} to {dtype}: {e}")
        else:
            self.df = self.df.infer_objects()
        return self.df
    
    def standardize_columns(self) -> pd.DataFrame:
        logger.info("Standardizing column names...")
        self.df.columns = (self.df.columns
                          .str.lower()
                          .str.replace(' ', '_')
                          .str.replace('[^a-z0-9_]', '', regex=True))
        logger.info(f"New columns: {list(self.df.columns)}")
        return self.df
    
    def remove_outliers(self, columns: list, method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
        logger.info(f"Removing outliers using {method} method...")
        rows_before = len(self.df)
        for col in columns:
            if col not in self.df.columns:
                logger.warning(f"Column {col} not found")
                continue
        
            if method == 'iqr':
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
            
            elif method == 'zscore':
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                self.df = self.df[z_scores < threshold]
        
        rows_after = len(self.df)
        self.cleaning_report['outliers'] = {
            'before': rows_before,
            'after': rows_after,
            'removed': rows_before - rows_after
        }
        logger.info(f"Rows after outlier removal: {rows_after} (removed {rows_before - rows_after})")
        return self.df
    
    def save_cleaned_data(self, output_path: str) -> None:
        try:
            self.df.to_csv(output_path, index=False)
            logger.info(f"Cleaned data saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def generate_report(self) -> Dict:
        report = {
            'original_shape': self.original_df.shape,
            'cleaned_shape': self.df.shape,
            'rows_removed': self.original_df.shape[0] - self.df.shape[0],
            'cleaning_details': self.cleaning_report
        }
        logger.info("\n=== CLEANING REPORT ===")
        logger.info(f"Original shape: {report['original_shape']}")
        logger.info(f"Cleaned shape: {report['cleaned_shape']}")
        logger.info(f"Total rows removed: {report['rows_removed']}")
        logger.info(f"Details: {report['cleaning_details']}")
        return report

def main():
    cleaner = DataCleaner('data/raw_data.csv')
    cleaner.load_data()
    type_mapping = {
        'id': 'int64',
        'age': 'float64',
        'salary': 'float64'
    }
    logger.info("\n=== STARTING DATA CLEANING PIPELINE ===\n")
    cleaner.standardize_columns()
    cleaner.handle_missing_values(strategy='drop')
    cleaner.remove_duplicates(subset=['name', 'email'])
    cleaner.standardize_text()
    cleaner.fix_data_types(type_mapping)
    cleaner.remove_outliers(columns=['salary', 'age'], method='iqr')
    cleaner.save_cleaned_data('data/cleaned_data.csv')
    report = cleaner.generate_report()
    logger.info("\n=== CLEANING PIPELINE COMPLETED ===\n")
    return cleaner.df, report

if __name__ == "__main__":
    cleaned_df, report = main()
    print("\nCleaned data preview:")
    print(cleaned_df.head())
