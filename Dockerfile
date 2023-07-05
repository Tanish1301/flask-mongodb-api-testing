# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory inside the Docker image
WORKDIR /app

# Copy the application files to the Docker image
COPY . /app

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the necessary ports
EXPOSE 5000

# Set environment variables for MongoDB connection
ENV MONGO_HOST=mongodb
ENV MONGO_PORT=27017
ENV MONGO_DB=mydatabase

# Start the Flask application
CMD ["python", "app.py"]
