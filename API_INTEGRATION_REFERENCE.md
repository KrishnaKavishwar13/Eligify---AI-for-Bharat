# API Integration Reference

## Overview

This document provides a complete reference for all API endpoints used by the Eligify frontend, including request/response formats, authentication requirements, and integration patterns.

## Base Configuration

### API Client Setup
```typescript
// lib/api.ts
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL, // http://localhost:8000
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Authentication Flow
- **JWT Tokens**: Access token (short-lived) + Refresh token (long-lived)
- **Storage**: localStorage with Zustand persistence
- **Auto-refresh**: Automatic token refresh on 401 responses
- **Interceptors**: Request/response interceptors handle auth automatically

## Authentication Endpoints

### 1. User Registration
```http
POST /auth/signup
Content-Type: application/json
```

**Request Body:**
```typescript
interface SignUpRequest {
  email: string;
  password: string;
  name: string;
  role?: 'student' | 'admin';
  qualification?: string;
  location?: string;
  linkedinUrl?: string;
  githubUrl?: string;
  resume?: File; // multipart/form-data if included
}
```

**Response:**
```typescript
interface AuthResponse {
  success: boolean;
  userId?: string;
  message?: string;
  error?: string;
}
```

**Frontend Usage:**
```typescript
// hooks/useAuth.ts
const signUpMutation = useMutation({
  mutationFn: async (data: SignUpRequest) => {
    const response = await api.post<AuthResponse>('/auth/signup', data);
    return response.data;
  }
});
```

### 2. User Login
```http
POST /auth/signin
Content-Type: application/json
```

**Request Body:**
```typescript
interface SignInRequest {
  email: string;
  password: string;
}
```

**Response:**
```typescript
interface AuthResponse {
  success: boolean;
  accessToken?: string;
  refreshToken?: string;
  idToken?: string;
  userId?: string;
  user?: {
    userId: string;
    email: string;
    name: string;
    role: string;
  };
  message?: string;
  error?: string;
}
```

### 3. Token Refresh
```http
POST /auth/refresh
Content-Type: application/json
```

**Request Body:**
```typescript
interface RefreshTokenRequest {
  refreshToken: string;
}
```

**Response:**
```typescript
interface AuthResponse {
  success: boolean;
  accessToken?: string;
  refreshToken?: string; // Optional new refresh token
}
```

### 4. User Logout
```http
POST /auth/signout
Authorization: Bearer {accessToken}
```

**Response:**
```typescript
interface AuthResponse {
  success: boolean;
  message?: string;
}
```

## Profile Management

### 1. Get User Profile
```http
GET /profile
Authorization: Bearer {accessToken}
```

**Response:**
```typescript
interface ApiResponse<StudentProfile> {
  success: boolean;
  data?: StudentProfile;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
}

interface StudentProfile {
  userId: string;
  personalInfo: PersonalInfo;
  education: Education[];
  experience: Experience[];
  projects: Project[];
  certifications: Certification[];
  resumeS3Uri?: string;
  resumeUploadedAt?: string;
  role: UserRole;
  onboardingComplete: boolean;
  createdAt: string;
  updatedAt: string;
  lastLoginAt?: string;
}
```

### 2. Update Profile
```http
PUT /profile
Authorization: Bearer {accessToken}
Content-Type: application/json
```

**Request Body:**
```typescript
// Partial update - any subset of StudentProfile fields
interface UpdateProfileRequest extends Partial<StudentProfile> {}
```

### 3. Upload Resume
```http
POST /profile/upload-resume
Authorization: Bearer {accessToken}
Content-Type: multipart/form-data
```

**Request Body:**
```typescript
// FormData with file
const formData = new FormData();
formData.append('file', file);
```

**Response:**
```typescript
interface UploadResumeResponse {
  success: boolean;
  s3Uri?: string;
  parsedProfile?: {
    name: string;
    email: string;
    phone?: string;
    education: unknown[];
    experience: unknown[];
    skills: string[];
    projects: unknown[];
    certifications: unknown[];
  };
  message?: string;
  error?: string;
}
```

## Skills Management

### 1. Get Skill Graph
```http
GET /skills
Authorization: Bearer {accessToken}
```

**Response:**
```typescript
interface ApiResponse<SkillGraph> {
  success: boolean;
  data?: SkillGraph;
}

interface SkillGraph {
  userId: string;
  skills: SkillNode[];
  totalSkills: number;
  verifiedSkills: number;
  lastUpdated: string;
}

