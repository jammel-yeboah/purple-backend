# Use an official Python + Node.js image
FROM node:18

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Copy package files first (for caching layers)
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the app
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose backend port
EXPOSE 8000

# Start the backend
CMD ["python3", "main.py"]
