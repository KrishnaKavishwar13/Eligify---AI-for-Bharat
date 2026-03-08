# Frontend Export Manifest

## Project Overview
- **Project Name**: Eligify MVP Frontend
- **Technology Stack**: Next.js 14, TypeScript, Tailwind CSS
- **Backend Integration**: FastAPI (Python) at http://localhost:8000
- **Authentication**: JWT tokens with localStorage persistence
- **State Management**: Zustand + React Query
- **Design System**: Blue gradient theme (Sky → Blue → Cyan)

## Complete File Structure

### Root Configuration Files
```
frontend/
├── package.json                    # Dependencies and scripts
├── package-lock.json              # Dependency lock file
├── next.config.js                 # Next.js configuration with API proxy
├── tailwind.config.js             # Tailwind CSS configuration with custom theme
├── tailwind.config.ts             # TypeScript version of Tailwind config
├── tsconfig.json                  # TypeScript configuration
├── postcss.config.js              # PostCSS configuration
├── next-env.d.ts                  # Next.js TypeScript declarations
├── .env.local.example             # Environment variables template
├── .eslintrc.json                 # ESLint configuration
├── .prettierrc                    # Prettier configuration
├── .gitignore                     # Git ignore rules
└── README.md                      # Project documentation
```

### Application Structure
```
app/                               # Next.js 14 App Router
├── layout.tsx                     # Root layout with providers
├── page.tsx                       # Home page (redirects to landing)
├── not-found.tsx                  # 404 page
├── auth/
│   ├── signin/
│   │   └── page.tsx              # Sign in page
│   └── signup/
│       └── page.tsx              # Sign up page
├── dashboard/
│   └── page.tsx                  # Main dashboard with stats and quick actions
├── landing/
│   └── page.tsx                  # Landing page for unauthenticated users
├── profile/
│   └── page.tsx                  # User profile management
├── internships/
│   └── page.tsx                  # Internship listings and matching
├── projects/
│   ├── page.tsx                  # Project listings
│   └── [id]/
│       └── page.tsx              # Individual project details
└── skillgenie/
    ├── page.tsx                  # SkillGenie dashboard
    ├── assessment/
    │   └── page.tsx              # Skill assessment interface
    ├── project/
    │   └── page.tsx              # Project generation
    ├── result/
    │   └── page.tsx              # Assessment results
    └── submit/
        └── page.tsx              # Project submission
```

### Components Architecture
```
components/
├── Providers.tsx                  # React Query and notification providers
├── ErrorBoundary.tsx             # Error boundary wrapper
├── NotificationBanner.tsx         # Toast notifications
├── ProtectedRoute.tsx             # Authentication guard
├── ChatWidget.tsx                 # AI chat interface
├── ConditionalChatWidget.tsx      # Conditional chat display
├── Layout/
│   ├── Header.tsx                # Navigation header
│   └── MainLayout.tsx            # Main application layout
├── Dashboard/                     # Dashboard-specific components
├── Profile/
│   ├── EditProfileModal.tsx      # Profile editing modal
│   └── ResumeUpload.tsx          # Resume upload component
├── Internships/
│   ├── InternshipCard.tsx        # Individual internship display
│   └── InternshipDetailModal.tsx # Internship details modal
├── Projects/
│   ├── ProjectCard.tsx           # Project card component
│   └── GenerateProjectModal.tsx  # Project generation modal
└── Skills/
    ├── SkillGraph.tsx            # Skill visualization
    └── AddSkillModal.tsx         # Manual skill addition
```

### Business Logic Layer
```
hooks/                            # Custom React hooks for data fetching
├── useAuth.ts                    # Authentication operations
├── useProfile.ts                 # Profile management
├── useInternships.ts             # Internship data fetching
├── useProjects.ts                # Project management
├── useSkillGraph.ts              # Skill graph operations
└── useNotifications.ts           # Notification management

lib/                              # Core utilities and configurations
├── api.ts                        # Axios instance with interceptors
├── auth.ts                       # Zustand auth store
├── constants.ts                  # API routes and app constants
├── utils.ts                      # Utility functions
├── queryClient.ts                # React Query configuration
├── notifications.ts              # Notification store
├── validations.ts                # Form validation schemas
├── mockAuth.ts                   # Mock authentication for development
└── mockData.ts                   # Mock data for development

types/                            # TypeScript type definitions
├── index.ts                      # Core domain types
└── api.ts                        # API request/response types
```

### Styling and Assets
```
styles/
└── globals.css                   # Global styles with Tailwind components

public/                           # Static assets (currently empty)
```

## Key Dependencies

### Production Dependencies
```json
{
  "@hookform/resolvers": "^3.3.4",     # Form validation
  "@tanstack/react-query": "^5.28.0",  # Data fetching and caching
  "axios": "^1.6.7",                   # HTTP client
  "clsx": "^2.1.0",                    # Conditional class names
  "lucide-react": "^0.356.0",          # Icon library
  "next": "^14.2.35",                  # React framework
  "react": "^18.3.0",                  # React library
  "react-dom": "^18.3.0",              # React DOM
  "react-hook-form": "^7.51.0",        # Form management
  "recharts": "^2.12.2",               # Chart library
  "tailwind-merge": "^2.2.1",          # Tailwind class merging
  "zod": "^3.22.4",                    # Schema validation
  "zustand": "^4.5.2"                  # State management
}
```

