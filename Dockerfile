# Use an official Python runtime as a parent image
FROM python:3.12.5-alpine3.20

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory contents into the container at /app
COPY src/ .

# Run main.py when the container launches
CMD ["python", "main.py"]
