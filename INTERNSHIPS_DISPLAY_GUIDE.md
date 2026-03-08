# Internships Display Guide

## Current Status

✅ **26 Internships Available** in `backend/data/internships.json`

### Breakdown by Company Type:
- **FAANG** (5): Google, Microsoft, Amazon, NVIDIA, Atlassian
- **Top MNC** (3): Salesforce, Accenture, Bosch  
- **Unicorn** (10): Flipkart, Swiggy, Zomato, Paytm, Ola, PhonePe, Razorpay, Freshworks, Myntra, Polygon
- **Startup** (2): Dream11, Unacademy
- **Enterprise** (6): Jio, Infosys, Wipro, TCS

---

## How Internships Display Works

### For New Users (0 Skills):
1. **Sign up** → Empty skill graph (totalSkills: 0)
2. **Go to Internships page** → `/internships`
3. **See tabs:**
   - Eligible: 0 internships
   - Almost Eligible: 0 internships
   - **Not Eligible: 26 internships** ✅

**This is correct!** New users with no skills won't be eligible for any internships yet.

### After Resume Upload:
1. **Upload resume** → AI extracts 10-15 skills
2. **Go to Internships page** → `/internships`
3. **See tabs:**
   - **Eligible: 5-10 internships** (80%+ match, 0 missing mandatory skills)
   - **Almost Eligible: 5-8 internships** (50%+ match, ≤2 missing mandatory skills)
   - **Not Eligible: 8-13 internships** (remaining)

---

## Eligibility Calculation Logic

### Match Score Formula:
```
matchScore = (achievedWeight / totalWeight) * 100
```

### Classification Thresholds:
1. **Eligible**: matchScore ≥ 80% AND 0 missing mandatory skills
2. **Almost Eligible**: matchScore ≥ 50% AND ≤ 2 missing mandatory skills
3. **Not Eligible**: Everything else

### Proficiency Matching:
- **Full credit**: User proficiency ≥ required proficiency
- **Partial credit**: User proficiency within 20 points of required
- **No credit**: User proficiency > 20 points below required OR skill missing

---

## Why Internships Might Not Show

### Issue 1: Not Logged In
**Symptom:** Blank page or error
**Solution:** Login with credentials

### Issue 2: No Skills Yet
**Symptom:** All 26 internships in "Not Eligible" tab
**Solution:** This is correct! Upload resume to get skills

### Issue 3: API Error
**Symptom:** Loading forever or error message
**Solution:** Check backend logs, ensure servers running

### Issue 4: Frontend Not Fetching
**Symptom:** Tabs show 0/0/0 counts
**Solution:** Check browser console for errors

---

## Testing the Flow

### Test 1: New User (No Skills)
```
1. Sign up with new account
2. Go to /internships
3. Click "Not Eligible" tab
4. Should see all 26 internships
```

### Test 2: After Resume Upload
```
1. Go to /profile
2. Upload resume (with Python, JavaScript, React skills)
3. Wait for AI extraction
4. Go to /internships
5. Should see:
   - Eligible: 5-8 internships (Flipkart, Wipro, TCS, etc.)
   - Almost Eligible: 6-10 internships (Google, Microsoft if missing 1-2 skills)
   - Not Eligible: Remaining
```

### Test 3: Existing User (rudradewatwal@gmail.com)
```
1. Login with test credentials
2. Go to /internships
3. Should see internships distributed across tabs based on skills
```

---

## Current Internship Dataset (26 Total)

### FAANG (5 internships):
1. **Google** - Software Engineering (Python, DS&A, System Design)
2. **Microsoft** - Full Stack (React, JavaScript, Node.js, SQL)
3. **Amazon** - Data Science (Python, ML, Statistics, Pandas)
4. **NVIDIA** - AI Research (Python, Deep Learning, PyTorch)
5. **Atlassian** - TypeScript Developer (TypeScript, React, Node.js)

### Top MNC (3 internships):
6. **Salesforce** - QA Automation (Selenium, Java, Testing)
7. **Accenture** - Business Analyst (Data Analysis, Excel, SQL)
8. **Bosch** - IoT Developer (IoT, Embedded Systems, C++)

