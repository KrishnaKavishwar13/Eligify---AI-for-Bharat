# Component Architecture Guide

## Overview

This document outlines the component architecture of the Eligify frontend, including component hierarchy, relationships, design patterns, and reusability guidelines.

## Architecture Principles

### 1. Component Hierarchy
```
App (layout.tsx)
├── Providers
│   ├── QueryClientProvider (React Query)
│   └── NotificationProvider (Zustand)
├── Pages (App Router)
│   ├── Landing
│   ├── Auth (SignIn/SignUp)
│   ├── Dashboard
│   ├── Profile
│   ├── Internships
│   ├── Projects
│   └── SkillGenie
├── Layout Components
│   ├── MainLayout
│   └── Header
├── Feature Components
│   ├── Profile Components
│   ├── Internship Components
│   ├── Project Components
│   └── Skill Components
├── UI Components
│   ├── Modals
│   ├── Forms
│   └── Cards
└── Global Components
    ├── NotificationBanner
    ├── ChatWidget
    └── ErrorBoundary
```

### 2. Design Patterns
- **Container/Presentational**: Hooks handle logic, components handle UI
- **Compound Components**: Complex components with sub-components
- **Render Props**: Flexible component composition
- **Custom Hooks**: Reusable business logic
- **Provider Pattern**: Global state management

## Core Layout Components

### 1. Root Layout (`app/layout.tsx`)
```typescript
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          {children}
          <NotificationBanner />
          <ConditionalChatWidget />
        </Providers>
      </body>
    </html>
  );
}
```

**Purpose**: 
- Root application wrapper
- Global providers setup
- Global components (notifications, chat)
- Font and metadata configuration

**Dependencies**: 
- `Providers.tsx` - React Query and state providers
- `NotificationBanner.tsx` - Toast notifications
- `ConditionalChatWidget.tsx` - AI chat interface

### 2. Providers (`components/Providers.tsx`)
```typescript
export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <NotificationBanner />
      {children}
    </QueryClientProvider>
  );
}
```

**Purpose**:
- React Query setup for server state
- Global notification system
- Error boundary wrapper

**Dependencies**:
- `@tanstack/react-query` - Server state management
- `lib/queryClient.ts` - Query client configuration

### 3. Main Layout (`components/Layout/MainLayout.tsx`)
```typescript
interface MainLayoutProps {
  children: React.ReactNode;
  showHeader?: boolean;
  className?: string;
}

export default function MainLayout({ 
  children, 
  showHeader = true, 
  className 
}: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-cyan-50">
      {showHeader && <Header />}
      <main className={cn("container mx-auto px-4 py-8", className)}>
        {children}
      </main>
    </div>
  );
}
```

**Purpose**:
- Consistent page layout
- Navigation header
- Background styling
- Container spacing

**Dependencies**:
- `Header.tsx` - Navigation component
- `lib/utils.ts` - Class name utilities

## Feature Components

### 1. Profile Components

#### Profile Management (`components/Profile/EditProfileModal.tsx`)
```typescript
interface EditProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  profile: StudentProfile;
}

export default function EditProfileModal({ 
  isOpen, 
  onClose, 
  profile 
}: EditProfileModalProps) {
  const { updateProfile, isUpdating } = useProfile();
  const { register, handleSubmit, formState: { errors } } = useForm();
  
  // Form handling logic
  // Validation with Zod schemas
  // Optimistic updates
}
```

**Features**:
- Form validation with react-hook-form + Zod
- Optimistic updates for better UX
- Error handling and loading states
- Modal overlay with proper accessibility

**Dependencies**:
- `hooks/useProfile.ts` - Profile data management
- `react-hook-form` - Form handling
- `zod` - Schema validation

#### Resume Upload (`components/Profile/ResumeUpload.tsx`)
```typescript
interface ResumeUploadProps {
  onUploadComplete?: (data: UploadResumeResponse) => void;
  className?: string;
}

export default function ResumeUpload({ 
  onUploadComplete, 
  className 
}: ResumeUploadProps) {
  const { uploadResume, isUploading, uploadProgress } = useProfile();
  
  // Drag & drop functionality
  // File validation (type, size)
  // Progress tracking
  // Error handling
}
```

**Features**:
- Drag & drop file upload
- File type and size validation
- Upload progress tracking
- Preview and error states

### 2. Internship Components

#### Internship Card (`components/Internships/InternshipCard.tsx`)
```typescript
interface InternshipCardProps {
  internship: Internship;
  matchScore?: number;
  missingSkills?: SkillGap[];
  matchedSkills?: string[];
  onClick?: () => void;
  className?: string;
}

export default function InternshipCard({
  internship,
  matchScore,
  missingSkills = [],
  matchedSkills = [],
  onClick,
  className
}: InternshipCardProps) {
  // Match score visualization
  // Skill gap indicators
  // Application deadline warnings
  // Responsive design
}
```

**Features**:
- Match score visualization with color coding
- Skill requirements vs user skills comparison
- Application deadline countdown
- Responsive card layout
- Click handling for details

