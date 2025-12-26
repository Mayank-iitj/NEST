# Deployment Guide - Railway

## Prerequisites
- Railway account (https://railway.app)
- GitHub repository (recommended) or Railway CLI

## Option 1: Deploy via GitHub (Recommended)

### Step 1: Push to GitHub
```bash
cd pharmacovigilance-system
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/pharmacovigilance-system.git
git push -u origin main
```

### Step 2: Create Railway Project
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository

### Step 3: Add Database Services
1. Click "+ New" → "Database" → "PostgreSQL"
2. Click "+ New" → "Database" → "Redis"

### Step 4: Configure Backend Service
1. Select the backend service
2. Go to "Variables" tab
3. Add the following environment variables:

```
DATABASE_URL=${POSTGRES_CONNECTION_STRING}
REDIS_URL=${REDIS_CONNECTION_STRING}
SECRET_KEY=your-random-secret-key-min-32-characters
ENCRYPTION_KEY=your-32-byte-encryption-key-here
OPENAI_API_KEY=sk-your-openai-api-key
WHATSAPP_API_KEY=your-whatsapp-key-or-mock
TWILIO_ACCOUNT_SID=your-twilio-sid-or-mock
TWILIO_AUTH_TOKEN=your-twilio-token-or-mock
ENVIRONMENT=production
CORS_ORIGINS=https://your-frontend-url.railway.app
```

4. Go to "Settings" → "Deploy"
   - Root Directory: `backend`
   - Build Command: (leave default)
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 5: Configure Frontend Service
1. Create new service from same repo
2. Go to "Settings" → "Deploy"
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Start Command: `npx serve -s build -l $PORT`

3. Add environment variable:
```
REACT_APP_API_URL=https://your-backend-url.railway.app
```

### Step 6: Deploy
1. Railway will auto-deploy both services
2. Get public URLs from each service's "Settings" → "Networking"
3. Update CORS_ORIGINS in backend with frontend URL

## Option 2: Deploy via Railway CLI

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Login and Initialize
```bash
railway login
cd pharmacovigilance-system
railway init
```

### Step 3: Create Services
```bash
# Add PostgreSQL
railway add --database postgresql

# Add Redis
railway add --database redis

# Link backend
cd backend
railway link
railway up

# Link frontend
cd ../frontend
railway link
railway up
```

### Step 4: Set Environment Variables
```bash
railway variables set OPENAI_API_KEY=sk-your-key
railway variables set SECRET_KEY=your-secret-key
# ... add other variables
```

### Step 5: Deploy
```bash
railway up
```

## Post-Deployment

### 1. Database Migration
Railway will automatically run the init.sql script on first PostgreSQL connection.

### 2. Verify Health
- Backend: https://your-backend.railway.app/health
- API Docs: https://your-backend.railway.app/api/docs

### 3. Test OTP
Mock mode will work immediately. For real SMS/WhatsApp, add Twilio credentials.

### 4. Monitor Logs
```bash
railway logs
```

## Cost Estimation (Railway)
- Hobby Plan: $5/month per project
- PostgreSQL: Included
- Redis: Included
- Backend + Frontend: ~$10-15/month total

## Troubleshooting

### Database Connection Issues
Ensure DATABASE_URL uses Railway's connection string:
```
postgresql://postgres:password@host.railway.internal:5432/railway
```

### CORS Errors
Update backend CORS_ORIGINS to include frontend URL:
```
CORS_ORIGINS=https://your-frontend.railway.app,https://your-backend.railway.app
```

### Build Failures
Check Railway logs and ensure:
- Python 3.11 is used for backend
- Node 18 is used for frontend
- All dependencies in requirements.txt/package.json

## Scaling
To handle more traffic:
1. Go to service settings
2. Increase instances in "Deploy" settings
3. Enable auto-scaling (Pro plan)

## SSL/TLS
Railway automatically provides SSL certificates for all deployments.
