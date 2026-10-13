# Phase 3: Continuous Testing Using JUnit 5, Mockito, Maven, and Jenkins

**Course / Lab**: DevOps Lab CAT Project  
**Project**: IT Helpdesk and Ticket Management System  
**Date**: October 2026  
**Status**: COMPLETED & VERIFIED LIVE  

---

## 1. Aim and Objectives

### Aim
To implement an enterprise automated testing suite using JUnit 5 and Mockito for the Spring Boot backend service, configure automated code coverage metrics with JaCoCo, and establish a declarative Jenkins Continuous Integration (CI) pipeline that enforces quality gates before Docker image construction.

### Objectives
1. **Unit Testing with JUnit 5 & Mockito**: Test business logic across service and controller layers in total isolation without relying on production databases.
2. **Comprehensive Negative & Edge Testing**: Validate security constraints, role-based access limits (Employee vs. Support vs. Admin), input validation failures, and illegal state transitions.
3. **Automated Coverage Reporting**: Configure `jacoco-maven-plugin` to analyze branch, line, and instruction coverage.
4. **Declarative CI Pipeline**: Define a multi-stage `Jenkinsfile` orchestrating source checkout, runtime validation, backend compilation, test execution, frontend compilation, Docker Compose validation, and image building.
5. **Quality Gates & Artifact Archiving**: Ensure pipeline execution halts immediately upon test failure, collects JUnit XML reports via Surefire, and archives production artifacts.

---

## 2. Why Continuous Testing is Essential in DevOps

Continuous Testing is the practice of executing automated tests as part of the software delivery pipeline to obtain immediate feedback on business risks:
- **Shift-Left Testing**: Defects are caught during compilation and unit testing rather than in production containers.
- **Regression Prevention**: Ensures new feature additions (such as ticket assignment or comments) do not silently break existing functionality.
- **Automated Quality Gates**: Prevents defective code from triggering downstream container builds or Ansible configuration rollouts.
- **Auditability**: Produces verifiable XML and HTML test execution records for compliance and academic evaluation.

---

## 3. Core Testing Technologies: JUnit 5 vs. Mockito

### 3.1 JUnit 5 (Jupiter Engine)
JUnit 5 is the standard testing framework for modern Java applications:
- **`@Test`**: Marks a method as an automated test case.
- **`@BeforeEach`**: Initializes test fixtures prior to each test invocation.
- **`assertNotNull()`, `assertEquals()`, `assertTrue()`, `assertThrows()`**: Fluent assertions that validate expected values and exception triggers.

### 3.2 Mockito
Mockito provides mock objects to simulate real dependencies:
- **`@Mock`**: Creates a dummy instance of a collaborator (e.g., `TicketRepository`, `UserRepository`, `PasswordEncoder`).
- **`@InjectMocks`**: Injects mock collaborators into the target class under test (e.g., `TicketService`, `AuthService`).
- **`when(...).thenReturn(...)`**: Stubs method behavior for deterministic outcomes.
- **`verify(..., times(1))`**: Asserts that an essential interaction actually occurred.
- **`never()`**: Asserts that a sensitive method (such as `save()`) was NOT invoked during validation errors or unauthorized requests.

### 3.3 Unit Tests vs. Integration Tests
| Aspect | Unit Tests (Implemented Here) | Integration Tests |
| :--- | :--- | :--- |
| **Scope** | Single class / method in isolation | Multiple layers working together |
| **Dependencies** | All external dependencies mocked | In-memory DB (H2) or test containers |
| **Execution Speed** | Milliseconds (< 1 sec for entire suite) | Seconds to minutes |
| **Failure Isolation** | Pinpoints exact broken line of code | Can fail due to DB, network, or config |
| **CI Role** | Fast-feedback gate (runs first) | Secondary gate before staging deploy |

---

## 4. Test Suite Implementation Breakdown

The automated test suite contains **43 unit and controller tests** organized into 7 test classes:

### 4.1 Service Layer Tests (`src/test/java/com/devops/ithelpdesk/service/`)

