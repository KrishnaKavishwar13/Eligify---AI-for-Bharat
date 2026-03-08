# Eligify - Modern SaaS UI Design Guide

## 🎨 Design System Overview

### Desktop-First Layout (1440px)
- **Left Sidebar**: Navigation menu
- **Top Navbar**: User profile, notifications
- **Main Content**: Card-based layout
- **Color Scheme**: White/light background with blue accents

### Design Inspiration
- Notion: Clean, minimal interface
- Linear: Modern SaaS aesthetics
- AWS Console: Professional dashboard layout

---

## 📄 Page Flow

```
Landing Page → Get Started → Login → Dashboard
```

---

## 🏠 Landing Page (`/landing`)

### Layout Structure

#### Top Navigation Bar
- **Left**: Eligify logo + brand name
- **Right**: Sign In button + Get Started (primary CTA)

#### Hero Section (Full Width)
**Left Column:**
- Badge: "AI-Powered Career Platform"
- Headline: "Unlock Opportunities Through Verified Skills"
- Description: Platform value proposition
- CTA Buttons:
  - Primary: "Get Started Free"
  - Secondary: "Watch Demo"
- Trust Indicators: 10K+ Students, 500+ Internships, 95% Success Rate

**Right Column:**
- Dashboard preview mockup
- Floating success badge
- Gradient background card

#### Features Section (3 Columns)

**Feature 1: Eligibility Analysis**
- Icon: Target (blue)
- Description: Real-time matching, compatibility scores
- Benefits list with checkmarks

**Feature 2: Skill Gap Detection**
- Icon: TrendingUp (yellow)
- Description: Visual skill comparison, priority ranking
- Benefits list with checkmarks

**Feature 3: AI Skill Unlocking (SkillGenie)**
- Icon: Sparkles (purple)
- Description: Custom project roadmaps, step-by-step guidance
- Benefits list with checkmarks

#### CTA Section
- Centered headline
- Large "Get Started Free" button

#### Footer
- Logo + copyright

---

## 🔐 Authentication Pages

### Sign In Page (`/auth/signin`)

**Layout:**
- Centered authentication card
- Demo account credentials displayed (for testing)
- Email + Password fields
- "Remember me" checkbox
- Sign in button
- Link to create account

**Demo Account Info Box:**
```
Email: test@example.com
Password: Test@123
```

### Sign Up Page (`/auth/signup`)

**Layout:**
- Centered authentication card
- Name, Email, Password, Confirm Password fields
- Validation messages
- Create account button
- Link to sign in

**Validation:**
- Email format check
- Password requirements (8+ chars, uppercase, lowercase, number, special char)
- Password confirmation match

---

## 📊 Dashboard (`/dashboard`)

### Layout Components

#### Top Navbar
- **Left**: Page title
- **Right**: 
  - Notifications icon
  - User profile dropdown
    - Name
    - Qualification
    - View Profile
    - Sign Out

#### Left Sidebar
- Logo
- Navigation items:
  - Dashboard (active)
  - Profile
  - Internships
  - Projects
- Collapsible on mobile

#### Main Content Area

**First-Time User State:**
- Large onboarding panel
- Upload resume CTA
- 3-step process cards:
  1. Upload Resume
  2. View Matches
  3. Fill Gaps

**Regular Dashboard:**

**Stats Grid (4 columns):**
1. Total Skills
2. Verified Skills
3. Eligible Internships
4. Almost Eligible

**Quick Actions (3 cards):**
- Upload Resume (if not uploaded)
- Browse Internships
- Generate Project

**Recent Activity:**
- Recent projects list
- Status badges

---

## 👤 Profile Page (`/profile`)

### Sections

#### Personal Information Card
- Name, Email, Phone
- Location
- LinkedIn, GitHub, Portfolio links
- Icons for each field

#### Education Card
- Institution, Degree, Field
- Start/End dates
- CGPA
- Timeline indicator (blue bar)

#### Experience Card
- Company, Role
- Description
- Dates
- Skills used (badges)
- Timeline indicator (green bar)

#### Resume Upload Card
- Drag-and-drop area
- File validation (PDF, DOCX, TXT, max 10MB)
- Upload progress bar
- Success notification

#### Skills Section
- Filter by status (Claimed, In Progress, Verified)
- Filter by category
- Skill cards with:
  - Skill name
  - Category badge
  - Status badge (color-coded)
  - Proficiency bar
  - Verification date
- "Add Skill" button

---

## 💼 Internships Page (`/internships`)

### Layout

#### Three Tabs
1. **Eligible** (Green badge) - 80%+ match
2. **Almost Eligible** (Yellow badge) - 50-79% match
3. **Not Eligible** (Gray badge) - <50% match

#### Filters
- Search by company/role
- Filter by type (Remote, Onsite, Hybrid)

#### Internship Cards (Grid Layout)