### Development Dependencies
```json
{
  "@types/node": "^20.11.0",
  "@types/react": "^18.2.0",
  "@types/react-dom": "^18.2.0",
  "@typescript-eslint/eslint-plugin": "^7.1.0",
  "@typescript-eslint/parser": "^7.1.0",
  "autoprefixer": "^10.4.27",
  "eslint": "^8.57.1",
  "eslint-config-next": "^14.2.35",
  "postcss": "^8.5.8",
  "prettier": "^3.2.5",
  "prettier-plugin-tailwindcss": "^0.5.11",
  "tailwindcss": "^3.4.19",
  "typescript": "^5.4.0"
}
```

## Environment Variables Required

```bash
# Backend API Configuration
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Mock API Mode (set to 'false' for production)
NEXT_PUBLIC_USE_MOCK_API=true

# File Upload Configuration
NEXT_PUBLIC_MAX_FILE_SIZE=10485760
NEXT_PUBLIC_ALLOWED_FILE_TYPES=.pdf,.docx,.txt

# JWT Configuration
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-here
```

## API Integration Points

### Authentication Endpoints
- `POST /auth/signup` - User registration
- `POST /auth/signin` - User login
- `POST /auth/signout` - User logout
- `POST /auth/refresh` - Token refresh

### Profile Management
- `GET /profile` - Fetch user profile
- `PUT /profile` - Update user profile
- `POST /profile/upload-resume` - Upload and parse resume

### Skills Management
- `GET /skills` - Fetch user skill graph
- `POST /skills` - Add new skill
- `GET /skills/gaps` - Get skill gap analysis

### Internships
- `GET /internships` - Fetch all internships
- `GET /internships/classify` - Get classified internships based on user skills

### Projects
- `GET /projects` - Fetch user projects
- `POST /copilot/generate-project` - Generate new project
- `PUT /projects/{id}/status` - Update project status
- `POST /projects/{id}/complete` - Mark project as complete

### Validation
- `POST /validate/submit` - Submit project for validation
- `GET /validate/{id}` - Get validation status
- `GET /validate/history` - Get validation history

## Mock API Implementation

The frontend includes a complete mock API implementation for development:
- Mock authentication with localStorage persistence
- Mock data for profiles, skills, internships, and projects
- Simulated API delays for realistic testing
- Error simulation for edge case testing

## File Purposes and Dependencies

### Core Configuration
- **package.json**: Defines all dependencies and npm scripts
- **next.config.js**: Configures API proxy to backend and image domains
- **tailwind.config.js**: Custom theme with blue gradients and animations
- **tsconfig.json**: TypeScript configuration with path aliases

### Application Entry Points
- **app/layout.tsx**: Root layout with providers and global components
- **app/page.tsx**: Home page that redirects to landing
- **components/Providers.tsx**: React Query and notification providers

### Authentication Flow
- **lib/auth.ts**: Zustand store for authentication state
- **hooks/useAuth.ts**: Authentication operations (login, logout, signup)
- **components/ProtectedRoute.tsx**: Route protection wrapper

### API Communication
- **lib/api.ts**: Axios instance with request/response interceptors
- **lib/constants.ts**: All API endpoints and application routes
- **types/api.ts**: Request/response type definitions

### State Management
- **Zustand stores**: Authentication, notifications
- **React Query**: Server state management and caching
- **Local storage**: Persistent authentication state

### UI Components
- **Tailwind CSS**: Utility-first styling with custom components
- **Lucide React**: Consistent icon system
- **Custom components**: Reusable UI elements with proper TypeScript types

## Build and Deployment

### Development
```bash
npm install
npm run dev
```

### Production Build
```bash
npm run build
npm start
```

### Code Quality
```bash
npm run lint
npm run format
```

## Integration Notes

1. **Backend Compatibility**: Designed for FastAPI backend with specific endpoint structure
2. **Authentication**: JWT tokens stored in localStorage with automatic refresh
3. **Error Handling**: Comprehensive error handling with user-friendly messages
4. **Loading States**: Proper loading and error states for all API calls
5. **Responsive Design**: Mobile-first responsive design
6. **Accessibility**: Basic accessibility features implemented
7. **Performance**: Code splitting, lazy loading, and optimized bundle size

## Known Limitations

1. **File Upload**: Resume upload UI implemented but requires backend integration
2. **Real-time Features**: No WebSocket implementation yet
3. **Offline Support**: No offline functionality
4. **Advanced Validation**: Some form validations may need backend verification
5. **Image Optimization**: Limited image optimization setup
6. **SEO**: Basic SEO setup, may need enhancement for production

This manifest provides a complete overview of the frontend implementation ready for backend integration.