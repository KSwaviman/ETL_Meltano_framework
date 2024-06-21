# ETL Project with Meltano and FastAPI

![ETL](https://img.shields.io/badge/ETL-Meltano-blue)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green)
![Docker](https://img.shields.io/badge/Docker-Containerization-orange)

## Overview

This project demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline that extracts data from an API (I used [DummyJSON.com/products](https://dummyjson.com/products)), transforms the data, and exposes it through a FastAPI endpoint. The entire solution is containerized using Docker for easy deployment.

If you intend to run the final solution, skip to the last two steps in the Table of Contents & follow the steps for "Pull Docker Container" & "Run Docker Container".

## Table of Contents

- [ETL Project with Meltano and FastAPI](#etl-project-with-meltano-and-fastapi)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Python Virtual Environment](#python-virtual-environment)
    - [Project Structure](#project-structure)
    - [Install Meltano](#install-meltano)
    - [Install Plugins](#install-plugins)
  - [ETL Pipeline](#etl-pipeline)
    - [Extract](#extract)
    - [Transform](#transform)
    - [Load](#load)
  - [API](#api)
  - [Execution Script](#execution-script)
  - [Docker](#docker)
    - [Build Docker Image](#build-docker-image)
    - [Push to Docker Hub](#push-to-docker-hub)
    - [Pull Docker Container](#pull-docker-container)
    - [Run Docker Container](#run-docker-container)

## Setup

### Python Virtual Environment

1. **Create a virtual environment:**

    ```sh
    python -m venv myenv
    ```

2. **Activate the virtual environment:**

    - **Windows:**

        ```sh
        myenv\Scripts\activate
        ```

### Project Structure

Create a project folder called `my_project` and navigate into it:

```sh
mkdir my_project
cd my_project
```
### Install Meltano

1. **Install Meltano:**

    ```sh
    pip install meltano
    ```

2. **Initialize Meltano project:**

    ```sh
    meltano init my_project
    cd my_project
    ```

### Install Plugins

1. **Install the `tap-rest-api-msdk` extractor:**

    ```sh
    meltano add extractor tap-rest-api-msdk
    ```

2. **Install the `target-csv` loader:**

    ```sh
    meltano add loader target-csv
    ```

## ETL Pipeline

### Extract

Configure the `tap-rest-api-msdk` to extract data from the API by editing the `meltano.yml` file. This involves specifying the API URL and the necessary configurations to extract the data.

### Transform

Create a transformation script (`transform_data.py`) to clean and process the data extracted from the API. This involves handling missing values, calculating new fields, and normalizing data. Follwoing are the basic transformations i applied to the fetched data.

1. **Extract and Flatten Tags:**
   - Converted the nested JSON format in the `tags` column into a comma-separated string for easy readability and analysis.

2. **Calculate Discounted Price:**
   - Created a new column `discounted_price` by applying the discount percentage to the original price. This gave us the actual cost after discount.

3. **Aggregate Reviews:**
   - Calculated the average rating from the `reviews` column by parsing the JSON data and computing the mean of all ratings. The average rating is rounded to one decimal value.
   - Additionally, counted the number of reviews for each product to understand its popularity and feedback volume.

4. **Normalize Dimensions:**
   - Combined the individual dimension columns (`dimensions_width`, `dimensions_height`, `dimensions_depth`) into a single `dimensions` column in the format `widthxheightxdepth`. This provides a compact and standardized view of the product dimensions.

5. **Determine Stock Status:**
   - Added a `stock_status` column that categorizes products as 'Low Stock' if the stock is less than 10, and 'In Stock' otherwise. This helps in quick identification of products that are running low.

6. **Handle Missing Values:**
   - Filled missing values in the `price` column with the mean price. This ensures that no product is left without a price, which is crucial for sales and analysis.
   - For numeric columns, replaced NaN values with 0, and for non-numeric columns, filled NaN values with the mode (most frequent value) of the respective column. This maintains the integrity of the dataset by avoiding gaps.

7. **Convert Dates to Datetime Format:**
   - Converted the `meta_createdAt` and `meta_updatedAt` columns to datetime format, allowing for more accurate time-based analysis and operations.

8. **Categorize Products:**
   - Introduced a new column `category_group` to group products into broader categories like 'Cosmetics' for beauty and makeup products, and 'Other' for the rest. This simplifies category-based filtering and analysis.

9. **Impute NaN Values:**
   - To ensure the dataset is free from any missing values, replaced NaN values in numeric columns with 0 and in non-numeric columns with the most frequent value (mode). This ensures consistency and completeness in the data.

### Load

The transformed data is saved into a CSV file (`transformed_data.csv`).

## API

Create an API using FastAPI to serve the transformed data. The API reads the transformed CSV file and returns the data in JSON format.

## Execution Script
To streamline the execution of the entire ETL pipeline and the FastAPI application, a `run_etl.sh` script is created. This script performs the following steps:

1. Create the loaded_data directory if it doesn't exist.
2. Run the Meltano ETL pipeline to extract and load the data.
3. Transform the data using the transformation script.
4. Start the FastAPI application to serve the data.

## Docker

### Build Docker Image

1. **Create a `Dockerfile` in your project directory.**

2. **Build the Docker image:**

    ```sh
    docker build -t swaviman/meltano_etl_project:latest .
    ```

### Push to Docker Hub

1. **Login to Docker Hub:**

    ```sh
    docker login
    ```

2. **Tag your Docker image:**

    ```sh
    docker tag swaviman/meltano_etl_project:latest
    ```

3. **Push the image:**

    ```sh
    docker push swaviman/meltano_etl_project:latest
    ```

### Pull Docker Container

Make sure Docker Desktop is up and running. To pull the docker image from Docker Hub, run in the terminal:
```sh
docker pull swaviman/meltano_etl_project:latest
```

### Run Docker Container

To run the Docker container:

```sh
docker run -p 8000:8000 swaviman/meltano_etl_project:latest
```

Visit http://127.0.0.1:8000/data in a browser window to view the result.

