# Requirements Document: Eligify Platform MVP

## Introduction

Eligify is an AI-powered Employability Operating System designed to help Indian students identify skill gaps, build missing skills through guided projects, and unlock internship opportunities. This MVP focuses on delivering a stable, demo-ready platform with core functionality: student authentication, profile management with AI-powered skill extraction, simplified skill tracking, deterministic internship eligibility classification, AI-driven project generation, and simulated skill verification.

The MVP prioritizes fast development (48-hour build target), minimal bugs through deterministic logic, demo stability, and low AWS costs using serverless architecture.

## Glossary

- **System**: The Eligify platform backend and frontend application
- **Student**: A registered user seeking internship opportunities
- **Profile**: Student's personal information, education, experience, and skills
- **Skill_Graph**: Collection of skills associated with a student, including proficiency levels and verification status
- **Internship**: Job opportunity listing with required skills and eligibility criteria
- **Eligibility_Engine**: Deterministic algorithm that classifies internships based on skill matching
- **AI_Generator**: AWS Bedrock service that generates personalized project roadmaps
- **Project**: AI-generated learning roadmap with milestones to build specific skills
- **Proficiency_Level**: Numeric score (0-100) representing skill mastery
- **Match_Score**: Percentage (0-100) indicating how well a student's skills align with internship requirements
- **Cognito**: Amazon Cognito authentication service
- **DynamoDB**: AWS NoSQL database for storing application data
- **S3**: AWS object storage for resume files
- **Bedrock**: AWS managed AI service for LLM access

## Requirements

### Requirement 1: User Authentication

**User Story:** As a student, I want to create an account and log in securely, so that I can access my personalized profile and internship recommendations.

#### Acceptance Criteria

1. WHEN a student provides valid email and password THEN THE System SHALL create a new account in Cognito
2. WHEN a student provides an email that already exists THEN THE System SHALL reject the signup and return an error message
3. WHEN a student provides valid credentials for login THEN THE System SHALL return a JWT access token and refresh token
4. WHEN a student provides invalid credentials THEN THE System SHALL reject the login and return an authentication error
5. WHEN a student's access token expires THEN THE System SHALL accept a valid refresh token to issue a new access token
6. WHEN a student logs out THEN THE System SHALL invalidate the current session

### Requirement 2: Profile Creation and Management

**User Story:** As a student, I want to create and update my profile with personal information and education details, so that the system can understand my background.

#### Acceptance Criteria

1. WHEN a student uploads a resume file THEN THE System SHALL store the file in S3 with user-specific access controls
2. WHEN a resume file exceeds 10MB THEN THE System SHALL reject the upload and return a file size error
3. WHEN a resume file is in an unsupported format THEN THE System SHALL reject the upload and return a format error
4. WHEN a student submits profile information THEN THE System SHALL validate required fields (name, email) before saving
5. WHEN a student updates profile information THEN THE System SHALL persist changes to DynamoDB and return the updated profile
6. WHEN a student requests their profile THEN THE System SHALL return all stored profile data including personal info, education, and experience

### Requirement 3: AI-Powered Skill Extraction

**User Story:** As a student, I want the system to automatically extract skills from my resume, so that I don't have to manually enter every skill.

#### Acceptance Criteria

1. WHEN a resume is uploaded THEN THE System SHALL invoke Bedrock to extract skills from the resume text
2. WHEN Bedrock is unavailable THEN THE System SHALL attempt to use OpenAI API as a fallback
3. WHEN skill extraction completes THEN THE System SHALL return a list of identified skills with normalized names
4. WHEN skill extraction fails after all retries THEN THE System SHALL return an error and allow manual skill entry
5. WHEN extracted skills are saved THEN THE System SHALL store each skill with status "claimed" and proficiency level 0

### Requirement 4: Skill Graph Management

**User Story:** As a student, I want to view and manage my skills with proficiency levels, so that I can track my learning progress.

#### Acceptance Criteria

1. WHEN a student's profile is created THEN THE System SHALL initialize an empty skill graph in DynamoDB
2. WHEN skills are extracted from a resume THEN THE System SHALL add each skill to the skill graph with default proficiency 0
3. WHEN a student requests their skill graph THEN THE System SHALL return all skills with name, proficiency level, and verification status
4. WHEN a student manually adds a skill THEN THE System SHALL validate the skill name and add it to the graph with status "claimed"
5. WHEN a skill is marked as verified THEN THE System SHALL update the proficiency level to minimum 70 and set status to "verified"
6. THE Skill_Graph SHALL maintain a count of total skills and verified skills

