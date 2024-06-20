from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
import json

app = FastAPI()

# Define a function to handle out-of-range float values
def handle_out_of_range_values(df):
    for column in df.select_dtypes(include=[np.float64]):
        df[column] = df[column].apply(lambda x: None if pd.isna(x) or x > np.finfo(np.float64).max or x < -np.finfo(np.float64).max else x)
    return df

@app.get("/data")
def read_data():
    try:
        # Read the transformed CSV file into a DataFrame
        df = pd.read_csv('transformed_data.csv')
        
        # Handle out-of-range float values
        df = handle_out_of_range_values(df)
        
        # Replace NaN values with None for JSON serialization
        df = df.where(pd.notnull(df), None)
        
        # Convert the DataFrame to a dictionary with records orientation
        data = df.to_dict(orient="records")
        
        # Convert data to JSON-safe format
        safe_data = json.loads(json.dumps(data, default=str))
        
        return safe_data
    except Exception as e:
        # Raise HTTPException if there is any error in reading or processing the CSV file
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
