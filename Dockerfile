# Use the official Python image from Docker Hub
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory into the container
COPY . .

# Expose the port that your Flask app runs on
EXPOSE 5000

RUN pip install Werkzeug==2.0.2

# Command to run your Flask application
CMD ["python", "app.py"]
