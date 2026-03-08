# Bugfix Requirements Document

## Introduction

New users who sign up for the application are incorrectly receiving pre-populated mock data (7 sample skills including Python, JavaScript, React, FastAPI, SQL, Git, and Communication) in their accounts immediately upon registration. This prevents the intended first-time user onboarding experience from being displayed, as the dashboard's onboarding flow only triggers when `totalSkills === 0`, which never occurs with the current implementation.

The bug impacts user experience by:
- Showing users skills they may not possess
- Bypassing the intended onboarding flow that guides users to upload their resume
- Creating confusion about the source of the pre-populated data
- Preventing the AI-powered skill extraction workflow from being the primary data source

## Bug Analysis

### Current Behavior (Defect)

1.1 WHEN a new user completes the sign-up process THEN the system automatically creates 7 mock skills (Python, JavaScript, React, FastAPI, SQL, Git, Communication) with predefined proficiency levels in their skill graph

1.2 WHEN a new user accesses the dashboard after sign-up THEN the system displays the standard dashboard view with mock skills instead of the first-time user onboarding flow

1.3 WHEN a new user's skill graph is initialized THEN the system sets `totalSkills: 7` and `verifiedSkills: 5`, preventing the onboarding condition (`totalSkills === 0`) from ever being true

### Expected Behavior (Correct)

2.1 WHEN a new user completes the sign-up process THEN the system SHALL create an empty skill graph with `totalSkills: 0` and `verifiedSkills: 0` and no pre-populated skills

2.2 WHEN a new user accesses the dashboard after sign-up THEN the system SHALL display the first-time user onboarding flow that prompts them to upload their resume

2.3 WHEN a new user's skill graph is initialized THEN the system SHALL create an empty skills array, allowing the onboarding condition to trigger correctly

### Unchanged Behavior (Regression Prevention)

3.1 WHEN a user already has skills in their profile (from resume upload or manual entry) THEN the system SHALL CONTINUE TO display the standard dashboard view with their actual skills

3.2 WHEN a user uploads a resume THEN the system SHALL CONTINUE TO extract and populate skills using the AI extraction service

3.3 WHEN a user manually adds skills THEN the system SHALL CONTINUE TO save those skills to their skill graph

3.4 WHEN the profile data structure is created during sign-up THEN the system SHALL CONTINUE TO initialize all required fields (personalInfo, education, experience, projects, certifications) with empty arrays or null values as appropriate

3.5 WHEN the user data structure is created during sign-up THEN the system SHALL CONTINUE TO hash the password, generate a unique user_id, set the role to STUDENT, and mark email as verified for local development
