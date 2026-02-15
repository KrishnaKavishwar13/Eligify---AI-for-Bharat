# Design Document: Eligify Platform

## Overview

Eligify is built as a modern web application with a React frontend, FastAPI backend, PostgreSQL database, and integrated AI services. The architecture follows a layered approach with clear separation between presentation, business logic, AI processing, and data persistence layers.

The system processes student resumes through an AI-powered pipeline that extracts skills, calculates eligibility scores for internships, identifies skill gaps, and generates personalized learning roadmaps. All data flows through a RESTful API with JWT-based authentication.

## System Architecture

The platform consists of four primary layers:

### Frontend Layer
- **Technology**: React with TypeScript
- **Responsibilities**: User interface, state management, API communication
- **Key Components**: Dashboard, Resume Upload, Internship Browser, Roadmap Viewer
- **State Management**: React Context API or Redux for global state
- **Routing**: React Router for navigation

### Backend Layer
- **Technology**: FastAPI (Python)
- **Responsibilities**: Business logic, API endpoints, request validation, authentication
- **Key Components**: API Gateway, Authentication Service, Business Logic Controllers
- **API Style**: RESTful with JSON payloads
- **Authentication**: JWT tokens with 24-hour expiration

### AI Layer
- **Technology**: LLM API integration (OpenAI GPT-4 or similar)
- **Responsibilities**: Resume parsing, skill extraction, roadmap generation
- **Key Components**: Resume Parser, Skill Extractor, SkillGenie AI
- **Integration Pattern**: Async API calls with retry logic and timeout handling

### Database Layer
- **Technology**: PostgreSQL
- **Responsibilities**: Data persistence, relational integrity, query optimization
- **Key Features**: ACID transactions, indexing, foreign key constraints
- **Connection**: SQLAlchemy ORM for Python backend

## Component Architecture

### API Gateway
The API Gateway serves as the entry point for all client requests.

**Responsibilities:**
- Route requests to appropriate service handlers
- Validate JWT tokens for protected endpoints
- Implement rate limiting (100 requests per minute per user)
- Log all requests for monitoring and debugging
- Handle CORS for frontend communication

**Endpoints:**
- `POST /auth/register` - User registration
- `POST /auth/login` - User authentication
- `POST /resume/upload` - Resume file upload
- `GET /profile` - Retrieve user profile
- `PUT /profile` - Update user profile
- `GET /internships` - List available internships
- `GET /internships/{id}/eligibility` - Get eligibility score for specific internship
- `GET /skill-gaps/{internship_id}` - Get skill gaps for internship
- `POST /roadmap/generate` - Generate learning roadmap
- `PUT /projects/{id}/complete` - Mark project as completed
- `GET /dashboard` - Get dashboard data

### Authentication Service
Handles user registration, login, and token management.

**Components:**
- **User Registration Handler**: Validates email format, checks for duplicates, hashes passwords using bcrypt
- **Login Handler**: Verifies credentials, generates JWT tokens
- **Token Validator**: Validates JWT tokens on protected routes
- **Password Hasher**: Uses bcrypt with salt rounds = 12

**Token Structure:**
```json
{
  "user_id": "uuid",
  "email": "string",
  "exp": "timestamp",
  "iat": "timestamp"
}
```

### Resume Parser
Extracts structured text from uploaded resume files.

**Input:** PDF or DOCX file (max 10MB)
**Output:** Plain text string with preserved structure

**Process:**
1. Validate file format and size
2. Extract text using PyPDF2 (PDF) or python-docx (DOCX)
3. Clean extracted text (remove extra whitespace, normalize encoding)
4. Return structured text for skill extraction

**Error Handling:**
- Unsupported format → Return 400 error with message
- File too large → Return 413 error
- Corrupted file → Return 422 error with details

### Skill Extractor (AI Component)
Uses LLM to identify and categorize skills from resume text.

**Input:** Resume text string
**Output:** List of skills with categories

**LLM Prompt Structure:**
```
You are a skill extraction expert. Analyze the following resume and extract all skills.
Categorize each skill as: programming_language, framework, tool, soft_skill, or domain_knowledge.

Resume:
{resume_text}

Return a JSON array with format:
[{"skill": "Python", "category": "programming_language"}, ...]
```

**Post-Processing:**
1. Parse LLM JSON response
2. Deduplicate skills (case-insensitive)
3. Validate minimum 5 skills extracted
4. Store skills in database linked to user profile

### Eligibility Engine
Calculates compatibility scores between student skills and internship requirements.

**Algorithm:**
```
eligibility_score = (matched_skills / required_skills) * 100

Where:
- matched_skills = count of student skills that match internship requirements
- required_skills = total count of skills required by internship
- Score is capped at 100
```

**Skill Matching Logic:**
- Exact match: Full credit (e.g., "Python" matches "Python")
- Partial match: 50% credit (e.g., "React" matches "React.js")
- Related skills: 25% credit (e.g., "JavaScript" provides partial credit for "TypeScript")

