# 🚀 Quick Start Guide

## For Immediate Demo (5 minutes)

### Option 1: Docker Compose (Recommended if Docker installed)

```bash
cd C:\Users\MS\.gemini\antigravity\scratch\pharmacovigilance-system

# Start all services
docker-compose up --build
```

**Access**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Option 2: Without Docker (Manual Setup)

**Backend**:
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend** (requires Node.js):
```bash
cd frontend
npm install
npm start
```

## For Production Deployment

### Railway (Easiest - 15 minutes)
See [DEPLOY_RAILWAY.md](file:///C:/Users/MS/.gemini/antigravity/scratch/pharmacovigilance-system/DEPLOY_RAILWAY.md)

1. Push to GitHub
2. Connect to Railway
3. Add PostgreSQL + Redis
4. Set environment variables
5. Deploy!

**Cost**: ~$10-15/month

### Render (Free tier available - 20 minutes)
See [DEPLOY_RENDER.md](file:///C:/Users/MS/.gemini/antigravity/scratch/pharmacovigilance-system/DEPLOY_RENDER.md)

1. Push to GitHub
2. Create database + Redis
3. Deploy backend web service
4. Deploy frontend static site
5. Configure environment

**Cost**: Free or ~$14-24/month

### Production Docker (Self-hosted)

**Windows**:
```powershell
.\deploy.ps1
```

**Linux/Mac**:
```bash
chmod +x deploy.sh
./deploy.sh
```

## Environment Setup

Before deployment, configure `backend/.env.example` and save as `backend/.env`:

```bash
# Required
SECRET_KEY=<generate-32-char-random-string>
ENCRYPTION_KEY=<generate-32-byte-random-string>
DATABASE_URL=<your-postgres-url>

# Optional (for full features)
OPENAI_API_KEY=sk-<your-key>  # AI features
WHATSAPP_API_KEY=<your-key>   # Real WhatsApp (or use "mock")
TWILIO_ACCOUNT_SID=<your-sid> # Real SMS (or use "mock")
```

**Generate secure keys**:
```powershell
# PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
```

## What's Included

✅ **Backend** (23 Python files)
- FastAPI REST API
- PostgreSQL database
- OpenAI GPT-4 integration
- OTP verification
- Multi-channel messaging
- Risk scoring engine

✅ **Frontend** (11 React files)
- OTP modal with 6-digit verification
- Micro-form (20-second questions)
- Real-time metrics dashboard
- Risk visualization
- Mobile-responsive UI

✅ **Infrastructure**
- Docker + Docker Compose
- Production Dockerfiles
- Nginx reverse proxy
- Health checks
- Rate limiting

✅ **Documentation**
- README.md
- Deployment guides (Railway, Render)
- API documentation
- Security checklist

## System Features

🔒 **Security**
- AES-256 encryption
- JWT authentication
- OTP verification
- RBAC roles
- Audit logging

🤖 **AI Automation**
- Missing field detection
- Risk scoring (0-100)
- Micro question generation
- Regulatory narratives

📱 **Multi-Channel**
- WhatsApp (preferred)
- SMS (fallback)
- Email (fallback)
- Voice input support

🌍 **Multilingual**
- EN, ES, FR, AR, HI, ZH, PT, RU, DE

📊 **Metrics**
- Real-time dashboard
- Response rate tracking
- Risk analytics
- AI performance monitoring

## Testing the Demo

1. **Submit Report** → OTP sent
2. **Verify OTP** → AI analyzes event
3. **View Risk** → Color-coded dashboard
4. **Send Follow-up** → Micro question generated
5. **Check Metrics** → Live updates every 5s

## Directory Structure

```
pharmacovigilance-system/
├── backend/           Backend API (FastAPI)
├── frontend/          Frontend UI (React)
├── database/          PostgreSQL schema
├── nginx/             Reverse proxy config
├── README.md          Full documentation
├── DEPLOY_RAILWAY.md  Railway guide
├── DEPLOY_RENDER.md   Render guide
├── DEPLOYMENT_CHECKLIST.md  100+ item checklist
├── docker-compose.yml       Development
├── docker-compose.prod.yml  Production
├── deploy.sh          Linux deployment script
└── deploy.ps1         Windows deployment script
```

## Getting Help

📖 **Documentation**:
- [README.md](file:///C:/Users/MS/.gemini/antigravity/scratch/pharmacovigilance-system/README.md) - Complete system documentation
- [Walkthrough](file:///C:/Users/MS/.gemini/antigravity/brain/205156ba-780c-4011-9272-70c4ac0b8be8/walkthrough.md) - Implementation details
- [API Docs](http://localhost:8000/api/docs) - Interactive API documentation

🔧 **Troubleshooting**:
See deployment guides for platform-specific issues.

⚠️ **Important Notes**:
- Mock mode works without API keys for demo
- Add OpenAI key for full AI features
- HTTPS required for production
- Complete security audit before real PHI data

## Project Location

```
C:\Users\MS\.gemini\antigravity\scratch\pharmacovigilance-system
```

**Total Files**: 45+ files created
**Ready for**: Demo, Development, Production Deployment
