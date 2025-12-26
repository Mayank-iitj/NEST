# Deployment script for Windows PowerShell

Write-Host "🚀 Starting deployment process..." -ForegroundColor Green

# Check if .env exists
if (-Not (Test-Path "backend\.env")) {
    Write-Host "❌ Error: backend\.env not found!" -ForegroundColor Red
    Write-Host "Please copy backend\.env.example to backend\.env and configure it."
    exit 1
}

# Check for default keys
$envContent = Get-Content "backend\.env" -Raw
if ($envContent -match "change-this") {
    Write-Host "⚠️  Warning: Default security keys detected!" -ForegroundColor Yellow
    Write-Host "You should generate secure keys before deploying to production:"
    Write-Host ""
    Write-Host "For SECRET_KEY and ENCRYPTION_KEY, use:"
    Write-Host "  [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))"
    Write-Host ""
}

# Build production images
Write-Host "🏗️  Building production Docker images..." -ForegroundColor Cyan
docker-compose -f docker-compose.prod.yml build --no-cache

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    exit 1
}

# Start database first
Write-Host "📊 Starting database..." -ForegroundColor Cyan
docker-compose -f docker-compose.prod.yml up -d postgres redis
Start-Sleep -Seconds 10

# Start all services
Write-Host "🌟 Starting all services..." -ForegroundColor Cyan
docker-compose -f docker-compose.prod.yml up -d

# Wait for services
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Health checks
Write-Host "🏥 Running health checks..." -ForegroundColor Cyan

# Check backend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Backend is healthy" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Backend health check failed" -ForegroundColor Red
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
}

# Check frontend via nginx
try {
    $response = Invoke-WebRequest -Uri "http://localhost/" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Frontend is healthy" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Frontend health check failed" -ForegroundColor Red
    docker-compose -f docker-compose.prod.yml logs frontend nginx
    exit 1
}

Write-Host ""
Write-Host "🎉 Deployment successful!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Service URLs:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost"
Write-Host "   Backend API: http://localhost/api"
Write-Host "   API Docs: http://localhost/api/docs"
Write-Host ""
Write-Host "📊 To view logs:" -ForegroundColor Cyan
Write-Host "   docker-compose -f docker-compose.prod.yml logs -f"
Write-Host ""
Write-Host "🛑 To stop services:" -ForegroundColor Cyan
Write-Host "   docker-compose -f docker-compose.prod.yml down"
Write-Host ""