1. **`AuthServiceTest.java` (8 Tests)**:
   - `register_SuccessfullyCreatesEmployeeAccount`: Verifies employee user creation with BCrypt hashed password.
   - `register_ThrowsExceptionWhenEmailAlreadyExists`: Ensures duplicate registration throws `BadRequestException`.
   - `login_ReturnsJwtTokenForValidCredentials`: Asserts valid login returns signed JWT token, user ID, and role.
   - `login_ThrowsBadCredentialsExceptionWhenPasswordIsInvalid`: Verifies invalid password triggers authentication rejection.
   - `login_ThrowsUnauthorizedExceptionWhenUserNotFoundInRepository`: Verifies unknown user email is rejected.
   - `getCurrentAuthenticatedUser_ReturnsUserWhenAuthenticated`: Validates extraction of authenticated principal from SecurityContext.
   - `getCurrentAuthenticatedUser_ThrowsUnauthorizedExceptionWhenNotAuthenticated`: Rejects unauthenticated requests.
   - `getCurrentAuthenticatedUser_ThrowsUnauthorizedExceptionWhenAnonymous`: Rejects anonymous guest principals.

2. **`TicketServiceTest.java` (13 Tests)**:
   - `createTicket_GeneratesUniqueTicketCodeAndSetsOpenStatus`: Ensures ticket code matches `HD-XXXX` and status defaults to `OPEN`.
   - `getTicketById_ReturnsTicketWhenAdminOrSupportViewsAnyTicket`: Asserts Support and Admin can view any ticket.
   - `getTicketById_ThrowsAccessDeniedWhenEmployeeViewsOtherEmployeeTicket`: Enforces privacy isolation across employees.
   - `getTicketById_ThrowsResourceNotFoundWhenIdDoesNotExist`: Returns 404 error when ticket ID is invalid.
   - `getTickets_PassesUserIdFilterForEmployee`: Verifies employee ticket lists are scoped to their own user ID.
   - `getTickets_PassesNullUserIdFilterForAdmin`: Verifies Admin ticket lists query all tickets without employee filter.
   - `assignTicket_UpdatesAssignedStaffAndTransitionsOpenToInProgress`: Asserts assignment to support moves `OPEN` tickets to `IN_PROGRESS`.
   - `assignTicket_PreservesStatusWhenTicketAlreadyInProgress`: Asserts assignment does not overwrite an active ticket's state.
   - `assignTicket_ThrowsAccessDeniedWhenAttemptedByEmployee`: Rejects ticket assignment attempts made by employees.
   - `updateTicketStatus_ResolvesTicketAndSetsResolvedAt`: Verifies transitioning to `RESOLVED` timestamps `resolvedAt`.
   - `updateTicketStatus_AllowsEmployeeToCloseOwnResolvedTicket`: Allows employees to close their own resolved tickets.
   - `updateTicketStatus_ThrowsAccessDeniedWhenEmployeeChangesToInProgress`: Forbids employees from advancing tickets directly.
   - `updateTicketStatus_ReopeningTicketClearsResolvedAt`: Ensures setting status back to `IN_PROGRESS` nullifies `resolvedAt`.

3. **`CommentServiceTest.java` (7 Tests)**:
   - `addComment_SuccessfullyAddsPublicCommentForOwnerEmployee`: Validates public comment creation.
   - `addComment_ThrowsAccessDeniedWhenEmployeeCommentsOnAnotherEmployeesTicket`: Forbids employees from commenting on others' tickets.
   - `addComment_AllowsStaffToCreateInternalNote`: Asserts Support staff can mark notes as internal.
   - `addComment_ForcesInternalNoteFalseWhenAuthorIsEmployee`: Forbids employees from creating internal notes even if requested.
   - `getComments_FiltersOutInternalNotesWhenCurrentUserIsEmployee`: Asserts internal staff notes are hidden from employees.
   - `getComments_IncludesInternalNotesWhenCurrentUserIsStaff`: Asserts Support staff can view all public and internal comments.
   - `getComments_ThrowsAccessDeniedWhenEmployeeViewsAnotherEmployeesComments`: Prevents unauthorized comment viewing.

4. **`UserServiceTest.java` (3 Tests)**:
   - `getSupportStaff_ReturnsOnlyAdminAndSupportUsers`: Verifies user filtering returns only staff with `ROLE_ADMIN` and `ROLE_SUPPORT`.
   - `getUserById_ReturnsUserResponseWhenUserExists`: Returns DTO when ID exists.
   - `findEntityById_ThrowsResourceNotFoundExceptionWhenUserNotFound`: Throws 404 when ID does not exist.

5. **`DashboardServiceTest.java` (2 Tests)**:
   - `getStats_ReturnsEmployeeSpecificMetricsWhenRoleIsEmployee`: Verifies counts are restricted to tickets owned by the employee.
   - `getStats_ReturnsGlobalSystemMetricsWhenRoleIsAdminOrSupport`: Verifies counts aggregate all tickets across the enterprise.

### 4.2 Controller MockMvc Tests (`src/test/java/com/devops/ithelpdesk/controller/`)

