# Use an official Python runtime as a base image
FROM python:3.10-slim

# Install necessary packages for Tesseract and other dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies (Poetry or requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=app.py

# Expose the port that Flask runs on
EXPOSE 5000

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