### Requirement 5: Internship Data Management

**User Story:** As a system administrator, I want to seed the database with predefined internship listings, so that students have opportunities to match against.

#### Acceptance Criteria

1. WHEN the system initializes THEN THE System SHALL load predefined internship data into DynamoDB
2. WHEN an internship is stored THEN THE System SHALL include title, company, description, required skills, and eligibility criteria
3. WHEN a student requests internship listings THEN THE System SHALL return all active internships
4. WHEN an internship has required skills THEN THE System SHALL store each skill with name, proficiency level, and mandatory flag
5. THE System SHALL support filtering internships by type (remote, onsite, hybrid)

### Requirement 6: Deterministic Eligibility Classification

**User Story:** As a student, I want to see which internships I'm eligible for based on my current skills, so that I can focus on realistic opportunities.

#### Acceptance Criteria

1. WHEN a student requests internship classification THEN THE Eligibility_Engine SHALL calculate a match score for each internship
2. WHEN calculating match score THEN THE Eligibility_Engine SHALL compare student skill proficiency against required skill proficiency
3. WHEN match score is >= 80 AND missing mandatory skills = 0 THEN THE Eligibility_Engine SHALL classify the internship as "Eligible"
4. WHEN match score is >= 50 AND missing mandatory skills <= 2 THEN THE Eligibility_Engine SHALL classify the internship as "Almost Eligible"
5. WHEN match score is < 50 OR missing mandatory skills > 2 THEN THE Eligibility_Engine SHALL classify the internship as "Not Eligible"
6. WHEN classification completes THEN THE System SHALL return three lists: eligible, almost eligible, and not eligible internships
7. WHEN an internship is classified as "Almost Eligible" THEN THE System SHALL include a list of missing skills with current and target proficiency levels
8. THE Eligibility_Engine SHALL ensure every internship appears in exactly one classification category

### Requirement 7: Match Score Calculation

**User Story:** As a student, I want to see a percentage match score for each internship, so that I can understand how close I am to being eligible.

#### Acceptance Criteria

1. WHEN calculating match score THEN THE Eligibility_Engine SHALL assign weights to each required skill based on importance
2. WHEN a student has a required skill THEN THE Eligibility_Engine SHALL calculate proficiency gap as (required level - student level)
3. WHEN proficiency gap <= 0 THEN THE Eligibility_Engine SHALL award full weight for that skill
4. WHEN proficiency gap is between 1 and 20 THEN THE Eligibility_Engine SHALL award partial credit proportional to the gap
5. WHEN proficiency gap > 20 THEN THE Eligibility_Engine SHALL award zero credit for that skill
6. WHEN a student lacks a required skill entirely THEN THE Eligibility_Engine SHALL award zero credit and mark it as missing
7. THE Eligibility_Engine SHALL calculate final match score as (achieved weight / total weight) * 100
8. THE Match_Score SHALL always be between 0 and 100 inclusive

### Requirement 8: AI Project Generation

**User Story:** As a student, I want the system to generate a personalized project roadmap for skills I'm missing, so that I have a clear path to improve my eligibility.

#### Acceptance Criteria

1. WHEN a student requests a project for specific skills THEN THE AI_Generator SHALL invoke Bedrock with target skills and student level
2. WHEN Bedrock generates a project THEN THE System SHALL parse the response into structured format with title, description, and milestones
3. WHEN a project is generated THEN THE System SHALL include at least 3 milestones with tasks and estimated hours
4. WHEN a project is generated THEN THE System SHALL include all requested target skills in the project specification
5. WHEN a project is generated THEN THE System SHALL store it in DynamoDB with status "suggested"
6. WHEN a project is generated THEN THE System SHALL include a tech stack with at least one technology
7. WHEN AI generation fails THEN THE System SHALL retry up to 3 times with exponential backoff
8. WHEN all retries fail THEN THE System SHALL return an error message to the student

### Requirement 9: Project Storage and Retrieval

**User Story:** As a student, I want to view my generated projects and track their status, so that I can manage my learning journey.

#### Acceptance Criteria

