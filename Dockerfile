# Use official n8n image as base
FROM n8nio/n8n:latest

# Set working directory
WORKDIR /home/node

# Set environment variables for production
ENV NODE_ENV=production
ENV N8N_PORT=5678
ENV N8N_PROTOCOL=https
ENV WEBHOOK_URL=https://$RAILWAY_PUBLIC_DOMAIN

# Expose the n8n port
EXPOSE 5678

# Use the default n8n entrypoint
CMD ["n8n"]
