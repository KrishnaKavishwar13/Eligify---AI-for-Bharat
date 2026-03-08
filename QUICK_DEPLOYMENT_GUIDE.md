# Eligify MVP - Quick Deployment Guide

## 🎯 What's Working Now

### Core Features ✅
- User authentication (signup/signin/signout)
- Profile management with education, experience, projects
- Skills tracking and verification
- Internship matching and classification
- Persistent database (JSON-based)
- 26 internships in dataset

### AI Features ⚠️
- Ollama integration configured (llama3.1:8b)
- Project generation endpoint ready
- Resume parsing endpoint ready
- **Note**: AI responses are slow (60-90s) - needs optimization

## 🚀 Quick Deploy Options

### Option 1: Vercel (Frontend) + Railway (Backend) - RECOMMENDED
**Best for**: Fast deployment, free tier available

**Frontend (Vercel)**:
```bash
cd frontend
vercel
```

**Backend (Railway)**:
1. Push to GitHub
2. Connect Railway to repo
3. Set environment variables
4. Deploy from `backend/` folder

**Pros**: Easy, fast, free tier
**Cons**: Need separate Ollama hosting for AI features

---

### Option 2: Single VPS (DigitalOcean/AWS EC2)
**Best for**: Full control, all services together

**Setup**:
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip nodejs npm nginx

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b

# Setup backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --host 0.0.0.0 --port 8000

# Setup frontend
cd frontend
npm install
npm run build
npm start
```

**Pros**: Everything in one place, Ollama included
**Cons**: More setup, costs ~$5-10/month

---

### Option 3: Docker Compose (Any Platform)
**Best for**: Consistent deployment anywhere

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_URL=http://ollama:11434
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
  
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
```

**Pros**: Portable, reproducible
**Cons**: Requires Docker knowledge

---

## 📝 Pre-Deployment Tasks

### 1. Environment Configuration

**Backend (.env)**:
```env
# Required
JWT_SECRET=your-super-secret-jwt-key-change-this
OLLAMA_URL=http://localhost:11434

# Optional
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_USE_MOCK_API=false
```

### 2. Database Migration
Current: JSON files in `backend/data/persistence/`

**For Production**:
- Option A: Keep JSON (simple, works for MVP)
- Option B: Migrate to PostgreSQL/MongoDB (scalable)
- Option C: Use AWS DynamoDB (serverless)

### 3. AI Service Optimization

**Current Issue**: Ollama responses take 60-90 seconds

**Solutions**:
1. **Use faster model**: `ollama pull llama3.1:8b-instruct-q4_0` (quantized)
2. **Add caching**: Cache common project templates
3. **Use cloud AI**: Switch to OpenAI/Anthropic for production
4. **Background jobs**: Generate projects asynchronously

### 4. Security Hardening
- [ ] Change JWT_SECRET to strong random value
- [ ] Enable HTTPS only
- [ ] Add rate limiting
- [ ] Sanitize user inputs
- [ ] Add CSRF protection
- [ ] Implement proper password reset

---

## 🧪 Testing Commands

### Test Backend
```bash
cd backend
python quick_health_check.py
curl http://localhost:8000/health
```

### Test Frontend
```bash
cd frontend
npm run build
npm start
```

### Test AI Features
```bash
cd backend
python test_ai_features.py
```

---

## 🎬 Recommended Deployment Flow

### Phase 1: MVP Deploy (This Week)
1. Deploy frontend to Vercel (5 minutes)
2. Deploy backend to Railway (10 minutes)
3. Disable AI features temporarily (or use OpenAI API)
4. Test with real users

### Phase 2: AI Integration (Next Week)
1. Set up dedicated Ollama server
2. Or integrate OpenAI/Anthropic API
3. Add background job queue
4. Enable AI features

### Phase 3: Production Ready (Week 3)
1. Migrate to production database
2. Add monitoring and logging
3. Set up CI/CD pipeline
4. Add analytics

---

## 💡 Quick Wins Before Deploy

1. **Add loading states** for AI features
2. **Add error messages** when Ollama is down
3. **Create demo video** showing the flow
4. **Write API documentation**
5. **Add health check dashboard**

---

## 🆘 Troubleshooting

### Ollama Too Slow
- Use smaller model: `ollama pull llama3.2:3b`
- Or disable AI and use templates for MVP

### Database Issues
- Check `backend/data/persistence/` has write permissions
- Verify JSON files are valid

### CORS Errors
- Update `backend/src/config/settings.py` CORS_ORIGINS
- Add your production domain

---

**Ready to deploy?** Start with Vercel + Railway for fastest results!
