# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the app to run on
EXPOSE 8080

# Set the environment variable for the bot to run
ENV ENVIRONMENT=ANYTHING

# Run the bot when the container starts
CMD ["python3", "fsubbot.py"]
