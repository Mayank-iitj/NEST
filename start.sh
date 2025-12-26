#!/bin/bash
# Docker Quick Start Script for Pharmacovigilance System

echo "🐳 Starting Pharmacovigilance System with Docker..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down -v 2>/dev/null || true

echo ""
echo "🏗️  Building and starting services..."
echo "This may take a few minutes on first run..."
echo ""

# Build and start all services
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo ""
echo "🏥 Checking service health..."

# Check PostgreSQL
if docker-compose exec -T postgres pg_isready -U pvuser -d pharmacovigilance > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "⚠️  PostgreSQL is starting (this is normal on first run)"
fi

# Check Redis
if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "⚠️  Redis is starting"
fi

# Check Backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is ready"
else
    echo "⚠️  Backend is starting (wait 30-60 seconds)"
fi

# Check Frontend
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is ready"
else
    echo "⚠️  Frontend is starting (wait 30-60 seconds)"
fi

echo ""
echo "🎉 Services are starting up!"
echo ""
echo "📍 Access URLs:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/api/docs"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
echo "💡 If services aren't ready yet, wait 60 seconds and refresh your browser"
echo ""
