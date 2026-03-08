# Integration Checklist for Backend Teammate

## Pre-Integration Setup

### ✅ Environment Preparation
- [ ] **Node.js 18+** installed on development machine
- [ ] **npm** or **yarn** package manager available
- [ ] **Git** for version control
- [ ] **VS Code** or preferred editor with TypeScript support
- [ ] **FastAPI backend** running on `http://localhost:8000`
- [ ] **PostgreSQL database** configured and running

### ✅ Frontend Setup
```bash
# 1. Navigate to frontend directory
cd rudra/frontend

# 2. Install dependencies
npm install

# 3. Copy environment file
cp .env.local.example .env.local

# 4. Configure environment variables
# Edit .env.local with your settings
```

### ✅ Environment Configuration
Edit `.env.local`:
```bash
# Start with mock API for testing
NEXT_PUBLIC_USE_MOCK_API=true
NEXT_PUBLIC_API_URL=http://localhost:8000

# File upload settings
NEXT_PUBLIC_MAX_FILE_SIZE=10485760
NEXT_PUBLIC_ALLOWED_FILE_TYPES=.pdf,.docx,.txt

# JWT secret (should match backend)
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-here
```

## Phase 1: Mock API Testing

### ✅ Frontend Functionality Verification
```bash
# Start frontend in mock mode
npm run dev
# Frontend should be available at http://localhost:3000
```

**Test these features with mock data:**
- [ ] **Landing Page** loads correctly
- [ ] **User Registration** form works
- [ ] **User Login** form works
- [ ] **Dashboard** displays mock data
- [ ] **Profile Management** shows mock profile
- [ ] **Resume Upload** UI functions (mock response)
- [ ] **Skill Graph** displays mock skills
- [ ] **Internship Listings** show mock internships
- [ ] **Project Generation** creates mock projects
- [ ] **SkillGenie** assessment flow works
- [ ] **Notifications** system functions
- [ ] **Responsive Design** works on mobile/desktop

### ✅ Code Quality Checks
```bash
# Run linting
npm run lint

# Format code
npm run format

# TypeScript compilation
npx tsc --noEmit

# Build test
npm run build
```

## Phase 2: Backend API Implementation

### ✅ Required Backend Endpoints

#### Authentication Endpoints
- [ ] `POST /auth/signup` - User registration
  ```json
  Request: { "email": "string", "password": "string", "name": "string" }
  Response: { "success": boolean, "userId": "string", "message": "string" }
  ```

- [ ] `POST /auth/signin` - User login
  ```json
  Request: { "email": "string", "password": "string" }
  Response: { 
    "success": boolean, 
    "accessToken": "string", 
    "refreshToken": "string",
    "user": { "userId": "string", "email": "string", "name": "string", "role": "string" }
  }
  ```

- [ ] `POST /auth/refresh` - Token refresh
  ```json
  Request: { "refreshToken": "string" }
  Response: { "success": boolean, "accessToken": "string" }
  ```

- [ ] `POST /auth/signout` - User logout
  ```json
  Headers: { "Authorization": "Bearer {token}" }
  Response: { "success": boolean, "message": "string" }
  ```

#### Profile Management
- [ ] `GET /profile` - Get user profile
  ```json
  Headers: { "Authorization": "Bearer {token}" }
  Response: { "success": boolean, "data": StudentProfile }
  ```

- [ ] `PUT /profile` - Update profile
  ```json
  Headers: { "Authorization": "Bearer {token}" }
  Request: Partial<StudentProfile>
  Response: { "success": boolean, "data": StudentProfile }
  ```

- [ ] `POST /profile/upload-resume` - Upload resume
  ```json
  Headers: { "Authorization": "Bearer {token}", "Content-Type": "multipart/form-data" }
  Request: FormData with file
  Response: { 
    "success": boolean, 
    "s3Uri": "string", 
    "parsedProfile": ParsedProfile 
  }
  ```

#### Skills Management
- [ ] `GET /skills` - Get skill graph
- [ ] `POST /skills` - Add skill
- [ ] `GET /skills/gaps` - Get skill gaps

#### Internships
- [ ] `GET /internships` - Get all internships
- [ ] `GET /internships/classify` - Get classified internships

#### Projects
- [ ] `GET /projects` - Get user projects
- [ ] `POST /copilot/generate-project` - Generate project
- [ ] `PUT /projects/{id}/status` - Update project status
- [ ] `POST /projects/{id}/complete` - Complete project

#### Validation
- [ ] `POST /validate/submit` - Submit for validation
- [ ] `GET /validate/{id}` - Get validation status
- [ ] `GET /validate/history` - Get validation history

### ✅ CORS Configuration
Ensure backend allows frontend origin:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ✅ JWT Configuration
- [ ] JWT secret matches frontend configuration
- [ ] Access token expiration (recommended: 15 minutes)
- [ ] Refresh token expiration (recommended: 7 days)
- [ ] Token refresh endpoint implemented

## Phase 3: Backend Integration

### ✅ Switch to Real API
Update `.env.local`:
```bash
# Switch to real backend
NEXT_PUBLIC_USE_MOCK_API=false
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### ✅ Test Each Endpoint

#### Authentication Flow
```bash
# Test registration
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Test login
curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Save the token from response for next tests
TOKEN="your-access-token-here"
```

#### Profile Management
```bash
# Test profile fetch
curl -X GET http://localhost:8000/profile \
  -H "Authorization: Bearer $TOKEN"