**Classification:**
- Score >= 70: "Highly Eligible" (green indicator)
- Score 40-69: "Moderately Eligible" (yellow indicator)
- Score < 40: "Low Eligibility" (red indicator)

### Skill Gap Detector
Identifies missing skills and calculates their impact on eligibility.

**Process:**
1. Retrieve internship required skills
2. Retrieve student current skills
3. Compute set difference: `gaps = required_skills - student_skills`
4. For each gap, calculate impact on eligibility score
5. Classify gaps as "Critical" (high-priority requirements) or "Nice-to-Have" (preferred requirements)
6. Sort gaps by impact in descending order

**Gap Impact Calculation:**
```
impact = (1 / total_required_skills) * 100 * priority_weight

Where:
- priority_weight = 1.5 for critical skills, 1.0 for nice-to-have
```

### Internship Matcher
Ranks and recommends internships based on eligibility scores.

**Process:**
1. Calculate eligibility scores for all active internships
2. Filter out expired internships (deadline passed)
3. Sort internships by eligibility score (descending)
4. Return top N internships (default N=20)

**Ranking Factors:**
- Primary: Eligibility score
- Secondary: Application deadline proximity (prefer sooner deadlines)
- Tertiary: Internship creation date (prefer newer listings)

### SkillGenie AI
Generates personalized project-based learning roadmaps using LLM.

**Input:** List of skill gaps with priorities
**Output:** Learning roadmap with 3-7 projects

**LLM Prompt Structure:**
```
You are SkillGenie, an expert learning path designer. Create a project-based learning roadmap to help a student acquire the following skills:

Skill Gaps:
{skill_gaps_json}

Generate 3-7 hands-on projects that:
1. Address the critical skill gaps first
2. Build progressively in complexity
3. Include clear learning objectives
4. Provide estimated completion time
5. Define 3-5 measurable milestones per project

Return JSON format:
{
  "roadmap_title": "string",
  "projects": [
    {
      "title": "string",
      "description": "string",
      "skills_addressed": ["skill1", "skill2"],
      "learning_objectives": ["objective1", "objective2"],
      "estimated_hours": number,
      "milestones": [
        {"title": "string", "description": "string"}
      ]
    }
  ]
}
```

**Post-Processing:**
1. Parse LLM JSON response
2. Validate project count (3-7)
3. Ensure all critical gaps are addressed
4. Store roadmap in database
5. Link roadmap to user profile

### Project Completion Handler
Updates student profile when projects are completed.

**Process:**
1. Validate project belongs to user
2. Mark project as completed with timestamp
3. Extract skills addressed by project
4. Add skills to student profile
5. Trigger eligibility score recalculation for all internships
6. Calculate score delta (new score - old score)
7. Return updated scores to frontend

## Data Models

### User
```python
{
  "id": UUID (primary key),
  "email": String (unique, indexed),
  "password_hash": String,
  "full_name": String,
  "created_at": Timestamp,
  "updated_at": Timestamp
}
```

### StudentProfile
```python
{
  "id": UUID (primary key),
  "user_id": UUID (foreign key → User),
  "resume_text": Text,
  "resume_file_path": String,
  "uploaded_at": Timestamp,
  "updated_at": Timestamp
}
```

### Skill
```python
{
  "id": UUID (primary key),
  "profile_id": UUID (foreign key → StudentProfile),
  "skill_name": String (indexed),
  "category": Enum (programming_language, framework, tool, soft_skill, domain_knowledge),
  "source": Enum (resume, project_completion, manual),
  "acquired_at": Timestamp
}
```

### Internship
```python
{
  "id": UUID (primary key),
  "title": String,
  "company": String,
  "description": Text,
  "application_deadline": Date (indexed),
  "is_active": Boolean (indexed),
  "created_at": Timestamp,
  "updated_at": Timestamp
}
```

### InternshipSkill
```python
{
  "id": UUID (primary key),
  "internship_id": UUID (foreign key → Internship),
  "skill_name": String,
  "priority": Enum (critical, nice_to_have),
  "category": Enum (programming_language, framework, tool, soft_skill, domain_knowledge)
}
```

### EligibilityScore
```python
{
  "id": UUID (primary key),
  "profile_id": UUID (foreign key → StudentProfile),
  "internship_id": UUID (foreign key → Internship),
  "score": Float (0-100),
  "classification": Enum (highly_eligible, moderately_eligible, low_eligibility),
  "calculated_at": Timestamp (indexed)
}
```

### LearningRoadmap
```python
{
  "id": UUID (primary key),
  "profile_id": UUID (foreign key → StudentProfile),
  "internship_id": UUID (foreign key → Internship),
  "title": String,
  "generated_at": Timestamp,
  "is_active": Boolean
}
```

