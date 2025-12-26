# Docker Quick Start Script for Windows PowerShell
# Pharmacovigilance System

Write-Host "🐳 Starting Pharmacovigilance System with Docker..." -ForegroundColor Green
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again."
    exit 1
}

Write-Host ""

# Stop any existing containers
Write-Host "🛑 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down -v 2>$null

Write-Host ""
Write-Host "🏗️  Building and starting services..." -ForegroundColor Cyan
Write-Host "This may take a few minutes on first run..." -ForegroundColor Yellow
Write-Host ""

# Build and start all services
docker-compose up --build -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start services!" -ForegroundColor Red
    Write-Host "Check Docker Desktop and try again."
    exit 1
}

Write-Host ""
Write-Host "⏳ Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check service health
Write-Host ""
Write-Host "🏥 Checking service health..." -ForegroundColor Cyan

# Check PostgreSQL
try {
    docker-compose exec -T postgres pg_isready -U pvuser -d pharmacovigilance | Out-Null
    Write-Host "✅ PostgreSQL is ready" -ForegroundColor Green
} catch {
    Write-Host "⚠️  PostgreSQL is starting (this is normal on first run)" -ForegroundColor Yellow
}

# Check Redis
try {
    docker-compose exec -T redis redis-cli ping | Out-Null
    Write-Host "✅ Redis is ready" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Redis is starting" -ForegroundColor Yellow
}

# Check Backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Backend API is ready" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend is starting (wait 30-60 seconds)" -ForegroundColor Yellow
}

# Check Frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✅ Frontend is ready" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Frontend is starting (wait 30-60 seconds)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Services are starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Access URLs:" -ForegroundColor Cyan
Write-Host "   Frontend:  http://localhost:3000"
Write-Host "   Backend:   http://localhost:8000"
Write-Host "   API Docs:  http://localhost:8000/api/docs"
Write-Host ""
Write-Host "📊 View logs:" -ForegroundColor Cyan
Write-Host "   docker-compose logs -f"
Write-Host ""
Write-Host "🛑 Stop services:" -ForegroundColor Cyan
Write-Host "   docker-compose down"
Write-Host ""
Write-Host "💡 If services aren't ready yet, wait 60 seconds and refresh your browser" -ForegroundColor Yellow
Write-Host ""
