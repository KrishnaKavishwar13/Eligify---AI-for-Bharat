# 🤖 Kiro Prompts for Your Teammate

**Purpose**: Exact prompts to give Kiro for getting started and working on tasks  
**Role-Specific**: Different prompts for Backend vs Frontend developer

---

## 🎯 Initial Setup Prompt (First Time)

### For Backend/AI Developer

```
I'm joining the Eligify MVP project as the backend/AI developer. I need to understand the current state and start working on my tasks.

Please read these files to understand the project:
- TEAM_HANDOFF_BACKEND.md
- TEAM_COORDINATION_GUIDE.md
- DEMO_SUCCESS_REPORT.md
- .kiro/specs/eligify-platform/tasks.md

Then help me:
1. Understand what's already complete
2. Understand my first task (Task 6.1-6.2: Eligibility Engine)
3. Get started with implementing the match score calculation algorithm

My focus areas are:
- Python FastAPI backend
- Ollama AI integration
- Eligibility engine (deterministic matching)
- Database layer (mock store)
```

---

### For Frontend Developer

```
I'm joining the Eligify MVP project as the frontend developer. I need to understand the current state and start working on my tasks.

Please read these files to understand the project:
- TEAM_HANDOFF_FRONTEND.md
- TEAM_COORDINATION_GUIDE.md
- FRONTEND_STRUCTURE.md
- .kiro/specs/eligify-platform/tasks.md

Then help me:
1. Understand what's already complete
2. Understand my first task (Task 12.3: Skill Graph Component)
3. Get started with building the skill graph visualization component

My focus areas are:
- React/Next.js 14 frontend
- UI components with Tailwind CSS
- API integration
- Responsive design
```

---

## 🚀 Starting First Task

### Backend Developer - Task 6.1-6.2 (Eligibility Engine)

```
I'm ready to start Task 6.1-6.2: Implement the Eligibility Engine.

Please help me implement the match score calculation algorithm in backend/src/services/eligibility_service.py.

According to the design document, I need to:
1. Implement calculateMatchScore(studentSkills, internship) that:
   - Compares student proficiency vs required proficiency for each skill
   - Awards full credit if proficiency gap <= 0
   - Awards partial credit if gap between 1-20: credit = weight * (1 - gap/100)
   - Awards zero credit if gap > 20 or skill missing
   - Calculates final score: (achievedWeight / totalWeight) * 100

2. Implement classifyInternships(userId) that:
   - Fetches student's skill graph
   - Fetches all active internships
   - Calculates match score for each internship
   - Classifies as "Eligible" if score >= 80 AND missing mandatory = 0
   - Classifies as "Almost Eligible" if score >= 50 AND missing mandatory <= 2
   - Classifies as "Not Eligible" otherwise
   - Sorts each category by match score descending

Please read the design document and help me implement this.
```

---

### Frontend Developer - Task 12.3 (Skill Graph Component)

```
I'm ready to start Task 12.3: Build the Skill Graph Visualization Component.

Please help me create frontend/components/SkillGraph.tsx.

According to the requirements, I need to build a component that:
1. Displays skills as cards or list
2. Shows skill name, category, proficiency level (0-100%), verification status
3. Uses color coding:
   - Gray for "claimed" skills
   - Yellow for "in_progress" skills
   - Green for "verified" skills
4. Has filters by category (programming_language, framework, tool, soft_skill)
5. Has filters by status (claimed, in_progress, verified)
6. Has an "Add Skill" button
7. Uses responsive grid layout
8. Follows the design system (purple/pink gradients, warm colors)

The component should fetch data from GET /skills endpoint and display it.

Please help me implement this component.
```

---

## 🔄 Continuing Work (Subsequent Tasks)

### Backend Developer - Next Tasks

**Task 8.2: Project Storage**
```
I've completed the eligibility engine. Now I need to work on Task 8.2: Project Storage & Retrieval.

Please help me implement the following in backend/src/services/project_service.py:
1. saveProject(project) - store with unique projectId
2. getProject(projectId) - fetch from Projects table
3. getUserProjects(userId, status?) - query by userId with optional status filter
4. updateProjectStatus(projectId, status) - update status and timestamp

The project storage should use the mock_store and be DynamoDB-ready.
```

