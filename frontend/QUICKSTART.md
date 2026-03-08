# Eligify Frontend - Quick Start Guide

## 🚀 Get Running in 2 Minutes

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Start Development Server
```bash
npm run dev
```

### Step 3: Open Browser
Navigate to: **http://localhost:3000**

That's it! The app is running with mock data. 🎉

---

## 🎮 Try These Features

### 1. Create an Account
1. Go to `/auth/signup`
2. Enter any name, email, and password (8+ chars with uppercase, lowercase, number, special char)
3. Click "Create Account"
4. You'll be redirected to sign in

**Note**: The app now validates credentials! You must create an account before signing in.

**Pre-created test account:**
- Email: `test@example.com`
- Password: `Test@123`

### 2. Sign In
1. Use the email and password you just created (or use the test account above)
2. Click "Sign In"
3. ✅ **Correct credentials**: You'll see the dashboard
4. ❌ **Wrong credentials**: You'll see an error message

### 3. View Your Profile
1. Click "Profile" in the header
2. See mock profile data (Rahul Kumar)
3. Scroll down to see skills

### 4. Upload a Resume (Simulated)
1. On Profile page, find "Upload Resume" section
2. Drag a file or click to browse
3. Upload any PDF/DOCX/TXT file
4. Wait 2 seconds for "AI extraction" (mocked)
5. See success notification

### 5. Add a Skill Manually
1. On Profile page, scroll to "Your Skills"
2. Click "Add Skill" button
3. Enter skill name (e.g., "TypeScript")
4. Select category
5. Set proficiency level
6. Click "Add Skill"

### 6. Browse Internships
1. Click "Internships" in header
2. See three tabs:
   - **Eligible** (green) - You qualify!
   - **Almost Eligible** (yellow) - Close!
   - **Not Eligible** (gray) - Need more skills
3. Click any internship card to see details
4. View match score and skill gaps

### 7. Generate a Learning Project
1. From internship details, click "Generate Learning Project"
   OR
2. Go to "Projects" page and click "Generate Project"
3. Enter skills to learn (e.g., "PostgreSQL, SQL")
4. Select experience level
5. Click "Generate Project"
6. Wait 3 seconds for AI generation (mocked)
7. See your personalized project roadmap!

### 8. Complete a Project
1. On Projects page, click a project card
2. Click "Accept Project"
3. Click "Start Working"
4. Click "Mark as Complete"
5. Confirm completion
6. See success notification with verified skills!

---

## 🎨 What You'll See

### Dashboard
- Total skills count
- Verified skills count
- Eligible internships count
- Quick action cards

### Profile
- Personal information
- Education history
- Work experience
- Resume upload
- Skill graph with filters

### Internships
- Three-tab classification
- Match score visualization
- Search and filters
- Detailed skill gap analysis

### Projects
- AI-generated roadmaps
- Milestones with tasks
- Tech stack recommendations
- Learning resources
- Status tracking

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Or use a different port
npm run dev -- -p 3001
```

### Dependencies Not Installing
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### TypeScript Errors
```bash
# Restart TypeScript server in VS Code
Cmd/Ctrl + Shift + P → "TypeScript: Restart TS Server"
```

---

## 📱 Test Responsive Design

### Desktop
- Open browser normally
- See full layout with sidebar

### Tablet
- Open DevTools (F12)
- Toggle device toolbar
- Select iPad or similar
- See two-column layout

### Mobile
- Select iPhone or similar
- See single-column layout
- Test hamburger menu

---

## 🎯 Key Features to Test

✅ Form validation (try invalid emails, weak passwords)
✅ Loading states (watch spinners during API calls)
✅ Error handling (check console for errors)
✅ Toast notifications (see success/error messages)
✅ Modal dialogs (click outside to close)
✅ Responsive design (resize browser window)
✅ Navigation (use header links)
✅ Protected routes (try accessing /dashboard without login)

---

## 🔄 Mock API Behavior

All API calls are intercepted and return mock data:
- **Sign up**: Always succeeds, creates mock user
- **Sign in**: Always succeeds with any credentials
- **Resume upload**: Simulates 2-second upload + extraction
- **Skill addition**: Instantly adds to mock skill graph
- **Internship classification**: Returns 3 pre-classified internships
- **Project generation**: Simulates 3-second AI generation
- **Project completion**: Instantly verifies skills

---

## 🚀 Next Steps

1. **Explore all pages** - Click through every feature
2. **Test edge cases** - Try invalid inputs, empty states
3. **Check mobile view** - Ensure responsive design works
4. **Review code** - Look at component structure
5. **Connect backend** - When ready, update `.env.local`

---

## 💡 Tips

- **Auto-save**: Forms validate on blur
- **Keyboard shortcuts**: Tab through forms
- **Search**: Use Cmd/Ctrl + K in internships
- **Filters**: Combine search + type filters
- **Modals**: Click outside or press Escape to close
- **Notifications**: Auto-dismiss after 5 seconds

---

## 📞 Need Help?

Check these files:
- `README.md` - Full documentation
- `IMPLEMENTATION_SUMMARY.md` - What's built
- `lib/mockData.ts` - Mock data structure
- `hooks/` - Custom hooks documentation

---

Enjoy exploring Eligify! 🎉
