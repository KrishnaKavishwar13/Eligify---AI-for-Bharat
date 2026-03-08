# Implementation Plan: Eligify Platform MVP

## Overview

This implementation plan breaks down the Eligify platform into discrete coding tasks optimized for a 48-hour build cycle. The plan follows a bottom-up approach: infrastructure setup → backend core → frontend core → integration → testing. Each task is designed to be incremental, with checkpoints to ensure stability before moving forward.

The MVP focuses on: serverless AWS architecture (Lambda + API Gateway + DynamoDB + S3 + Cognito + Bedrock), deterministic eligibility engine, AI-powered skill extraction and project generation, and simulated skill verification (no GitHub integration).

**Technology Stack:**
- Backend: Node.js + TypeScript + Express (on Lambda)
- Frontend: Next.js 14 + React + TypeScript + Tailwind CSS
- Database: DynamoDB
- Storage: S3
- Auth: Amazon Cognito
- AI: AWS Bedrock (Claude 3 Sonnet) with OpenAI fallback
- Deployment: AWS SAM / Serverless Framework

**Time Estimate:** 48 hours total (6 hours per day × 8 days or 12 hours per day × 4 days)

## Tasks

- [x] 1. Project setup and infrastructure foundation (6 hours)
  - [x] 1.1 Initialize backend project structure
    - Create `backend/` directory with TypeScript + Node.js setup
    - Install dependencies: `express`, `aws-sdk`, `@aws-sdk/client-dynamodb`, `@aws-sdk/lib-dynamodb`, `@aws-sdk/client-s3`, `@aws-sdk/client-bedrock-runtime`, `jsonwebtoken`, `bcryptjs`, `zod`, `cors`, `dotenv`
    - Configure `tsconfig.json` with strict mode and ES2020 target
    - Create folder structure: `src/handlers/`, `src/services/`, `src/models/`, `src/utils/`, `src/middleware/`
    - _Requirements: NFR-3, NFR-5_
  
  - [x] 1.2 Initialize frontend project structure
    - Create Next.js 14 app with TypeScript: `npx create-next-app@latest frontend --typescript --tailwind --app`
    - Install dependencies: `axios`, `@tanstack/react-query`, `zustand`, `react-hook-form`, `zod`, `lucide-react`
    - Create folder structure: `app/`, `components/`, `lib/`, `hooks/`, `types/`, `services/`
    - Configure `next.config.js` for API proxy and environment variables
    - _Requirements: NFR-3, NFR-7, NFR-8_
  
  - [x] 1.3 Set up AWS infrastructure with SAM/Serverless
    - Create `template.yaml` (AWS SAM) or `serverless.yml` (Serverless Framework)
    - Define DynamoDB tables: `Students`, `Skills`, `Internships`, `Projects`, `Validations`
    - Define S3 bucket for resume storage with encryption enabled
    - Define Cognito User Pool with email/password auth
    - Define API Gateway with CORS configuration
    - Define Lambda functions for each service endpoint
    - Configure IAM roles with least privilege access
    - _Requirements: 1.1, 13.1, 14.2, 17.2, 17.3, NFR-4_


- [x] 2. Core data models and utilities (4 hours)
  - [x] 2.1 Create TypeScript interfaces and types
    - Define all interfaces from design document: `StudentProfile`, `SkillGraph`, `SkillNode`, `Internship`, `GeneratedProject`, `ValidationResult`
    - Define enums: `UserRole`, `SkillStatus`, `SkillCategory`, `SkillSource`
    - Define API request/response types for all endpoints
    - Create `types/index.ts` as central export
    - _Requirements: 2.4, 4.1, 5.2, 8.2, 9.1_
  
  - [x] 2.2 Implement DynamoDB utility functions
    - Create `utils/dynamodb.ts` with helper functions for CRUD operations
    - Implement `getItem`, `putItem`, `updateItem`, `deleteItem`, `query`, `scan` wrappers
    - Add error handling and retry logic with exponential backoff
    - Implement optimistic locking for concurrent updates
    - _Requirements: 13.1, 13.4, 15.5_
  
  - [x] 2.3 Implement S3 utility functions
    - Create `utils/s3.ts` with upload, download, and presigned URL generation
    - Implement `uploadFile` with unique key generation (userId + timestamp)
    - Implement `generatePresignedUrl` with 1-hour expiration
    - Add file type validation (PDF, DOCX, TXT) and size limit (10MB)
    - _Requirements: 2.1, 2.2, 14.1, 14.4, 14.5, 14.6_
  
  - [x] 2.4 Implement JWT authentication utilities
    - Create `utils/auth.ts` with token generation and validation functions
    - Implement `generateTokens` (access token 1h, refresh token 30d)
    - Implement `verifyToken` with expiration checking
    - Implement `extractUserFromToken` to get userId and role
    - _Requirements: 1.3, 1.5, 12.3, 17.4_
  
  - [x] 2.5 Create validation schemas with Zod
    - Create `utils/validation.ts` with Zod schemas for all API inputs
    - Define schemas: `signupSchema`, `signinSchema`, `profileSchema`, `skillSchema`, `projectRequestSchema`
    - Add custom validators for email, password strength, GitHub URLs
    - _Requirements: 2.4, 12.1, 15.1, 17.5_

