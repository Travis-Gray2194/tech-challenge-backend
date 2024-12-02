# Use Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose Flask app port
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=run.py

# Run Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
