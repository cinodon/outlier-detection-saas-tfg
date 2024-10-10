# Use a light image for Node
FROM node:16-alpine

# Set th working directory
WORKDIR /app

# Copy json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build app
RUN npm run build

# Server for the app
RUN npm install -g serve
CMD ["serve", "-s", "build"]

# Expose port 3000
EXPOSE 3000