1. WHEN a student requests their projects THEN THE System SHALL return all projects associated with their user ID
2. WHEN a student requests a specific project THEN THE System SHALL return complete project details including milestones and resources
3. WHEN a student accepts a project THEN THE System SHALL update the project status to "accepted"
4. WHEN a student marks a project as in progress THEN THE System SHALL update the project status to "in_progress"
5. WHEN a student marks a project as complete THEN THE System SHALL update the project status to "completed"
6. THE System SHALL support filtering projects by status

### Requirement 10: Simulated Skill Verification

**User Story:** As a student, I want to mark projects as complete to increase my skill proficiency, so that I can unlock new internship opportunities.

#### Acceptance Criteria

1. WHEN a student marks a project as complete THEN THE System SHALL update all target skills in the project to proficiency level 70
2. WHEN a student marks a project as complete THEN THE System SHALL change skill status from "claimed" to "verified"
3. WHEN a student marks a project as complete THEN THE System SHALL set the verifiedAt timestamp to current time
4. WHEN skill proficiency is updated THEN THE System SHALL increment the verified skills count in the skill graph
5. WHEN skills are verified THEN THE System SHALL trigger re-classification of internships for that student
6. WHEN re-classification completes THEN THE System SHALL return newly eligible internships to the student

### Requirement 11: Eligibility Progression

**User Story:** As a student, I want my internship eligibility to improve automatically when I verify new skills, so that I can see my progress toward opportunities.

#### Acceptance Criteria

1. WHEN a student verifies skills that fill missing mandatory requirements THEN THE System SHALL reclassify affected internships
2. WHEN an internship moves from "Not Eligible" to "Almost Eligible" THEN THE System SHALL notify the student of the change
3. WHEN an internship moves from "Almost Eligible" to "Eligible" THEN THE System SHALL notify the student of the change
4. WHEN reclassification occurs THEN THE System SHALL recalculate match scores using updated skill proficiency levels
5. THE System SHALL ensure eligibility never regresses (skills cannot become unverified)

### Requirement 12: API Authentication and Authorization

**User Story:** As a developer, I want all API endpoints to be protected with JWT authentication, so that only authorized users can access their data.

#### Acceptance Criteria

1. WHEN a request is made to a protected endpoint THEN THE System SHALL validate the JWT token in the Authorization header
2. WHEN a JWT token is invalid or expired THEN THE System SHALL return 401 Unauthorized error
3. WHEN a JWT token is valid THEN THE System SHALL extract the user ID and role from the token
4. WHEN a student attempts to access another student's data THEN THE System SHALL return 403 Forbidden error
5. WHEN a request is made without an Authorization header THEN THE System SHALL return 401 Unauthorized error
6. THE System SHALL support only the "student" role for MVP (no admin role)

### Requirement 13: Data Persistence and Consistency

**User Story:** As a system operator, I want all data to be persisted reliably in DynamoDB, so that student progress is never lost.

#### Acceptance Criteria

1. WHEN a profile is created or updated THEN THE System SHALL persist changes to DynamoDB before returning success
2. WHEN a skill graph is modified THEN THE System SHALL update the lastUpdated timestamp
3. WHEN a project is generated THEN THE System SHALL assign a unique project ID and persist to DynamoDB
4. WHEN concurrent updates occur to the same record THEN THE System SHALL use optimistic locking to prevent data corruption
5. WHEN a database write fails THEN THE System SHALL return an error and not report success to the user
6. THE System SHALL ensure skill graph verified count always equals the number of skills with status "verified"

### Requirement 14: Resume File Storage

**User Story:** As a student, I want my resume to be stored securely, so that I can reference it later and the system can re-parse it if needed.

#### Acceptance Criteria

1. WHEN a resume is uploaded THEN THE System SHALL generate a unique S3 key using user ID and timestamp
2. WHEN a resume is stored in S3 THEN THE System SHALL enable server-side encryption
3. WHEN a resume is stored THEN THE System SHALL set appropriate access controls limiting access to the owning user
4. WHEN a resume upload succeeds THEN THE System SHALL store the S3 URI in the student's profile
5. WHEN a student requests their resume THEN THE System SHALL generate a pre-signed URL valid for 1 hour
6. THE System SHALL support PDF, DOCX, and TXT file formats

### Requirement 15: Error Handling and Resilience

**User Story:** As a student, I want the system to handle errors gracefully and provide clear error messages, so that I understand what went wrong and how to fix it.

#### Acceptance Criteria

