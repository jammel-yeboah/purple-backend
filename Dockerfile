# Use an official Node.js image with Debian
FROM node:18

# Install Python & required system dependencies
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Set the working directory
WORKDIR /app

# Copy package files first (for caching layers)
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Create a virtual environment and install dependencies
RUN python3 -m venv /app/venv
RUN /app/venv/bin/pip install -r requirements.txt

# Expose backend port
EXPOSE 8000

# Start the backend using the virtual environment
CMD ["/app/venv/bin/python", "main.py"]
