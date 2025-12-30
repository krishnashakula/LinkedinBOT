# Use official n8n image as base
FROM n8nio/n8n:latest

# Set working directory
WORKDIR /home/node

# Set environment variables for production
ENV NODE_ENV=production \
    N8N_PORT=5678 \
    N8N_PROTOCOL=https

# Expose the n8n port
EXPOSE 5678

# Use the entrypoint and command from the base image
# Don't override CMD - let the base image handle it
