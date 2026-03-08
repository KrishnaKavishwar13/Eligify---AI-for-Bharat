# Implementation Plan: Career Intelligence System

## Overview

This plan implements the AI-powered Career Intelligence System for Eligify, adding 6 new intelligent services that integrate with existing services to provide skill gap analysis, personalized project recommendations, career roadmaps, and explainable AI insights. The implementation follows a 4-phase approach over 7 weeks, building from core intelligence through personalization to career planning and final polish.

## Tasks

- [x] 1. Phase 1: Core Intelligence Services (Weeks 1-2)
  - [x] 1.1 Create Skill Gap Intelligence Service foundation
    - Create `backend/src/services/skill_gap_intelligence_service.py`
    - Implement data models: `SkillGapAnalysis`, `SkillGap`, `PrioritizedSkill`, `CurrentProfile`
    - Implement `analyze_profile()` method with profile aggregation from existing services
    - Implement `calculate_priority_score()` helper function
    - Implement `topological_sort_skills()` for dependency-aware learning paths
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 1.10, 1.11, 1.12, 1.13_

  - [ ]* 1.2 Write property test for Skill Gap Intelligence
    - **Property 1: Skill Gap Consistency**
    - **Validates: Requirements 1.5, 7.1, 7.2**

  - [x] 1.3 Implement skill gap priority and readiness calculations
    - Implement `get_skill_priorities()` method
    - Implement `calculate_readiness_score()` method
    - Add integration with `internship_mapping_service` for impact calculations
    - _Requirements: 1.6, 1.7, 1.8_

  - [ ]* 1.4 Write property test for priority score bounds
    - **Property 2: Priority Score Bounds**
    - **Validates: Requirements 1.6, 7.3**

  - [x] 1.5 Create Internship Mapping Service
    - Create `backend/src/services/internship_mapping_service.py`
    - Implement data models: `InternshipSkillGraph`, `SkillInternshipMapping`, `InternshipCluster`, `SkillDependency`
    - Implement `build_skill_internship_graph()` method
    - Implement `get_internships_by_skill()` method
    - Implement `find_skill_clusters()` method
    - Implement `get_skill_dependencies()` method
    - Implement `calculate_skill_impact()` method
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 2.10, 2.11_

  - [ ]* 1.6 Write property test for skill-internship mapping consistency
    - **Property 4: Skill-Internship Mapping Consistency**
    - **Validates: Requirements 2.8, 2.9, 7.10, 7.11**

  - [x] 1.7 Add API endpoints for core intelligence
    - Create `backend/src/routes/intelligence.py`
    - Implement `POST /api/v1/intelligence/analyze-profile` endpoint
    - Implement `GET /api/v1/intelligence/skill-priorities/{user_id}` endpoint
    - Implement `GET /api/v1/intelligence/internship-graph` endpoint
    - Add request validation and error handling
    - Register routes in main FastAPI app
    - _Requirements: 1.1-1.13, 2.1-2.11, 8.1-8.12, 10.1-10.11_

  - [ ]* 1.8 Write unit tests for core intelligence services
    - Test priority score calculation with various gap sizes
    - Test topological sort with dependencies and cycles
    - Test graph building with overlapping skills
    - Test skill clustering algorithms
    - Test with empty/minimal user profiles
    - _Requirements: 1.1-1.13, 2.1-2.11_

- [x] 2. Checkpoint - Core Intelligence Complete
  - Ensure all tests pass, verify API endpoints work with existing services, ask the user if questions arise.

