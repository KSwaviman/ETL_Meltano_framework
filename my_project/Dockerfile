# Use an official Python runtime as a parent image
FROM python:3.10.5-slim

# Install git and other necessary dependencies
RUN apt-get update && apt-get install -y git

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Meltano
RUN pip install meltano

# Initialize Meltano project ( meltano.yml is in /app)
RUN meltano install

# Install the specific tap and target
RUN meltano install extractor tap-rest-api-msdk
RUN meltano install loader target-csv

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Ensure the shell script is executable
RUN chmod +x run_etl.sh

# Run the script
CMD ["./run_etl.sh"]