interface SkillNode {
  skillId: string;
  name: string;
  category: SkillCategory;
  status: SkillStatus;
  proficiencyLevel: number;
  verifiedAt?: string;
  validationId?: string;
  source: SkillSource;
  relatedSkills: string[];
}
```

### 2. Add Skill
```http
POST /skills
Authorization: Bearer {accessToken}
Content-Type: application/json
```

**Request Body:**
```typescript
interface AddSkillRequest {
  skillName: string;
  category: string;
  proficiencyLevel?: number;
}
```

### 3. Get Skill Gaps
```http
GET /skills/gaps
Authorization: Bearer {accessToken}
```

**Response:**
```typescript
interface ApiResponse<SkillGap[]> {
  success: boolean;
  data?: SkillGap[];
}

interface SkillGap {
  skillName: string;
  required: boolean;
  currentProficiency: number;
  targetProficiency: number;
  priority: 'high' | 'medium' | 'low';
}
```

## Internship Management

### 1. Get All Internships
```http
GET /internships
Authorization: Bearer {accessToken}
```

**Query Parameters:**
- `page?: number` - Page number (default: 1)
- `limit?: number` - Items per page (default: 20)
- `type?: string` - Filter by type (remote, onsite, hybrid)
- `location?: string` - Filter by location

**Response:**
```typescript
interface ApiResponse<Internship[]> {
  success: boolean;
  data?: Internship[];
}

interface Internship {
  internshipId: string;
  title: string;
  company: string;
  description: string;
  requiredSkills: RequiredSkill[];
  preferredSkills: string[];
  duration: string;
  stipend?: {
    amount: number;
    currency: string;
    period: 'monthly' | 'total';
  };
  location: string;
  type: 'remote' | 'onsite' | 'hybrid';
  applicationDeadline: string;
  startDate: string;
  endDate?: string;
  applicationUrl?: string;
  status: 'active' | 'closed' | 'draft';
  createdAt: string;
  updatedAt: string;
}
```

### 2. Get Classified Internships
```http
GET /internships/classify
Authorization: Bearer {accessToken}
```

**Response:**
```typescript
interface ApiResponse<ClassifiedInternships> {
  success: boolean;
  data?: ClassifiedInternships;
}

interface ClassifiedInternships {
  eligible: InternshipMatch[];
  almostEligible: InternshipMatch[];
  notEligible: InternshipMatch[];
}

interface InternshipMatch {
  internship: Internship;
  matchScore: number;
  missingSkills: SkillGap[];
  matchedSkills: string[];
  recommendation?: string;
}
```

## Project Management

### 1. Get Projects
```http
GET /projects
Authorization: Bearer {accessToken}
```

**Query Parameters:**
- `status?: string` - Filter by status (suggested, accepted, in_progress, submitted, completed)

**Response:**
```typescript
interface ApiResponse<GeneratedProject[]> {
  success: boolean;
  data?: GeneratedProject[];
}

