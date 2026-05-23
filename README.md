# Data Cleaning and Preprocessing Pipeline

A comprehensive Python project for cleaning and preprocessing

# Overview

This project provides a framework for handling common data quality issues including:
- Missing values
- Duplicate records
- Inconsistent data formats
- Outliers
- Data type inconsistencies
- Text standardization

# Features

 - Flexible Missing Value Handling: Multiple strategies (drop, mean, forward fill, custom)
 - Duplicate Detection and Removal: Remove exact or partial duplicates
 - Text Standardization: Clean and standardize text columns
 - Data Type Conversion: Automatic and manual type conversion
 - Outlier Detection: IQR and Z-score methods
 - Comprehensive Logging: Track all operations and changes
 - Detailed Reports: Generate cleaning reports with statistics

# Project Structure
data-cleaning-project/
├── data/
│   ├── raw_data.csv           
│   └── cleaned_data.csv       
├── src/
│   └── data_cleaner.py        
├── tests/
│   └── test_data_cleaner.py   
├── docs/
│   └── USAGE_GUIDE.md         
├── requirements.txt           
├── README.md                  
└── LICENSE                    

# Installation

# Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

# Setup Steps

1. # Create a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

2. # Install dependencies
pip install -r requirements.txt