- [x] 3. Authentication service (4 hours)
  - [x] 3.1 Implement Cognito integration
    - Create `services/auth.service.ts` with Cognito SDK integration
    - Implement `signUp(email, password, name)` → create user in Cognito User Pool
    - Implement `signIn(email, password)` → authenticate and return Cognito tokens
    - Implement `refreshToken(refreshToken)` → get new access token
    - Implement `signOut(userId)` → invalidate session
    - Handle Cognito errors and map to user-friendly messages
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_
  
  - [x] 3.2 Create authentication API handlers
    - Create `handlers/auth.handler.ts` with Lambda handler functions
    - Implement `POST /auth/signup` endpoint with input validation
    - Implement `POST /auth/signin` endpoint with error handling
    - Implement `POST /auth/refresh` endpoint for token refresh
    - Implement `POST /auth/signout` endpoint
    - Return standardized response format: `{ success, data, error }`
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 15.1, 15.2_
  
  - [x] 3.3 Create authentication middleware
    - Create `middleware/auth.middleware.ts` for JWT validation
    - Implement `authenticateRequest` middleware to validate Authorization header
    - Extract userId and role from token and attach to request object
    - Return 401 for missing/invalid tokens, 403 for unauthorized access
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_


- [x] 4. Profile service with AI skill extraction (6 hours)
  - [x] 4.1 Implement resume upload handler
    - Create `handlers/profile.handler.ts` with `POST /profile/upload-resume` endpoint
    - Parse multipart form data to extract file
    - Validate file type (PDF, DOCX, TXT) and size (<10MB)
    - Generate unique S3 key: `resumes/${userId}/${timestamp}-${filename}`
    - Upload to S3 with server-side encryption
    - Store S3 URI in student profile
    - _Requirements: 2.1, 2.2, 2.3, 14.1, 14.2, 14.3, 14.4_
  
  - [x] 4.2 Implement AI skill extraction with Ollama
    - Create `services/ai_service.py` with Ollama integration
    - Implement `extract_skills_from_resume(resumeText)` using Llama 3.1 8B
    - Create prompt: "Extract technical skills, soft skills, and domain knowledge from this resume. Return as JSON array with skill names and categories."
    - Parse Ollama response into structured skill list
    - Normalize skill names (lowercase, trim whitespace)
    - Implement retry logic (3 attempts with exponential backoff)
    - _Requirements: 3.1, 3.3, 15.5, 15.6_
    - **Note**: Replaced Bedrock with Ollama for local development
  
  - [x] 4.3 Ollama integration (replaced OpenAI fallback)
    - Installed Ollama with Llama 3.1 8B model
    - Implemented `extract_skills_from_resume` with Ollama
    - Successfully tested: extracts 17 skills with proficiency levels
    - Processing time: 10-20 seconds
    - _Requirements: 3.2, 3.4, 15.7_
    - **Note**: Using Ollama as primary AI provider instead of Bedrock/OpenAI
  
  - [x] 4.4 Implement profile CRUD operations
    - Create `services/profile.service.ts` with DynamoDB operations
    - Implement `createProfile(userId, profileData)` → store in Students table
    - Implement `getProfile(userId)` → fetch from Students table
    - Implement `updateProfile(userId, updates)` → partial update with timestamp
    - Implement `deleteProfile(userId)` → remove from Students table
    - Validate required fields before saving
    - _Requirements: 2.4, 2.5, 2.6, 13.1, 13.2_
    - **Status**: COMPLETE - All CRUD operations working with mock store
  
  - [x] 4.5 Create profile API endpoints
    - Implement `GET /profile` → return current user's profile
    - Implement `PUT /profile` → update profile with validation
    - Implement `DELETE /profile` → delete profile and associated data
    - Add authentication middleware to all endpoints
    - Ensure users can only access their own profile
    - _Requirements: 2.4, 2.5, 2.6, 12.4, 15.1_
    - **Status**: COMPLETE - All endpoints implemented and tested

