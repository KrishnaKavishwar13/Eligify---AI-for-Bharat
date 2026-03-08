# New User Onboarding Flow Bugfix Design

## Overview

This bugfix addresses the issue where new users are incorrectly initialized with 7 mock skills during sign-up, preventing the first-time user onboarding flow from displaying. The fix involves modifying the `sign_up` method in `auth_service.py` to create an empty skill graph instead of pre-populating it with sample data. This ensures the dashboard's onboarding condition (`totalSkills === 0`) triggers correctly, guiding new users to upload their resume for AI-powered skill extraction.

## Glossary

- **Bug_Condition (C)**: The condition that triggers the bug - when a new user signs up and receives pre-populated mock skills
- **Property (P)**: The desired behavior - new users should have an empty skill graph (`totalSkills: 0`) to trigger the onboarding flow
- **Preservation**: Existing user creation logic, profile initialization, and skill management functionality that must remain unchanged
- **sign_up**: The method in `backend/src/services/auth_service.py` (line 29) that handles new user registration
- **skill_graph_data**: The data structure containing a user's skills, totalSkills count, and verifiedSkills count
- **totalSkills**: The count property that determines whether the onboarding flow should display (triggers when === 0)

## Bug Details

### Fault Condition

The bug manifests when a new user completes the sign-up process. The `sign_up` method in `auth_service.py` creates a skill graph with 7 pre-populated mock skills (Python, JavaScript, React, FastAPI, SQL, Git, Communication), setting `totalSkills: 7` and `verifiedSkills: 5`. This prevents the dashboard onboarding flow from ever triggering since it requires `totalSkills === 0`.

**Formal Specification:**
```
FUNCTION isBugCondition(input)
  INPUT: input of type SignUpRequest with fields (email, password, name)
  OUTPUT: boolean
  
  RETURN input.isNewUserSignUp == true
         AND skillGraphCreated(input.userId)
         AND skillGraph.totalSkills > 0
         AND skillGraph.skills.length > 0
END FUNCTION
```

### Examples

- **Example 1**: User "Alice" signs up with email "alice@example.com"
  - Current behavior: Receives 7 mock skills, sees standard dashboard
  - Expected behavior: Receives 0 skills, sees onboarding flow prompting resume upload

- **Example 2**: User "Bob" signs up and immediately checks their dashboard
  - Current behavior: Dashboard shows Python (70%), JavaScript (65%), React (60%), etc.
  - Expected behavior: Dashboard shows onboarding widget: "Welcome! Upload your resume to get started"

- **Example 3**: User "Carol" signs up and the system checks `totalSkills === 0`
  - Current behavior: Condition evaluates to false (totalSkills is 7), onboarding skipped
  - Expected behavior: Condition evaluates to true (totalSkills is 0), onboarding displayed

- **Edge Case**: User signs up but the skill graph creation fails
  - Expected behavior: Sign-up should still succeed, but skill graph operations should be handled gracefully

## Expected Behavior

### Preservation Requirements

**Unchanged Behaviors:**
- User record creation with hashed password, unique user_id, role assignment, and email verification must continue to work exactly as before
- Profile data initialization with personalInfo, education, experience, projects, and certifications must remain unchanged
- Existing users with skills already in their profiles must continue to see the standard dashboard view
- Resume upload and AI skill extraction functionality must continue to work for all users
- Manual skill addition and editing must continue to function correctly
- The skill graph data structure and schema must remain compatible with existing code

**Scope:**
All inputs that do NOT involve new user sign-up should be completely unaffected by this fix. This includes:
- Existing user sign-in operations
- Resume upload and skill extraction for users with existing accounts
- Manual skill management (add, edit, delete) operations
- Profile updates and data retrieval
- Token refresh and authentication flows

## Hypothesized Root Cause

Based on the bug description and code analysis, the root cause is clear:

1. **Intentional Mock Data Population**: The `sign_up` method (lines 95-193 in auth_service.py) explicitly creates 7 mock skills with hardcoded values during user registration. This was likely added for development/testing purposes but should not be present in production code.

2. **Hardcoded Skill Array**: The skill_graph_data structure contains a hardcoded array of 7 skill objects with predefined names, categories, proficiency levels, and statuses.

3. **Incorrect Initial Counts**: The `totalSkills: 7` and `verifiedSkills: 5` values are set based on the mock data, preventing the onboarding condition from ever being true.

4. **No Conditional Logic**: There is no flag or environment variable to disable mock data population, meaning all new users receive these skills regardless of environment or intent.

## Correctness Properties

Property 1: Fault Condition - Empty Skill Graph Initialization

_For any_ new user sign-up request where the user does not already exist in the system, the fixed sign_up function SHALL create a skill graph with an empty skills array, `totalSkills: 0`, and `verifiedSkills: 0`, allowing the dashboard onboarding flow to trigger correctly.

**Validates: Requirements 2.1, 2.2, 2.3**

Property 2: Preservation - Existing User Creation Logic

_For any_ new user sign-up request, the fixed sign_up function SHALL continue to create the user record, profile data, and all other initialization logic exactly as before, preserving password hashing, user_id generation, role assignment, email verification, and profile structure initialization.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

## Fix Implementation

### Changes Required

**File**: `backend/src/services/auth_service.py`

**Function**: `sign_up` (line 29)

**Specific Changes**:

1. **Remove Mock Skills Array**: Delete the hardcoded skills array (lines ~95-190) containing the 7 mock skills (Python, JavaScript, React, FastAPI, SQL, Git, Communication)