6. **`AuthControllerTest.java` (5 Tests)**:
   - `login_Returns200AndTokenForValidPayload`: Validates HTTP 200 and JSON structure.
   - `login_Returns400BadRequestWhenEmailIsInvalid`: Validates `@Email` constraint rejection with HTTP 400.
   - `login_Returns400BadRequestWhenPasswordIsBlank`: Validates `@NotBlank` constraint rejection.
   - `register_Returns201CreatedForValidPayload`: Validates HTTP 201 Created.
   - `register_Returns400BadRequestWhenFullNameIsBlank`: Validates required name rejection.

7. **`TicketControllerTest.java` (5 Tests)**:
   - `createTicket_Returns201CreatedForValidPayload`: Validates ticket creation HTTP 201.
   - `createTicket_Returns400BadRequestWhenTitleIsTooShort`: Validates `@Size(min=3)` rejects 2-character titles with HTTP 400.
   - `getTicketById_Returns200AndTicket`: Validates retrieval endpoint.
   - `updateStatus_Returns200ForValidPayload`: Validates PUT `/api/tickets/{id}/status`.
   - `assignTicket_Returns200ForValidPayload`: Validates PUT `/api/tickets/{id}/assign`.

---

## 5. Actual Maven Test Execution & Surefire Report Results

Command executed from `backend/`:
```bash
mvn test
```

### Observed Execution Log:
```text
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.devops.ithelpdesk.controller.AuthControllerTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 7.443 s
[INFO] Running com.devops.ithelpdesk.controller.TicketControllerTest
[INFO] Tests run: 5, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.659 s
[INFO] Running com.devops.ithelpdesk.service.AuthServiceTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.960 s
[INFO] Running com.devops.ithelpdesk.service.CommentServiceTest
[INFO] Tests run: 7, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.217 s
[INFO] Running com.devops.ithelpdesk.service.DashboardServiceTest
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.196 s
[INFO] Running com.devops.ithelpdesk.service.TicketServiceTest
[INFO] Tests run: 13, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.162 s
[INFO] Running com.devops.ithelpdesk.service.UserServiceTest
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0, Time elapsed: 0.025 s
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: 43, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] --- jacoco:0.8.11:report (report) @ it-helpdesk-backend ---
[INFO] Loading execution data file backend\target\jacoco.exec
[INFO] Analyzed bundle 'IT Helpdesk and Ticket Management System' with 40 classes
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] Total time:  23.801 s
```

### Generated Surefire Reports Directory:
- Path: `backend/target/surefire-reports/`
- Report files:
  - `TEST-com.devops.ithelpdesk.controller.AuthControllerTest.xml`
  - `TEST-com.devops.ithelpdesk.controller.TicketControllerTest.xml`
  - `TEST-com.devops.ithelpdesk.service.AuthServiceTest.xml`
  - `TEST-com.devops.ithelpdesk.service.CommentServiceTest.xml`
  - `TEST-com.devops.ithelpdesk.service.DashboardServiceTest.xml`
  - `TEST-com.devops.ithelpdesk.service.TicketServiceTest.xml`
  - `TEST-com.devops.ithelpdesk.service.UserServiceTest.xml`

### JaCoCo Code Coverage Report:
- Path: `backend/target/site/jacoco/index.html`
- Execution Data: `backend/target/jacoco.exec`
- Data CSV: `backend/target/site/jacoco/jacoco.csv`

---

## 6. Jenkins Architecture & Environment Inspection

### 6.1 Current Verified Host State
- **Jenkins Controller**: Windows Service (`C:\Program Files\Jenkins\jenkins.exe`)
- **Status**: Running (`Status: 200 OK`)
- **Version**: **Jenkins 2.568.2**
- **Web Server Engine**: Embedded Winstone / Jetty 12.1.8
- **Port Allocation**:
  - `8080`: Jenkins Web Controller
  - `8088`: Spring Boot Backend (Docker Container)
  - `80`: React / Nginx Frontend (Docker Container)
  - `3306`: MySQL Database (Docker Container)
- **Runtimes on Host**:
  - Java: `21.0.11 LTS` (Oracle JDK)
  - Maven: `3.9.6`
  - Node.js: `v22.20.0`
  - Docker Desktop: Engine `29.8.2`, Compose `v5.6.0`

---

## 7. Declarative Jenkinsfile Implementation