- [ ] 5. Skill graph service (4 hours)
  - [x] 5.1 Implement skill graph initialization
    - Create `services/skillGraph.service.ts` with DynamoDB operations
    - Implement `initializeSkillGraph(userId, initialSkills)` → create Skills table entry
    - Set all initial skills to status "claimed", proficiency 0
    - Initialize counters: totalSkills, verifiedSkills = 0
    - Set lastUpdated timestamp
    - _Requirements: 4.1, 4.2, 3.5_
    - **Status**: COMPLETE - Initialization working with default skills
  
  - [x] 5.2 Implement skill graph CRUD operations
    - Implement `getSkillGraph(userId)` → fetch from Skills table
    - Implement `addSkill(userId, skillName, category)` → add new skill node
    - Implement `updateSkillStatus(userId, skillId, status)` → change skill status
    - Implement `verifySkill(userId, skillId, validationId)` → mark as verified with proficiency 70
    - Ensure verified count consistency with actual verified skills
    - _Requirements: 4.3, 4.4, 4.5, 4.6, 13.6_
    - **Status**: COMPLETE - All operations working, tested with manual skill addition
  
  - [x] 5.3 Create skill graph API endpoints
    - Implement `GET /skills` → return user's skill graph
    - Implement `POST /skills` → manually add a skill
    - Implement `PUT /skills/:skillId` → update skill status
    - Add authentication middleware
    - _Requirements: 4.3, 4.4, 12.1_


- [ ] 6. Deterministic eligibility engine (6 hours)
  - [x] 6.1 Implement match score calculation algorithm
    - Create `services/eligibility.service.ts` with deterministic matching logic
    - Implement `calculateMatchScore(studentSkills, internship)` following design pseudocode
    - For each required skill: compare student proficiency vs required proficiency
    - Award full credit if proficiency gap <= 0
    - Award partial credit if gap between 1-20: `credit = weight * (1 - gap/100)`
    - Award zero credit if gap > 20 or skill missing
    - Calculate final score: `(achievedWeight / totalWeight) * 100`
    - Return match score (0-100), matched skills, missing skills
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8_
  
  - [x] 6.2 Implement internship classification logic
    - Implement `classifyInternships(userId)` following design pseudocode
    - Fetch student's skill graph from DynamoDB
    - Fetch all active internships from DynamoDB
    - For each internship: calculate match score and count missing mandatory skills
    - Classify as "Eligible" if score >= 80 AND missing mandatory = 0
    - Classify as "Almost Eligible" if score >= 50 AND missing mandatory <= 2
    - Classify as "Not Eligible" otherwise
    - Sort each category by match score descending
    - Ensure every internship appears in exactly one category
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8_
  
  - [ ]* 6.3 Write property tests for eligibility engine
    - **Property 4: Match Score Bounds** - Match score is always between 0 and 100
    - **Property 3: Classification Completeness** - All internships classified into exactly one category
    - **Property 10: Eligibility Progression** - Adding skills improves or maintains eligibility
    - **Validates: Requirements 6.8, 7.8**
  
  - [x] 6.4 Create eligibility API endpoints
    - Implement `GET /internships/classify` → return classified internships for current user
    - Implement `GET /skills/gaps?internshipId=<id>` → return missing skills for specific internship
    - Add authentication middleware
    - Cache classification results for 1 hour per user
    - _Requirements: 6.1, 6.6, 6.7, 16.2_

- [ ] 7. Internship data management (3 hours)
  - [x] 7.1 Create internship seed data
    - Create `data/internships.json` with 20-30 predefined internships
    - Include variety: software engineering, data science, product management, design
    - Define required skills with proficiency levels and mandatory flags
    - Include companies: Google, Microsoft, Amazon, Flipkart, Swiggy, Zomato, etc.
    - Set realistic stipends, locations, and durations
    - _Requirements: 5.1, 5.2, 5.4_
  
  - [x] 7.2 Implement internship seeding script
    - Create `scripts/seedInternships.ts` to load data into DynamoDB
    - Read from `internships.json` and batch write to Internships table
    - Handle duplicates (skip if internshipId already exists)
    - Log success/failure for each internship
    - _Requirements: 5.1, 5.2_
  
  - [x] 7.3 Create internship API endpoints
    - Implement `GET /internships` → list all active internships with optional filters
    - Implement `GET /internships/:id` → get specific internship details
    - Support query parameters: `type`, `location`, `minStipend`
    - Add authentication middleware
    - _Requirements: 5.3, 5.5_


