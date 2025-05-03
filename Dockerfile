# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 5002 available to the world outside this container
# (Gunicorn default port, can be overridden)
EXPOSE 5002

# Define environment variables (optional, can be set at runtime)
# ENV FLASK_APP=run.py
# ENV FLASK_RUN_HOST=0.0.0.0
# Using Gunicorn, these might not be needed directly by Flask

# Command to run the application using Gunicorn
# Bind to 0.0.0.0 so it's accessible from outside the container
# run:app refers to the 'app' variable in 'run.py'
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "run:app"]
