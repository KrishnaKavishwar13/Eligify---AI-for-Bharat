# 🚀 Quick Start Guide - Eligify MVP

**Welcome to the team!** This guide will get you up and running in 15 minutes.

---

## 📋 What You Need to Know

### Project Overview
Eligify is an AI-powered employability platform that:
1. Extracts skills from student resumes using AI
2. Matches students with internships using a deterministic algorithm
3. Generates personalized projects to fill skill gaps
4. Verifies skills when projects are completed
5. Shows newly eligible internships after skill verification

### Tech Stack
- **Backend**: Python FastAPI + Ollama (Llama 3.1 8B)
- **Frontend**: Next.js 14 + React + TypeScript + Tailwind CSS
- **Database**: Mock in-memory store (DynamoDB-ready)
- **Auth**: JWT tokens

### Current Status
- ✅ Core backend features complete (auth, profile, skills, projects)
- ✅ Basic frontend pages complete (landing, auth, profile, dashboard)
- ⏳ Need: UI components, eligibility engine, integration polish

---

## 🎯 Your Role

### If You're the Backend/AI Developer
**Read**: `TEAM_HANDOFF_BACKEND.md`

**Your Focus**:
1. Eligibility engine (match score calculation)
2. Project storage & retrieval
3. Error handling & optimization
4. AI integration improvements

**Your First Task**: Implement eligibility engine (Task 6.1-6.2)

---

### If You're the Frontend Developer
**Read**: `TEAM_HANDOFF_FRONTEND.md`

**Your Focus**:
1. Skill graph visualization component
2. Internship cards & detail modal
3. Project generation modal & detail page
4. Dashboard enhancements

**Your First Task**: Build skill graph component (Task 12.3)

---

## ⚡ 15-Minute Setup

### Step 1: Clone the Repository
```bash
# Clone the repo (if not already done)
git clone <repository-url>
cd eligify-platform
```

### Step 2: Backend Setup (5 minutes)
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env if needed (defaults should work)

# Start the server
python src/main.py
```

✅ Backend should be running at: `http://127.0.0.1:8000`

### Step 3: Ollama Setup (5 minutes)
```bash
# Install Ollama (if not already installed)
# Windows/Mac: Download from https://ollama.ai
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Pull the model
ollama pull llama3.1:8b

# Verify it's working
ollama list
```

✅ You should see `llama3.1:8b` in the list

### Step 4: Frontend Setup (5 minutes)
```bash
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local:
# NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Start dev server
npm run dev
```

✅ Frontend should be running at: `http://localhost:3000`

---

## 🧪 Verify Everything Works

### Test 1: Backend API
Open browser: `http://127.0.0.1:8000/docs`

You should see the FastAPI Swagger documentation.

### Test 2: Frontend Landing Page
Open browser: `http://localhost:3000`

You should see the Eligify landing page with purple/pink gradients.

### Test 3: End-to-End Demo
```bash
cd backend
python demo_complete_flow.py
```

You should see:
- ✅ User created
- ✅ Resume parsed (17 skills extracted)
- ✅ Internships classified (2 almost eligible)
- ✅ Project generated

### Test 4: Sign Up Flow
1. Go to `http://localhost:3000`
2. Click "Get Started"
3. Sign up with test credentials
4. You should be redirected to dashboard

---

## 📁 Project Structure

```
eligify-platform/
├── backend/                    # Python FastAPI backend
│   ├── src/
│   │   ├── main.py            # Entry point
│   │   ├── handlers/          # API routes
│   │   ├── services/          # Business logic
│   │   ├── models/            # Pydantic models
│   │   └── utils/             # Utilities
│   ├── data/                  # Seed data
│   ├── tests/                 # Test files
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Next.js 14 frontend
│   ├── app/                   # Pages (App Router)
│   ├── components/            # React components
│   ├── lib/                   # Utilities (API, auth)
│   └── package.json           # Node dependencies
│
├── .kiro/specs/               # Project specifications
│   └── eligify-platform/
│       ├── requirements.md    # Requirements
│       ├── design.md          # Design document
│       └── tasks.md           # Task list
│
├── TEAM_HANDOFF_BACKEND.md    # Backend developer guide
├── TEAM_HANDOFF_FRONTEND.md   # Frontend developer guide
├── TEAM_COORDINATION_GUIDE.md # Team coordination
├── DEMO_SUCCESS_REPORT.md     # Demo results
└── FRONTEND_STRUCTURE.md      # Frontend architecture
```

---

## 🎯 Your First Day

### Backend/AI Developer
1. ✅ Complete setup (above)
2. 📖 Read `TEAM_HANDOFF_BACKEND.md` (30 minutes)
3. 🔍 Explore backend code:
   - `backend/src/services/eligibility_service.py` (your main focus)
   - `backend/src/services/ai_service.py` (Ollama integration)
   - `backend/test_backend_features.py` (test script)
