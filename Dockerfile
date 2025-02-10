# Use an official Python 3.13 image
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies, including gdbm for shelve support
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-gdbm \
    && rm -rf /var/lib/apt/lists/*

# Copy all files from your local directory to /app in the container
COPY . /app

# Install Python dependencies (with no cache for a clean install)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 for the FastAPI service
EXPOSE 80

# Ensure your Python modules can be found in /app
ENV PYTHONPATH=/app

# Run the main FastAPI app
CMD ["python", "api/main.py"]
