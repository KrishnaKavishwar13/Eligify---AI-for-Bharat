# Frontend Setup Guide

## Prerequisites

### System Requirements
- **Node.js**: Version 18.0 or higher
- **npm**: Version 8.0 or higher (comes with Node.js)
- **Git**: For version control
- **Code Editor**: VS Code recommended with extensions:
  - TypeScript and JavaScript Language Features
  - Tailwind CSS IntelliSense
  - ES7+ React/Redux/React-Native snippets
  - Prettier - Code formatter

### Backend Requirements
- **FastAPI Backend**: Running on http://localhost:8000
- **Database**: PostgreSQL (for backend)
- **Python**: Version 3.8+ (for backend)

## Installation Steps

### 1. Clone and Navigate
```bash
# If you have the complete project
cd rudra/frontend

# Or if setting up from exported files
mkdir eligify-frontend
cd eligify-frontend
# Copy all frontend files here
```

### 2. Install Dependencies
```bash
# Install all dependencies
npm install

# Verify installation
npm list --depth=0
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.local.example .env.local

# Edit environment variables
nano .env.local  # or use your preferred editor
```

### 4. Environment Variables Setup

Edit `.env.local` with your configuration:

```bash
# Backend API Configuration
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Mock API Mode
# Set to 'true' for development without backend
# Set to 'false' when backend is ready
NEXT_PUBLIC_USE_MOCK_API=true

# File Upload Configuration
NEXT_PUBLIC_MAX_FILE_SIZE=10485760
NEXT_PUBLIC_ALLOWED_FILE_TYPES=.pdf,.docx,.txt

# JWT Configuration (should match backend)
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-here
```

### 5. Development Server
```bash
# Start development server
npm run dev

# Server will start on http://localhost:3000
```

### 6. Verify Installation
Open your browser and navigate to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000 (should be running separately)

## Development Workflow

### 1. Mock API Development
When `NEXT_PUBLIC_USE_MOCK_API=true`:
- All API calls use mock data
- No backend required
- Perfect for frontend development
- Mock data located in `lib/mockData.ts`

### 2. Backend Integration
When `NEXT_PUBLIC_USE_MOCK_API=false`:
- All API calls go to FastAPI backend
- Requires backend server running
- Real authentication and data persistence

### 3. Code Quality Tools
```bash
# Run linting
npm run lint

# Format code
npm run format

# Type checking
npx tsc --noEmit
```

## Project Structure Understanding

### Key Directories
```
frontend/
├── app/                    # Next.js 14 App Router pages
├── components/             # Reusable React components
├── hooks/                  # Custom React hooks
├── lib/                    # Utilities and configurations
├── types/                  # TypeScript type definitions
├── styles/                 # Global styles
└── public/                 # Static assets
```

### Important Files
- **app/layout.tsx**: Root layout with providers
- **lib/api.ts**: API client configuration
- **lib/auth.ts**: Authentication state management
- **lib/constants.ts**: API routes and constants
- **components/Providers.tsx**: React Query and notification setup

## Backend Integration Steps

### 1. Prepare Backend
Ensure your FastAPI backend has these endpoints:

```python
# Authentication
POST /auth/signup
POST /auth/signin  
POST /auth/signout
POST /auth/refresh

# Profile
GET /profile
PUT /profile
POST /profile/upload-resume

# Skills
GET /skills
POST /skills
GET /skills/gaps

# Internships
GET /internships
GET /internships/classify

# Projects
GET /projects
POST /copilot/generate-project
PUT /projects/{id}/status
POST /projects/{id}/complete

# Validation
POST /validate/submit
GET /validate/{id}
GET /validate/history
```

### 2. Update Environment
```bash
# Switch to backend mode
NEXT_PUBLIC_USE_MOCK_API=false
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Test Integration
```bash
# Start both servers
# Terminal 1: Backend
cd ../backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend  
cd frontend
npm run dev
```

### 4. Verify Endpoints
Test each major feature:
- [ ] User registration/login
- [ ] Profile management
- [ ] Resume upload
- [ ] Skill management
- [ ] Internship browsing
- [ ] Project generation

## Common Issues and Solutions

### 1. Port Conflicts
```bash
# If port 3000 is busy
npm run dev -- -p 3001

# Or set in package.json
"dev": "next dev -p 3001"
```

### 2. CORS Issues
Ensure backend allows frontend origin:
```python
# In FastAPI backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. API Connection Issues
```bash
# Check backend is running
curl http://localhost:8000/health

# Check frontend can reach backend
curl http://localhost:3000/api/health
```

### 4. Environment Variables Not Loading
```bash
# Restart development server after .env changes
# Ctrl+C then npm run dev

# Verify variables are loaded
console.log(process.env.NEXT_PUBLIC_API_URL)
```

### 5. TypeScript Errors
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript
npx tsc --noEmit
```

### 6. Styling Issues
```bash
# Rebuild Tailwind
npm run build

# Check Tailwind config
npx tailwindcss -i ./styles/globals.css -o ./dist/output.css --watch
```

## Production Deployment

### 1. Build for Production
```bash
# Create production build
npm run build

# Test production build locally
npm start
```

### 2. Environment Variables for Production
```bash
# Production .env.local
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_USE_MOCK_API=false
NEXT_PUBLIC_JWT_SECRET=your-production-secret
```

### 3. Deployment Options

#### Vercel (Recommended)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
```

#### Docker
```dockerfile
# Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

#### Static Export (if no server-side features needed)
```bash
# Add to next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  }
}

# Build static files
npm run build
```

## Development Tips

### 1. Hot Reloading
- Changes to components auto-reload
- Changes to .env require server restart
- Changes to next.config.js require server restart

### 2. Debugging
```javascript
// Use React Developer Tools
// Add debug logs
console.log('API Response:', data);

// Use React Query DevTools (already configured)
// Available in development mode
```

### 3. Performance Monitoring
```bash
# Analyze bundle size
npm run build
npx @next/bundle-analyzer
```

### 4. Testing API Integration
```javascript
// Test API calls in browser console
fetch('/api/profile', {
  headers: {
    'Authorization': 'Bearer ' + localStorage.getItem('accessToken')
  }
})
.then(r => r.json())
.then(console.log)
```

## Next Steps

1. **Start with Mock API**: Develop and test frontend features
2. **Integrate Backend**: Switch to real API when backend is ready
3. **Add Features**: Implement additional functionality as needed
4. **Optimize**: Performance and SEO optimization
5. **Deploy**: Production deployment with proper environment setup

## Support

For issues or questions:
1. Check console for error messages
2. Verify environment variables
3. Test API endpoints directly
4. Check network tab in browser DevTools
5. Review this setup guide

The frontend is designed to work seamlessly with the FastAPI backend once properly configured.