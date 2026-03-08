# Implementation Plan

- [x] 1. Write bug condition exploration test
  - **Property 1: Fault Condition** - Empty Skill Graph Initialization
  - **CRITICAL**: This test MUST FAIL on unfixed code - failure confirms the bug exists
  - **DO NOT attempt to fix the test or the code when it fails**
  - **NOTE**: This test encodes the expected behavior - it will validate the fix when it passes after implementation
  - **GOAL**: Surface counterexamples that demonstrate the bug exists
  - **Scoped PBT Approach**: Scope the property to new user sign-up scenarios with valid credentials
  - Test that new user sign-up creates skill graph with totalSkills > 0 and populated skills array (from Fault Condition in design)
  - The test assertions should verify: `totalSkills == 0`, `verifiedSkills == 0`, `skills.length == 0`, and onboarding condition triggers
  - Run test on UNFIXED code
  - **EXPECTED OUTCOME**: Test FAILS (this is correct - it proves the bug exists)
  - Document counterexamples found (e.g., "New user receives 7 mock skills instead of 0", "totalSkills is 7 instead of 0")
  - Mark task complete when test is written, run, and failure is documented
  - _Requirements: 2.1, 2.2, 2.3_

- [x] 2. Write preservation property tests (BEFORE implementing fix)
  - **Property 2: Preservation** - Existing User Creation Logic
  - **IMPORTANT**: Follow observation-first methodology
  - Observe behavior on UNFIXED code for user record creation, profile initialization, and authentication flows
  - Write property-based tests capturing observed behavior patterns from Preservation Requirements
  - Test that user_id generation, password hashing, role assignment, email verification work correctly
  - Test that profile data structure (personalInfo, education, experience, projects, certifications) is initialized correctly
  - Test that newly created users can sign in successfully with their credentials
  - Test that duplicate email detection and error responses work correctly
  - Property-based testing generates many test cases for stronger guarantees
  - Run tests on UNFIXED code
  - **EXPECTED OUTCOME**: Tests PASS (this confirms baseline behavior to preserve)
  - Mark task complete when tests are written, run, and passing on unfixed code
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 3. Fix for new user onboarding flow bug

  - [x] 3.1 Implement the fix in auth_service.py
    - Remove the 7 hardcoded mock skills array (lines ~95-190) containing Python, JavaScript, React, FastAPI, SQL, Git, Communication
    - Initialize empty skills array: `"skills": []`
    - Set zero counts: `"totalSkills": 0` and `"verifiedSkills": 0`
    - Preserve timestamps: Keep `"lastUpdated": now` field unchanged
    - Maintain data structure: Ensure skill_graph_data contains all required fields (userId, skills, totalSkills, verifiedSkills, lastUpdated)
    - _Bug_Condition: isBugCondition(input) where input.isNewUserSignUp == true AND skillGraphCreated(input.userId) AND skillGraph.totalSkills > 0_
    - _Expected_Behavior: skillGraph.totalSkills == 0 AND skillGraph.verifiedSkills == 0 AND skillGraph.skills.length == 0 AND onboardingConditionTriggered == true_
    - _Preservation: User record creation, profile initialization, authentication flows, error handling must remain unchanged_
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 3.2 Verify bug condition exploration test now passes
    - **Property 1: Expected Behavior** - Empty Skill Graph Initialization
    - **IMPORTANT**: Re-run the SAME test from task 1 - do NOT write a new test
    - The test from task 1 encodes the expected behavior
    - When this test passes, it confirms the expected behavior is satisfied
    - Run bug condition exploration test from step 1
    - **EXPECTED OUTCOME**: Test PASSES (confirms bug is fixed)
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 3.3 Verify preservation tests still pass
    - **Property 2: Preservation** - Existing User Creation Logic
    - **IMPORTANT**: Re-run the SAME tests from task 2 - do NOT write new tests
    - Run preservation property tests from step 2
    - **EXPECTED OUTCOME**: Tests PASS (confirms no regressions)
    - Confirm all tests still pass after fix (no regressions)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [x] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.
