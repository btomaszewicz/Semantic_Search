FROM python:3.10.6-slim

# Set the working directory inside the container
WORKDIR /app

# Unlikely to change often, so copy first to leverage Docker's build cache
COPY models models

# Copy dependency files first to leverage Docker's build cache
COPY requirements.txt requirements.txt
COPY setup.py setup.py

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++

# Install dependencies
RUN pip install -U pip setuptools wheel
RUN pip install -e .

RUN python -m spacy download en_core_web_sm

# Copy application code
COPY package_folder package_folder

#Run container with hot reload
CMD uvicorn package_folder.api_file:app --reload --host 0.0.0.0 --port $PORT