**Dependencies**:
- `types/index.ts` - Type definitions
- `lib/utils.ts` - Utility functions for formatting

#### Internship Detail Modal (`components/Internships/InternshipDetailModal.tsx`)
```typescript
interface InternshipDetailModalProps {
  internship: Internship | null;
  isOpen: boolean;
  onClose: () => void;
  matchData?: {
    matchScore: number;
    missingSkills: SkillGap[];
    matchedSkills: string[];
  };
}
```

**Features**:
- Detailed internship information
- Skill gap analysis visualization
- Application link handling
- Responsive modal design

### 3. Project Components

#### Project Card (`components/Projects/ProjectCard.tsx`)
```typescript
interface ProjectCardProps {
  project: GeneratedProject;
  onStatusChange?: (status: ProjectStatus) => void;
  onViewDetails?: () => void;
  className?: string;
}

export default function ProjectCard({
  project,
  onStatusChange,
  onViewDetails,
  className
}: ProjectCardProps) {
  // Progress calculation
  // Status badge rendering
  // Action buttons based on status
  // Milestone tracking
}
```

**Features**:
- Project progress visualization
- Status-based action buttons
- Milestone completion tracking
- Skill tags display
- Responsive design

#### Generate Project Modal (`components/Projects/GenerateProjectModal.tsx`)
```typescript
interface GenerateProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  onGenerate: (request: GenerateProjectRequest) => void;
  isGenerating: boolean;
}
```

**Features**:
- Multi-step form for project generation
- Skill selection with autocomplete
- Difficulty level selection
- Time commitment estimation
- Preference customization

### 4. Skill Components

#### Skill Graph (`components/Skills/SkillGraph.tsx`)
```typescript
interface SkillGraphProps {
  skillGraph: SkillGraph;
  onSkillClick?: (skill: SkillNode) => void;
  className?: string;
}

export default function SkillGraph({
  skillGraph,
  onSkillClick,
  className
}: SkillGraphProps) {
  // Recharts integration for visualization
  // Interactive skill nodes
  // Proficiency level indicators
  // Category grouping
}
```

**Features**:
- Interactive skill visualization using Recharts
- Proficiency level color coding
- Category-based grouping
- Click handlers for skill details
- Responsive chart design

**Dependencies**:
- `recharts` - Chart library
- `types/index.ts` - Skill type definitions

## UI Components

### 1. Modal System
```typescript
// Base modal component
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

export default function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  className
}: ModalProps) {
  // Portal rendering
  // Escape key handling
  // Click outside to close
  // Focus management
  // Animation transitions
}
```

**Features**:
- Portal-based rendering
- Keyboard navigation (Escape to close)
- Click outside to close
- Focus trap for accessibility
- Size variants
- Smooth animations

### 2. Form Components
```typescript
// Reusable form input
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
  required?: boolean;
}

export default function Input({
  label,
  error,
  helperText,
  required,
  className,
  ...props
}: InputProps) {
  // Error state styling
  // Label and helper text
  // Accessibility attributes
}
```

**Features**:
- Consistent styling across forms
- Error state handling
- Accessibility attributes
- Helper text support
- Integration with react-hook-form

### 3. Card Components
```typescript
// Base card component
interface CardProps {
  children: React.ReactNode;
  hover?: boolean;
  padding?: 'sm' | 'md' | 'lg';
  className?: string;
  onClick?: () => void;
}

export default function Card({
  children,
  hover = false,
  padding = 'md',
  className,
  onClick
}: CardProps) {
  // Hover effects
  // Padding variants
  // Click handling
  // Shadow and border styling
}
```

## Global Components

### 1. Notification System (`components/NotificationBanner.tsx`)
```typescript
interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

export default function NotificationBanner() {
  const { notifications, removeNotification } = useNotificationStore();
  
  // Auto-dismiss functionality
  // Animation transitions
  // Multiple notification stacking
  // Click to dismiss
}
```

**Features**:
- Multiple notification types with color coding
- Auto-dismiss with configurable duration
- Manual dismiss functionality
- Smooth enter/exit animations
- Stacking for multiple notifications

**Dependencies**:
- `lib/notifications.ts` - Zustand notification store
- `lucide-react` - Icons for notification types

### 2. Chat Widget (`components/ChatWidget.tsx`)
```typescript
interface ChatWidgetProps {
  isOpen: boolean;
  onToggle: () => void;
  className?: string;
}

export default function ChatWidget({
  isOpen,
  onToggle,
  className
}: ChatWidgetProps) {
  // Chat interface
  // Message history
  // Typing indicators
  // File upload support
}
```

**Features**:
- Collapsible chat interface
- Message history persistence
- Typing indicators
- File upload support
- Responsive design

### 3. Error Boundary (`components/ErrorBoundary.tsx`)
```typescript
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

export default class ErrorBoundary extends React.Component<
  React.PropsWithChildren<{}>,
  ErrorBoundaryState
> {
  // Error catching
  // Error reporting
  // Fallback UI
  // Recovery mechanisms
}
```

