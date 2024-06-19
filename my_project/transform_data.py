import pandas as pd
import os
import glob
import csv

def transform():
    # Find the latest CSV file in the loaded_data directory
    list_of_files = glob.glob('./loaded_data/products-*.csv')  # Adjust the pattern if needed
    if not list_of_files:
        raise FileNotFoundError("No CSV files found in the loaded_data directory")
    
    latest_file = max(list_of_files, key=os.path.getctime)
    
    # Load the extracted data with appropriate settings to handle commas in quoted text
    try:
        df = pd.read_csv(latest_file, encoding='ISO-8859-1', skip_blank_lines=True, quotechar="'", quoting=csv.QUOTE_ALL)
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file: {e}")
        return
    
    # Define your transformation here
    # For example, let's keep only id, title, price
    df = df[['id', 'title', 'price']]
    
    # Save the transformed data
    df.to_csv('transformed_data.csv', index=False)

if __name__ == "__main__":
    transform()
