# Requirements Document: Career Intelligence System

## Introduction

The Career Intelligence System extends the Eligify platform with AI-powered career guidance capabilities. The system analyzes student profiles to identify skill gaps, provides personalized project recommendations, generates progressive career roadmaps, and offers explainable AI insights. It integrates seamlessly with existing services (ai_service, eligibility_service, skill_service, project_service, verification_service) while maintaining the deterministic eligibility engine as the source of truth. The system helps students navigate from their current skill level to target career goals through intelligent, data-driven recommendations.

## Glossary

- **System**: The Career Intelligence System as a whole
- **Skill_Gap_Service**: Service that analyzes student profiles and identifies skill gaps
- **Internship_Mapping_Service**: Service that maintains skill-internship relationship graphs
- **Personalization_Service**: Service that generates personalized project suggestions
- **Career_Path_Service**: Service that creates progressive career roadmaps
- **Explanation_Service**: Service that generates natural language explanations for AI decisions
- **Prediction_Service**: Service that predicts skill progress and career readiness
- **AI_Service**: Existing Ollama integration service for LLM capabilities
- **Eligibility_Service**: Existing deterministic internship matching service
- **Skill_Service**: Existing service for skill graph management
- **Project_Service**: Existing service for project generation
- **Student**: User of the system seeking career guidance
- **Profile**: Complete snapshot of student's skills, projects, and progress
- **Skill_Gap**: Difference between current and target skill proficiency
- **Priority_Score**: Calculated score (0-100) indicating learning priority
- **Learning_Velocity**: Metrics tracking student's learning speed and consistency
- **Roadmap**: Progressive plan with milestones from current position to career goal
- **Milestone**: Discrete step in career roadmap with skills, projects, and timeline
- **Relevance_Score**: Calculated score (0-100) indicating project fit for student
- **Confidence_Score**: Calculated score (0-100) indicating prediction certainty
- **Internship_Graph**: Data structure mapping skills to internships requiring them
- **Proficiency_Level**: Numeric value (0-100) representing skill mastery

## Requirements

### Requirement 1: Profile Analysis and Skill Gap Detection

**User Story:** As a student, I want the system to analyze my complete profile and identify skill gaps, so that I understand what skills I need to learn to reach my career goals.

#### Acceptance Criteria

1. WHEN a student requests profile analysis with target internships, THE Skill_Gap_Service SHALL aggregate data from Skill_Service, Project_Service, and resume parsing
2. WHEN analyzing a profile, THE Skill_Gap_Service SHALL calculate current proficiency for each skill in the student's skill graph
3. WHEN target internships are specified, THE Skill_Gap_Service SHALL identify all required skills across those internships
4. WHEN comparing current and target skills, THE Skill_Gap_Service SHALL create a skill gap for each skill where current proficiency is less than target proficiency
5. WHEN calculating skill gaps, THE Skill_Gap_Service SHALL ensure gap_size equals target_proficiency minus current_proficiency
6. WHEN prioritizing skill gaps, THE Skill_Gap_Service SHALL calculate priority scores between 0 and 100 based on gap size, mandatory status, and impact
7. WHEN a skill is mandatory for multiple internships, THE Skill_Gap_Service SHALL assign higher priority scores
8. WHEN estimating learning effort, THE Skill_Gap_Service SHALL calculate estimated learning hours based on gap size and student's learning velocity
9. WHEN creating a learning path, THE Skill_Gap_Service SHALL order skills using topological sort to respect prerequisites
10. WHEN generating analysis results, THE Skill_Gap_Service SHALL include current profile snapshot, skill gaps, prioritized skills, learning path, and timeline estimate
11. WHEN calculating confidence scores, THE Skill_Gap_Service SHALL decrease confidence as prediction distance increases
12. WHEN analysis is complete, THE Skill_Gap_Service SHALL save results to storage with 7-day expiration
13. IF a student has no skills or profile data, THEN THE Skill_Gap_Service SHALL return empty analysis with confidence score of zero

### Requirement 2: Skill-Internship Relationship Mapping

**User Story:** As a student, I want to understand which internships require which skills, so that I can make informed decisions about what to learn.

#### Acceptance Criteria

