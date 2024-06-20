import pandas as pd
import os
import glob
import csv
import json
import numpy as np

def transform():
    list_of_files = glob.glob('./loaded_data/products-*.csv')
    if not list_of_files:
        raise FileNotFoundError("No CSV files found in the loaded_data directory")
    
    latest_file = max(list_of_files, key=os.path.getctime)
    
    try:
        df = pd.read_csv(latest_file, encoding='ISO-8859-1', skip_blank_lines=True, quotechar="'", quoting=csv.QUOTE_ALL)
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file: {e}")
        return
    
    df['tags'] = df['tags'].apply(lambda x: ','.join(json.loads(x)) if pd.notna(x) else '')
    df['discounted_price'] = df['price'] * (1 - df['discountPercentage'] / 100)
    
    def calculate_average_rating(reviews):
        try:
            reviews_list = json.loads(reviews)
            if reviews_list:
                average_rating = sum(review['rating'] for review in reviews_list) / len(reviews_list)
                return round(average_rating, 1)  # Round to 1 decimal place
            else:
                return None
        except (json.JSONDecodeError, TypeError):
            return None
    
    def count_reviews(reviews):
        try:
            reviews_list = json.loads(reviews)
            return len(reviews_list) if reviews_list else 0
        except (json.JSONDecodeError, TypeError):
            return 0
    
    df['average_rating'] = df['reviews'].apply(calculate_average_rating)
    df['number_of_reviews'] = df['reviews'].apply(count_reviews)
    df['dimensions'] = df['dimensions_width'].astype(str) + 'x' + df['dimensions_height'].astype(str) + 'x' + df['dimensions_depth'].astype(str)
    df['stock_status'] = df['stock'].apply(lambda x: 'Low Stock' if x < 10 else 'In Stock')
    df['price'].fillna(df['price'].mean(), inplace=True)
    df['meta_createdAt'] = pd.to_datetime(df['meta_createdAt'], errors='coerce')
    df['meta_updatedAt'] = pd.to_datetime(df['meta_updatedAt'], errors='coerce')
    df['category_group'] = df['category'].apply(lambda x: 'Cosmetics' if x in ['beauty', 'makeup'] else 'Other')
    
    # Impute NaN values
    for column in df.select_dtypes(include=[np.number]).columns:
        df[column].fillna(0, inplace=True)
    for column in df.select_dtypes(exclude=[np.number]).columns:
        df[column].fillna(df[column].mode()[0], inplace=True)
    
    df_transformed = df[['id', 'title', 'description', 'price', 'discounted_price', 'average_rating', 'number_of_reviews', 'stock_status', 'category_group', 'dimensions', 'meta_createdAt', 'meta_updatedAt']]
    df_transformed.to_csv('transformed_data.csv', index=False)

if __name__ == "__main__":
    transform()