4. 🚀 Start Task 6.1: Implement match score calculation
5. 💬 Post in shared channel: "Backend setup complete, starting Task 6.1"

### Frontend Developer
1. ✅ Complete setup (above)
2. 📖 Read `TEAM_HANDOFF_FRONTEND.md` (30 minutes)
3. 🔍 Explore frontend code:
   - `frontend/app/profile/page.tsx` (where skill graph will go)
   - `frontend/components/ResumeUpload.tsx` (example component)
   - `frontend/lib/api.ts` (API client)
4. 🚀 Start Task 12.3: Build skill graph component
5. 💬 Post in shared channel: "Frontend setup complete, starting Task 12.3"

---

## 🔌 API Testing

### Using Swagger UI
1. Go to `http://127.0.0.1:8000/docs`
2. Click "Authorize" button
3. Sign up first: `POST /auth/signup`
4. Sign in: `POST /auth/signin` → copy `accessToken`
5. Click "Authorize" → paste token → "Authorize"
6. Now you can test all protected endpoints

### Using Postman
1. Import API collection (if available)
2. Set base URL: `http://127.0.0.1:8000`
3. Add Authorization header: `Bearer <token>`
4. Test endpoints

### Using curl
```bash
# Sign up
curl -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"Test123!"}'

# Sign in
curl -X POST http://127.0.0.1:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Get profile (replace TOKEN)
curl -X GET http://127.0.0.1:8000/profile \
  -H "Authorization: Bearer TOKEN"
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version (need 3.11+)
python --version

# Reinstall dependencies
pip install -r requirements.txt

# Check if port 8000 is in use
# Windows:
netstat -ano | findstr :8000
# Mac/Linux:
lsof -ti:8000
```

### Ollama not working
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve

# Pull model again
ollama pull llama3.1:8b
```

### Frontend won't start
```bash
# Check Node version (need 18+)
node --version

# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run dev
```

### CORS errors
- Ensure backend is running
- Check `.env.local` has correct API URL
- Check backend `main.py` has CORS enabled for `http://localhost:3000`

---

## 📚 Key Documents to Read

### Must Read (30 minutes)
1. **Your handoff document**:
   - Backend: `TEAM_HANDOFF_BACKEND.md`
   - Frontend: `TEAM_HANDOFF_FRONTEND.md`
2. **Team coordination**: `TEAM_COORDINATION_GUIDE.md`

### Reference (as needed)
- `DEMO_SUCCESS_REPORT.md` - What's working
- `FRONTEND_STRUCTURE.md` - Frontend architecture
- `.kiro/specs/eligify-platform/tasks.md` - All tasks
- `.kiro/specs/eligify-platform/design.md` - System design

---

## 💬 Communication

### Daily Updates
Post in shared channel:
```
✅ Completed: [Task description]
🚧 In Progress: [Task description]
⏳ Next: [Task description]
❓ Questions: [Any blockers or questions]
```

### When You're Blocked
1. Post in shared channel with details
2. Include error messages and screenshots
3. Tag the other developer if it's related to their work
4. Schedule a quick call if needed

### When You Complete a Task
1. Mark task as complete in `tasks.md`
2. Commit and push your code
3. Post in shared channel
4. Create PR if ready for review

---

## ✅ Checklist

Before you start coding:
- [ ] Backend is running at `http://127.0.0.1:8000`
- [ ] Frontend is running at `http://localhost:3000`
- [ ] Ollama is installed and model is pulled
- [ ] You can sign up and sign in on the frontend
- [ ] You've read your handoff document
- [ ] You've read the coordination guide
- [ ] You know your first task
- [ ] You've posted in shared channel that you're ready

---

## 🎉 You're Ready!

You now have:
- ✅ Working development environment
- ✅ Understanding of the project
- ✅ Your first task identified
- ✅ Resources to reference

**Next steps**:
1. Read your handoff document thoroughly
2. Explore the codebase
3. Start your first task
4. Post updates in shared channel
5. Ask questions when blocked

**Welcome to the team! Let's build something amazing! 🚀**

---

## 📞 Need Help?

- **Backend questions**: Check `TEAM_HANDOFF_BACKEND.md`
- **Frontend questions**: Check `TEAM_HANDOFF_FRONTEND.md`
- **API questions**: Check `TEAM_COORDINATION_GUIDE.md`
- **Stuck**: Post in shared channel with `@urgent` tag

---

**Last Updated**: January 2025  
**Setup Time**: ~15 minutes  
**First Task Time**: ~2-4 hours