### Project
```python
{
  "id": UUID (primary key),
  "roadmap_id": UUID (foreign key → LearningRoadmap),
  "title": String,
  "description": Text,
  "estimated_hours": Integer,
  "is_completed": Boolean (indexed),
  "completed_at": Timestamp,
  "order_index": Integer
}
```

### ProjectSkill
```python
{
  "id": UUID (primary key),
  "project_id": UUID (foreign key → Project),
  "skill_name": String
}
```

### Milestone
```python
{
  "id": UUID (primary key),
  "project_id": UUID (foreign key → Project),
  "title": String,
  "description": Text,
  "order_index": Integer,
  "is_completed": Boolean,
  "completed_at": Timestamp
}
```

## Database Relationships

```
User (1) ──→ (1) StudentProfile
StudentProfile (1) ──→ (many) Skill
StudentProfile (1) ──→ (many) EligibilityScore
StudentProfile (1) ──→ (many) LearningRoadmap
Internship (1) ──→ (many) InternshipSkill
Internship (1) ──→ (many) EligibilityScore
LearningRoadmap (1) ──→ (many) Project
Project (1) ──→ (many) ProjectSkill
Project (1) ──→ (many) Milestone
```

## Process Flow

### 1. User Registration and Login
```
User → Frontend: Enter email/password
Frontend → API Gateway: POST /auth/register
API Gateway → Auth Service: Validate and create user
Auth Service → Database: Store user with hashed password
Database → Auth Service: Confirm creation
Auth Service → API Gateway: Return JWT token
API Gateway → Frontend: Return token
Frontend: Store token in localStorage
```

### 2. Resume Upload and Skill Extraction
```
User → Frontend: Upload resume file
Frontend → API Gateway: POST /resume/upload (multipart/form-data)
API Gateway: Validate token and file
API Gateway → Resume Parser: Extract text from file
Resume Parser → API Gateway: Return resume text
API Gateway → Database: Store resume text and file path
API Gateway → Skill Extractor: Extract skills from text
Skill Extractor → LLM API: Send prompt with resume text
LLM API → Skill Extractor: Return skills JSON
Skill Extractor → Database: Store skills linked to profile
Database → API Gateway: Confirm storage
API Gateway → Frontend: Return extracted skills
Frontend: Display skills for user verification
```

### 3. Internship Matching and Eligibility Calculation
```
User → Frontend: Navigate to internships page
Frontend → API Gateway: GET /internships
API Gateway → Database: Fetch active internships
API Gateway → Eligibility Engine: Calculate scores for all internships
Eligibility Engine → Database: Fetch student skills
Eligibility Engine: Compute eligibility scores
Eligibility Engine → Database: Store/update eligibility scores
Database → API Gateway: Return internships with scores
API Gateway → Frontend: Return ranked internships
Frontend: Display internship cards with eligibility indicators
```

### 4. Skill Gap Detection
```
User → Frontend: Click on internship card
Frontend → API Gateway: GET /skill-gaps/{internship_id}
API Gateway → Skill Gap Detector: Identify gaps
Skill Gap Detector → Database: Fetch internship required skills
Skill Gap Detector → Database: Fetch student current skills
Skill Gap Detector: Compute gaps and impact
API Gateway → Frontend: Return skill gaps with priorities
Frontend: Display skill gap visualization (chart/graph)
```

### 5. Learning Roadmap Generation
```
User → Frontend: Click "Generate Roadmap" button
Frontend → API Gateway: POST /roadmap/generate {internship_id}
API Gateway → Skill Gap Detector: Get skill gaps
Skill Gap Detector → API Gateway: Return prioritized gaps
API Gateway → SkillGenie AI: Generate roadmap
SkillGenie AI → LLM API: Send prompt with skill gaps
LLM API → SkillGenie AI: Return roadmap JSON
SkillGenie AI: Validate and parse response
SkillGenie AI → Database: Store roadmap, projects, milestones
Database → API Gateway: Confirm storage
API Gateway → Frontend: Return roadmap with projects
Frontend: Display roadmap with project cards
```

### 6. Project Completion and Score Update
```
User → Frontend: Mark project as completed
Frontend → API Gateway: PUT /projects/{id}/complete
API Gateway → Project Completion Handler: Process completion
Project Completion Handler → Database: Update project status
Project Completion Handler → Database: Add skills to student profile
Project Completion Handler → Eligibility Engine: Recalculate scores
Eligibility Engine: Compute new scores for all internships
Eligibility Engine → Database: Update eligibility scores
Eligibility Engine: Calculate score deltas
Database → API Gateway: Confirm updates
API Gateway → Frontend: Return updated scores with deltas
Frontend: Display score improvements with animations
```

### 7. Dashboard Data Aggregation
```
User → Frontend: Navigate to dashboard
Frontend → API Gateway: GET /dashboard
API Gateway → Database: Fetch student profile
API Gateway → Database: Fetch top eligibility scores
API Gateway → Database: Fetch active roadmaps with progress
API Gateway → Database: Fetch skill gap summaries
API Gateway: Aggregate all data
API Gateway → Frontend: Return dashboard payload
Frontend: Render dashboard with charts and cards
```