- [ ] 8. AI project generation service (5 hours)
  - [x] 8.1 Implement project generation with Ollama
    - Create `services/project_service.py` with Ollama integration
    - Implement `generate_project(userId, targetSkills, studentLevel)` using Llama 3.1 8B
    - Create detailed prompt: "Generate a project roadmap to learn [skills] for a [level] student. Include: title, description, 3-5 milestones with tasks, tech stack, estimated duration. Return as JSON."
    - Parse Ollama response into `GeneratedProject` structure
    - Validate response has required fields (title, milestones, targetSkills)
    - Implement retry logic (3 attempts with exponential backoff)
    - _Requirements: 8.1, 8.2, 8.7, 15.5_
    - **Note**: Successfully tested - generates complete projects in 15-30 seconds
  
  - [x] 8.2 Implement project storage and retrieval
    - Implement `saveProject(project)` → store in Projects table with unique projectId
    - Implement `getProject(projectId)` → fetch from Projects table
    - Implement `getUserProjects(userId, status?)` → query by userId with optional status filter
    - Implement `updateProjectStatus(projectId, status)` → update status and timestamp
    - Ensure all target skills are included in stored project
    - _Requirements: 8.3, 8.4, 8.5, 8.6, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_
  
  - [ ]* 8.3 Write property tests for project generation
    - **Property 7: Project Generation Completeness** - Generated project contains all target skills and at least one milestone
    - **Validates: Requirements 8.3, 8.4**
  
  - [x] 8.4 Create project API endpoints
    - Implement `POST /copilot/generate-project` → generate new project
    - Implement `GET /projects` → list user's projects with optional status filter
    - Implement `GET /projects/:id` → get specific project details
    - Implement `PUT /projects/:id/status` → update project status
    - Add authentication middleware
    - Handle AI generation failures gracefully with error messages
    - _Requirements: 8.1, 8.8, 9.1, 9.2, 9.3, 9.4, 9.5, 15.1_

- [ ] 9. Simulated skill verification (3 hours)
  - [x] 9.1 Implement skill verification logic
    - Create `services/verification.service.ts` with simulated verification
    - Implement `verifyProjectCompletion(userId, projectId)` → mark project as complete
    - For each target skill in project: update proficiency to 70, status to "verified"
    - Set verifiedAt timestamp and increment verified skills count
    - Trigger internship re-classification after verification
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
    - **Status**: COMPLETE - Verification service implemented and tested
  
  - [x] 9.2 Implement eligibility progression tracking
    - Implement `detectEligibilityChanges(userId, oldClassification, newClassification)` 
    - Compare classifications before and after skill verification
    - Identify internships that moved from "Not Eligible" → "Almost Eligible" or "Eligible"
    - Identify internships that moved from "Almost Eligible" → "Eligible"
    - Return list of newly eligible internships
    - _Requirements: 11.1, 11.2, 11.3, 11.4_
    - **Status**: COMPLETE - Change detection working correctly
  
  - [ ]* 9.3 Write property tests for skill verification
    - **Property 6: Skill Verification Monotonicity** - Once verified, skills remain verified
    - **Property 2: Skill Graph Consistency** - Verified count equals number of verified skills
    - **Validates: Requirements 10.4, 13.6**
  
  - [x] 9.4 Create verification API endpoint
    - Implement `POST /projects/:id/complete` → mark project complete and verify skills
    - Return updated skill graph and newly eligible internships
    - Add authentication middleware
    - Ensure user owns the project before allowing completion
    - _Requirements: 10.1, 10.5, 10.6, 11.1, 11.4_
    - **Status**: COMPLETE - Endpoint implemented and tested


- [x] 10. Checkpoint - Backend core complete
  - ✅ All backend services are implemented and tested
  - ✅ All API endpoints return correct responses
  - ✅ Authentication flow tested end-to-end
  - ✅ Skill extraction tested with sample resumes (17 skills extracted)
  - ✅ Eligibility classification tested with seed data (2 almost eligible, 18 not eligible)
  - ✅ Project generation tested with various skill combinations (working perfectly)
  - ✅ Complete end-to-end demo flow working successfully
  - **Status**: COMPLETE - All core backend functionality verified

- [ ] 11. Frontend authentication and layout (4 hours)
  - [x] 11.1 Create authentication pages
    - Create `app/auth/signup/page.tsx` with signup form (email, password, name)
    - Create `app/auth/signin/page.tsx` with signin form (email, password)
    - Use `react-hook-form` with Zod validation
    - Display validation errors inline
    - Handle API errors and show user-friendly messages
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 15.1, 15.2_
  
  - [x] 11.2 Implement authentication state management
    - Create `lib/auth.ts` with Zustand store for auth state
    - Store: `user`, `accessToken`, `refreshToken`, `isAuthenticated`
    - Actions: `signIn`, `signOut`, `refreshToken`, `setUser`
    - Persist tokens in localStorage (or httpOnly cookies for production)
    - _Requirements: 1.3, 1.5, 1.6_
  
  - [ ] 11.3 Create API client with authentication
    - Create `lib/api.ts` with Axios instance
    - Add request interceptor to attach Authorization header
    - Add response interceptor to handle 401 errors and refresh token
    - Implement automatic token refresh on expiration
    - _Requirements: 12.1, 12.2, 1.5_
  
  - [x] 11.4 Create protected route wrapper
    - Create `components/ProtectedRoute.tsx` HOC
    - Check authentication state before rendering
    - Redirect to signin if not authenticated
    - Show loading state while checking auth
    - _Requirements: 12.1, 12.5_
  
  - [x] 11.5 Create main layout and navigation
    - Create `components/Layout.tsx` with header, sidebar, and main content area
    - Add navigation links: Dashboard, Profile, Internships, Projects
    - Add user menu with logout button
    - Make responsive for mobile (hamburger menu)
    - Use Tailwind CSS for styling
    - _Requirements: NFR-7, NFR-8_