- [x] 3. Phase 2: Personalization and Prediction Services (Weeks 3-4)
  - [x] 3.1 Create Personalization Service foundation
    - Create `backend/src/services/personalization_service.py`
    - Implement data models: `PersonalizationContext`, `PersonalizedProjectSuggestion`, `LearningVelocityMetrics`
    - Implement `suggest_projects()` method with AI integration
    - Implement `calculate_relevance_score()` helper function
    - Implement difficulty matching logic (beginner/intermediate/advanced)
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13_

  - [ ]* 3.2 Write property test for personalization relevance
    - **Property 5: Personalization Relevance**
    - **Validates: Requirements 3.4, 3.5, 3.11, 7.5, 7.6**

  - [x] 3.3 Implement project ranking and adaptation
    - Implement `rank_projects()` method
    - Implement `adapt_project_difficulty()` method
    - Implement `calculate_learning_velocity()` method
    - Add internship unlocking simulation logic
    - _Requirements: 3.2, 3.8, 3.12, 3.13_

  - [ ]* 3.4 Write property test for learning velocity non-negativity
    - **Property 9: Learning Velocity Non-Negativity**
    - **Validates: Requirements 3.12, 6.2, 6.12, 7.7**

  - [x] 3.5 Create Prediction Service
    - Create `backend/src/services/prediction_service.py`
    - Implement data models: `SkillProgressPrediction`, `CareerReadinessPrediction`
    - Implement `predict_skill_progress()` method
    - Implement `predict_career_readiness()` method
    - Implement `estimate_project_completion()` method
    - Implement `calculate_learning_trajectory()` method
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.10, 6.11, 6.12, 6.13_

  - [ ]* 3.6 Write property test for prediction monotonicity
    - **Property 6: Prediction Monotonicity**
    - **Validates: Requirements 6.3, 6.4, 6.5, 6.9_

  - [x] 3.7 Add API endpoints for personalization and prediction
    - Implement `POST /api/v1/intelligence/suggest-projects` endpoint
    - Implement `GET /api/v1/intelligence/predict/skill-progress/{user_id}/{skill_name}` endpoint
    - Implement `GET /api/v1/intelligence/predict/career-readiness/{user_id}/{target_role}` endpoint
    - Add request validation and error handling
    - _Requirements: 3.1-3.13, 6.1-6.13, 8.1-8.12, 9.1-9.10, 10.1-10.11_

  - [ ]* 3.8 Write unit tests for personalization and prediction
    - Test relevance score calculation
    - Test difficulty matching logic
    - Test learning velocity calculations with various histories
    - Test prediction confidence intervals
    - Test with insufficient historical data
    - _Requirements: 3.1-3.13, 6.1-6.13_

- [x] 4. Checkpoint - Personalization Complete
  - Ensure all tests pass, verify project suggestions are relevant, ask the user if questions arise.

- [x] 5. Phase 3: Career Planning and Explanation Services (Weeks 5-6)
  - [x] 5.1 Create Career Path Service foundation
    - Create `backend/src/services/career_path_service.py`
    - Implement data models: `CareerRoadmap`, `RoadmapMilestone`, `CareerGoal`, `CurrentPosition`
    - Implement `generate_roadmap()` method with AI integration
    - Implement milestone enrichment with project suggestions and internship targets
    - Implement milestone dependency validation (DAG check)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.10, 4.11, 4.12, 4.13, 4.14, 4.15_

  - [ ]* 5.2 Write property test for learning path dependencies
    - **Property 3: Learning Path Dependency**
    - **Validates: Requirements 4.6, 4.13, 4.14, 7.8, 7.9_

  - [x] 5.3 Implement roadmap progress tracking
    - Implement `update_roadmap_progress()` method
    - Implement `suggest_next_steps()` method
    - Implement `estimate_timeline()` method
    - Implement progress percentage calculation
    - _Requirements: 4.11, 4.12, 4.13_

  - [ ]* 5.4 Write property test for roadmap progress consistency
    - **Property 8: Roadmap Progress Consistency**
    - **Validates: Requirements 4.11, 4.12_

  - [x] 5.5 Create Explanation Service
    - Create `backend/src/services/explanation_service.py`
    - Implement data models: `Explanation`, `ExplanationFactor`, `ExplanationType`
    - Implement `explain_internship_match()` method
    - Implement `explain_project_suggestion()` method
    - Implement `explain_skill_priority()` method
    - Implement `explain_career_step()` method
    - Implement `generate_batch_explanations()` method
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 5.11, 5.12_

  - [ ]* 5.6 Write property test for explanation completeness
    - **Property 7: Explanation Completeness**
    - **Validates: Requirements 5.6, 5.7, 5.8, 5.11_

  - [x] 5.7 Add API endpoints for career planning and explanations
    - Implement `POST /api/v1/intelligence/career-roadmap` endpoint
    - Implement `PUT /api/v1/intelligence/career-roadmap/{roadmap_id}/progress` endpoint
    - Implement `GET /api/v1/intelligence/next-steps/{user_id}/{roadmap_id}` endpoint
    - Implement `POST /api/v1/intelligence/explain` endpoint
    - Add request validation and error handling
    - _Requirements: 4.1-4.15, 5.1-5.12, 8.1-8.12, 10.1-10.11_

  - [ ]* 5.8 Write unit tests for career planning and explanations
    - Test milestone ordering and dependencies
    - Test roadmap progress tracking
    - Test explanation generation for each type
    - Test factor weight normalization
    - Test with various match scores and contexts
    - _Requirements: 4.1-4.15, 5.1-5.12_