## Tech Stack

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS for utility-first styling
- **Charts**: Recharts or Chart.js for skill gap visualization
- **HTTP Client**: Axios for API communication
- **State Management**: React Context API or Zustand
- **Routing**: React Router v6
- **Form Handling**: React Hook Form with Zod validation

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic for database migrations
- **Authentication**: python-jose for JWT, passlib for password hashing
- **Validation**: Pydantic models for request/response validation
- **File Processing**: PyPDF2 for PDF parsing, python-docx for DOCX parsing
- **HTTP Client**: httpx for async LLM API calls
- **CORS**: FastAPI CORS middleware

### Database
- **RDBMS**: PostgreSQL 15+
- **Connection Pooling**: SQLAlchemy connection pool
- **Indexing**: B-tree indexes on frequently queried columns
- **Constraints**: Foreign keys, unique constraints, check constraints

### AI/ML
- **LLM Provider**: OpenAI GPT-4 or GPT-3.5-turbo
- **API Integration**: OpenAI Python SDK
- **Prompt Engineering**: Structured prompts with JSON output format
- **Fallback**: Retry logic with exponential backoff

### Infrastructure
- **Deployment**: Docker containers
- **Web Server**: Uvicorn (ASGI server for FastAPI)
- **Reverse Proxy**: Nginx for production
- **File Storage**: Local filesystem or S3-compatible storage
- **Environment**: Python virtual environment (venv)

### Development Tools
- **Version Control**: Git
- **Code Quality**: ESLint (frontend), Black + Flake8 (backend)
- **Testing**: Jest + React Testing Library (frontend), pytest (backend)
- **API Documentation**: FastAPI automatic OpenAPI/Swagger docs

## UI Overview

### Dashboard Page
**Layout:**
- Header with user name and logout button
- Eligibility score summary card (average score across all internships)
- Top 5 matched internships as cards with scores and visual indicators
- Skill gap summary chart (bar chart showing top gaps)
- Active learning roadmap progress (progress bars for each project)
- Quick action buttons: "Upload New Resume", "Browse All Internships"

**Visual Elements:**
- Color-coded eligibility indicators (green/yellow/red)
- Progress bars for roadmap completion
- Animated score changes when projects are completed
- Responsive grid layout

### Internship Browser Page
**Layout:**
- Search and filter bar (by company, skills, deadline)
- Internship cards in grid layout
- Each card shows:
  - Company logo placeholder
  - Internship title
  - Eligibility score with color indicator
  - Top 3 required skills
  - Application deadline
  - "View Details" button

**Interactions:**
- Click card to view full details and skill gaps
- Sort by eligibility score, deadline, or company
- Filter by eligibility classification

### Internship Detail Page
**Layout:**
- Internship information (title, company, description, deadline)
- Eligibility score prominently displayed
- Required skills list with checkmarks for matched skills
- Skill gap section with impact visualization
- "Generate Learning Roadmap" button
- Link to existing roadmap if already generated

**Visual Elements:**
- Skill gap chart (horizontal bar chart showing impact)
- Matched vs. missing skills comparison
- Critical gaps highlighted in red

### Learning Roadmap Page
**Layout:**
- Roadmap title and generation date
- Target internship reference
- Project cards in sequential order
- Each project card shows:
  - Project title and description
  - Skills addressed (tags)
  - Estimated completion time
  - Milestone checklist
  - "Mark as Complete" button
- Overall progress indicator at top

**Interactions:**
- Expand/collapse project details
- Check off individual milestones
- Mark entire project as complete
- View eligibility score projection after completion

### Profile Page
**Layout:**
- User information (name, email)
- Resume upload section with current resume display
- Extracted skills list (editable)
- Skill acquisition timeline
- Account settings

**Interactions:**
- Upload new resume (replaces old one)
- Manually add/remove skills
- Edit profile information
- Change password

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system - essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Authentication and User Management Properties

Property 1: User registration creates accessible accounts
*For any* valid email and password combination, registering a user then authenticating with those credentials should succeed and grant access.
**Validates: Requirements 1.1, 1.2**

Property 2: Profile updates are persistent
*For any* user profile and any valid profile data, updating the profile then retrieving it should return the updated data (round-trip property).
**Validates: Requirements 1.3**

Property 3: Invalid credentials are rejected
*For any* invalid credential combination (wrong password, non-existent email), authentication attempts should fail with appropriate error messages.
**Validates: Requirements 1.4**

Property 4: Passwords are never stored in plaintext
*For any* user account, the stored password hash should never match the original plaintext password.
**Validates: Requirements 1.5**

### Resume Processing Properties