**Card Structure:**
- Company logo placeholder
- Internship title
- Company name
- Match score (circular progress)
- Details:
  - Location (MapPin icon)
  - Type (Briefcase icon)
  - Stipend (DollarSign icon)
  - Duration (Calendar icon)
- Matched skills count
- Missing skills preview
- Recommendation text
- **"Unlock with SkillGenie" button** (if skills missing)

**Card Colors:**
- Eligible: Green left border
- Almost Eligible: Yellow left border
- Not Eligible: Gray left border

---

## 🎯 Skill Gap Detection

### Visual Comparison

**Required Skills vs Student Skills:**

```
Communication ✓ (Green checkmark)
HR Basics ✗ (Red X)
Recruitment ✗ (Red X)
```

**Missing Skills Card:**
- Skill name
- Required badge (if mandatory)
- Current proficiency: 0%
- Target proficiency: 70%
- Priority badge (High/Medium/Low)

**Unlock Button:**
- Gradient purple-to-blue background
- Sparkles icon
- "Unlock with SkillGenie" text
- Redirects to `/projects?skills=HR Basics,Recruitment`

---

## ✨ SkillGenie (Projects Page)

### Generate Project Modal

**Inputs:**
- Target skills (multi-select with chips)
- Experience level (Beginner/Intermediate/Advanced)
- Time commitment (optional)

**AI Generation:**
- Loading state (3 seconds)
- Success notification
- Redirect to project detail

### Project Cards

**Card Content:**
- Project title
- Description
- Status badge
- Target skills (badges)
- Difficulty level
- Estimated duration
- Progress bar (0/3 milestones)

### Project Detail Page

**Sections:**
1. **Header**: Title, description, status, quick stats
2. **Objectives**: Checkmark list
3. **Skills You'll Build**: Skill badges
4. **Tech Stack**: Technology cards with purpose
5. **Milestones**: Numbered timeline with tasks
6. **Resources**: Learning materials with links

**Action Buttons:**
- Accept Project
- Start Working
- Mark as Complete

---

## 🎨 Design Tokens

### Colors
```css
Primary: #3B82F6 (Blue-500)
Success: #10B981 (Green-500)
Warning: #F59E0B (Amber-500)
Danger: #EF4444 (Red-500)
Neutral: #9CA3AF (Gray-400)
Background: #F3F4F6 (Gray-100)
```

### Typography
- Font: Inter
- Headings: Bold, 24-48px
- Body: Regular, 14-16px
- Small: 12-14px

### Spacing
- Card padding: 24px
- Section gap: 32px
- Element gap: 16px

### Shadows
- Card: `shadow-sm` (subtle)
- Card hover: `shadow-md`
- Modal: `shadow-xl`

### Border Radius
- Cards: 12px
- Buttons: 8px
- Badges: 9999px (full)

### Components

#### Buttons
```css
.btn-primary: Blue background, white text
.btn-secondary: White background, gray border
.btn-success: Green background, white text
```

#### Cards
```css
.card: White background, border, shadow
.card-hover: Hover effect with shadow increase
```

#### Badges
```css
.badge-success: Green background
.badge-warning: Yellow background
.badge-danger: Red background
.badge-neutral: Gray background
.badge-primary: Blue background
```

---

## 📱 Responsive Behavior

### Desktop (1440px+)
- Full sidebar visible
- 3-4 column grids
- Large cards

### Tablet (768-1440px)
- Collapsible sidebar
- 2-3 column grids
- Medium cards

### Mobile (<768px)
- Hidden sidebar (hamburger menu)
- Single column
- Stacked cards

---

## ✅ Implementation Checklist

- [x] Landing page with hero section
- [x] Feature cards (3 columns)
- [x] Authentication pages (sign in/up)
- [x] Dashboard with stats
- [x] First-time onboarding panel
- [x] Profile page with resume upload
- [x] Skill graph visualization
- [x] Internships with 3-tab classification
- [x] Skill gap detection
- [x] "Unlock with SkillGenie" button
- [x] Project generation modal
- [x] Project detail with milestones
- [x] Responsive design
- [x] Color-coded status indicators

---

## 🚀 Next Steps

1. **Test the new landing page**: Visit `/landing`
2. **Create account**: Test authentication flow
3. **Upload resume**: Trigger skill extraction
4. **Browse internships**: See skill gaps
5. **Click "Unlock with SkillGenie"**: Generate project
6. **Complete project**: Verify skills

---

## 📸 Key UI Patterns

### Card-Based Layout
All content uses card components with consistent styling

### Color Coding
- Green: Success, eligible, verified
- Yellow: Warning, almost eligible, in progress
- Red: Danger, not eligible, missing
- Blue: Primary actions, links
- Gray: Neutral, inactive

### Progressive Disclosure
- Summary cards → Detail modals
- Collapsed sections → Expandable
- Tabs for categorization

### Visual Hierarchy
- Large headings for sections
- Icons for quick recognition
- Badges for status
- Progress bars for metrics

---

Ready to use! 🎉
