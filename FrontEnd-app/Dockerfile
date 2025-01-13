# Use Node.js as the base image
FROM node:16

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to install dependencies
COPY package.json  ./

# Install dependencies
RUN npm install

# Copy the rest of the application's source code
COPY . .

# Expose port 3000 for the React development server
EXPOSE 3000

# Command to start the React development server
CMD ["npm", "start"]
