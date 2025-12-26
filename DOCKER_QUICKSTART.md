# 🐳 Docker Quick Start Guide

## Prerequisites

- **Docker Desktop** installed and running
- At least 4GB RAM allocated to Docker
- At least 10GB free disk space

### Install Docker Desktop
- **Windows/Mac**: https://www.docker.com/products/docker-desktop/
- **Linux**: https://docs.docker.com/engine/install/

## 🚀 Quick Start (Easiest Way)

### Windows (PowerShell):
```powershell
.\start.ps1
```

### Linux/Mac (Bash):
```bash
chmod +x start.sh
./start.sh
```

## 🎯 Manual Start

If the scripts don't work, run these commands:

```bash
# Start Docker Desktop first!

# Navigate to project
cd pharmacovigilance-system

# Start all services
docker-compose up --build
```

**Wait 60-90 seconds** for all services to start, then access:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

## 📊 Service Status

Check if services are running:
```bash
docker-compose ps
```

Expected output:
```
NAME          STATUS        PORTS
pv_backend    Up (healthy)  0.0.0.0:8000->8000/tcp
pv_frontend   Up            0.0.0.0:3000->3000/tcp
pv_postgres   Up (healthy)  0.0.0.0:5432->5432/tcp
pv_redis      Up (healthy)  0.0.0.0:6379->6379/tcp
```

## 🔍 View Logs

**All services:**
```bash
docker-compose logs -f
```

**Specific service:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

## 🛑 Stop Services

**Stop (keep data):**
```bash
docker-compose down
```

**Stop and remove data:**
```bash
docker-compose down -v
```

## 🔄 Restart After Code Changes

**Backend changes:**
```bash
docker-compose restart backend
```

**Frontend changes:**
```bash
docker-compose restart frontend
```

**Rebuild everything:**
```bash
docker-compose up --build
```

## ⚙️ Environment Variables

Edit `backend/.env` or set in `docker-compose.yml`:

```bash
# Optional - for full AI features
OPENAI_API_KEY=sk-your-key-here

# Optional - for real SMS/WhatsApp
WHATSAPP_API_KEY=your-key
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
```

**Without these, the system runs in MOCK mode** (perfect for demo).

## 🐛 Troubleshooting

### "Cannot connect to Docker daemon"
→ Start Docker Desktop and wait for it to fully start (whale icon in system tray)

### "Port already in use"
→ Stop conflicting services:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <process-id> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### "Build failed" errors
→ Clean Docker and rebuild:
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

### Frontend shows "Cannot connect to backend"
→ Wait 60 seconds for backend to fully start
→ Check backend logs: `docker-compose logs backend`

### Database connection errors
→ Ensure PostgreSQL is healthy:
```bash
docker-compose exec postgres pg_isready -U pvuser
```

## 📦 What's Running?

| Service | Port | Purpose |
|---------|------|---------|
| **Frontend** | 3000 | React UI |
| **Backend** | 8000 | FastAPI REST API |
| **PostgreSQL** | 5432 | Database |
| **Redis** | 6379 | Cache |

## 💾 Data Persistence

Data is stored in Docker volumes:
- `postgres_data` - All database data persists between restarts

To completely reset the database:
```bash
docker-compose down -v
docker-compose up --build
```

## 🔧 Advanced Docker Commands

**Enter container shell:**
```bash
docker-compose exec backend bash
docker-compose exec postgres psql -U pvuser -d pharmacovigilance
```

**Check resource usage:**
```bash
docker stats
```

**Clean up everything:**
```bash
docker-compose down -v
docker system prune -a -f --volumes
```

## ✅ System Requirements

**Minimum:**
- 2 CPU cores
- 4GB RAM
- 10GB disk space

**Recommended:**
- 4 CPU cores
- 8GB RAM
- 20GB disk space

## 🎯 Demo Flow

Once services are running:

1. Open http://localhost:3000
2. Submit an adverse event report
3. Verify with OTP (works in mock mode)
4. View AI risk assessment
5. Check live dashboard at http://localhost:3000/dashboard
6. Explore API at http://localhost:8000/api/docs

## 🔐 Security Notes

**Development Mode:**
- Mock OTP codes (any 6 digits work)
- Default database credentials
- CORS allows all origins

**Before Production:**
- Change all passwords in docker-compose.yml
- Set real API keys
- Enable TLS/HTTPS
- Restrict CORS origins

## 📚 More Information

- Full README: [README.md](./README.md)
- Deployment guides: [DEPLOY_RAILWAY.md](./DEPLOY_RAILWAY.md), [DEPLOY_RENDER.md](./DEPLOY_RENDER.md)
- Complete walkthrough: See artifacts directory

---

**The easiest way**: Just run `.\start.ps1` (Windows) or `./start.sh` (Linux/Mac)! 🚀
