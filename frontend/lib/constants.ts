// API Routes
export const API_ROUTES = {
  // Auth
  SIGNUP: '/auth/signup',
  SIGNIN: '/auth/signin',
  SIGNOUT: '/auth/signout',
  REFRESH: '/auth/refresh',

  // Profile
  PROFILE: '/profile',
  UPLOAD_RESUME: '/profile/upload-resume',

  // Skills
  SKILLS: '/skills',
  SKILL_GAPS: '/skills/gaps',

  // Internships
  INTERNSHIPS: '/internships',
  INTERNSHIPS_CLASSIFY: '/internships/classify',

  // Projects
  PROJECTS: '/projects',
  GENERATE_PROJECT: '/projects/generate',
  PROJECT_COMPLETE: (id: string) => `/projects/${id}/complete`,
  PROJECT_STATUS: (id: string) => `/projects/${id}/status`,

  // Validation
  VALIDATE_SUBMIT: '/validate/submit',
  VALIDATE_STATUS: (id: string) => `/validate/${id}`,
  VALIDATE_HISTORY: '/validate/history',
  
  // Chat
  CHAT_MESSAGE: '/api/v1/chat/message',
  
  // Intelligence
  PREDICT_CAREER_READINESS: (userId: string, targetRole: string) => 
    `/api/v1/intelligence/predict/career-readiness/${userId}/${encodeURIComponent(targetRole)}`,
} as const;

// App Routes
export const APP_ROUTES = {
  HOME: '/',
  SIGNUP: '/auth/signup',
  SIGNIN: '/auth/signin',
  DASHBOARD: '/dashboard',
  PROFILE: '/profile',
  INTERNSHIPS: '/internships',
  PROJECTS: '/projects',
  PROJECT_DETAIL: (id: string) => `/projects/${id}`,
  SKILLGENIE: '/skillgenie',
  SKILLGENIE_ASSESSMENT: '/skillgenie/assessment',
  SKILLGENIE_PROJECT: '/skillgenie/project',
  SKILLGENIE_RESULT: '/skillgenie/result',
  SKILLGENIE_SUBMIT: '/skillgenie/submit',
} as const;

// Skill Categories
export const SKILL_CATEGORIES = [
  { value: 'programming_language', label: 'Programming Language' },
  { value: 'framework', label: 'Framework' },
  { value: 'tool', label: 'Tool' },
  { value: 'soft_skill', label: 'Soft Skill' },
  { value: 'domain_knowledge', label: 'Domain Knowledge' },
] as const;

// Student Levels
export const STUDENT_LEVELS = [
  { value: 'beginner', label: 'Beginner' },
  { value: 'intermediate', label: 'Intermediate' },
  { value: 'advanced', label: 'Advanced' },
] as const;

// Internship Types
export const INTERNSHIP_TYPES = [
  { value: 'remote', label: 'Remote' },
  { value: 'onsite', label: 'On-site' },
  { value: 'hybrid', label: 'Hybrid' },
] as const;

// Project Status
export const PROJECT_STATUSES = [
  { value: 'suggested', label: 'Suggested' },
  { value: 'accepted', label: 'Accepted' },
  { value: 'in_progress', label: 'In Progress' },
  { value: 'submitted', label: 'Submitted' },
  { value: 'completed', label: 'Completed' },
] as const;

// File Upload
export const ALLOWED_RESUME_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain',
] as const;

export const MAX_RESUME_SIZE = 10 * 1024 * 1024; // 10MB

// Pagination
export const DEFAULT_PAGE_SIZE = 20;
export const INTERNSHIPS_PAGE_SIZE = 50;

// Cache Times (in milliseconds)
export const CACHE_TIMES = {
  PROFILE: 5 * 60 * 1000, // 5 minutes
  SKILLS: 5 * 60 * 1000, // 5 minutes
  INTERNSHIPS: 60 * 60 * 1000, // 1 hour
  PROJECTS: 5 * 60 * 1000, // 5 minutes
} as const;

// Toast Auto-dismiss Time
export const TOAST_DURATION = 5000; // 5 seconds

// Validation
export const PASSWORD_MIN_LENGTH = 8;
export const PASSWORD_REGEX =
  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/;
