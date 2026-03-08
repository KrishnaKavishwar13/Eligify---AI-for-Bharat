# Eligify - Deployment Guide

## 🚀 Quick Deploy (5 Minutes)

### Prerequisites
- GitHub account
- Vercel account (free)
- Railway account (free)

### Step 1: Deploy Backend to Railway

1. **Push to GitHub** (if not already)
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Set root directory: `backend`
   - Add environment variables:
     ```
     JWT_SECRET=your-super-secret-key-min-32-chars
     CORS_ORIGINS=https://your-frontend-domain.vercel.app
     ```
   - Deploy!
   - Copy the generated URL (e.g., `https://eligify-backend.up.railway.app`)

### Step 2: Deploy Frontend to Vercel

1. **Deploy on Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project" → Import from GitHub
   - Select your repo
   - Set root directory: `frontend`
   - Add environment variable:
     ```
     NEXT_PUBLIC_API_URL=https://your-railway-backend-url
     NEXT_PUBLIC_USE_MOCK_API=false
     ```
   - Deploy!

2. **Update CORS**:
   - Go back to Railway
   - Update `CORS_ORIGINS` with your Vercel URL
   - Redeploy

### Step 3: Test

Visit your Vercel URL and test:
- Signup/Signin
- Dashboard
- Profile
- Internships
- Projects (without AI for now)

---

## 🐳 Docker Deployment

### Local Testing
```bash
# Build and run all services
docker-compose up --build

# Pull Ollama model
docker exec -it eligify-ollama ollama pull llama3.1:8b

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Ollama: http://localhost:11434
```

### Production with Docker
```bash
# Build images
docker-compose -f docker-compose.prod.yml build

# Deploy to your server
docker-compose -f docker-compose.prod.yml up -d
```

---

## ⚙️ Environment Variables

### Backend Required
```env
JWT_SECRET=min-32-character-secret-key
CORS_ORIGINS=https://frontend-domain.com
```

### Backend Optional
```env
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
LOG_LEVEL=INFO
```

### Frontend Required
```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_USE_MOCK_API=false
```

---

## 🔧 Post-Deployment Configuration

### 1. Database Persistence
Current: JSON files in `backend/data/persistence/`

**For Production**:
- Mount persistent volume for `backend/data/`
- Or migrate to PostgreSQL/MongoDB

### 2. AI Service (Optional)
**Option A**: Keep Ollama (need GPU server)
**Option B**: Switch to OpenAI API (faster, paid)
**Option C**: Disable AI features for MVP

To disable AI temporarily:
```python
# backend/src/services/ai_service.py
# Return mock data instead of calling Ollama
```

### 3. File Uploads
Current: Not implemented

**For Production**:
- Add AWS S3 integration
- Or use Cloudinary
- Update resume upload handler

---

## 📊 Monitoring

### Health Checks
- Backend: `https://your-backend/health`
- Frontend: `https://your-frontend`

### Logs
- Railway: Built-in logs viewer
- Vercel: Built-in logs viewer
- Docker: `docker-compose logs -f`

---

## 🎯 MVP Deployment Strategy

### Phase 1: Core Features (Deploy Now)
- ✅ Authentication
- ✅ Profile management
- ✅ Internship matching
- ✅ Skills tracking
- ❌ AI features (disable for speed)

### Phase 2: AI Features (Week 2)
- Add OpenAI API integration
- Or optimize Ollama setup
- Enable project generation
- Enable resume parsing

### Phase 3: Scale (Week 3+)
- Migrate to production database
- Add caching layer
- Implement CDN
- Add analytics

---

## 🚨 Known Issues & Fixes

### Issue 1: Ollama Slow (60-90s responses)
**Fix**: Use OpenAI API or disable AI for MVP

### Issue 2: JSON Database Not Scalable
**Fix**: Migrate to PostgreSQL when you hit 1000+ users

### Issue 3: No File Upload Storage
**Fix**: Add S3 integration when needed

---

## 📞 Support

- Backend API Docs: `http://your-backend/docs`
- Frontend: Check browser console for errors
- Backend: Check Railway/Docker logs

---

## ✅ Deployment Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend deployed and accessible
- [ ] Environment variables set
- [ ] CORS configured correctly
- [ ] Health checks passing
- [ ] Test user can signup
- [ ] Test user can signin
- [ ] Dashboard loads correctly
- [ ] Internships display
- [ ] Profile page works
- [ ] (Optional) AI features working

**Once all checked, you're live! 🎉**
