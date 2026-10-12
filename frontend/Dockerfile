# Multi-stage Dockerfile for IT Helpdesk Frontend (React 18 + Vite 5)

# -------------------------------------------------------------
# Stage 1: Build static distribution
# -------------------------------------------------------------
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies using cached package locks
COPY package*.json ./
RUN npm ci

# Copy application source code
COPY . .

# Set build-time API base URL to relative path /api (handled by Nginx reverse proxy)
ENV VITE_API_URL=/api
RUN npm run build

# -------------------------------------------------------------
# Stage 2: Production Nginx Server
# -------------------------------------------------------------
FROM nginx:alpine

LABEL maintainer="DevOps Team <devops@ithelpdesk.local>"
LABEL description="IT Helpdesk Frontend Web Server (Nginx)"
LABEL version="1.0.0"

# Purge default static files
RUN rm -rf /usr/share/nginx/html/*

# Copy compiled static assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Apply reverse proxy configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port 80
EXPOSE 80

# Healthcheck for frontend web server
HEALTHCHECK --interval=20s --timeout=5s --start-period=10s --retries=3 \
  CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1

# Start Nginx in foreground mode
CMD ["nginx", "-g", "daemon off;"]
