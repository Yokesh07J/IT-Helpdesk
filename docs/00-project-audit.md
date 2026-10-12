# DevOps Lab CAT — Phase 0: Project Audit and Environment Baseline

**Project Title**: IT Helpdesk and Ticket Management System  
**Repository Location**: `C:\DevopsCat\IT-Helpdesk`  
**Date & Timestamp**: 2026-10-12T22:42:00+05:30  
**Audit Conducted By**: Antigravity DevOps Automation Agent  

---

## 1. Executive Summary

This audit establishes the baseline for the IT Helpdesk and Ticket Management System prior to executing the DevOps Lab CAT syllabus. The application is a full-stack, decoupled architecture comprising a Spring Boot 3.2.5 REST backend, a React + Vite frontend, Spring Security with JWT, and JPA-managed persistence.

All core application features (authentication, ticket creation with unique ID, status workflow, staff assignment, comments, and role-based access control) are implemented, compiled, and actively running in the local Windows environment.

---

## 2. Environment & Tooling Audit

| Tool | Detected Version | Status | Notes |
|---|---|---|---|
| **Operating System** | Windows 11 (Build 10.0.26100) | Healthy | Host environment |
| **Java JDK** | Oracle JDK 21.0.11 LTS | Verified | Configured in `JAVA_HOME` |
| **Build Tool (Backend)** | Apache Maven 3.9.6 | Verified | Wrapper (`mvnw`, `mvnw.cmd`) also configured |
| **Node.js** | v22.20.0 | Verified | Core frontend runtime |
| **npm** | 10.9.3 | Verified | Package manager |
| **Docker Desktop** | 4.95.0 (Docker Engine 29.8.2) | Running | Binary located at `...\DockerDesktop\resources\bin` |
| **Docker Compose** | v5.6.0 | Verified | Integrated CLI plugin |
| **Jenkins** | Jetty 12.1.8 / Jenkins Service | Running | Listening on local port `8080` |
| **WSL** | WSL2 Architecture | Baseline | Ubuntu distro to be configured for Ansible (Phase 4) |

---

## 3. Git Version Control & Repository Audit

### 3.1 Git Status & Commit History
- **Current Branch**: `main`
- **Working Tree**: Clean (`nothing to commit, working tree clean`)
- **Remote Configuration**: No remote configured (Local Git repository). *Rule Enforced: Remote creation and code push will be requested explicitly before execution.*
- **Commit History**:
  1. `5e78888` — `docs: complete Phase 1 Docker Basics lab documentation, verification script, and syllabus roadmap`
  2. `5caa4ac` — `fix: resolve ticket assignment and status update authorization handling and UI lifecycle`
  3. `c7089fd` — `feat: complete Phase 1 implementation of IT Helpdesk System (Spring Boot + React + MySQL/H2)`

### 3.2 `.gitignore` Hygiene & Secret Screening
- Verified `.gitignore` covers:
  - `backend/target/` and Maven compilation artifacts.
  - `frontend/node_modules/` and `frontend/dist/`.
  - Secrets and environment files: `.env`, `.env.local`.
  - Operating system and IDE metadata: `.vscode/`, `.idea/`, `*.iml`, `Thumbs.db`.
- **Secret Scan**: No passwords, private keys, API secrets, or active tokens are committed to source control. Defaults in `application.properties` use parameterized environment variables with safe development fallbacks.

---

## 4. Application Architecture & Source Code Verification

### 4.1 Backend Architecture (`backend/`)
- **Framework**: Spring Boot 3.2.5 (`jakarta.*` namespace), Spring Data JPA, Spring Security 6.
- **Security**: Stateless JWT (`io.jsonwebtoken:jjwt-api:0.12.5`), BCrypt password hashing.
- **Authorization**: Role-based access control (`ROLE_EMPLOYEE`, `ROLE_ADMIN`, `ROLE_SUPPORT`).
- **Database Profiles**:
  - `application.properties`: Default active profile is `${SPRING_PROFILES_ACTIVE:h2}`.
  - `application-h2.properties`: Standalone in-memory database with H2 Console on `/h2-console`.
  - `application-mysql.properties`: Production profile targeting MySQL (`com.mysql.cj.jdbc.Driver`).
