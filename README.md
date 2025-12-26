# 🏥 Pharmacovigilance Adverse Event Follow-Up System

A real-time, secure, multilingual, fraud-proof, OTP-verified, AI-automated adverse-event follow-up system that increases patient safety, accelerates regulatory compliance, and boosts follow-up response rates.

## 🎯 Key Features

- **Real-time Patient Safety Impact**: Immediate risk assessment and escalation
- **AI-Powered Automation**: OpenAI GPT-4 for missing field detection, risk scoring, and micro follow-up generation
- **Secure Identity Verification**: OTP-based authentication via SMS/WhatsApp
- **Multi-Channel Communication**: WhatsApp, SMS, and email support
- **Multilingual Support**: EN, ES, FR, AR, HI, ZH, PT, RU, DE
- **Medical-Grade Security**: AES-256 encryption, TLS 1.3, RBAC
- **Micro Follow-Up UX**: 20-second questions, no app install required
- **Real-Time Dashboard**: Live metrics and AI performance tracking

## 🏛 System Architecture

### Backend (Python FastAPI)
- FastAPI REST API
- PostgreSQL database
- Redis caching
- OpenAI AI integration
- JWT authentication
- AES-256 encryption

### Frontend (React + Tailwind)
- Mobile-first responsive design
- Custom color palette (#1B211A, #628141, #8BAE66, #EBD5AB)
- Real-time dashboard
- Voice input support
- Scam-safety badges

### Infrastructure
- Docker containerized
- Docker Compose orchestration
- Deployable to Railway, Render, AWS, Azure

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- OpenAI API key (optional, system works in mock mode)

### Setup

1. **Clone or navigate to the project directory:**
```bash
cd pharmacovigilance-system
```

2. **Configure environment variables:**
```bash
# Copy example env file
cp backend/.env.example backend/.env

# Edit backend/.env and add your keys:
# - OPENAI_API_KEY (required for AI features)
# - WHATSAPP_API_KEY (optional, uses mock mode)
# - TWILIO credentials (optional, uses mock mode)
```

3. **Start the system with Docker Compose:**
```bash
docker-compose up --build
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

## 📊 Demo Workflow

1. **Submit Initial Report**
   - Patient submits adverse event with basic information
   - System sends OTP for identity verification

2. **OTP Verification**
   - 6-digit code sent via SMS/WhatsApp
   - 15-minute expiry, 3 attempts allowed

3. **AI Analysis**
   - Detects missing regulatory-relevant fields
   - Calculates risk score (0-100)
   - Classifies as low/medium/high/critical

4. **Micro Follow-Up**
   - Generates 20-second question in user's language
   - Sends via WhatsApp/SMS with secure link
   - Includes scam-safety messaging

5. **Dashboard Updates**
   - Real-time metrics refresh
   - High-risk escalation alerts
   - Compliance tracking

## 📡 API Endpoints

### OTP
- `POST /otp/send` - Send OTP to user
- `POST /otp/verify` - Verify OTP code

### Reports
- `POST /report/reporter` - Create reporter (patient/HCP)
- `POST /report/init` - Initialize adverse event report
- `GET /report/event/{id}` - Get event details
- `POST /report/missing-fields/{id}` - Detect missing fields
- `GET /report/narrative/{id}` - Generate regulatory narrative

### Follow-ups
- `POST /followup/send` - Send follow-up question
- `POST /followup/answer` - Submit answer
- `GET /followup/questions/{event_id}` - Get event questions

### Risk
- `GET /risk/score/{event_id}` - Calculate risk score

### Dashboard
- `GET /dashboard/metrics` - Get real-time metrics

## 🎨 Color Palette

```css
Primary Dark: #1B211A
Accent Green 1: #628141
Accent Green 2: #8BAE66
Sand Light: #EBD5AB
```

## 📈 Success Metrics

The system is designed to achieve:

- **+40%** response rate increase
- **+60%** missing field completion
- **-50%** cycle time reduction
- **90%+** high-risk detection accuracy

## 🔐 Security Features

- **Encryption**: AES-256-GCM for PHI at rest
- **Transport**: TLS 1.3 enforced
- **Authentication**: JWT with short expiry (15-60 min)
- **OTP Verification**: SHA-256 hashed tokens
- **RBAC**: Role-based access control
- **Audit Logging**: Full compliance trail

## 🌍 Supported Languages

EN (English), ES (Spanish), FR (French), AR (Arabic), HI (Hindi), ZH (Chinese), PT (Portuguese), RU (Russian), DE (German)

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Reset database
docker-compose down -v
docker-compose up --build
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ --cov=app

# Frontend (if Node.js installed)
cd frontend
npm test
```

## 📝 Environment Variables

### Required
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - JWT signing key
- `ENCRYPTION_KEY` - AES-256 encryption key (32 bytes)

### Optional (for full functionality)
- `OPENAI_API_KEY` - OpenAI API key for AI features
- `WHATSAPP_API_KEY` - WhatsApp Cloud API key
- `TWILIO_ACCOUNT_SID` - Twilio Account SID
- `TWILIO_AUTH_TOKEN` - Twilio Auth Token
- `TWILIO_PHONE_NUMBER` - Twilio phone number

## 🚢 Deployment

### Railway
1. Create new project on Railway
2. Connect GitHub repository
3. Add PostgreSQL and Redis services
4. Set environment variables
5. Deploy

### Render
1. Create new web service
2. Connect repository
3. Add PostgreSQL database
4. Configure environment variables
5. Deploy

### AWS / Azure
See Docker Compose configuration for container deployment guidance.

## 📚 Documentation

- API Docs: http://localhost:8000/api/docs (Swagger)
- ReDoc: http://localhost:8000/api/redoc
- Database Schema: `database/init.sql`

## 🤝 Contributing

This is a demo/prototype system. For production use:
1. Replace mock messaging with real API credentials
2. Configure production database with backups
3. Enable HTTPS/TLS certificates
4. Implement rate limiting
5. Add comprehensive error monitoring
6. Conduct security audit

## 📄 License

Prototype/Demo System - Not for production medical use without proper validation and regulatory approval.

## ⚠️ Important Notes

- **Mock Mode**: Without API credentials, system runs in mock mode (simulates SMS/WhatsApp)
- **OpenAI**: Requires valid API key for AI features (missing field detection, risk scoring)
- **Medical Data**: Ensure HIPAA/GDPR compliance before handling real patient data
- **Regulatory**: Seek proper regulatory approval before production deployment

## 📞 Support

For questions or issues, refer to the implementation plan in the artifacts directory.