2. **Initialize Empty Skills Array**: Replace the populated skills array with an empty array: `"skills": []`

3. **Set Zero Counts**: Change `"totalSkills": 7` to `"totalSkills": 0` and `"verifiedSkills": 5` to `"verifiedSkills": 0`

4. **Preserve Timestamps**: Keep the `"lastUpdated": now` field unchanged

5. **Maintain Data Structure**: Ensure the skill_graph_data structure maintains all required fields (userId, skills, totalSkills, verifiedSkills, lastUpdated) with the same types and schema

**Modified Code Structure**:
```python
# Create default skill graph with empty skills
skill_graph_data = {
    "userId": user_id,
    "skills": [],  # Empty array instead of 7 mock skills
    "totalSkills": 0,  # Changed from 7
    "verifiedSkills": 0,  # Changed from 5
    "lastUpdated": now
}

mock_store.save_skill_graph(user_id, skill_graph_data)
```

## Testing Strategy

### Validation Approach

The testing strategy follows a two-phase approach: first, surface counterexamples that demonstrate the bug on unfixed code, then verify the fix works correctly and preserves existing behavior.

### Exploratory Fault Condition Checking

**Goal**: Surface counterexamples that demonstrate the bug BEFORE implementing the fix. Confirm that new users receive mock skills and the onboarding flow does not trigger.

**Test Plan**: Create test cases that simulate new user sign-up and verify that the skill graph contains mock skills. Run these tests on the UNFIXED code to observe the incorrect behavior and confirm the root cause.

**Test Cases**:
1. **New User Sign-Up Test**: Create a new user and verify skill graph contains 7 skills (will pass on unfixed code, should fail after fix)
2. **Total Skills Count Test**: Create a new user and verify `totalSkills === 7` (will pass on unfixed code, should fail after fix)
3. **Onboarding Condition Test**: Create a new user and verify `totalSkills === 0` evaluates to false (will pass on unfixed code, should fail after fix)
4. **Mock Skills Content Test**: Create a new user and verify skills include "Python", "JavaScript", "React" (will pass on unfixed code, should fail after fix)

**Expected Counterexamples**:
- New users have `totalSkills: 7` instead of `totalSkills: 0`
- New users have a populated skills array instead of an empty array
- Dashboard onboarding condition (`totalSkills === 0`) never evaluates to true for new users

### Fix Checking

**Goal**: Verify that for all new user sign-ups (where the bug condition holds), the fixed function produces the expected behavior.

**Pseudocode:**
```
FOR ALL input WHERE isBugCondition(input) DO
  result := sign_up_fixed(input.email, input.password, input.name)
  skillGraph := getSkillGraph(result.userId)
  ASSERT skillGraph.totalSkills == 0
  ASSERT skillGraph.verifiedSkills == 0
  ASSERT skillGraph.skills.length == 0
  ASSERT onboardingConditionTriggered(result.userId) == true
END FOR
```

### Preservation Checking

**Goal**: Verify that for all aspects of user creation that are NOT related to skill graph initialization, the fixed function produces the same result as the original function.

**Pseudocode:**
```
FOR ALL input WHERE isNewUserSignUp(input) DO
  result_original := sign_up_original(input.email, input.password, input.name)
  result_fixed := sign_up_fixed(input.email, input.password, input.name)
  
  ASSERT result_fixed.user.user_id EXISTS
  ASSERT result_fixed.user.password_hash == hash_password(input.password)
  ASSERT result_fixed.user.role == "STUDENT"
  ASSERT result_fixed.user.email_verified == true
  ASSERT result_fixed.profile.personalInfo.name == input.name
  ASSERT result_fixed.profile.education == []
  ASSERT result_fixed.profile.experience == []
  ASSERT result_fixed.profile.projects == []
  ASSERT result_fixed.profile.certifications == []
END FOR
```

**Testing Approach**: Property-based testing is recommended for preservation checking because:
- It generates many test cases automatically across different user inputs
- It catches edge cases that manual unit tests might miss (special characters in names, various email formats)
- It provides strong guarantees that user creation logic is unchanged for all valid inputs

**Test Plan**: Observe behavior on UNFIXED code first for user record creation, profile initialization, and authentication, then write property-based tests capturing that behavior.

**Test Cases**:
1. **User Record Preservation**: Verify user_id generation, password hashing, role assignment, and email verification continue to work identically
2. **Profile Initialization Preservation**: Verify profile data structure with personalInfo, education, experience, projects, certifications is created identically
3. **Authentication Flow Preservation**: Verify that newly created users can sign in successfully with their credentials
4. **Error Handling Preservation**: Verify that duplicate email detection and error responses work identically

### Unit Tests

- Test new user sign-up creates empty skill graph with `totalSkills: 0`
- Test new user sign-up creates empty skills array
- Test skill graph data structure contains all required fields
- Test that user record and profile creation remain unchanged
- Test edge cases: special characters in name, various email formats, minimum password length

### Property-Based Tests

- Generate random valid user credentials and verify all create empty skill graphs
- Generate random user data and verify user records are created with correct structure
- Generate random inputs and verify profile initialization matches expected schema
- Test that onboarding condition (`totalSkills === 0`) evaluates to true for all new users

### Integration Tests

- Test full sign-up flow: user creation → profile creation → skill graph creation → dashboard access
- Test that dashboard displays onboarding flow for new users with zero skills
- Test that resume upload after sign-up populates skills correctly
- Test that manual skill addition after sign-up works correctly
- Test that existing users with skills continue to see standard dashboard view