- [ ] 12. Frontend profile and skill management (4 hours)
  - [x] 12.1 Create profile page
    - Create `app/profile/page.tsx` with profile display and edit form
    - Display: name, email, education, experience, resume link
    - Allow editing personal info, education, experience
    - Show resume upload button with file picker
    - Display upload progress and success/error messages
    - _Requirements: 2.4, 2.5, 2.6_
  
  - [x] 12.2 Implement resume upload component
    - Create `components/ResumeUpload.tsx` with drag-and-drop support
    - Validate file type (PDF, DOCX, TXT) and size (<10MB) on client side
    - Show upload progress bar
    - Display extracted skills after upload completes
    - Handle errors (file too large, unsupported format, upload failed)
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.3, 15.1_
    - **Status**: COMPLETE - Full drag-and-drop component with skill display
  
  - [ ] 12.3 Create skill graph visualization
    - Create `components/SkillGraph.tsx` to display skills as cards or list
    - Show skill name, category, proficiency level, verification status
    - Use color coding: gray for claimed, yellow for in-progress, green for verified
    - Add filter by category and status
    - Add "Add Skill" button to manually add skills
    - _Requirements: 4.3, 4.4, 4.5_
  
  - [ ] 12.4 Create skill addition modal
    - Create `components/AddSkillModal.tsx` with form
    - Input: skill name, category dropdown
    - Validate skill name is not empty
    - Call API to add skill and refresh skill graph
    - _Requirements: 4.4_


- [ ] 13. Frontend internship discovery (5 hours)
  - [x] 13.1 Create internships listing page
    - Create `app/internships/page.tsx` with three tabs: Eligible, Almost Eligible, Not Eligible
    - Fetch classified internships from API on page load
    - Display loading state while fetching
    - Show count for each category in tab badges
    - _Requirements: 6.1, 6.6_
  
  - [ ] 13.2 Create internship card component
    - Create `components/InternshipCard.tsx` to display internship summary
    - Show: title, company, location, type, stipend, match score
    - Use color coding: green for eligible, yellow for almost eligible, gray for not eligible
    - Add "View Details" button
    - Show match score as progress bar or percentage badge
    - _Requirements: 6.6, 7.1_
  
  - [ ] 13.3 Create internship detail modal
    - Create `components/InternshipDetailModal.tsx` with full internship info
    - Display: description, required skills, preferred skills, duration, deadline
    - Show matched skills (green checkmarks) and missing skills (red X)
    - For missing skills: show current proficiency vs required proficiency
    - Add "Generate Project" button for missing skills
    - _Requirements: 6.7, 7.1_
  
  - [ ] 13.4 Implement filters and search
    - Add filter dropdowns: type (remote/onsite/hybrid), location
    - Add search input to filter by company or title
    - Apply filters client-side on classified internships
    - _Requirements: 5.5_
  
  - [ ] 13.5 Create skill gap visualization
    - Create `components/SkillGapChart.tsx` to show missing skills for "Almost Eligible" internships
    - Display as horizontal bar chart: current proficiency vs required
    - Highlight mandatory skills in red
    - Add "Learn This Skill" button next to each missing skill
    - _Requirements: 6.7, 7.3, 7.4, 7.5, 7.6_

