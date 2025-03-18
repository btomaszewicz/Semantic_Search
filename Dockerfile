FROM python:3.10.6-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first to leverage Docker's build cache
COPY requirements.txt requirements.txt
COPY setup.py setup.py

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -e .

# Copy application code
COPY models models
COPY package_folder package_folder


#Run container locally
# CMD uvicorn package_folder.api_file:app --reload --host 0.0.0.0

#Run container deployed -> GCP
CMD uvicorn package_folder.api_file:app --reload --host 0.0.0.0 --port $PORT
