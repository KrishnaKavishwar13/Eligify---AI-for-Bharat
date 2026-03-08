# Intelligence Features Integration Guide

## Overview
This guide shows how to integrate the 9 unused intelligence endpoints into the frontend.

---

## 🎯 QUICK WINS (Easy to Integrate)

### 1. Skill Priorities Widget (Dashboard)
**Backend:** `GET /api/v1/intelligence/skill-priorities/{user_id}`

**What it does:** Returns top skills to learn, ranked by impact

**Integration Steps:**
1. Create `frontend/hooks/useSkillPriorities.ts`:
```typescript
export function useSkillPriorities(limit = 5) {
  const { user } = useAuthStore();
  
  return useQuery({
    queryKey: ['skill-priorities', user?.userId, limit],
    queryFn: async () => {
      const response = await api.get(
        `/api/v1/intelligence/skill-priorities/${user.userId}?limit=${limit}`
      );
      return response.data.data;
    },
    enabled: !!user?.userId,
  });
}
```

2. Create `frontend/components/Dashboard/SkillPrioritiesWidget.tsx`:
```typescript
export default function SkillPrioritiesWidget() {
  const { data: priorities, isLoading } = useSkillPriorities(5);
  
  return (
    <div className="card">
      <h3>Skills to Focus On</h3>
      {priorities?.map((skill, index) => (
        <div key={skill.skillName}>
          <span>#{index + 1}</span>
          <span>{skill.skillName}</span>
          <span>{skill.priorityScore}/100</span>
        </div>
      ))}
    </div>
  );
}
```

3. Add to dashboard: `<SkillPrioritiesWidget />`

**Time:** 30 minutes

---

### 2. AI Project Suggestions (Projects Page)
**Backend:** `POST /api/v1/intelligence/suggest-projects`

**What it does:** Smarter project suggestions based on skill gaps & career goals

**Integration Steps:**
1. Add to `frontend/hooks/useProjects.ts`:
```typescript
const suggestProjectsMutation = useMutation({
  mutationFn: async (data: {
    targetSkills?: string[];
    careerGoals?: string[];
    timeAvailablePerWeek?: number;
  }) => {
    const response = await api.post(
      '/api/v1/intelligence/suggest-projects',
      { userId: user.userId, ...data }
    );
    return response.data.data;
  },
});
```

2. Add "Get AI Suggestions" button on projects page
3. Display suggestions with relevance scores

**Time:** 45 minutes

---

## 🚀 MEDIUM EFFORT (New Pages)

### 3. Career Roadmap Page
**Backend:** 
- `POST /api/v1/intelligence/career-roadmap` - Generate roadmap
- `PUT /api/v1/intelligence/career-roadmap/{id}/progress` - Update progress
- `GET /api/v1/intelligence/next-steps/{user_id}/{roadmap_id}` - Get next steps

**What it does:** Creates 3-5 milestone career plan with progress tracking

**Integration Steps:**
1. Create `frontend/app/career-roadmap/page.tsx`
2. Create `frontend/hooks/useCareerRoadmap.ts`
3. Create components:
   - `RoadmapGenerator.tsx` - Form to create roadmap
   - `RoadmapTimeline.tsx` - Visual timeline with milestones
   - `MilestoneCard.tsx` - Individual milestone with tasks
   - `NextStepsWidget.tsx` - Recommended actions

**UI Layout:**
```
┌─────────────────────────────────────┐
│  Career Roadmap: Software Engineer  │
├─────────────────────────────────────┤
│  Progress: 40% (2/5 milestones)     │
├─────────────────────────────────────┤
│  ● Milestone 1 [Completed]          │
│  ● Milestone 2 [In Progress]        │
│  ○ Milestone 3 [Not Started]        │
│  ○ Milestone 4 [Not Started]        │
│  ○ Milestone 5 [Not Started]        │
├─────────────────────────────────────┤
│  Next Steps:                        │
│  - Complete React project           │
│  - Learn TypeScript basics          │
└─────────────────────────────────────┘
```

**Time:** 3-4 hours

---

### 4. Skill Progress Tracker
**Backend:** `GET /api/v1/intelligence/predict/skill-progress/{user_id}/{skill_name}`

**What it does:** Predicts timeline to reach target proficiency

**Integration Steps:**
1. Add to skill detail view/modal
2. Show timeline visualization
3. Display recommended projects to accelerate learning

**UI Component:**
```typescript
<SkillProgressPredictor 
  skillName="React"
  targetProficiency={80}
/>
```

Shows:
- Current: 45% → Target: 80%
- Estimated: 45 days
- Milestones: 50% (15 days), 65% (30 days), 80% (45 days)
- Recommended projects

**Time:** 2-3 hours

---

### 5. Profile Analysis Page
**Backend:** `POST /api/v1/intelligence/analyze-profile`

**What it does:** Comprehensive skill gap analysis with learning path

**Integration Steps:**
1. Create `frontend/app/analysis/page.tsx`
2. Create `frontend/hooks/useProfileAnalysis.ts`
3. Display:
   - Current profile snapshot
   - Skill gaps with priorities
   - Recommended learning path
   - Timeline estimates