- [ ] 14. Frontend project generation and management (4 hours)
  - [ ] 14.1 Create project generation modal
    - Create `components/GenerateProjectModal.tsx` with form
    - Inputs: target skills (multi-select), student level (dropdown), time commitment
    - Show loading state during AI generation (can take 5-10 seconds)
    - Display generated project preview with title, description, milestones
    - Add "Accept Project" and "Regenerate" buttons
    - _Requirements: 8.1, 8.2, 8.3_
  
  - [x] 14.2 Create projects page
    - Create `app/projects/page.tsx` with project list
    - Show tabs: Suggested, In Progress, Completed
    - Display project cards with title, target skills, estimated duration, status
    - Add "Generate New Project" button
    - _Requirements: 9.1, 9.2, 9.6_
  
  - [ ] 14.3 Create project detail page
    - Create `app/projects/[id]/page.tsx` with full project details
    - Display: title, description, objectives, tech stack, milestones with tasks
    - Show progress indicator (which milestone is current)
    - Add "Mark as In Progress" button for suggested projects
    - Add "Mark as Complete" button for in-progress projects
    - _Requirements: 9.2, 9.3, 9.4, 9.5_
  
  - [ ] 14.4 Implement project completion flow
    - When "Mark as Complete" clicked, show confirmation modal
    - Explain that skills will be verified and proficiency updated to 70
    - Call API to complete project
    - Show success message with newly verified skills
    - Display newly eligible internships in a modal or notification
    - _Requirements: 10.1, 10.2, 10.3, 10.5, 10.6, 11.2, 11.3_


- [ ] 15. Frontend dashboard and notifications (3 hours)
  - [x] 15.1 Create dashboard page
    - Create `app/dashboard/page.tsx` as landing page after login
    - Display key metrics: total skills, verified skills, eligible internships count
    - Show "Quick Actions" section: Upload Resume, View Internships, Generate Project
    - Display recent activity: recently verified skills, newly eligible internships
    - Show progress chart: skill verification progress over time
    - _Requirements: 4.6, 6.6, 10.4_
  
  - [ ] 15.2 Create notification system
    - Create `components/NotificationBanner.tsx` for success/error messages
    - Use Zustand store for notification state
    - Auto-dismiss after 5 seconds
    - Support types: success, error, warning, info
    - _Requirements: 11.2, 11.3, 15.1, 15.2, 15.3_
  
  - [ ] 15.3 Implement eligibility change notifications
    - When project is completed, show notification: "You're now eligible for X new internships!"
    - Display list of newly eligible internships in modal
    - Add "View Internships" button to navigate to internships page
    - _Requirements: 11.2, 11.3_

- [ ] 16. Checkpoint - Frontend core complete
  - Ensure all pages render correctly
  - Test authentication flow: signup → signin → dashboard
  - Test profile creation: upload resume → view extracted skills
  - Test internship discovery: view classified internships → see skill gaps
  - Test project generation: generate project → accept → mark complete
  - Test skill verification: complete project → see updated skills → see new eligible internships
  - Verify responsive design on mobile devices
  - Ask the user if questions arise

- [ ] 17. Error handling and resilience (3 hours)
  - [x] 17.1 Implement comprehensive error handling in backend
    - Add try-catch blocks to all Lambda handlers
    - Map errors to appropriate HTTP status codes (400, 401, 403, 404, 500, 503)
    - Return standardized error response: `{ success: false, error: { code, message, details } }`
    - Log all errors to CloudWatch with full context (userId, requestId, stack trace)
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.7_
  
  - [x] 17.2 Implement retry logic for external services
    - Add exponential backoff retry for Bedrock API calls (3 attempts)
    - Add exponential backoff retry for S3 operations (3 attempts)
    - Add exponential backoff retry for DynamoDB operations (3 attempts)
    - Return 503 Service Unavailable after all retries exhausted
    - _Requirements: 15.5, 15.6_
  
  - [ ] 17.3 Add frontend error boundaries
    - Create `components/ErrorBoundary.tsx` to catch React errors
    - Display user-friendly error page with "Try Again" button
    - Log errors to console for debugging
    - _Requirements: 15.1_
  
  - [ ] 17.4 Implement loading states and timeouts
    - Add loading spinners for all async operations
    - Set timeout for API calls (30 seconds)
    - Show timeout error message if request takes too long
    - Add retry button for failed requests
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_


- [ ] 18. Performance optimization (3 hours)
  - [ ] 18.1 Implement caching for internship classification
    - Add in-memory cache (or Redis if needed) for classification results
    - Cache key: `classification:${userId}`
    - TTL: 1 hour
    - Invalidate cache when skills are verified
    - _Requirements: 16.2_
  
  - [ ] 18.2 Optimize Lambda cold starts
    - Configure provisioned concurrency for critical endpoints (auth, profile, classification)
    - Minimize Lambda package size by excluding dev dependencies
    - Use Lambda layers for shared dependencies (AWS SDK, common utilities)
    - Set appropriate memory allocation (1024MB for AI operations, 512MB for others)
    - _Requirements: 16.7, NFR-5_
  
  - [ ] 18.3 Implement pagination for large result sets
    - Add pagination to `GET /internships` endpoint (limit: 50 per page)
    - Add pagination to `GET /projects` endpoint (limit: 20 per page)
    - Return pagination metadata: `{ items, total, page, pageSize, hasMore }`
    - _Requirements: 16.1, 16.2_
  
  - [ ] 18.4 Optimize frontend bundle size
    - Enable Next.js code splitting and tree shaking
    - Lazy load heavy components (charts, modals)
    - Use dynamic imports for non-critical pages
    - Optimize images with Next.js Image component
    - _Requirements: NFR-5, NFR-7_

