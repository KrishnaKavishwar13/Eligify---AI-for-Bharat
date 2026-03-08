# 🧪 Eligify - Complete Testing Flows

## 🎯 Flow 1: New User Complete Journey (Start Here!)

### Test User for Flow 1
- **Name**: Priya Sharma
- **Email**: priya.sharma@example.com  
- **Password**: Priya@2026

### Steps to Test

#### ✅ Step 1: Landing Page
1. Open: http://localhost:3000/landing
2. **Check**: Purple-pink-orange gradient displays
3. **Check**: Hero section with "Eligify" title
4. **Check**: Features section visible
5. **Click**: "Get Started" button
6. **Expected**: Redirects to signup page

#### ✅ Step 2: Signup
1. **Fill form**:
   - Name: Priya Sharma
   - Email: priya.sharma@example.com
   - Password: Priya@2026
2. **Click**: "Sign Up"
3. **Expected**: 
   - Success message appears
   - Redirects to signin page
   - No errors in console

#### ✅ Step 3: Signin
1. **Fill form**:
   - Email: priya.sharma@example.com
   - Password: Priya@2026
2. **Click**: "Sign In"
3. **Expected**:
   - Redirects to dashboard
   - No errors

#### ✅ Step 4: Dashboard First View
1. **Check displays**:
   - Welcome message: "Welcome back, Priya!"
   - Total Skills: 7
   - Verified Skills: 5
   - Eligible Internships: (number)
   - Almost Eligible: (number)