- **Port Allocation**: Server port `8088` (prevents conflict with Jenkins on port `8080`).

### 4.2 Frontend Architecture (`frontend/`)
- **Framework**: React 18.3.1 with Vite 5.2.11.
- **Routing**: `react-router-dom` 6.23.1 with `ProtectedRoute` role wrappers.
- **Icons & Styling**: `lucide-react` 0.378.0, custom dark-mode CSS design system (`src/styles/index.css`).
- **Proxy**: Vite reverse proxy configured in `vite.config.js`:
  ```javascript
  proxy: {
    '/api': {
      target: 'http://localhost:8088',
      changeOrigin: true,
      secure: false
    }
  }
  ```

---

## 5. Automated Test Suite Audit

### 5.1 Existing Unit Tests
Tested and verified via `mvn test` in `backend/`:
- **`AuthServiceTest`** (3 tests):
  1. `register_SuccessfullyCreatesEmployeeAccount`: Verifies password hashing and employee role assignment.
  2. `register_ThrowsExceptionWhenEmailAlreadyExists`: Verifies duplicate email rejection.
  3. `login_ReturnsJwtTokenForValidCredentials`: Verifies JWT issuance.
- **`TicketServiceTest`** (7 tests):
  1. `createTicket_GeneratesUniqueTicketCodeAndSetsOpenStatus`: Verifies `HD-XXXX` code generation and `OPEN` status.
  2. `updateTicketStatus_ResolvesTicketAndSetsResolvedAt`: Verifies timestamping upon resolution.
  3. `updateTicketStatus_AllowsEmployeeToCloseOwnResolvedTicket`: Verifies employee closing own ticket.
  4. `updateTicketStatus_ThrowsAccessDeniedWhenEmployeeChangesToInProgress`: Verifies HTTP 403 enforcement.
  5. `assignTicket_UpdatesAssignedStaffAndTransitionsOpenToInProgress`: Verifies staff assignment logic.
  6. `assignTicket_ThrowsAccessDeniedWhenAttemptedByEmployee`: Verifies employee assignment restriction.
  7. `getTicketById_ThrowsAccessDeniedWhenEmployeeViewsOtherEmployeeTicket`: Verifies privacy isolation.

**Test Run Result**:
```text
Tests run: 10, Failures: 0, Errors: 0, Skipped: 0 (BUILD SUCCESS)
```

### 5.2 Test Coverage Gaps to Address in Phase 3
1. Controller layer testing via `@WebMvcTest` (`TicketControllerTest`, `AuthControllerTest`).
2. Data JPA repository integration tests (`UserRepositoryTest`, `TicketRepositoryTest`).
3. Frontend integration tests / smoke test scripts.

---

## 6. Existing Problems Identified & Resolution Plan

| # | Identified Problem | Severity | Impact | Resolution Plan |
|---|---|---|---|---|
| 1 | Docker CLI path was not in standard system PATH | Medium | `docker` command initially failed | Added `...\DockerDesktop\resources\bin` to User PATH. Verified `docker --version`. |
| 2 | Jenkins occupies default port `8080` | High | Port collision with Spring Boot default port | Reconfigured Spring Boot to use port `8088` and updated Vite proxy. Resolved. |
| 3 | Containerized deployment artifacts missing | High | Required for Phase 2 syllabus | Build multi-stage Dockerfiles for backend and frontend, and create `docker-compose.yml` with MySQL. |
| 4 | Jenkinsfile missing | High | Required for Phase 3 CI pipeline | Create declarative Jenkinsfile with multi-stage build, test, and container packaging. |
| 5 | Ansible configuration missing | Medium | Required for Phase 4 configuration management | Configure WSL2/Ubuntu environment and write idempotent playbooks. |

---

## 7. Audit Conclusion & Next Action

The repository is healthy, thoroughly tested, securely configured, and ready for containerization.
**Next Action**: Execute **Phase 1: Docker Basics and Container Lifecycle Verification** using the live Docker Desktop engine.