- [ ] 19. Security hardening (3 hours)
  - [ ] 19.1 Implement rate limiting
    - Add rate limiting middleware to API Gateway or Lambda
    - Limit: 1000 requests per minute per user
    - Return 429 Too Many Requests when limit exceeded
    - _Requirements: 17.7_
  
  - [ ] 19.2 Add input sanitization
    - Sanitize all user inputs to prevent XSS attacks
    - Escape HTML in user-generated content (profile descriptions, project notes)
    - Validate and sanitize file uploads (check magic bytes, not just extension)
    - _Requirements: 17.1, 17.5_
  
  - [ ] 19.3 Implement CORS configuration
    - Configure API Gateway CORS to allow only frontend domain
    - Set allowed methods: GET, POST, PUT, DELETE
    - Set allowed headers: Authorization, Content-Type
    - Enable credentials for cookie-based auth
    - _Requirements: 17.1_
  
  - [ ] 19.4 Add security headers
    - Set security headers in API responses: `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`
    - Enable HSTS (HTTP Strict Transport Security)
    - Set CSP (Content Security Policy) for frontend
    - _Requirements: 17.1_
  
  - [ ] 19.5 Implement secrets management
    - Store sensitive config in AWS Secrets Manager or SSM Parameter Store
    - Never hardcode API keys, database credentials, or JWT secrets
    - Load secrets at Lambda initialization
    - Rotate secrets regularly
    - _Requirements: 17.6, NFR-4_


- [ ] 20. Monitoring and observability (2 hours)
  - [ ] 20.1 Implement CloudWatch logging
    - Add structured logging to all Lambda functions
    - Log format: `{ timestamp, level, message, userId, requestId, duration, error }`
    - Log levels: DEBUG, INFO, WARN, ERROR
    - Never log sensitive data (passwords, tokens, PII)
    - _Requirements: 18.1, 18.2, 17.6_
  
  - [ ] 20.2 Add custom CloudWatch metrics
    - Emit custom metrics for business events: user signups, resume uploads, projects generated, skills verified
    - Track API latency per endpoint
    - Track error rates per endpoint
    - Track AI service usage (tokens, latency)
    - _Requirements: 18.3_
  
  - [ ] 20.3 Configure CloudWatch alarms
    - Create alarm: API error rate > 5% for 5 minutes
    - Create alarm: API latency p95 > 1000ms for 5 minutes
    - Create alarm: Lambda throttling events > 10 in 5 minutes
    - Create alarm: DynamoDB throttling events > 5 in 5 minutes
    - Send notifications to SNS topic or email
    - _Requirements: 18.4, 18.5_
  
  - [ ] 20.4 Enable X-Ray tracing
    - Enable X-Ray for all Lambda functions
    - Add X-Ray SDK to trace external service calls (DynamoDB, S3, Bedrock)
    - View distributed traces in X-Ray console
    - _Requirements: 18.6_

- [ ] 21. Testing and quality assurance (4 hours)
  - [ ]* 21.1 Write unit tests for core services
    - Test authentication service: token generation, validation, expiration
    - Test eligibility engine: match score calculation with various inputs
    - Test skill graph service: CRUD operations, consistency checks
    - Test project generator: parsing AI responses, validation
    - Target: 80% code coverage
    - _Requirements: NFR-3_
  
  - [ ]* 21.2 Write integration tests for API endpoints
    - Test auth flow: signup → signin → refresh → signout
    - Test profile flow: create → upload resume → extract skills → update
    - Test internship flow: list → classify → get details
    - Test project flow: generate → accept → complete → verify skills
    - Use test database and mock external services
    - _Requirements: All functional requirements_
  
  - [ ]* 21.3 Perform manual testing
    - Test complete user journey: signup → profile → internships → project → verification
    - Test error scenarios: invalid inputs, network failures, service timeouts
    - Test on multiple browsers: Chrome, Firefox, Safari, Edge
    - Test on mobile devices: iOS Safari, Android Chrome
    - Test accessibility: keyboard navigation, screen reader compatibility
    - _Requirements: NFR-7, NFR-8, NFR-9_
  
  - [ ]* 21.4 Load testing
    - Use Artillery or k6 to simulate 100 concurrent users
    - Test critical endpoints: signin, classification, project generation
    - Verify response times meet targets (p95 < 500ms for most endpoints)
    - Verify no errors under load
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5, 16.6_


