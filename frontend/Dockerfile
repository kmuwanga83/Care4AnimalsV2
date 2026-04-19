# Use Node.js for building
FROM node:20-slim

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the code
COPY . .

# Expose the Vite port
EXPOSE 5173

# Run the dev server
CMD ["npm", "run", "dev", "--", "--host"]