- [x] 6. Checkpoint - Career Planning Complete
  - Ensure all tests pass, verify roadmaps are coherent and actionable, ask the user if questions arise.

- [ ] 7. Phase 4: Error Handling, Optimization, and Integration (Week 7)
  - [ ] 7.1 Implement comprehensive error handling
    - Add AI service unavailable fallback with caching (24 hours)
    - Add rule-based recommendations fallback
    - Implement exponential backoff retry logic (3 attempts)
    - Add circular dependency detection and cycle breaking
    - Add AI response parsing with JSON cleaning and retry
    - Add insufficient data handling with platform averages
    - Add roadmap generation timeout handling (30 seconds)
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 8.10, 8.11, 8.12_

  - [ ]* 7.2 Write integration tests for error recovery
    - Test AI service failure scenarios
    - Test retry logic and backoff
    - Test cached data usage
    - Test fallback mechanisms
    - Test user-facing error messages
    - _Requirements: 8.1-8.12_

  - [ ] 7.3 Implement performance optimizations
    - Add AI response caching (24 hours)
    - Implement batch AI request processing
    - Add skill-internship graph caching (daily rebuild)
    - Add database query indexing for user_id, internship_id, skill_name
    - Implement pagination for large result sets
    - Add memoization for priority score and topological sort
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 9.10_

  - [ ]* 7.4 Write performance tests
    - Test skill gap analysis completes in < 5 seconds
    - Test project suggestion completes in < 10 seconds
    - Test career roadmap generation completes in < 30 seconds
    - Test explanation generation completes in < 3 seconds
    - Test prediction calculation completes in < 2 seconds
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ] 7.5 Implement security and validation
    - Add input validation for all API endpoints
    - Add user_id authentication checks
    - Implement rate limiting (10 requests/minute per user)
    - Add AI response content filtering
    - Add input sanitization for skill names and user inputs
    - Add list size limits (max 100 items)
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 10.10, 10.11_

  - [ ]* 7.6 Write security tests
    - Test authentication enforcement
    - Test rate limiting
    - Test input validation and sanitization
    - Test error message sanitization
    - Test AI content filtering
    - _Requirements: 10.1-10.11_

  - [ ] 7.7 Add comprehensive integration tests
    - Test complete career intelligence flow (resume → gaps → projects → roadmap)
    - Test skill gap to project suggestion flow
    - Test roadmap progress tracking flow
    - Test explanation generation consistency
    - Test prediction accuracy with simulated data
    - Verify data consistency across all services
    - _Requirements: 1.1-10.11_

  - [ ]* 7.8 Write property test for internship unlocking accuracy
    - **Property 10: Internship Unlocking Accuracy**
    - **Validates: Requirements 3.7, 3.8_

  - [ ] 7.9 Add missing dependencies and update configuration
    - Add `networkx` to requirements.txt for graph algorithms
    - Add `numpy` to requirements.txt for numerical computations
    - Add `hypothesis` to dev requirements for property-based testing
    - Update API documentation with new endpoints
    - Add configuration for caching and rate limiting
    - _Requirements: All_

- [ ] 8. Final Checkpoint - System Complete
  - Run full test suite, verify all performance targets met, verify all API endpoints documented, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional testing tasks and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation after each phase
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- Integration tests verify end-to-end flows across services
- The implementation preserves existing Eligify architecture patterns
- All new services integrate with existing ai_service, eligibility_service, skill_service, project_service
- AI calls use Ollama with Llama 3.1 8B model
- Data storage uses mock_store initially (DynamoDB migration separate)
- Performance targets: skill gap < 5s, projects < 10s, roadmap < 30s, explanations < 3s, predictions < 2s
