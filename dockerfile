# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies (if necessary)
RUN apt-get update && apt-get install -y \
    # Add any system dependencies here, if needed
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir google-api-python-client google-auth-oauthlib Flask

# Copy the local directory contents into the container
# COPY . .
COPY drive_connection.py .
COPY app.py .
COPY token.pickle .

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "./app.py"]
