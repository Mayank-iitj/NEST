# Deployment Guide - Render

## Prerequisites
- Render account (https://render.com)
- GitHub repository

## Step 1: Push to GitHub
```bash
cd pharmacovigilance-system
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/pharmacovigilance-system.git
git push -u origin main
```

## Step 2: Create PostgreSQL Database
1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `pv-database`
   - Database: `pharmacovigilance`
   - User: `pvuser`
   - Region: Choose closest to your users
   - Plan: Free or Starter ($7/month)
4. Click "Create Database"
5. Copy the "Internal Database URL" for later

## Step 3: Create Redis Instance
1. Click "New +" → "Redis"
2. Configure:
   - Name: `pv-redis`
   - Plan: Free or Starter ($10/month)
   - Region: Same as database
3. Click "Create Redis"
4. Copy the "Internal Redis URL"

## Step 4: Deploy Backend Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `pv-backend`
   - Region: Same as database
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free or Starter ($7/month)

4. Add Environment Variables:
```
DATABASE_URL=<paste Internal Database URL>
REDIS_URL=<paste Internal Redis URL>
SECRET_KEY=your-random-secret-key-min-32-characters
ENCRYPTION_KEY=your-32-byte-encryption-key
OPENAI_API_KEY=sk-your-openai-api-key
WHATSAPP_API_KEY=mock
TWILIO_ACCOUNT_SID=mock
TWILIO_AUTH_TOKEN=mock
ENVIRONMENT=production
PYTHON_VERSION=3.11.0
```

5. Click "Create Web Service"

## Step 5: Initialize Database
After backend deploys:
1. Go to PostgreSQL database dashboard
2. Click "Connect" → "External Connection"
3. Use provided credentials to connect via psql or pgAdmin
4. Run the init.sql script:
```bash
psql -h <hostname> -U pvuser -d pharmacovigilance -f database/init.sql
```

Or use Render Shell:
1. Go to backend service
2. Click "Shell" tab
3. Run: `python -c "from app.core.database import Base, engine; Base.metadata.create_all(engine)"`

## Step 6: Deploy Frontend Service
1. Click "New +" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - Name: `pv-frontend`
   - Branch: `main`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `build`

4. Add Environment Variable:
```
REACT_APP_API_URL=https://pv-backend.onrender.com
```
(Replace with your actual backend URL)

5. Click "Create Static Site"

## Step 7: Update CORS
After frontend deploys:
1. Go to backend service
2. Add to Environment Variables:
```
CORS_ORIGINS=https://pv-frontend.onrender.com,https://pv-backend.onrender.com
```
3. Trigger redeploy

## Step 8: Verify Deployment
1. Frontend: https://pv-frontend.onrender.com
2. Backend API: https://pv-backend.onrender.com/api/docs
3. Health Check: https://pv-backend.onrender.com/health

## Auto-Deploy Setup
Render automatically deploys on git push to main branch.

## Cost Estimation (Render)
- PostgreSQL Starter: $7/month
- Redis Starter: $10/month (optional, can use free tier)
- Backend Web Service: $7/month (free tier available with limitations)
- Frontend Static Site: Free
- **Total: ~$14-24/month** (or free with limitations)

## Free Tier Limitations
- Services spin down after 15 min of inactivity
- 750 hours/month free compute
- Slower cold starts

## Custom Domain
1. Go to frontend static site
2. Click "Settings" → "Custom Domain"
3. Add your domain and configure DNS

## SSL/TLS
Render automatically provides SSL certificates for all services.

## Monitoring
1. Go to service dashboard
2. Click "Metrics" to view:
   - Response times
   - Memory usage
   - CPU usage
   - Request volume

## Logs
1. Go to service dashboard
2. Click "Logs" tab
3. Filter by severity or search

## Troubleshooting

### Database Connection Failed
- Ensure using Internal Database URL (ends with `.render-internal.com`)
- Check database is in same region as backend

### OOM (Out of Memory) Errors
- Upgrade to larger instance
- Or optimize Python worker count in start command:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2
```

### Slow Cold Starts
- Upgrade to paid plan (always-on instances)
- Or implement health check endpoint pinging

## Scaling
To handle more traffic:
1. Go to service settings
2. Increase instance type
3. Add more instances (paid plans)
