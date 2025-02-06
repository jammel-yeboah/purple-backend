# Use the official Node.js image as the base image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json first (for better caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN apt-get update && apt-get install -y python3 build-essential && npm install

# Copy the rest of your application code
COPY . .

# Expose the port your app runs on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
