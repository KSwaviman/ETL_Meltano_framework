#!/bin/sh

# Create the loaded_data directory if it doesn't exist
mkdir -p ./loaded_data

# Run the ETL pipeline
meltano run tap-rest-api-msdk target-csv

# Transform the data
python transform_data.py

# Run the FastAPI application
uvicorn app:app --host 0.0.0.0 --port 8000