2. **Check**: Quick action cards visible
3. **Test**: Refresh page (Ctrl+R)
4. **Expected**: Stays on dashboard (doesn't redirect to signin)

#### ✅ Step 5: View Skills
1. **Click**: "Total Skills" stat card
2. **Expected**: Goes to Profile page
3. **Check**: Skills section shows 7 default skills:
   - Python (70%)
   - JavaScript (65%)
   - React (60%)
   - FastAPI (55%)
   - SQL (50%)
   - Git (65%)
   - Communication (70%)

#### ✅ Step 6: Browse Internships
1. **Click**: "Browse Internships" or Internships link
2. **Check tabs**: Eligible, Almost Eligible, Not Eligible
3. **Check**: At least 1-2 internships in "Eligible" tab
4. **Click**: First internship card
5. **Expected**: Modal opens with full details
6. **Check modal shows**:
   - Company and title
   - Description
   - Required skills
   - Match score
   - Stipend
   - Location
7. **Click**: Close modal
8. **Click**: "Almost Eligible" tab
9. **Check**: Shows internships with missing skills
10. **Check**: Missing skills section displays in red

#### ✅ Step 7: Add New Skill
1. **Go to**: Profile page
2. **Scroll to**: Skills section
3. **Click**: "Add Skill" button
4. **Fill form**:
   - Skill Name: Docker
   - Category: Tool
   - Proficiency: 60
5. **Click**: "Add Skill"
6. **Expected**: 
   - Skill appears in list
   - Total skills: 8
   - Success notification

#### ✅ Step 8: Check Updated Matches
1. **Go to**: Internships page
2. **Expected**: Some internships moved from "Almost Eligible" to "Eligible"
3. **Check**: Match scores updated
4. **Check**: Missing skills list updated

---

## 🎯 Flow 2: AI-Powered Skill Building (Advanced)

### Test User for Flow 2
- **Email**: rudradewatwal@gmail.com
- **Password**: Password@123
- **Note**: This user has complete profile with 15 skills

### Steps to Test

#### ✅ Step 1: Signin as Existing User
1. **Signout** if logged in as Priya
2. **Signin** with Rudra's credentials
3. **Expected**: Dashboard shows full profile data

#### ✅ Step 2: View Complete Profile
1. **Go to**: Profile page
2. **Check displays**:
   - Personal info: Phone, location, LinkedIn, GitHub, portfolio
   - Education: 2 entries (IIT Mumbai, DPS)
   - Experience: 1 entry (TechStart India)
   - Projects: 2 entries (E-Commerce, Task Manager)
   - Certifications: 1 entry (AWS)
   - Skills: 15 skills with high proficiency

#### ✅ Step 3: Find Skill Gap
1. **Go to**: Internships page
2. **Click**: "Almost Eligible" tab
3. **Find**: Internship requiring Docker/Kubernetes
4. **Click**: Card to open modal
5. **Check**: Missing skills section shows Docker
6. **Click**: "Learn Docker" button (if available)
7. **Expected**: Redirects to SkillGenie

#### ✅ Step 4: SkillGenie - Start Learning
1. **Check displays**:
   - Skill name in header: "Docker"
   - 3-step journey visualization
   - Step 1 (Assessment) is current
   - Assessment details: 5 questions, 10 min, 60% pass
2. **Click**: "Start Assessment" button
3. **Expected**: Goes to assessment page

#### ✅ Step 5: Take Assessment (Optional - if implemented)
1. **Check**: Questions display
2. **Answer**: Questions
3. **Submit**: Assessment
4. **Expected**: Shows results and next step

#### ✅ Step 6: Generate AI Project
1. **Go to**: Projects page
2. **Click**: "Generate Project" button
3. **Fill form**:
   - Target Skills: Docker, Kubernetes
   - Student Level: Intermediate
4. **Click**: "Generate Project with AI"
5. **Expected**: 
   - Loading spinner appears
   - Message: "This may take 60 seconds"
   - Project generates (or shows error if Ollama slow)

#### ✅ Step 7: View Project Details
1. **Check project shows**:
   - Title: (AI-generated)
   - Description: (AI-generated)
   - Objectives: 3-5 bullet points
   - Tech Stack: List of technologies
   - Milestones: 3 phases with tasks
   - Estimated duration: 1-2 weeks
2. **Click**: "Accept Project"
3. **Expected**: Status changes to "In Progress"

#### ✅ Step 8: Track Progress (Mock)
1. **View**: Project detail page
2. **Check**: Progress bar at 0%
3. **Check**: Milestone checklist
4. **Mock**: Mark first milestone as complete
5. **Expected**: Progress bar updates

#### ✅ Step 9: Submit Project
1. **Mock**: Mark all milestones complete
2. **Click**: "Submit for Verification"
3. **Fill form**:
   - GitHub URL: https://github.com/rudradewatwal/docker-project
   - Description: Completed all milestones
4. **Click**: "Submit"
5. **Expected**: 
   - Verification starts
   - Shows loading state
   - (If AI slow, may timeout - that's okay for testing)

---

## 🐛 Bug Tracking Template

### Issue Report Format
```
Feature: [e.g., Internships Page]
Step: [e.g., Step 6 - Browse Internships]
Issue: [e.g., Modal doesn't open on card click]
Expected: [e.g., Modal should open with full details]
Actual: [e.g., Nothing happens, console shows error]
Console Error: [paste error if any]
Priority: High/Medium/Low
```

---

## ✅ Success Criteria

### Flow 1 Success
- [ ] Signup works without errors
- [ ] Signin works and persists on refresh
- [ ] Dashboard shows correct stats
- [ ] Profile displays default data
- [ ] Internships load and classify correctly
- [ ] Can add new skill
- [ ] Match scores update after adding skill

### Flow 2 Success
- [ ] Existing user profile shows all data
- [ ] Can identify skill gaps
- [ ] SkillGenie flow is clear
- [ ] Project generation works (or shows proper loading)
- [ ] Can accept and track projects
- [ ] Can submit for verification

---

## 🎬 Ready to Test!

**Start with Flow 1**:
1. Open http://localhost:3000/landing
2. Go through each step
3. Note any issues
4. Report back what works and what doesn't

**I'll fix issues immediately as you find them!**

---

## 💡 Quick Fixes I Can Do

- UI not displaying correctly → Fix CSS/layout
- Data not showing → Fix API/data structure
- Errors on page → Fix undefined/null checks
- Features not working → Fix logic/handlers
- Performance issues → Add loading states
- Missing features → Implement quickly

**Let's test Flow 1 now!** 🚀
