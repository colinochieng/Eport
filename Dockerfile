# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . /app

# Make port 8080 available to the world outside this container
EXPOSE 8000

# Default to listening on port 8000 (for local development)
ENV PORT=8000

# Run the application
CMD ["sh", "-c", "gunicorn -w 2 -b 0.0.0.0:$PORT app:app"]