**Features**:
- Catches JavaScript errors in component tree
- Displays fallback UI
- Error reporting to logging service
- Recovery mechanisms

## Custom Hooks Integration

### 1. Data Fetching Hooks
```typescript
// Example: useProfile hook integration
export function ProfilePage() {
  const { profile, isLoading, error, updateProfile } = useProfile();
  
  if (isLoading) return <ProfileSkeleton />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    <MainLayout>
      <ProfileForm 
        profile={profile} 
        onUpdate={updateProfile}
      />
    </MainLayout>
  );
}
```

### 2. Form Hooks
```typescript
// Example: Form handling with validation
export function SignUpForm() {
  const { signUp, isSigningUp } = useAuth();
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(signUpSchema)
  });
  
  const onSubmit = (data: SignUpRequest) => {
    signUp(data);
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

## State Management Integration

### 1. Zustand Stores
```typescript
// Authentication state
const { user, isAuthenticated, setAuth, clearAuth } = useAuthStore();

// Notifications
const { addNotification, removeNotification } = useNotificationStore();
```

### 2. React Query Integration
```typescript
// Server state management
const { data, isLoading, error, refetch } = useQuery({
  queryKey: ['profile'],
  queryFn: fetchProfile,
  staleTime: 5 * 60 * 1000
});

// Mutations with optimistic updates
const mutation = useMutation({
  mutationFn: updateProfile,
  onMutate: async (newData) => {
    // Optimistic update
    queryClient.setQueryData(['profile'], newData);
  },
  onError: (error, variables, context) => {
    // Rollback on error
    queryClient.setQueryData(['profile'], context.previousData);
  }
});
```

## Styling Architecture

### 1. Tailwind CSS Classes
```typescript
// Utility classes for consistent styling
const buttonClasses = {
  base: "rounded-lg px-4 py-2 font-medium transition-all duration-200",
  primary: "bg-gradient-to-r from-sky-500 to-blue-600 text-white hover:from-sky-600 hover:to-blue-700",
  secondary: "border-2 border-blue-300 bg-white text-blue-700 hover:bg-blue-50"
};
```

### 2. Component Variants
```typescript
// Variant-based styling
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
}

export default function Button({ variant = 'primary', size = 'md', ...props }: ButtonProps) {
  const classes = cn(
    buttonClasses.base,
    buttonClasses[variant],
    sizeClasses[size],
    props.className
  );
  
  return <button className={classes} {...props} />;
}
```

## Performance Optimizations

### 1. Code Splitting
```typescript
// Lazy loading for large components
const ProjectDetailModal = lazy(() => import('./ProjectDetailModal'));

// Usage with Suspense
<Suspense fallback={<ModalSkeleton />}>
  <ProjectDetailModal />
</Suspense>
```

### 2. Memoization
```typescript
// Memoized components for expensive renders
const MemoizedSkillGraph = memo(SkillGraph, (prevProps, nextProps) => {
  return prevProps.skillGraph.lastUpdated === nextProps.skillGraph.lastUpdated;
});

// Memoized values
const expensiveValue = useMemo(() => {
  return calculateComplexMetrics(data);
}, [data]);
```

### 3. Virtual Scrolling
```typescript
// For large lists (internships, projects)
import { FixedSizeList as List } from 'react-window';

const InternshipList = ({ internships }: { internships: Internship[] }) => (
  <List
    height={600}
    itemCount={internships.length}
    itemSize={200}
    itemData={internships}
  >
    {({ index, style, data }) => (
      <div style={style}>
        <InternshipCard internship={data[index]} />
      </div>
    )}
  </List>
);
```

## Testing Considerations

### 1. Component Testing
```typescript
// Example test structure
describe('InternshipCard', () => {
  it('displays match score correctly', () => {
    render(<InternshipCard internship={mockInternship} matchScore={85} />);
    expect(screen.getByText('85%')).toBeInTheDocument();
  });
  
  it('shows missing skills', () => {
    const missingSkills = [{ skillName: 'React', required: true }];
    render(<InternshipCard internship={mockInternship} missingSkills={missingSkills} />);
    expect(screen.getByText('Missing: React')).toBeInTheDocument();
  });
});
```

### 2. Hook Testing
```typescript
// Testing custom hooks
import { renderHook, waitFor } from '@testing-library/react';
import { useProfile } from '../hooks/useProfile';

test('useProfile fetches profile data', async () => {
  const { result } = renderHook(() => useProfile());
  
  await waitFor(() => {
    expect(result.current.profile).toBeDefined();
  });
});
```

## Accessibility Guidelines

### 1. Keyboard Navigation
- All interactive elements are keyboard accessible
- Proper tab order and focus management
- Escape key handling for modals

### 2. Screen Reader Support
- Semantic HTML elements
- ARIA labels and descriptions
- Proper heading hierarchy

### 3. Color and Contrast
- Sufficient color contrast ratios
- Information not conveyed by color alone
- Focus indicators for keyboard users

This architecture provides a scalable, maintainable, and performant component system for the Eligify frontend application.