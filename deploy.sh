#!/bin/bash
# Deployment script for production

set -e

echo "🚀 Starting deployment process..."

# Check if .env exists
if [ ! -f backend/.env ]; then
    echo "❌ Error: backend/.env not found!"
    echo "Please copy backend/.env.example to backend/.env and configure it."
    exit 1
fi

# Generate secure keys if needed
echo "🔐 Checking security keys..."
if grep -q "change-this" backend/.env; then
    echo "⚠️  Warning: Default security keys detected!"
    echo "Generating secure keys..."
    
    SECRET_KEY=$(openssl rand -hex 32)
    ENCRYPTION_KEY=$(openssl rand -hex 16)
    
    echo "Generated SECRET_KEY: $SECRET_KEY"
    echo "Generated ENCRYPTION_KEY: $ENCRYPTION_KEY"
    echo ""
    echo "Please update these in backend/.env before deploying to production!"
fi

# Build production images
echo "🏗️  Building production Docker images..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Run database migrations
echo "📊 Running database migrations..."
docker-compose -f docker-compose.prod.yml up -d postgres
sleep 5
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U pvuser -d pharmacovigilance -f /docker-entrypoint-initdb.d/init.sql || echo "Database already initialized"

# Start all services
echo "🌟 Starting all services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Health checks
echo "🏥 Running health checks..."

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
fi

# Check frontend
if curl -f http://localhost:80 > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    docker-compose -f docker-compose.prod.yml logs frontend nginx
    exit 1
fi

echo ""
echo "🎉 Deployment successful!"
echo ""
echo "📍 Service URLs:"
echo "   Frontend: http://localhost"
echo "   Backend API: http://localhost/api"
echo "   API Docs: http://localhost/api/docs"
echo ""
echo "📊 To view logs:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose -f docker-compose.prod.yml down"
echo ""