1. WHEN building the internship graph, THE Internship_Mapping_Service SHALL process all internships and extract required skills
2. WHEN processing skills, THE Internship_Mapping_Service SHALL normalize skill names for consistent matching
3. WHEN a skill appears in multiple internships, THE Internship_Mapping_Service SHALL aggregate proficiency requirements and calculate average, minimum, and maximum
4. WHEN tracking skill usage, THE Internship_Mapping_Service SHALL count mandatory occurrences separately from total occurrences
5. WHEN calculating skill impact, THE Internship_Mapping_Service SHALL determine how many internships would become eligible if the skill is learned
6. WHEN identifying skill clusters, THE Internship_Mapping_Service SHALL find common skill patterns across related internships
7. WHEN determining skill dependencies, THE Internship_Mapping_Service SHALL identify prerequisite relationships
8. WHEN validating the graph, THE Internship_Mapping_Service SHALL ensure mandatory counts never exceed total counts
9. WHEN validating proficiency ranges, THE Internship_Mapping_Service SHALL ensure minimum is less than or equal to average which is less than or equal to maximum
10. WHEN storing the graph, THE Internship_Mapping_Service SHALL include total internship count and total unique skill count
11. IF circular dependencies are detected, THEN THE Internship_Mapping_Service SHALL break cycles by removing lowest-weight edges

### Requirement 3: Personalized Project Recommendations

**User Story:** As a student, I want personalized project suggestions that match my skill level and career goals, so that I can efficiently close my skill gaps.

#### Acceptance Criteria

1. WHEN generating project suggestions, THE Personalization_Service SHALL consider student's current skills, skill gaps, completed projects, and career goals
2. WHEN determining project difficulty, THE Personalization_Service SHALL map current proficiency to beginner (0-29), intermediate (30-69), or advanced (70-100) levels
3. WHEN generating projects using AI, THE Personalization_Service SHALL provide student context including completed projects, career goals, and time availability
4. WHEN calculating relevance scores, THE Personalization_Service SHALL consider skill gap closure, internships unlocked, difficulty match, and learning velocity
5. WHEN a project addresses multiple skill gaps, THE Personalization_Service SHALL include all addressed skills in the suggestion
6. WHEN calculating skill gap closure, THE Personalization_Service SHALL compute percentage of total gap size addressed by the project
7. WHEN predicting internships unlocked, THE Personalization_Service SHALL simulate skill graph with project completion and check eligibility changes
8. WHEN estimating completion time, THE Personalization_Service SHALL adjust base hours using student's learning velocity
9. WHEN generating reasoning, THE Personalization_Service SHALL use AI to create natural, encouraging explanations
10. WHEN ranking suggestions, THE Personalization_Service SHALL order by relevance score descending
11. WHEN returning suggestions, THE Personalization_Service SHALL include only projects where prerequisites are met
12. WHEN calculating learning velocity, THE Personalization_Service SHALL use historical project completion data and skill verification rates
13. IF a student has fewer than 2 completed projects, THEN THE Personalization_Service SHALL use platform average learning velocity

### Requirement 4: Career Roadmap Generation

**User Story:** As a student, I want a progressive career roadmap showing steps from my current position to my target role, so that I have a clear path forward.

#### Acceptance Criteria

1. WHEN generating a roadmap, THE Career_Path_Service SHALL analyze student's current position including skills, projects, and eligible internships
2. WHEN using AI for roadmap structure, THE Career_Path_Service SHALL provide current position, target role, and timeline to generate 3-5 progressive milestones
3. WHEN creating milestones, THE Career_Path_Service SHALL include skills to acquire, target proficiency levels, estimated duration, and estimated hours
4. WHEN enriching milestones, THE Career_Path_Service SHALL request personalized project suggestions for milestone skills
5. WHEN identifying target internships, THE Career_Path_Service SHALL find internships matching milestone skill requirements
6. WHEN ordering milestones, THE Career_Path_Service SHALL assign sequential order numbers
7. WHEN establishing dependencies, THE Career_Path_Service SHALL link each milestone to its predecessor
8. WHEN calculating total duration, THE Career_Path_Service SHALL sum estimated hours from all milestones
9. WHEN calculating confidence scores, THE Career_Path_Service SHALL consider current position, goal difficulty, timeline feasibility, and data quality
10. WHEN determining next action, THE Career_Path_Service SHALL recommend starting the first milestone
11. WHEN a milestone is completed, THE Career_Path_Service SHALL update roadmap progress percentage
12. WHEN calculating progress percentage, THE Career_Path_Service SHALL divide completed milestones by total milestones and multiply by 100
13. WHEN suggesting next steps, THE Career_Path_Service SHALL identify incomplete milestones whose dependencies are satisfied
14. WHEN validating roadmaps, THE Career_Path_Service SHALL ensure milestone dependencies form a valid directed acyclic graph
15. IF AI roadmap generation times out after 30 seconds, THEN THE Career_Path_Service SHALL generate simplified roadmap using templates