Property 5: Valid file formats are accepted
*For any* valid PDF or DOCX file under 10MB, the platform should accept the upload and extract text content successfully.
**Validates: Requirements 2.1, 2.2**

Property 6: Skill extraction produces categorized output
*For any* resume text, the skill extractor should return skills where each skill has a valid category (programming_language, framework, tool, soft_skill, or domain_knowledge).
**Validates: Requirements 2.3, 3.1, 3.2**

Property 7: Invalid file formats are rejected
*For any* unsupported file format (not PDF or DOCX) or file exceeding 10MB, the upload should be rejected with a descriptive error message.
**Validates: Requirements 2.4**

Property 8: Skill extraction round-trip
*For any* resume upload, extracting skills then retrieving the student profile should contain all extracted skills.
**Validates: Requirements 2.5**

Property 9: Duplicate skills are consolidated
*For any* resume text containing duplicate skill mentions, the extracted skill list should contain each unique skill exactly once (idempotence property).
**Validates: Requirements 3.3**

Property 10: Minimum skill extraction threshold
*For any* valid resume, the skill extractor should identify at least 5 skills.
**Validates: Requirements 3.4**

### Eligibility Calculation Properties

Property 11: Eligibility scores are bounded
*For any* student profile and internship listing, the calculated eligibility score should be between 0 and 100 inclusive.
**Validates: Requirements 4.3**

Property 12: Eligibility scores reflect skill overlap
*For any* student profile and internship listing, if the student has all required skills, the eligibility score should be 100; if the student has no required skills, the score should be 0.
**Validates: Requirements 4.2**

Property 13: Eligibility classification matches score ranges
*For any* eligibility score, the classification should be "Highly Eligible" when score >= 70, "Moderately Eligible" when 40 <= score < 70, and "Low Eligibility" when score < 40.
**Validates: Requirements 4.4, 4.5, 4.6**

Property 14: Internships are ranked by eligibility
*For any* list of internships with eligibility scores, the returned ranking should be sorted in descending order by eligibility score.
**Validates: Requirements 4.7**

Property 15: Eligibility scores are calculated for all internships
*For any* student profile with skills, eligibility scores should be calculated for every active internship listing.
**Validates: Requirements 4.1**

### Skill Gap Detection Properties

Property 16: Skill gaps are set differences
*For any* student profile and internship listing, the identified skill gaps should be exactly the set of required skills not present in the student's skill set.
**Validates: Requirements 5.1**

Property 17: All skill gaps have categories
*For any* detected skill gap, it should be categorized as either "Critical" or "Nice-to-Have".
**Validates: Requirements 5.2**

Property 18: Skill gaps have calculated impacts
*For any* skill gap, there should be a calculated numeric impact value representing its effect on eligibility score.
**Validates: Requirements 5.3**

Property 19: Skill gaps are ordered by impact
*For any* list of skill gaps, they should be displayed in descending order of impact on eligibility.
**Validates: Requirements 5.4**

### Learning Roadmap Generation Properties

Property 20: Roadmaps contain valid project counts
*For any* generated learning roadmap, it should contain between 3 and 7 projects inclusive.
**Validates: Requirements 6.4**

Property 21: Roadmap projects address all skill gaps
*For any* set of skill gaps and generated roadmap, every skill gap should be addressed by at least one project in the roadmap.
**Validates: Requirements 6.2**

Property 22: Projects have required structure
*For any* generated project, it should include a title, description, learning objectives, and estimated completion time.
**Validates: Requirements 6.3**

Property 23: Projects have milestones
*For any* generated project, it should contain at least one measurable milestone.
**Validates: Requirements 6.5**

Property 24: Critical gaps are prioritized
*For any* generated roadmap with both critical and nice-to-have skill gaps, projects addressing critical gaps should appear before projects addressing only nice-to-have gaps.
**Validates: Requirements 6.6**

Property 25: Roadmap persistence round-trip
*For any* generated learning roadmap, storing it to the database then retrieving it should return an equivalent roadmap with all projects and milestones intact.
**Validates: Requirements 6.7**

### Score Tracking and Update Properties

Property 26: Project completion adds skills
*For any* completed project, the student profile should be updated to include all skills addressed by that project.
**Validates: Requirements 7.1**

Property 27: Skill updates trigger score recalculation
*For any* student profile skill update, eligibility scores for all internships should be recalculated, and at least one score should change if the new skill matches any internship requirement.
**Validates: Requirements 7.2**

Property 28: Score deltas are accurate
*For any* eligibility score change, the displayed score difference should equal the new score minus the old score.
**Validates: Requirements 7.3**

Property 29: Score history is maintained
*For any* eligibility score change, a historical record should be created with the old score, new score, and timestamp.
**Validates: Requirements 7.4**

### Dashboard and Data Display Properties

Property 30: Dashboard displays all matched internships
*For any* user with eligibility scores, the dashboard should display scores for all matched internships (or top N if limited).
**Validates: Requirements 7.5, 8.2**