- [ ] 22. Deployment and infrastructure (3 hours)
  - [ ] 22.1 Configure AWS SAM/Serverless deployment
    - Finalize `template.yaml` or `serverless.yml` with all resources
    - Set environment variables for each Lambda function
    - Configure API Gateway stages: dev, staging, prod
    - Set up IAM roles with least privilege access
    - _Requirements: NFR-5_
  
  - [ ] 22.2 Deploy backend to AWS
    - Run `sam deploy` or `serverless deploy` to deploy backend
    - Verify all Lambda functions are created
    - Verify API Gateway endpoints are accessible
    - Verify DynamoDB tables are created with correct schema
    - Verify S3 bucket is created with encryption enabled
    - Verify Cognito User Pool is created
    - Test API endpoints with Postman or curl
    - _Requirements: 1.1, 13.1, 14.1, 14.2, 17.2, 17.3_
  
  - [ ] 22.3 Deploy frontend to Vercel/Amplify
    - Configure environment variables: `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_COGNITO_*`
    - Deploy to Vercel or AWS Amplify
    - Configure custom domain (optional)
    - Enable HTTPS
    - Test frontend in production environment
    - _Requirements: NFR-5, 17.1_
  
  - [ ] 22.4 Run database seeding scripts
    - Execute `seedInternships.ts` to populate Internships table
    - Verify internships are loaded correctly
    - Create test user accounts for demo
    - _Requirements: 5.1_
  
  - [ ] 22.5 Configure CI/CD pipeline
    - Set up GitHub Actions or AWS CodePipeline
    - Automate backend deployment on push to main branch
    - Automate frontend deployment on push to main branch
    - Run tests before deployment
    - _Requirements: NFR-5_

- [ ] 23. Documentation and demo preparation (2 hours)
  - [ ] 23.1 Create API documentation
    - Generate OpenAPI/Swagger spec from code
    - Document all endpoints with request/response examples
    - Host documentation on Swagger UI or Postman
    - _Requirements: NFR-10_
  
  - [ ] 23.2 Create demo script and test data
    - Create demo user account with pre-populated profile
    - Create demo resume files for testing
    - Prepare demo flow: signup → upload resume → view skills → classify internships → generate project → complete project → see new eligibility
    - Document demo steps in README
    - _Requirements: All functional requirements_
  
  - [ ] 23.3 Write README and setup instructions
    - Document project structure and architecture
    - Document environment variables and configuration
    - Document deployment steps for backend and frontend
    - Document how to run locally for development
    - Add troubleshooting section for common issues
    - _Requirements: NFR-3_

- [ ] 24. Final checkpoint and polish
  - Perform end-to-end testing of complete user journey
  - Fix any remaining bugs or UI issues
  - Verify all acceptance criteria are met
  - Verify performance targets are met
  - Verify security measures are in place
  - Verify monitoring and logging are working
  - Prepare demo presentation
  - Ask the user if questions arise


## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation and allow for course correction
- Property tests validate universal correctness properties from the design document
- Unit and integration tests validate specific examples and edge cases
- The 48-hour estimate assumes 2 developers working in parallel or 1 developer working full-time
- Backend and frontend tasks can be parallelized for faster completion
- AI service calls (Bedrock) may take 5-10 seconds; ensure proper loading states
- DynamoDB tables should use on-demand pricing for MVP to minimize costs
- Lambda functions should use appropriate memory allocation to balance cost and performance
- Frontend should be optimized for mobile-first design with responsive breakpoints

## Time Breakdown by Phase

1. **Infrastructure & Setup** (6 hours): Tasks 1.1-1.3
2. **Backend Core** (26 hours): Tasks 2.1-9.4
3. **Frontend Core** (20 hours): Tasks 11.1-15.3
4. **Quality & Optimization** (11 hours): Tasks 17.1-21.4
5. **Deployment & Documentation** (5 hours): Tasks 22.1-23.3

**Total: 48 hours** (excluding optional testing tasks)

## Parallel Execution Strategy

**Track 1 (Backend Developer):**
- Tasks 1.1, 1.3 → 2.1-2.5 → 3.1-3.3 → 4.1-4.5 → 5.1-5.3 → 6.1-6.4 → 7.1-7.3 → 8.1-8.4 → 9.1-9.4 → 17.1-17.2 → 18.1-18.3 → 19.1-19.5 → 20.1-20.4 → 22.1-22.2

**Track 2 (Frontend Developer):**
- Tasks 1.2 → 11.1-11.5 → 12.1-12.4 → 13.1-13.5 → 14.1-14.4 → 15.1-15.3 → 17.3-17.4 → 18.4 → 22.3

**Joint Tasks:**
- Tasks 10, 16, 21.1-21.4, 22.4-22.5, 23.1-23.3, 24

This parallel approach can reduce total time to 30-36 hours with 2 developers.