### Requirement 5: Explainable AI Recommendations

**User Story:** As a student, I want clear explanations for why projects and internships are recommended, so that I understand the reasoning and can make informed decisions.

#### Acceptance Criteria

1. WHEN explaining internship matches, THE Explanation_Service SHALL reference student's current skills and internship requirements
2. WHEN explaining project suggestions, THE Explanation_Service SHALL describe how the project addresses skill gaps and unlocks opportunities
3. WHEN explaining skill priorities, THE Explanation_Service SHALL clarify why a skill has high priority based on impact and mandatory status
4. WHEN explaining career steps, THE Explanation_Service SHALL describe how a milestone builds toward the target role
5. WHEN generating explanations using AI, THE Explanation_Service SHALL provide relevant context including user data and recommendation details
6. WHEN creating explanations, THE Explanation_Service SHALL identify key factors with impact labels (positive, negative, neutral) and weights
7. WHEN validating explanations, THE Explanation_Service SHALL ensure key factor weights sum to approximately 1.0
8. WHEN generating actionable insights, THE Explanation_Service SHALL provide at least one specific, achievable action
9. WHEN calculating confidence, THE Explanation_Service SHALL base it on data quality and AI certainty
10. WHEN generating batch explanations, THE Explanation_Service SHALL process multiple requests efficiently
11. WHEN explanation text is generated, THE Explanation_Service SHALL ensure it is non-empty and student-friendly
12. IF AI response is malformed, THEN THE Explanation_Service SHALL attempt to clean the response and retry once before falling back to templates

### Requirement 6: Skill Progress and Career Readiness Prediction

**User Story:** As a student, I want predictions of my skill progress and career readiness, so that I can set realistic expectations and track my trajectory.

#### Acceptance Criteria

1. WHEN predicting skill progress, THE Prediction_Service SHALL use historical learning velocity to estimate future proficiency
2. WHEN calculating learning velocity, THE Prediction_Service SHALL analyze projects completed, average completion time, and skills verified per month
3. WHEN generating predictions, THE Prediction_Service SHALL ensure predicted proficiency is greater than or equal to current proficiency
4. WHEN generating predictions, THE Prediction_Service SHALL ensure predicted proficiency does not exceed 100
5. WHEN predicting far into the future, THE Prediction_Service SHALL decrease confidence scores for predictions beyond 12 weeks
6. WHEN predicting career readiness, THE Prediction_Service SHALL calculate current readiness score based on skill gaps and eligible internships
7. WHEN estimating readiness date, THE Prediction_Service SHALL consider required skills, current proficiency, and learning velocity
8. WHEN identifying required actions, THE Prediction_Service SHALL list specific skills to learn and projects to complete
9. WHEN calculating prediction confidence, THE Prediction_Service SHALL consider data quality and prediction distance
10. WHEN estimating project completion, THE Prediction_Service SHALL adjust base estimates using student's learning velocity
11. WHEN calculating learning trajectory, THE Prediction_Service SHALL identify acceleration trends (increasing, stable, decreasing)
12. WHEN all velocity metrics are calculated, THE Prediction_Service SHALL ensure they are non-negative
13. IF a student has insufficient historical data, THEN THE Prediction_Service SHALL return predictions with confidence below 30 percent

### Requirement 7: Data Validation and Consistency

**User Story:** As a system administrator, I want all data to be validated and consistent, so that the system produces reliable results.

#### Acceptance Criteria

