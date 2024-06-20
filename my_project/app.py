# Import the necessary libraries
from fastapi import FastAPI
import pandas as pd

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route to get the data from the CSV file
@app.get("/data")
def read_data():
    # Read the transformed CSV file into a DataFrame
    df = pd.read_csv('transformed_data.csv')
    # Convert the DataFrame to a dictionary with records orientation
    return df.to_dict(orient="records")

# This block runs the application if the script is executed directly
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app on host 0.0.0.0 and port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