Property 31: Roadmap progress is accurate
*For any* learning roadmap, the displayed completion percentage should equal (completed_projects / total_projects) * 100.
**Validates: Requirements 8.4**

Property 32: Internship cards contain required data
*For any* displayed internship card, it should include the internship title, company, required skills, and eligibility score.
**Validates: Requirements 8.5**

### Internship Management Properties

Property 33: Internship listings have required fields
*For any* stored internship listing, it should contain title, company, description, required skills, and application deadline.
**Validates: Requirements 9.1**

Property 34: Incomplete internship data is rejected
*For any* internship listing missing required fields, the creation attempt should be rejected with a validation error.
**Validates: Requirements 9.2**

Property 35: Expired internships are marked
*For any* internship listing where the application deadline has passed, the is_active flag should be set to false.
**Validates: Requirements 9.3**

Property 36: Expired internships are filtered out
*For any* internship matching query, the results should not include any internships where is_active is false.
**Validates: Requirements 9.4**

Property 37: Internship updates trigger recalculation
*For any* internship listing update that changes required skills, eligibility scores for all student profiles should be recalculated.
**Validates: Requirements 9.5**

### Data Persistence Properties

Property 38: Student profile data round-trip
*For any* student profile with skills, completed projects, and eligibility history, storing then retrieving the profile should return all associated data intact.
**Validates: Requirements 10.2**

Property 39: Roadmap structure round-trip
*For any* learning roadmap with projects and milestones, storing then retrieving should return the complete hierarchical structure.
**Validates: Requirements 10.3**

Property 40: User login retrieves all data
*For any* authenticated user, the retrieved data should include profile, skills, roadmaps, projects, and eligibility scores.
**Validates: Requirements 10.4**

Property 41: Transaction rollback on failure
*For any* database operation that fails mid-transaction, no partial changes should persist in the database (atomicity property).
**Validates: Requirements 10.5, 10.6**

### API Properties

Property 42: Invalid requests are rejected
*For any* API request with invalid format or missing authentication, the request should be rejected with appropriate 4xx error code.
**Validates: Requirements 11.2**

Property 43: Successful operations return 2xx codes
*For any* successful API operation, the response should have an HTTP status code in the 200-299 range.
**Validates: Requirements 11.3**

Property 44: Failed operations return error codes with messages
*For any* failed API operation, the response should have an appropriate 4xx or 5xx status code and include a descriptive error message.
**Validates: Requirements 11.4**

Property 45: API responses are valid JSON
*For any* API response, the content should be parseable as valid JSON.
**Validates: Requirements 11.5**

Property 46: Rate limiting prevents abuse
*For any* user making more than 100 requests per minute, subsequent requests should be rejected with a 429 status code.
**Validates: Requirements 11.6**

### AI Integration Properties

Property 47: AI failures trigger retries
*For any* failed AI API call, the system should retry the request at least once before returning an error to the user.
**Validates: Requirements 12.2**

Property 48: Exhausted retries produce errors
*For any* AI API call that fails after all retry attempts, the system should log the error and return a user-facing error message.
**Validates: Requirements 12.3**

Property 49: AI calls timeout appropriately
*For any* AI API call that exceeds 30 seconds, the request should be terminated and treated as a failure.
**Validates: Requirements 12.4**

Property 50: AI responses are validated
*For any* AI API response, the system should validate the response format matches expected structure before processing.
**Validates: Requirements 12.5**

Property 51: Identical AI requests return cached responses
*For any* AI API request that matches a previous request (same input), the system should return the cached response without making a new API call (idempotence property).
**Validates: Requirements 12.6**

### Error Handling Properties

Property 52: Errors produce user-friendly messages
*For any* error condition, the system should return a user-friendly error message (not internal stack traces or technical details).
**Validates: Requirements 14.1**

Property 53: File upload errors specify reasons
*For any* failed file upload, the error message should specify the reason (unsupported format, file too large, corrupted file, etc.).
**Validates: Requirements 14.2**

Property 54: AI failures suggest retry
*For any* AI processing failure, the error response should notify the user and suggest retry options.
**Validates: Requirements 14.3**

Property 55: Errors are logged with context
*For any* error, a log entry should be created containing timestamp, error details, and relevant context (user_id, operation, etc.).
**Validates: Requirements 14.4**

### Security Properties

Property 56: Users can only access their own data
*For any* user and any data access operation, the user should only be able to retrieve or modify data associated with their own user_id.
**Validates: Requirements 15.3**

Property 57: Expired tokens are rejected
*For any* authentication token that has exceeded its 24-hour expiration time, authentication attempts using that token should fail.
**Validates: Requirements 15.4**

Property 58: Logged-out tokens are invalidated
*For any* user who has logged out, subsequent requests using their previous authentication token should be rejected.
**Validates: Requirements 15.5**

