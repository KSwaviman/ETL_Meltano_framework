# Step 1: Setup virtual environment
if (-Not (Test-Path "myenv")) {
    python -m venv myenv
}

# Step 2: Activate virtual environment
& myenv\Scripts\Activate

# Step 3: Install dependencies from requirements.txt
pip install -r requirements.txt

# Step 4: Initialize Meltano project if not already initialized
if (-Not (Test-Path ".meltano")) {
    meltano init my_project
    cd my_project

    # Add extractors, loaders, and transformers
    meltano add extractor tap-rest-api-msdk
    meltano add loader target-csv

    # Configure tap-rest-api-msdk
    meltano config tap-rest-api-msdk set api_url https://dummyjson.com/products
    meltano config tap-rest-api-msdk set streams '[{"name": "products", "path": "/", "primary_keys": ["id"], "records_path": "$.products[*]", "num_inference_records": 50}]'

    cd ..
}

# Step 5: Check if loaded_data directory exists, create if not
if (-Not (Test-Path "./loaded_data")) {
    New-Item -ItemType Directory -Path "./loaded_data"
}

# Step 6: Configure target-csv to use the loaded_data directory
meltano config target-csv set destination_path ./loaded_data

# Step 7: Run the Meltano extractor and loader
meltano run tap-rest-api-msdk target-csv

# Step 8: Run the transformation script
python transform_data.py

# Step 9: Start the FastAPI server
Start-Process -NoNewWindow -FilePath "uvicorn" -ArgumentList "app:app --reload"
