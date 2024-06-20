# ETL Project with Meltano and FastAPI

![ETL](https://img.shields.io/badge/ETL-Meltano-blue)
![FastAPI](https://img.shields.io/badge/API-FastAPI-green)
![Docker](https://img.shields.io/badge/Docker-Containerization-orange)

## Overview

This project demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline that extracts data from an API (I used [DummyJSON.com/](https://dummyjson.com/products)), transforms the data, and exposes it through a FastAPI endpoint. The entire solution is containerized using Docker for easy deployment.

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
  - [Docker](#docker)
    - [Build Docker Image](#build-docker-image)
    - [Push to Docker Hub](#push-to-docker-hub)
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

Create a transformation script (`transform_data.py`) to clean and process the data extracted from the API. This involves handling missing values, calculating new fields, and normalizing data.

### Load

The transformed data is saved into a CSV file (`transformed_data.csv`).

## API

Create an API using FastAPI to serve the transformed data. The API reads the transformed CSV file and returns the data in JSON format.

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

### Run Docker Container

To run the Docker container:

```sh
docker run -p 8000:8000 swaviman/meltano_etl_project:latest
```