**Time:** 2-3 hours

---

## 🎨 ADVANCED (Visualizations)

### 6. Internship Graph Visualization
**Backend:** `GET /api/v1/intelligence/internship-graph`

**What it does:** Shows skill-internship relationships as network graph

**Integration Steps:**
1. Install graph library: `npm install react-force-graph-2d`
2. Create `frontend/components/Insights/InternshipGraph.tsx`
3. Create new "Insights" page
4. Visualize:
   - Skills as nodes
   - Internships as nodes
   - Connections showing requirements
   - Color-code by proficiency level

**Time:** 4-5 hours

---

### 7. Explanation System
**Backend:** `POST /api/v1/intelligence/explain`

**What it does:** Generates natural language explanations

**Integration Steps:**
1. Add tooltip/help icon components
2. On click, fetch explanation
3. Display in modal/popover
4. Use for:
   - Why skill is prioritized
   - Why internship matches
   - Why project is suggested
   - How eligibility is calculated

**Time:** 2-3 hours

---

## 📋 RECOMMENDED INTEGRATION ORDER

### Phase 1: Quick Wins (1-2 hours)
1. ✅ Fix project generator fallback (DONE)
2. Add Skill Priorities Widget to dashboard
3. Add AI Project Suggestions button

### Phase 2: Core Features (6-8 hours)
4. Create Career Roadmap page
5. Add Skill Progress Tracker
6. Create Profile Analysis page

### Phase 3: Advanced (6-8 hours)
7. Add Internship Graph visualization
8. Implement Explanation system

---

## 🛠️ IMPLEMENTATION TEMPLATES

### Hook Template
```typescript
// frontend/hooks/useIntelligence.ts
export function useSkillPriorities(limit = 10) {
  const { user } = useAuthStore();
  
  return useQuery({
    queryKey: ['skill-priorities', user?.userId, limit],
    queryFn: async () => {
      const response = await api.get(
        `/api/v1/intelligence/skill-priorities/${user.userId}?limit=${limit}`
      );
      return response.data.data;
    },
    enabled: !!user?.userId,
    staleTime: 5 * 60 * 1000,
  });
}

export function useCareerRoadmap() {
  const { user } = useAuthStore();
  const queryClient = useQueryClient();
  
  const generateMutation = useMutation({
    mutationFn: async (data: { targetRole: string; timelineMonths: number }) => {
      const response = await api.post('/api/v1/intelligence/career-roadmap', {
        userId: user.userId,
        ...data,
      });
      return response.data.roadmap;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['roadmaps'] });
    },
  });
  
  return { generateRoadmap: generateMutation.mutate };
}
```

### Component Template
```typescript
// frontend/components/Intelligence/SkillPrioritiesCard.tsx
export default function SkillPrioritiesCard() {
  const { data: priorities, isLoading } = useSkillPriorities(5);
  
  if (isLoading) return <div>Loading...</div>;
  
  return (
    <div className="card">
      <h3 className="text-lg font-bold">Top Skills to Learn</h3>
      <div className="mt-4 space-y-3">
        {priorities?.map((skill, index) => (
          <div key={skill.skillName} className="flex items-center gap-3">
            <div className="badge">{index + 1}</div>
            <div className="flex-1">
              <p className="font-semibold">{skill.skillName}</p>
              <p className="text-sm text-gray-600">{skill.reasoning}</p>
            </div>
            <div className="text-right">
              <p className="font-bold">{skill.priorityScore}</p>
              <p className="text-xs">Priority</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 🔍 TESTING CHECKLIST

After integration, test:
- [ ] Skill priorities load and display correctly
- [ ] Career roadmap generates with milestones
- [ ] Roadmap progress updates persist
- [ ] Skill progress predictions show timeline
- [ ] Profile analysis shows skill gaps
- [ ] AI project suggestions return relevant projects
- [ ] Internship graph renders without errors
- [ ] Explanations generate on demand
- [ ] All features handle Ollama timeouts gracefully

---

## 💡 DESIGN RECOMMENDATIONS

### Color Scheme (Match Landing Page)
- Primary: Purple (#8b5cf6)
- Secondary: Pink (#ec4899)
- Accent: Orange (#f97316)
- Use gradients: `from-purple-500 via-pink-500 to-orange-400`

### Component Patterns
- Use `card` class for containers
- Use `badge` for tags/labels
- Use gradient backgrounds for headers
- Add hover effects with `hover:scale-105`
- Use loading skeletons during fetch

### Layout Patterns
- Dashboard widgets: 2-column grid on desktop
- Detail pages: 3-column layout (sidebar + main + actions)
- Timelines: Vertical with connecting lines
- Graphs: Full-width with responsive container

---

## 🚨 CURRENT ISSUE: Project Generator

**Problem:** Ollama timeouts causing project generation to fail

**Solution Applied:** Added fallback template-based project generator

**Fallback Features:**
- Generates structured project without AI
- Adjusts complexity based on student level
- Creates 3 milestones (Setup, Development, Testing)
- Includes realistic time estimates
- Works instantly without Ollama dependency

**Testing:** Try generating a project now - it should work even if Ollama is slow/unavailable