### Unicorn (10 internships):
9. **Flipkart** - Frontend Developer (React, JavaScript, HTML, CSS)
10. **Swiggy** - Backend Developer (Java, Spring Boot, Microservices)
11. **Zomato** - Mobile App Developer (React Native, JavaScript)
12. **Zomato** - Python Backend (Python, FastAPI, SQL)
13. **Paytm** - DevOps (Linux, Docker, Kubernetes, CI/CD)
14. **Ola** - Machine Learning (Python, ML, Deep Learning)
15. **PhonePe** - Product Management (PM, Data Analysis, SQL)
16. **Razorpay** - UI/UX Design (Figma, UI/UX, Prototyping)
17. **Razorpay** - Full Stack JavaScript (JavaScript, React, Node.js)
18. **Freshworks** - Cloud Engineer (AWS, Python, Terraform)
19. **Myntra** - Data Analyst (SQL, Excel, Data Visualization)
20. **Polygon** - Blockchain Developer (Solidity, Blockchain, Web3)

### Startup (2 internships):
21. **Dream11** - Game Developer (Unity, C#, Game Development)
22. **Unacademy** - Content Writer (Content Writing, Communication)

### Enterprise (6 internships):
23. **Jio** - Cybersecurity (Cybersecurity, Networking, Linux)
24. **Infosys** - Web Developer (HTML, CSS, JavaScript, React)
25. **Wipro** - React Developer (React, JavaScript, HTML, CSS)
26. **TCS** - Junior Web Developer (HTML, CSS, JavaScript)

---

## Expanding the Dataset (Optional)

If you want to add more internships, here's what to add:

### More FAANG (add 5):
- Meta - Frontend Engineer
- Apple - iOS Developer
- Netflix - Backend Engineer
- Adobe - Creative Cloud Developer
- Intel - Hardware Engineer

### More Unicorns (add 5):
- CRED - Product Designer
- Meesho - Growth Analyst
- Urban Company - Operations Intern
- Byju's - EdTech Developer
- Zerodha - Trading Platform Developer

### More Startups (add 5):
- Razorpay - Payment Gateway Developer
- Dunzo - Logistics Engineer
- Licious - Supply Chain Analyst
- Nykaa - E-commerce Developer
- Groww - Fintech Developer

---

## Quick Fix: If Internships Not Showing

### Step 1: Check Backend
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check internships endpoint (requires auth)
# Login first to get token, then:
curl http://localhost:8000/internships
```

### Step 2: Check Frontend
```
1. Open browser console (F12)
2. Go to /internships page
3. Check Network tab for API calls
4. Look for errors in Console tab
```

### Step 3: Check Authentication
```
1. Ensure you're logged in
2. Check localStorage for auth token
3. Token should be valid (not expired)
```

### Step 4: Check User Skills
```
1. Go to /profile
2. Check if skills are loaded
3. If 0 skills, all internships will be "Not Eligible"
4. Upload resume to get skills
```

---

## Expected Behavior Summary

| User State | Eligible | Almost Eligible | Not Eligible |
|------------|----------|-----------------|--------------|
| **New User (0 skills)** | 0 | 0 | 26 |
| **After Resume (10-15 skills)** | 5-10 | 5-8 | 8-13 |
| **Experienced (20+ skills)** | 12-18 | 5-8 | 0-6 |

---

## Demo Script

For video demo, follow this flow:

1. **Show New User:**
   - "New users see all 26 internships in Not Eligible tab"
   - "This shows them what's available"

2. **Upload Resume:**
   - "AI extracts skills in seconds"
   - "Watch the magic happen"

3. **Show Classification:**
   - "Now eligible for 8 internships immediately"
   - "6 more are just 1-2 skills away"
   - "Clear path to unlock opportunities"

4. **Click Almost Eligible:**
   - "See exactly which skills are missing"
   - "Click 'Unlock with SkillGenie' to start learning"

---

**The system is working correctly! New users with 0 skills will see all internships in "Not Eligible" tab, which is the expected behavior.**