interface GeneratedProject {
  projectId: string;
  userId: string;
  title: string;
  description: string;
  objectives: string[];
  targetSkills: string[];
  techStack: TechStackItem[];
  milestones: Milestone[];
  validationCriteria: ValidationCriterion[];
  resources: Resource[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimatedDuration: string;
  status: ProjectStatus;
  submissionId?: string;
  githubRepoUrl?: string;
  submittedAt?: string;
  createdAt: string;
  updatedAt: string;
}
```

### 2. Generate Project
```http
POST /copilot/generate-project
Authorization: Bearer {accessToken}
Content-Type: application/json
```

**Request Body:**
```typescript
interface GenerateProjectRequest {
  targetSkills: string[];
  studentLevel: 'beginner' | 'intermediate' | 'advanced';
  timeCommitment?: string;
  preferences?: {
    domain?: string;
    techStack?: string[];
    projectType?: string;
  };
}
```

### 3. Update Project Status
```http
PUT /projects/{projectId}/status
Authorization: Bearer {accessToken}
Content-Type: application/json
```

**Request Body:**
```typescript
interface UpdateProjectStatusRequest {
  status: 'accepted' | 'in_progress' | 'submitted' | 'completed';
}
```

### 4. Complete Project
```http
POST /projects/{projectId}/complete
Authorization: Bearer {accessToken}
```

**Response:**
```typescript
interface ProjectCompletionResponse {
  verifiedSkills: string[];
  newEligibleInternships: number;
  message?: string;
}
```

## Validation System

### 1. Submit Project for Validation
```http
POST /validate/submit
Authorization: Bearer {accessToken}
Content-Type: application/json
```

**Request Body:**
```typescript
interface SubmitProjectRequest {
  projectId: string;
  githubRepoUrl: string;
  description?: string;
  additionalNotes?: string;
}
```

**Response:**
```typescript
interface ValidationSubmissionResponse {
  validationId: string;
  status: 'pending' | 'processing';
  estimatedCompletionTime?: string;
}
```

### 2. Get Validation Status
```http
GET /validate/{validationId}
Authorization: Bearer {accessToken}
```

**Response:**
```typescript
interface ApiResponse<ValidationResult> {
  success: boolean;
  data?: ValidationResult;
}

interface ValidationResult {
  validationId: string;
  userId: string;
  projectId: string;
  status: ValidationStatus;
  overallScore: number;
  skillScores: SkillScore[];
  verifiedSkills: string[];
  feedback: ValidationFeedback;
  validatedAt: string;
}
```

### 3. Get Validation History
```http
GET /validate/history
Authorization: Bearer {accessToken}
```

**Query Parameters:**
- `page?: number`
- `limit?: number`

## Error Handling

### Standard Error Response
```typescript
interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}
```

### Common Error Codes
- `AUTH_REQUIRED` - Authentication required
- `AUTH_INVALID` - Invalid credentials
- `AUTH_EXPIRED` - Token expired
- `VALIDATION_ERROR` - Request validation failed
- `NOT_FOUND` - Resource not found
- `RATE_LIMITED` - Too many requests
- `SERVER_ERROR` - Internal server error

### Frontend Error Handling
```typescript
// lib/api.ts
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    return (
      error.response?.data?.error?.message ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred'
    );
  }
  
  if (error instanceof Error) {
    return error.message;
  }
  
  return 'An unexpected error occurred';
}
```

## Request/Response Interceptors

### Request Interceptor
```typescript
api.interceptors.request.use(
  (config) => {
    const { accessToken } = useAuthStore.getState();
    
    if (accessToken && config.headers) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);
```

### Response Interceptor
```typescript
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config;
    
    // Handle 401 - Token expired
    if (error.response?.status === 401 && !originalRequest?._retry) {
      originalRequest._retry = true;
      
      try {
        // Attempt token refresh
        const { refreshToken } = useAuthStore.getState();
        const response = await axios.post('/auth/refresh', { refreshToken });
        const { accessToken } = response.data;
        
        // Update token and retry request
        useAuthStore.getState().setAccessToken(accessToken);
        originalRequest.headers.Authorization = `Bearer ${accessToken}`;
        
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed - logout user
        useAuthStore.getState().clearAuth();
        window.location.href = '/auth/signin';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
```

## Mock API Implementation

For development without backend, the frontend includes mock implementations:

```typescript
// lib/mockData.ts - Sample mock data
export const mockProfile: StudentProfile = { /* ... */ };
export const mockProjects: GeneratedProject[] = [ /* ... */ ];
export const mockClassifiedInternships: ClassifiedInternships = { /* ... */ };

// hooks/useAuth.ts - Mock authentication
if (useMockApi) {
  await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate delay
  const result = mockAuthStore.signIn(data.email, data.password);
  if (!result.success) throw new Error(result.error);
  return { success: true, accessToken: 'mock-token', user: result.user };
}
```

## Integration Testing

### Test API Endpoints
```bash
# Test backend health
curl http://localhost:8000/health

# Test authentication
curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# Test protected endpoint
curl http://localhost:8000/profile \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Frontend API Testing
```javascript
// Browser console testing
const token = localStorage.getItem('accessToken');
fetch('/api/profile', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(console.log);
```

## Performance Considerations

### Caching Strategy
```typescript
// React Query configuration
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// Cache times by endpoint
export const CACHE_TIMES = {
  PROFILE: 5 * 60 * 1000,     // 5 minutes
  SKILLS: 5 * 60 * 1000,      // 5 minutes  
  INTERNSHIPS: 60 * 60 * 1000, // 1 hour
  PROJECTS: 5 * 60 * 1000,     // 5 minutes
};
```

### Request Optimization
- Debounced search queries
- Pagination for large datasets
- Selective field updates
- Optimistic updates for better UX

This reference provides everything needed to integrate the frontend with the FastAPI backend successfully.