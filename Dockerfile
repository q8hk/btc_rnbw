# Use an official Python runtime as a parent image (smallest version - Alpine Linux)
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Define the command to run your bot script
CMD ["python", "app.py"]