The root [Jenkinsfile](file:///C:/DevopsCat/IT-Helpdesk/Jenkinsfile) is written in standard Jenkins Declarative Pipeline syntax with dual-OS compatibility (`isUnix()` conditional):

```groovy
pipeline {
    agent any

    environment {
        APP_NAME = 'it-helpdesk'
        APP_VERSION = '1.0.0'
        FRONTEND_PORT = '80'
        BACKEND_PORT = '8088'
        MYSQL_PORT = '3306'
    }

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'STAGE 1: Checking out IT Helpdesk Source Code'
                checkout scm
            }
        }

        stage('Validate Environment & Tools') {
            steps {
                echo 'STAGE 2: Validating Host Prerequisites and Runtimes'
                script {
                    if (isUnix()) {
                        sh 'java -version'
                        sh 'mvn -version'
                        sh 'node -v'
                        sh 'npm -v'
                        sh 'docker --version'
                        sh 'docker compose version'
                    } else {
                        bat 'java -version'
                        bat 'mvn -version'
                        bat 'node -v'
                        bat 'npm -v'
                        bat 'docker --version'
                        bat 'docker compose version'
                    }
                }
            }
        }

        stage('Build Backend') {
            steps {
                echo 'STAGE 3: Compiling Spring Boot 3.2.5 Backend (Java 21)'
                dir('backend') {
                    script {
                        if (isUnix()) {
                            sh 'mvn clean compile'
                        } else {
                            bat 'mvn clean compile'
                        }
                    }
                }
            }
        }

        stage('Run Backend Unit & Integration Tests') {
            steps {
                echo 'STAGE 4: Executing Automated JUnit 5 & Mockito Tests'
                dir('backend') {
                    script {
                        if (isUnix()) {
                            sh 'mvn test'
                        } else {
                            bat 'mvn test'
                        }
                    }
                }
            }
        }

        stage('Build Frontend Bundle') {
            steps {
                echo 'STAGE 5: Installing Dependencies & Building React SPA'
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm ci'
                            sh 'npm run build'
                        } else {
                            bat 'npm.cmd ci'
                            bat 'npm.cmd run build'
                        }
                    }
                }
            }
        }

        stage('Validate Docker Compose') {
            steps {
                echo 'STAGE 6: Validating Docker Compose Orchestration Graph'
                script {
                    if (isUnix()) {
                        sh 'docker compose config'
                    } else {
                        bat 'docker compose config'
                    }
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'STAGE 7: Building Multi-Stage Docker Images'
                script {
                    if (isUnix()) {
                        sh 'docker compose build'
                    } else {
                        bat 'docker compose build'
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'POST: Publishing Automated Test Results'
            junit testResults: 'backend/target/surefire-reports/*.xml', allowEmptyResults: true
        }
        success {
            echo 'POST: Archiving Build Artifacts'
            archiveArtifacts artifacts: 'backend/target/*.jar,backend/target/site/jacoco/**', allowEmptyArchive: true, fingerprint: true
            echo 'BUILD SUCCESSFUL: All tests passed, bundle compiled, and Docker images built.'
        }
        failure {
            echo 'BUILD FAILED: Investigation required. Consult stage console output for diagnostic details.'
        }
    }
}
```

---

## 8. Step-by-Step Jenkins Job Setup & Live Verification

### 8.1 Configuration Details
The pipeline job `IT-Helpdesk-Pipeline` in Jenkins 2.568.2 LTS connects directly to the GitHub remote:
1. **Jenkins Web UI**: `http://localhost:8080/`
2. **Pipeline Job Name**: `IT-Helpdesk-Pipeline`
3. **SCM Definition**: **Pipeline script from SCM**
4. **SCM Type**: **Git**
5. **Repository URL**: `https://github.com/Yokesh07J/IT-Helpdesk.git`
6. **Branch Specifier**: `*/main`
7. **Script Path**: `Jenkinsfile`
8. **Lightweight Checkout**: Enabled

### 8.2 Live Build Execution Evidence (Build #6)
- **Status**: `SUCCESS`
- **Revision Checked Out**: `e9b80c4` (`origin/main`)
- **Execution Stages**:
  - `Stage 1: Checkout SCM` — Cloned GitHub repository `https://github.com/Yokesh07J/IT-Helpdesk.git`.
  - `Stage 2: Validate Environment` — Verified Java 21, Maven 3.9.6, Node.js 22, Docker 29.8, Docker Compose.
  - `Stage 3: Build Backend` — Clean compiled Spring Boot backend (`mvn clean compile`).
  - `Stage 4: Run Tests` — Executed all 43 JUnit 5 & Mockito tests; generated JaCoCo coverage (`Tests run: 43, Failures: 0, Errors: 0, Skipped: 0`).
  - `Stage 5: Build Frontend` — Executed `npm ci` and `npm run build` (Vite SPA production bundle built in 4.16s).
  - `Stage 6: Validate Docker Compose` — Validated multi-service orchestration graph (`docker-compose config`).
  - `Stage 7: Build Multi-Stage Docker Images` — Assembled `it-helpdesk-backend:1.0.0` and `it-helpdesk-frontend:1.0.0`.
  - `Post-Build Actions`:
    - Recorded JUnit test results: **43 / 43 tests passed (0 failures, 0 errors, 0 skipped)**.
    - Archiving artifacts: Archived Spring Boot JAR and full JaCoCo code coverage site.
- **Pipeline Result**: `BUILD SUCCESSFUL: All tests passed, bundle compiled, and Docker images built.`

---

## 9. Viva Questions & Answers (Phase 3)

### Q1: What is the difference between JUnit 4 and JUnit 5?
**Answer**: JUnit 5 is composed of three sub-modules: JUnit Platform (test launcher), JUnit Jupiter (new programming model and extension API), and JUnit Vintage (backward compatibility for JUnit 3/4). JUnit 5 natively supports Java 8+ lambdas, parameterized tests, and uses `@ExtendWith` instead of `@RunWith`.

### Q2: What is Mockito and why do we use it in service layer testing?
**Answer**: Mockito is a Java mocking library used to isolate the unit under test from its real dependencies (such as databases or external APIs). It simulates repository and third-party behavior, allowing tests to run rapidly in memory without creating database side effects.

### Q3: What is the purpose of `@Mock` versus `@InjectMocks`?
**Answer**: `@Mock` creates a mock object for a dependency (e.g., `TicketRepository`), while `@InjectMocks` instantiates the class under test (e.g., `TicketService`) and automatically injects all defined `@Mock` objects into its constructor or fields.

### Q4: How does Mockito verify that a sensitive database operation did NOT execute?
**Answer**: By using `verify(repository, never()).save(any())`. This ensures that when validation errors or unauthorized requests occur, no persistent changes are committed.

### Q5: What is the role of Maven Surefire Plugin?
**Answer**: The Maven Surefire Plugin executes unit tests during the `test` lifecycle phase and generates standard XML and plain text test execution reports in the `target/surefire-reports` directory for CI servers like Jenkins to parse.

### Q6: What does JaCoCo measure in a Spring Boot application?
**Answer**: JaCoCo (Java Code Coverage) uses bytecode instrumentation to measure instruction, branch, line, complexity, and method coverage, generating detailed metrics in XML, CSV, and HTML reports.

### Q7: Explain the difference between `sh` and `bat` steps in a Jenkinsfile.
**Answer**: `sh` executes shell scripts on Unix/Linux/macOS nodes, while `bat` executes batch or command line commands on Windows nodes. Using `if (isUnix())` allows pipelines to dynamically adapt to both OS environments.

### Q8: What does `junit testResults: '**/surefire-reports/*.xml'` do in a Jenkins pipeline?
**Answer**: It parses the JUnit XML reports generated by Maven Surefire, creates a visual Test Result Trend graph on the Jenkins dashboard, and allows drill-down inspection of failed test cases.

### Q9: Why must unit tests avoid connecting to production MySQL?
**Answer**: Unit tests must be fast, deterministic, and repeatable. Connecting to production databases causes race conditions, risk of data corruption, latency, and dependency on external network infrastructure.

### Q10: What is a Declarative Pipeline in Jenkins and how does it differ from a Scripted Pipeline?
**Answer**: Declarative Pipeline enforces a structured, opinionated syntax (`pipeline { stages { stage { steps } } }`) with built-in directives for environments, timeouts, and post-build actions. Scripted Pipeline uses arbitrary Groovy code, which is more flexible but less standardized and harder to maintain.

---

## 10. Screenshots Checklist for Lab Submission

| Step | Item to Capture | Verification Detail |
| :--- | :--- | :--- |
| 1 | Maven Test Execution | Terminal output showing `Tests run: 43, Failures: 0, Errors: 0, Skipped: 0` and `BUILD SUCCESS` |
| 2 | JaCoCo HTML Report | Browser viewing `backend/target/site/jacoco/index.html` showing analyzed package coverage |
| 3 | Jenkins Web Login Screen | Browser viewing `http://localhost:8080/login` showing Jenkins 2.568.2 active on Windows |
| 4 | Jenkinsfile in IDE | Workspace editor displaying declarative `Jenkinsfile` stages |
| 5 | Surefire XML Reports | File Explorer showing `backend/target/surefire-reports/TEST-*.xml` files |