Property 59: Malicious inputs are sanitized
*For any* user input containing SQL injection or XSS attack patterns, the input should be sanitized or rejected before processing.
**Validates: Requirements 15.6**

## Error Handling

### Error Categories

**Client Errors (4xx)**
- 400 Bad Request: Invalid request format, validation failures
- 401 Unauthorized: Missing or invalid authentication token
- 403 Forbidden: Valid token but insufficient permissions
- 404 Not Found: Requested resource doesn't exist
- 413 Payload Too Large: File upload exceeds 10MB limit
- 422 Unprocessable Entity: Valid format but semantic errors (corrupted file)
- 429 Too Many Requests: Rate limit exceeded

**Server Errors (5xx)**
- 500 Internal Server Error: Unexpected server-side errors
- 502 Bad Gateway: External API (LLM) failures
- 503 Service Unavailable: Database connection failures
- 504 Gateway Timeout: AI API timeout exceeded

### Error Response Format

All error responses follow a consistent JSON structure:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "User-friendly error message",
    "details": {
      "field": "specific_field",
      "reason": "detailed_reason"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "uuid"
  }
}
```

### Error Handling Strategies

**Resume Upload Errors**
- Unsupported format → 400 with message "File format not supported. Please upload PDF or DOCX."
- File too large → 413 with message "File size exceeds 10MB limit."
- Corrupted file → 422 with message "Unable to read file. Please ensure the file is not corrupted."
- Text extraction failure → 500 with message "Failed to process resume. Please try again."

**AI Processing Errors**
- LLM API timeout → 504 with message "AI processing took too long. Please try again."
- LLM API failure → 502 with message "AI service temporarily unavailable. Please retry."
- Invalid AI response → 500 with message "AI processing error. Please try again."
- Rate limit exceeded → 429 with message "Too many AI requests. Please wait before retrying."

**Authentication Errors**
- Invalid credentials → 401 with message "Invalid email or password."
- Expired token → 401 with message "Session expired. Please log in again."
- Missing token → 401 with message "Authentication required."
- Invalid token format → 401 with message "Invalid authentication token."

**Database Errors**
- Connection failure → 503 with message "Service temporarily unavailable. Please try again."
- Transaction failure → 500 with message "Operation failed. Please try again."
- Constraint violation → 400 with message "Invalid data. [Specific constraint message]."
- Duplicate entry → 409 with message "Resource already exists."

**Validation Errors**
- Missing required field → 400 with details specifying which field
- Invalid format → 400 with details explaining expected format
- Out of range value → 400 with details specifying valid range

### Retry Logic

**AI API Calls**
- Retry on: 500, 502, 503, 504 status codes
- Retry strategy: Exponential backoff (1s, 2s, 4s)
- Max retries: 3 attempts
- Timeout per attempt: 30 seconds

**Database Operations**
- Retry on: Connection timeouts, deadlocks
- Retry strategy: Linear backoff (1s, 2s, 3s)
- Max retries: 3 attempts
- Transaction isolation: Read Committed

### Logging Strategy

**Error Logs**
- Level: ERROR
- Include: timestamp, user_id, request_id, error_type, stack_trace, context
- Storage: Structured logs (JSON format)
- Retention: 90 days

**Warning Logs**
- Level: WARN
- Include: timestamp, user_id, operation, warning_message
- Examples: Slow queries, approaching rate limits, cache misses

**Info Logs**
- Level: INFO
- Include: timestamp, user_id, operation, duration
- Examples: Successful operations, API calls, score calculations

## Testing Strategy

The testing strategy employs both unit tests for specific examples and property-based tests for universal correctness properties. Both approaches are complementary and necessary for comprehensive coverage.

### Testing Philosophy

**Unit Tests**: Verify specific examples, edge cases, and error conditions
- Focus on concrete scenarios that demonstrate correct behavior
- Test integration points between components
- Validate error handling for known failure modes
- Provide fast feedback during development

**Property-Based Tests**: Verify universal properties across randomized inputs
- Test correctness properties that should hold for all valid inputs
- Discover edge cases through randomization
- Provide high confidence in system correctness
- Each property test runs minimum 100 iterations

### Property-Based Testing Framework

**Python Backend**: Hypothesis
- Generates random test data based on strategies
- Shrinks failing examples to minimal reproducible cases
- Integrates with pytest

**Example Property Test Structure**:
```python
from hypothesis import given, strategies as st
import pytest

# Feature: eligify-platform, Property 11: Eligibility scores are bounded
@given(
    student_skills=st.lists(st.text(min_size=1), min_size=1, max_size=20),
    required_skills=st.lists(st.text(min_size=1), min_size=1, max_size=20)
)
def test_eligibility_scores_are_bounded(student_skills, required_skills):
    """For any student profile and internship listing, 
    eligibility score should be between 0 and 100."""
    score = calculate_eligibility_score(student_skills, required_skills)
    assert 0 <= score <= 100
