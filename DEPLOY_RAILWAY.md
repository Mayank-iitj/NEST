# Railway Deployment Guide - Fixed for Monorepo

## ✅ Project Structure Fixed

This project is now properly configured for Railway deployment with:
- `backend/nixpacks.toml` - Backend build configuration
- `frontend/nixpacks.toml` - Frontend build configuration
- Separate service deployment support

## 🚂 Deploy to Railway - Step by Step

### Step 1: Create New Project

1. Go to https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Authorize and select `Mayank-iitj/NEST`

### Step 2: Deploy Backend Service

**IMPORTANT**: You need to create the backend service FIRST.

1. After connecting the repo, Railway will show "Failed to detect"
2. Click **"Settings"** in the left sidebar
3. Under **"Service Settings"**:
   - **Root Directory**: `backend`
   - **Build Command**: (leave default - nixpacks will detect)
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 4`

4. Click **"Variables"** tab and add:

```bash
# These will be auto-filled by Railway plugins
DATABASE_URL=${POSTGRES_CONNECTION_STRING}
REDIS_URL=${REDIS_CONNECTION_STRING}

# You must set these manually
SECRET_KEY=your-random-32-character-secret-key-here
ENCRYPTION_KEY=your-random-32-byte-encryption-key-here
OPENAI_API_KEY=sk-your-openai-api-key
ENVIRONMENT=production
CORS_ORIGINS=*
WHATSAPP_API_KEY=mock
TWILIO_ACCOUNT_SID=mock
TWILIO_AUTH_TOKEN=mock
```

**Generate secure keys:**
```bash
# SECRET_KEY (32 chars)
openssl rand -hex 32

# ENCRYPTION_KEY (32 bytes)
openssl rand -hex 16
```

### Step 3: Add Database Services

1. Click **"+ New"** in your project
2. Select **"Database" → "PostgreSQL"**
   - Railway will automatically set `POSTGRES_CONNECTION_STRING`
   - This becomes `DATABASE_URL` in your backend

3. Click **"+ New"** again
4. Select **"Database" → "Redis"**
   - Railway will automatically set `REDIS_CONNECTION_STRING`
   - This becomes `REDIS_URL` in your backend

### Step 4: Deploy Frontend Service (Optional)

1. In the same project, click **"+ New"**
2. Select **"GitHub Repo"** → Choose `Mayank-iitj/NEST` again
3. Go to **"Settings"**:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npx serve -s build -l $PORT`

4. Add **Variables**:
```bash
REACT_APP_API_URL=https://your-backend-service.railway.app
```
(Replace with your actual backend Railway URL)

### Step 5: Deploy & Verify

1. Save all settings
2. Railway will automatically deploy both services
3. Check deployment logs for any errors
4. Get your service URLs:
   - Backend: https://your-backend.railway.app
   - Frontend: https://your-frontend.railway.app

5. Test endpoints:
   - Backend health: `https://your-backend.railway.app/health`
   - API docs: `https://your-backend.railway.app/api/docs`
   - Frontend: `https://your-frontend.railway.app`

## 🔧 Troubleshooting

### "Railpack could not determine how to build"
✅ **FIXED** - Root Directory must be set to `backend` or `frontend`

### Build Fails
- Check **Logs** tab in Railway dashboard
- Verify `nixpacks.toml` exists in the service directory
- Ensure all dependencies are in `requirements.txt` or `package.json`

### Database Connection Issues
- Use the **internal** connection string (ends with `.railway.internal`)
- Railway automatically injects these as environment variables

### CORS Errors
- Set `CORS_ORIGINS` to include your frontend URL
- Or use `*` for testing (not recommended for production)

## 💰 Cost Estimate

- **Starter Plan**: $5/month
- **PostgreSQL**: Included
- **Redis**: Included  
- **Backend + Frontend**: ~$10-15/month total

Free trial: $5 credit (runs backend for ~1 month)

## 🎯 Alternative: Backend Only on Railway

**Cheaper option**: 
- Deploy only backend + databases on Railway
- Deploy frontend on **Vercel** (free for React apps)

### Deploy Frontend to Vercel:
1. Go to https://vercel.com/new/import
2. Import `Mayank-iitj/NEST`
3. Framework: Create React App
4. Root Directory: `frontend`
5. Environment Variable: `REACT_APP_API_URL=https://your-backend.railway.app`
6. Deploy!

**Cost**: Railway backend + Vercel frontend = ~$10/month total

## ✅ You're Ready!

Railway will now properly detect and build your project. Just follow the steps above!
