# Eligify - AI-Powered Employability Platform

> Empowering Indian students to bridge skill gaps and unlock internship opportunities

## 🌟 Features

- **Smart Internship Matching**: AI-powered eligibility classification
- **Skill Gap Analysis**: Identify missing skills for dream internships
- **SkillGenie**: AI learning assistant with personalized projects
- **Profile Management**: Track education, experience, and certifications
- **Project Verification**: Build skills through hands-on projects

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Ollama (for AI features)

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python quick_start.py
```

Backend runs on: http://localhost:8000

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on: http://localhost:3000

### Ollama Setup (Optional - for AI features)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Start server
ollama serve
```

## 🐳 Docker Deployment

### One-Command Deploy
```bash
# Linux/Mac
chmod +x deploy.sh
./deploy.sh

# Windows
deploy.bat
```

### Manual Docker
```bash
docker-compose up --build
```

Access at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## ☁️ Cloud Deployment

See [DEPLOY.md](./DEPLOY.md) for detailed deployment guides:
- Vercel + Railway (Recommended)
- AWS/DigitalOcean VPS
- Docker on any platform

## 📚 Documentation

- [Deployment Guide](./DEPLOY.md) - Cloud deployment instructions
- [Quick Deployment Guide](./QUICK_DEPLOYMENT_GUIDE.md) - Platform comparisons
- [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md) - Testing checklist
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Component Architecture](./COMPONENT_ARCHITECTURE.md) - System design

## 🧪 Test Credentials

**Email**: rudradewatwal@gmail.com  
**Password**: Password@123

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **AI**: Ollama (Llama 3.1 8B)
- **Database**: JSON persistence (MVP) → PostgreSQL (Production)
- **Auth**: JWT tokens

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **State**: Zustand
- **API**: React Query

## 📁 Project Structure

```
eligify-ai-for-bharat/
├── backend/
│   ├── src/
│   │   ├── handlers/      # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── models/        # Data models
│   │   ├── utils/         # Utilities
│   │   └── main.py        # FastAPI app
│   ├── data/
│   │   ├── internships.json
│   │   └── persistence/   # User data
│   └── requirements.txt
├── frontend/
│   ├── app/               # Next.js pages
│   ├── components/        # React components
│   ├── lib/               # Utilities
│   ├── hooks/             # Custom hooks
│   └── types/             # TypeScript types
└── docker-compose.yml
```

## 🎯 Roadmap

### MVP (Current)
- [x] User authentication
- [x] Profile management
- [x] Internship matching
- [x] Skills tracking
- [x] Basic AI integration

### v1.0 (Next)
- [ ] Resume upload & parsing
- [ ] Project submission & verification
- [ ] Skill assessment tests
- [ ] Email notifications
- [ ] Admin dashboard

### v2.0 (Future)
- [ ] Career path recommendations
- [ ] Mentor matching
- [ ] Company partnerships
- [ ] Mobile app
- [ ] Analytics dashboard

## 🤝 Contributing

This is an MVP for AI for Bharat initiative. Contributions welcome!

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built for Indian students to bridge the employability gap through AI-powered learning.

---

**Ready to deploy?** Check [DEPLOY.md](./DEPLOY.md) for step-by-step instructions!
