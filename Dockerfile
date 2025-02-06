# Use a clean Python 3.11 image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y python3-pip python3-venv

# Create a virtual environment
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Upgrade pip and reinstall dependencies from scratch
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose backend port
EXPOSE 8000

# Start backend
CMD ["python", "main.py"]