**Task 17.1-17.2: Error Handling**
```
I need to implement comprehensive error handling across the backend.

Please help me:
1. Add try-catch blocks to all Lambda handlers
2. Map errors to appropriate HTTP status codes (400, 401, 403, 404, 500, 503)
3. Return standardized error response: { success: false, error: { code, message, details } }
4. Add exponential backoff retry for Ollama API calls (3 attempts)
5. Add exponential backoff retry for S3 operations (3 attempts)
6. Add exponential backoff retry for DynamoDB operations (3 attempts)

Start with the auth handlers and then move to other handlers.
```

---

### Frontend Developer - Next Tasks

**Task 12.4: Skill Addition Modal**
```
I've completed the skill graph component. Now I need to work on Task 12.4: Skill Addition Modal.

Please help me create frontend/components/AddSkillModal.tsx.

The modal should:
1. Have a modal overlay with backdrop
2. Have a form with:
   - Skill name input (text)
   - Category dropdown (programming_language, framework, tool, soft_skill)
   - Proficiency slider (0-100%)
3. Validate that skill name is required
4. Have "Add Skill" and "Cancel" buttons
5. Close on backdrop click or ESC key
6. Call POST /skills API endpoint
7. Show success/error messages

Please implement this modal component.
```

**Task 13.2: Internship Card Component**
```
I need to build the Internship Card Component (Task 13.2).

Please help me create frontend/components/InternshipCard.tsx.

The card should display:
1. Title, company, location, type (remote/onsite/hybrid)
2. Stipend amount
3. Match score as progress bar or percentage badge
4. Color coding based on category:
   - Green for "eligible" (score >= 80%)
   - Yellow for "almostEligible" (score >= 50%)
   - Gray for "notEligible" (score < 50%)
5. "View Details" button
6. Hover effects (lift, shadow)
7. Responsive design

Use the existing Card.tsx component as a base and follow the design system.
```

**Task 13.3: Internship Detail Modal**
```
I need to build the Internship Detail Modal (Task 13.3).

Please help me create frontend/components/InternshipDetailModal.tsx.

The modal should show:
1. Full internship information (title, company, location, type, duration, stipend)
2. Description (full text)
3. Required skills with proficiency levels
4. Preferred skills
5. Deadline, application URL
6. Matched skills section (green checkmarks)
7. Missing skills section (red X) with proficiency gaps
   - Show: "You have 40%, need 70%" for each missing skill
8. "Generate Project" button for missing skills
9. "Apply Now" button (opens application URL)
10. Close button and backdrop click to close

The modal should fetch data from GET /internships/:id and GET /skills endpoints.
```

**Task 14.1: Project Generation Modal**
```
I need to build the Project Generation Modal (Task 14.1).

Please help me create frontend/components/ProjectGenerationModal.tsx.

The modal should have:
1. Form with:
   - Target skills multi-select (checkboxes or tags)
   - Student level dropdown (beginner, intermediate, advanced)
   - Time commitment input (optional)
2. "Generate Project" button
3. Loading state during AI generation (15-30 seconds)
   - Show spinner and "AI is creating your project..." message
4. Generated project preview:
   - Title, description
   - Objectives (bullet list)
   - Milestones with estimated hours
   - Tech stack
   - Estimated duration, difficulty
5. "Accept Project" and "Regenerate" buttons
6. Close button

The modal should call POST /copilot/generate-project endpoint.
```

**Task 14.3: Project Detail Page**
```
I need to build the Project Detail Page (Task 14.3).

Please help me create frontend/app/projects/[id]/page.tsx.

The page should show:
1. Project header (title, difficulty badge, status badge, target skills as tags, estimated duration)
2. Description section
3. Objectives section (numbered list)
4. Tech stack section (icon grid or list)
5. Milestones section:
   - Expandable/collapsible milestones
   - Tasks as checkboxes (for in-progress projects)
   - Estimated hours per milestone
   - Progress indicator (which milestone is current)
6. Action buttons:
   - "Mark as In Progress" (for suggested projects)
   - "Mark as Complete" (for in-progress projects)
   - "Back to Projects" button
7. Completion confirmation modal

The page should fetch data from GET /projects/:id and handle PUT /projects/:id/status and POST /projects/:id/complete endpoints.
```

---

## 🐛 Debugging & Help

### When Stuck on Implementation

```
I'm stuck on [specific issue]. Here's what I'm trying to do:
[Describe the task]

Here's what I've tried:
[Describe attempts]

Here's the error I'm getting:
[Paste error message]

Please help me debug this issue.
```

---

### When Need to Understand Existing Code