1. WHEN an API request fails validation THEN THE System SHALL return 400 Bad Request with a descriptive error message
2. WHEN an authentication error occurs THEN THE System SHALL return 401 Unauthorized with the reason
3. WHEN a resource is not found THEN THE System SHALL return 404 Not Found with the resource type
4. WHEN an internal error occurs THEN THE System SHALL return 500 Internal Server Error and log the full error details
5. WHEN an external service (Bedrock, S3) fails THEN THE System SHALL retry with exponential backoff up to 3 times
6. WHEN all retries are exhausted THEN THE System SHALL return 503 Service Unavailable with a retry-after suggestion
7. THE System SHALL log all errors to CloudWatch with request context for debugging

### Requirement 16: Performance and Scalability

**User Story:** As a system operator, I want the system to respond quickly and handle multiple concurrent users, so that the demo is smooth and responsive.

#### Acceptance Criteria

1. WHEN a student requests their profile THEN THE System SHALL respond within 300ms at p95
2. WHEN a student requests internship classification THEN THE System SHALL respond within 2000ms at p95 for up to 100 internships
3. WHEN a student uploads a resume THEN THE System SHALL complete the upload within 5000ms at p95
4. WHEN AI project generation is requested THEN THE System SHALL respond within 10000ms at p95
5. WHEN skill verification occurs THEN THE System SHALL complete re-classification within 3000ms at p95
6. THE System SHALL support at least 100 concurrent users without degradation
7. THE System SHALL use Lambda provisioned concurrency for critical endpoints to minimize cold starts

### Requirement 17: Security and Data Protection

**User Story:** As a student, I want my personal data and resume to be protected, so that my information remains private and secure.

#### Acceptance Criteria

1. WHEN data is transmitted THEN THE System SHALL use HTTPS/TLS 1.2 or higher for all communication
2. WHEN a resume is stored in S3 THEN THE System SHALL enable server-side encryption
3. WHEN data is stored in DynamoDB THEN THE System SHALL enable encryption at rest
4. WHEN a JWT token is issued THEN THE System SHALL set expiration to 1 hour for access tokens
5. WHEN a password is provided THEN THE System SHALL enforce minimum 8 characters with uppercase, lowercase, number, and special character
6. THE System SHALL not log sensitive data (passwords, tokens) to CloudWatch
7. THE System SHALL implement rate limiting of 1000 requests per minute per user

### Requirement 18: Monitoring and Observability

**User Story:** As a system operator, I want to monitor system health and performance, so that I can identify and fix issues quickly.

#### Acceptance Criteria

1. WHEN an API request is processed THEN THE System SHALL log the request method, path, status code, and duration to CloudWatch
2. WHEN an error occurs THEN THE System SHALL log the full error stack trace and request context
3. WHEN Lambda functions execute THEN THE System SHALL emit custom metrics for business operations (signups, classifications, projects generated)
4. WHEN API latency exceeds thresholds THEN THE System SHALL trigger CloudWatch alarms
5. WHEN error rate exceeds 5% THEN THE System SHALL trigger CloudWatch alarms
6. THE System SHALL use X-Ray for distributed tracing across Lambda functions

## Non-Functional Requirements

### NFR-1: Availability
THE System SHALL maintain 99% uptime during business hours (9 AM - 9 PM IST) for the MVP period.

### NFR-2: Scalability
THE System SHALL automatically scale to handle up to 1000 concurrent users using AWS Lambda auto-scaling.

### NFR-3: Maintainability
THE System SHALL use TypeScript for type safety and include inline documentation for all public functions.

### NFR-4: Cost Efficiency
THE System SHALL optimize AWS costs by using serverless pay-per-use pricing and staying within $100/month budget for MVP.

### NFR-5: Deployment Speed
THE System SHALL support deployment of backend and frontend changes within 10 minutes using CI/CD pipelines.

### NFR-6: Data Retention
THE System SHALL retain all student data indefinitely unless the student requests account deletion.

### NFR-7: Browser Compatibility
THE System SHALL support the latest versions of Chrome, Firefox, Safari, and Edge browsers.

### NFR-8: Mobile Responsiveness
THE System SHALL provide a responsive UI that works on mobile devices with screen widths down to 375px.

### NFR-9: Accessibility
THE System SHALL follow WCAG 2.1 Level AA guidelines for basic accessibility compliance.

### NFR-10: API Documentation
THE System SHALL provide OpenAPI/Swagger documentation for all REST API endpoints.
