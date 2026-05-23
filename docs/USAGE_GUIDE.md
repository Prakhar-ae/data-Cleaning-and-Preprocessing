# Data Cleaning Pipeline - Usage Guide

# Quick Start

# Step 1: Install Dependencies
pip install -r requirements.txt

# Step 2: Prepare Your Data
Place your CSV file in the `data/` directory

# Step 3: Run the Pipeline
python src/data_cleaner.py
The cleaned data will be saved to `data/cleaned_data.csv`

# Example

# Basic Cleaning Workflow
from src.data_cleaner import DataCleaner

# Initialize the cleaner with your CSV file
cleaner = DataCleaner('data/my_dataset.csv')

# Load the data
cleaner.load_data()

# Perform basic cleaning operations
cleaner.remove_duplicates()
cleaner.handle_missing_values(strategy='drop')
cleaner.standardize_text()

# Save the cleaned data
cleaner.save_cleaned_data('data/my_dataset_cleaned.csv')