1. WHEN creating skill gaps, THE System SHALL ensure gap_size equals target_proficiency minus current_proficiency
2. WHEN validating proficiency levels, THE System SHALL ensure all values are between 0 and 100 inclusive
3. WHEN validating priority scores, THE System SHALL ensure all values are between 0 and 100 inclusive
4. WHEN validating confidence scores, THE System SHALL ensure all values are between 0 and 100 inclusive
5. WHEN validating relevance scores, THE System SHALL ensure all values are between 0 and 100 inclusive
6. WHEN validating estimated hours, THE System SHALL ensure all values are positive
7. WHEN validating learning velocity metrics, THE System SHALL ensure all values are non-negative
8. WHEN validating milestone dependencies, THE System SHALL ensure all referenced milestone IDs exist in the roadmap
9. WHEN validating milestone order, THE System SHALL ensure dependencies have lower order numbers than dependents
10. WHEN validating skill-internship mappings, THE System SHALL ensure mandatory counts are less than or equal to total counts
11. WHEN validating proficiency ranges, THE System SHALL ensure minimum is less than or equal to average which is less than or equal to maximum

### Requirement 8: Error Handling and Recovery

**User Story:** As a student, I want the system to handle errors gracefully and provide helpful feedback, so that I can continue using the system even when issues occur.

#### Acceptance Criteria

1. IF the AI_Service is unavailable, THEN THE System SHALL return cached analysis if available and less than 24 hours old
2. IF the AI_Service is unavailable and no cache exists, THEN THE System SHALL fall back to rule-based recommendations
3. IF the AI_Service fails, THEN THE System SHALL retry with exponential backoff for up to 3 attempts
4. IF all AI retries fail, THEN THE System SHALL notify the student with message "AI recommendations temporarily unavailable"
5. IF a student has no profile data, THEN THE System SHALL suggest resume upload or manual skill entry
6. IF circular skill dependencies are detected, THEN THE System SHALL break cycles by removing lowest-weight edges and log a warning
7. IF AI returns malformed JSON, THEN THE System SHALL attempt to clean the response and retry once
8. IF JSON cleaning fails, THEN THE System SHALL fall back to template-based generation
9. IF a student has insufficient data for predictions, THEN THE System SHALL use platform averages and add disclaimers
10. IF roadmap generation times out, THEN THE System SHALL generate simplified roadmap using templates
11. WHEN errors occur, THE System SHALL log detailed information server-side without exposing internal details to students
12. WHEN returning error messages, THE System SHALL provide clear, actionable guidance to students

### Requirement 9: Performance and Optimization

**User Story:** As a student, I want fast responses from the system, so that I can efficiently explore career options without waiting.

#### Acceptance Criteria

1. WHEN performing skill gap analysis, THE System SHALL complete within 5 seconds
2. WHEN generating project suggestions, THE System SHALL complete within 10 seconds
3. WHEN generating career roadmaps, THE System SHALL complete within 30 seconds
4. WHEN generating explanations, THE System SHALL complete within 3 seconds
5. WHEN calculating predictions, THE System SHALL complete within 2 seconds
6. WHEN making multiple AI requests, THE System SHALL batch requests when possible
7. WHEN AI responses are received, THE System SHALL cache them for 24 hours
8. WHEN building internship graphs, THE System SHALL cache results and rebuild daily
9. WHEN querying frequently accessed data, THE System SHALL use indexed fields for user_id, internship_id, and skill_name
10. WHEN processing large result sets, THE System SHALL implement pagination

### Requirement 10: Security and Privacy

**User Story:** As a student, I want my profile data to be secure and private, so that my career information is protected.

#### Acceptance Criteria

1. WHEN storing user profile data, THE System SHALL encrypt data at rest
2. WHEN creating AI prompts, THE System SHALL sanitize inputs to remove personally identifiable information
3. WHEN a student requests data deletion, THE System SHALL remove all career intelligence data
4. WHEN logging AI interactions, THE System SHALL create audit logs for compliance
5. WHEN a student accesses career data, THE System SHALL verify the user_id matches the authenticated user
6. WHEN receiving API requests, THE System SHALL enforce rate limiting of 10 requests per minute per user
7. WHEN validating inputs, THE System SHALL check all user_id and internship_id references exist
8. WHEN validating inputs, THE System SHALL sanitize skill names to prevent injection attacks
9. WHEN validating inputs, THE System SHALL limit list sizes to maximum 100 items
10. WHEN AI generates content, THE System SHALL validate responses before storage and filter harmful content
11. WHEN errors occur, THE System SHALL return generic error messages without exposing internal details