# Test profile update
curl -X PUT http://localhost:8000/profile \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"personalInfo":{"name":"Updated Name"}}'
```

#### File Upload
```bash
# Test resume upload
curl -X POST http://localhost:8000/profile/upload-resume \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sample-resume.pdf"
```

### ✅ Frontend Integration Testing

**Start both servers:**
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Test complete user flows:**
- [ ] **Registration → Login → Dashboard** flow
- [ ] **Profile Update** with real data persistence
- [ ] **Resume Upload** with file processing
- [ ] **Skill Management** with database storage
- [ ] **Internship Browsing** with real data
- [ ] **Project Generation** with AI integration
- [ ] **Token Refresh** on expiration
- [ ] **Logout** clears session

## Phase 4: Error Handling & Edge Cases

### ✅ Error Scenarios
- [ ] **Invalid credentials** - proper error messages
- [ ] **Expired tokens** - automatic refresh
- [ ] **Network errors** - user-friendly messages
- [ ] **File upload errors** - size/type validation
- [ ] **Server errors** - graceful degradation
- [ ] **Rate limiting** - proper handling

### ✅ Validation Testing
- [ ] **Email format** validation
- [ ] **Password strength** requirements
- [ ] **File type/size** restrictions
- [ ] **Required fields** validation
- [ ] **SQL injection** prevention
- [ ] **XSS protection** measures

## Phase 5: Performance & Security

### ✅ Performance Checks
- [ ] **API response times** < 2 seconds
- [ ] **File upload progress** tracking
- [ ] **Loading states** for all operations
- [ ] **Caching** for frequently accessed data
- [ ] **Pagination** for large datasets

### ✅ Security Verification
- [ ] **HTTPS** in production
- [ ] **JWT tokens** properly secured
- [ ] **File upload** security (virus scanning)
- [ ] **Input sanitization** on backend
- [ ] **Rate limiting** implemented
- [ ] **CORS** properly configured

## Phase 6: Production Readiness

### ✅ Environment Setup
```bash
# Production environment variables
NEXT_PUBLIC_USE_MOCK_API=false
NEXT_PUBLIC_API_URL=https://your-production-api.com
NEXT_PUBLIC_JWT_SECRET=your-production-secret
```

### ✅ Build & Deploy
```bash
# Test production build
npm run build
npm start

# Deploy to your platform (Vercel, Netlify, etc.)
```

### ✅ Final Verification
- [ ] **All features** work in production
- [ ] **SSL certificates** properly configured
- [ ] **Database connections** stable
- [ ] **File uploads** work with cloud storage
- [ ] **Error monitoring** set up
- [ ] **Performance monitoring** configured

## Common Issues & Solutions

### Issue: CORS Errors
**Solution:**
```python
# Backend: Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: Token Refresh Not Working
**Solution:**
- Verify refresh endpoint returns new access token
- Check token expiration times
- Ensure refresh token is stored securely

### Issue: File Upload Fails
**Solution:**
- Check file size limits on both frontend and backend
- Verify multipart/form-data handling
- Test with different file types

### Issue: API Calls Failing
**Solution:**
```bash
# Check if backend is running
curl http://localhost:8000/health

# Verify API endpoint exists
curl -I http://localhost:8000/profile

# Check request format matches backend expectations
```

### Issue: Environment Variables Not Loading
**Solution:**
- Restart development server after .env changes
- Verify variable names start with `NEXT_PUBLIC_`
- Check for typos in variable names

## Testing Checklist

### ✅ Manual Testing
- [ ] Complete user registration flow
- [ ] Login with valid/invalid credentials
- [ ] Profile management (view/edit)
- [ ] Resume upload and parsing
- [ ] Skill graph visualization
- [ ] Internship browsing and filtering
- [ ] Project generation and management
- [ ] SkillGenie assessment flow
- [ ] Responsive design on mobile
- [ ] Cross-browser compatibility

### ✅ Automated Testing
```bash
# Run frontend tests (if implemented)
npm test

# API endpoint testing
npm run test:api

# E2E testing (if implemented)
npm run test:e2e
```

## Success Criteria

### ✅ Integration Complete When:
- [ ] All API endpoints respond correctly
- [ ] Frontend displays real data from backend
- [ ] User authentication works end-to-end
- [ ] File uploads process successfully
- [ ] Error handling works gracefully
- [ ] Performance meets requirements
- [ ] Security measures are in place
- [ ] Production deployment successful

## Next Steps After Integration

1. **User Testing**: Get feedback from real users
2. **Performance Optimization**: Monitor and optimize slow endpoints
3. **Feature Enhancement**: Add new features based on user feedback
4. **Monitoring Setup**: Implement logging and error tracking
5. **Documentation**: Update API documentation
6. **Backup Strategy**: Implement data backup procedures

## Support & Resources

- **Frontend Documentation**: See `FRONTEND_SETUP_GUIDE.md`
- **API Reference**: See `API_INTEGRATION_REFERENCE.md`
- **Component Guide**: See `COMPONENT_ARCHITECTURE.md`
- **Troubleshooting**: Check browser console and network tab
- **Backend Logs**: Monitor FastAPI logs for errors

This checklist ensures a smooth integration process between the frontend and backend systems.