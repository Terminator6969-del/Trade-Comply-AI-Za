FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY apps/web/package*.json ./

# Install dependencies
RUN npm ci

# Copy application code
COPY apps/web .

# Build
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY apps/web/package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# Copy built app from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY apps/web/next.config.js .
COPY apps/web/tsconfig.json .

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

# Run the app
CMD ["npm", "start"]