```
I need to understand how [specific feature] works in the existing codebase.

Please explain:
1. Which files are involved
2. How the data flows
3. What the key functions/components do
4. How I should integrate my new code with this

Specifically, I'm looking at [file path] and need to understand [specific part].
```

---

### When Need API Documentation

```
I need to understand the API endpoint [endpoint name].

Please explain:
1. What data it expects (request format)
2. What data it returns (response format)
3. What authentication is required
4. Any error cases I should handle
5. Example request/response

I'm working on [task description] and need to integrate with this endpoint.
```

---

## 🧪 Testing Prompts

### Backend Testing

```
I've implemented [feature name]. Please help me:
1. Write tests for this feature
2. Run the existing test suite to make sure I didn't break anything
3. Test the API endpoint manually

The feature is in [file path] and the endpoint is [endpoint].
```

---

### Frontend Testing

```
I've built [component name]. Please help me:
1. Test the component manually in the browser
2. Check if it follows the design system
3. Verify it's responsive on mobile and desktop
4. Test the API integration

The component is in [file path].
```

---

## 🔄 Integration Testing

### Testing with Backend

```
I need to test my frontend component with the backend API.

Please help me:
1. Verify the backend is running
2. Test the API endpoint [endpoint] with the correct data
3. Debug any CORS or authentication issues
4. Verify the response format matches what my component expects

My component is [component name] and it calls [endpoint].
```

---

### Testing with Frontend

```
I need to test my backend endpoint with the frontend.

Please help me:
1. Verify the endpoint returns the correct data format
2. Test with the frontend component
3. Debug any serialization issues (camelCase vs snake_case)
4. Verify error handling works correctly

My endpoint is [endpoint] and it's called by [component name].
```

---

## 📝 Code Review Prompts

### Before Committing

```
I've completed [task name]. Before I commit, please:
1. Review my code for any issues
2. Check if I followed the coding standards
3. Verify error handling is implemented
4. Check if I updated the tasks.md file
5. Suggest any improvements

The changes are in [file paths].
```

---

### After Completing Task

```
I've completed Task [X.X]: [task name].

Please help me:
1. Mark the task as complete in .kiro/specs/eligify-platform/tasks.md
2. Verify all acceptance criteria are met
3. Prepare a summary for the team update
4. Suggest what task I should work on next

The implementation is in [file paths].
```

---

## 🎯 Daily Workflow Prompts

### Starting the Day

```
Good morning! I'm ready to continue working on the Eligify project.

Please remind me:
1. What task I was working on yesterday
2. What I completed
3. What's left to do on the current task
4. Any blockers or issues I should be aware of

Then help me continue where I left off.
```

---

### End of Day

```
I'm wrapping up for the day. Please help me:
1. Summarize what I completed today
2. Note any blockers or issues
3. Prepare an update for the team channel
4. Suggest what I should work on tomorrow

Format the update as:
✅ Completed: [tasks]
🚧 In Progress: [tasks]
⏳ Next: [tasks]
```

---

## 💡 Tips for Using Kiro

### Be Specific
❌ "Help me build the component"
✅ "Help me build the SkillGraph component in frontend/components/SkillGraph.tsx that displays skills with proficiency bars and filters"

### Provide Context
❌ "This isn't working"
✅ "I'm implementing Task 12.3 (Skill Graph). The API call to GET /skills is returning 401. Here's my code: [paste code]"

### Reference Documentation
❌ "How do I do this?"
✅ "According to TEAM_HANDOFF_FRONTEND.md, I need to build a skill graph component. Please help me implement it following the specifications in that document"

### Ask for Explanations
❌ "Write the code"
✅ "Please explain how this should work first, then help me implement it step by step"

---

## 🚀 Quick Reference

### Backend Developer First Prompt
```
I'm the backend developer for Eligify MVP. Read TEAM_HANDOFF_BACKEND.md and help me start Task 6.1-6.2: Eligibility Engine.
```

### Frontend Developer First Prompt
```
I'm the frontend developer for Eligify MVP. Read TEAM_HANDOFF_FRONTEND.md and help me start Task 12.3: Skill Graph Component.
```

### When Stuck
```
I'm stuck on [issue]. I've tried [attempts]. Error: [error message]. Please help debug.
```

### When Done with Task
```
Completed Task [X.X]. Please mark it complete in tasks.md and suggest next task.
```

---

**Last Updated**: January 2025  
**Purpose**: Help teammate work effectively with Kiro  
**Tip**: Always reference the handoff documents for context!