```

### Test Coverage by Component

**Authentication Service**
- Unit tests: Valid registration, valid login, invalid credentials, token expiration
- Property tests: Property 1 (registration round-trip), Property 3 (invalid credentials rejected), Property 4 (password encryption)

**Resume Parser**
- Unit tests: PDF parsing, DOCX parsing, corrupted file handling
- Property tests: Property 5 (valid formats accepted), Property 7 (invalid formats rejected)

**Skill Extractor**
- Unit tests: Sample resumes with known skills, empty resumes, malformed text
- Property tests: Property 6 (categorized output), Property 9 (deduplication), Property 10 (minimum threshold)

**Eligibility Engine**
- Unit tests: Perfect match (100%), no match (0%), partial match
- Property tests: Property 11 (bounded scores), Property 12 (reflects overlap), Property 13 (classification), Property 14 (ranking)

**Skill Gap Detector**
- Unit tests: No gaps, all gaps, mixed gaps
- Property tests: Property 16 (set difference), Property 17 (categorization), Property 19 (ordering)

**SkillGenie AI**
- Unit tests: Single gap, multiple gaps, critical vs nice-to-have
- Property tests: Property 20 (project count), Property 21 (gap coverage), Property 22 (structure), Property 24 (prioritization)

**Project Completion Handler**
- Unit tests: Single project completion, multiple completions, invalid project
- Property tests: Property 26 (skill addition), Property 27 (score recalculation), Property 28 (delta accuracy)

**API Gateway**
- Unit tests: Valid requests, missing auth, invalid format
- Property tests: Property 42 (invalid rejected), Property 43 (success codes), Property 44 (error codes), Property 45 (JSON format)

**Database Layer**
- Unit tests: CRUD operations, constraint violations, transaction rollback
- Property tests: Property 38 (profile round-trip), Property 39 (roadmap round-trip), Property 41 (atomicity)

### Integration Testing

**End-to-End Flows**
- User registration → login → resume upload → skill extraction → internship matching
- Skill gap detection → roadmap generation → project completion → score update
- Dashboard data aggregation with all components

**API Integration Tests**
- Test all endpoints with valid and invalid inputs
- Verify authentication and authorization
- Test rate limiting behavior
- Verify error response formats

**Database Integration Tests**
- Use Testcontainers for PostgreSQL
- Test migrations and schema changes
- Verify foreign key constraints
- Test transaction isolation

### Test Configuration

**Property Test Settings**
```python
# pytest.ini or conftest.py
from hypothesis import settings, Verbosity

settings.register_profile("ci", max_examples=100, verbosity=Verbosity.verbose)
settings.register_profile("dev", max_examples=20, verbosity=Verbosity.normal)
settings.load_profile("ci")  # Use in CI/CD
```

**Test Tagging**
- Each property test includes a comment with format: `# Feature: eligify-platform, Property N: [property text]`
- Tags enable filtering: `pytest -m "property_test"` or `pytest -m "unit_test"`

### Mocking Strategy

**External Dependencies**
- LLM API: Mock with predefined responses for deterministic tests
- File system: Use temporary directories for file operations
- Time-dependent operations: Mock datetime for deadline testing

**Database**
- Unit tests: Use in-memory SQLite or mocked repositories
- Integration tests: Use Testcontainers PostgreSQL
- Property tests: Use transaction rollback for isolation

### Test Data Generation

**Factories (factory_boy)**
```python
class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    email = factory.Faker('email')
    password_hash = factory.LazyFunction(lambda: hash_password('password123'))
    full_name = factory.Faker('name')

class InternshipFactory(factory.Factory):
    class Meta:
        model = Internship
    
    title = factory.Faker('job')
    company = factory.Faker('company')
    description = factory.Faker('text')
    application_deadline = factory.Faker('future_date')
```

**Hypothesis Strategies**
```python
# Custom strategies for domain objects
@st.composite
def student_profile_strategy(draw):
    return StudentProfile(
        skills=draw(st.lists(st.text(min_size=1), min_size=5, max_size=20)),
        resume_text=draw(st.text(min_size=100, max_size=5000))
    )
```

### Continuous Integration

**CI Pipeline**
1. Lint and format check (Black, Flake8, ESLint)
2. Unit tests (fast feedback)
3. Property tests (100 iterations per property)
4. Integration tests (with Testcontainers)
5. Coverage report (minimum 80% coverage)

**Test Execution Time**
- Unit tests: < 2 minutes
- Property tests: < 10 minutes
- Integration tests: < 5 minutes
- Total CI time: < 20 minutes

### Coverage Goals

- Unit test coverage: 80% minimum
- Property test coverage: All 59 correctness properties implemented
- Integration test coverage: All API endpoints
- E2E test coverage: Critical user flows (registration, resume upload, roadmap generation)

### Test Maintenance

- Review and update tests when requirements change
- Add regression tests for discovered bugs
- Refactor tests to maintain readability
- Keep test data factories up to date with schema changes
