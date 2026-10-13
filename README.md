# IT Helpdesk and Ticket Management System

**Course**: 23IT723 – DevOps Laboratory  
**Institution**: Coimbatore Institute of Technology, Coimbatore  
**Author**: YOKESH J (`Yokesh07J`)  
**Repository**: [https://github.com/Yokesh07J/IT-Helpdesk](https://github.com/Yokesh07J/IT-Helpdesk)  
**Status**: Completed & Verified Live across all 6 DevOps Phases  

---

## 1. Project Overview

The **IT Helpdesk and Ticket Management System** is an enterprise-grade service desk web application paired with a complete, end-to-end automated DevOps delivery pipeline. The application allows employees to submit categorized technical support requests (Hardware, Software, Network, Access) and empowers support engineers and administrators to manage queue assignments, update resolution statuses, and append internal diagnostic notes.

### Technology Stack
- **Frontend**: React 18, Vite 5, Tailwind/Vanilla CSS, Axios, served by Nginx 1.25 Alpine
- **Backend**: Java 21 LTS, Spring Boot 3.2.5, Spring Data JPA, Spring Security 6.2.4 (JWT + BCrypt)
- **Database**: MySQL Server 8.0 with persistent named Docker volume (`mysql_data`)
- **Automated Testing**: JUnit 5, Mockito 5 (43 passing unit & controller tests), JaCoCo Code Coverage
- **Continuous Integration**: Jenkins 2.568.2 LTS Declarative Pipeline (`Jenkinsfile`)
- **Containerization & Orchestration**: Docker Engine 29.8, Docker Compose
- **Configuration Management**: Ansible Core 2.20.1 in Ubuntu 26.04 WSL2 (Strict Idempotency verified: `changed=0`)

---

## 2. End-to-End DevOps Architecture

```
Developer (Windows 11)
       │
       ▼ (git push)
GitHub Repository (main branch)
       │
       ▼ (SCM trigger)
Jenkins CI Pipeline (LocalSystem Service :8080)
       ├── Stage 1: Checkout SCM
       ├── Stage 2: Validate Host Runtimes (Java 21, Maven 3.9, Node 22, Docker)
       ├── Stage 3: Clean Compile Spring Boot Backend
       ├── Stage 4: Automated Testing Gate (43 JUnit 5 & Mockito Tests + JaCoCo)
       ├── Stage 5: Compile React SPA Production Bundle (dist/)
       ├── Stage 6: Validate Docker Compose Orchestration Graph
       └── Stage 7: Build Multi-Stage Docker Images (Temurin 21 JRE & Nginx Alpine)
       │
       ▼ (Configuration Management)
Ansible Control Node (Ubuntu WSL2)
       ├── Deploy directory hierarchies (/opt/it-helpdesk/{config,logs,scripts} - mode 0755)
       ├── Render Jinja2 environment templates (helpdesk.env - mode 0600)
       └── Enforce idempotency (ok=14 changed=0 failed=0)
       │
       ▼ (Runtime Launch)
Docker Compose Multi-Container Stack
       ├── helpdesk-frontend (Port 80 -> React SPA + API reverse proxy)
       ├── helpdesk-backend (Port 8088 -> Java 21 Spring Boot REST API)
       └── helpdesk-mysql (Port 3306 -> MySQL 8.0 + volume mysql_data)
       │
       ▼ (Automated Verification)
Health Check Probing (/actuator/health -> status: UP)
```

---

## 3. Quickstart & Verification

### Running the Multi-Container Application Locally
Ensure Docker Desktop is running on Windows, then execute:
```powershell
# Launch the full stack
docker compose up -d

# Verify container status
docker compose ps
```
- **Frontend Web UI**: [http://localhost/](http://localhost/)
- **Backend Actuator Health**: [http://localhost:8088/actuator/health](http://localhost:8088/actuator/health)
- **Jenkins CI Server**: [http://localhost:8080/](http://localhost:8080/)

### Running Backend Unit & Controller Tests
```powershell
cd backend
mvn test
```
*Result*: 43 tests pass (0 failures, 0 errors). Coverage report generated at `backend/target/site/jacoco/index.html`.

### Running Ansible Configuration Management (WSL2)
```bash
wsl -d Ubuntu
cd /mnt/c/DevopsCat/IT-Helpdesk/ansible
export ANSIBLE_CONFIG=./ansible.cfg
ansible-playbook -i inventory.ini playbook.yml
```
*Result*: `ok=14 changed=0 unreachable=0 failed=0` (Strict Idempotency).

### Running End-to-End Pipeline Verification
```powershell
powershell -ExecutionPolicy Bypass -File "scripts/verify-integrated-devops-workflow.ps1"
```
*Result*: All 20 pipeline checkpoints pass with 100% success.

---

## 4. Documentation Index

Comprehensive academic lab documentation is available under [`docs/`](docs/):
- **Phase 0**: [docs/00-project-audit.md](docs/00-project-audit.md) — Initial project audit & environment baseline
- **Phase 1**: [docs/01-docker-basics.md](docs/01-docker-basics.md) — Docker commands, lifecycle exercises, and lab record
- **Phase 2**: [docs/02-docker-deployment.md](docs/02-docker-deployment.md) — Multi-container Docker deployment & volume persistence
- **Phase 3**: [docs/03-continuous-testing-jenkins.md](docs/03-continuous-testing-jenkins.md) — Continuous testing & Jenkins CI pipeline
- **Phase 4**: [docs/04-ansible-configuration-management.md](docs/04-ansible-configuration-management.md) — Ansible configuration management & idempotency in WSL2
- **Phase 5**: [docs/05-integrated-devops-workflow.md](docs/05-integrated-devops-workflow.md) — Integrated CI/CD workflow & Mermaid diagrams
- **Phase 6 Final Report**:
  - Word Document: [`docs/final-report/23IT723_Final_Project_Report_IT_Helpdesk.docx`](docs/final-report/23IT723_Final_Project_Report_IT_Helpdesk.docx)
  - PDF Document: [`docs/final-report/23IT723_Final_Project_Report_IT_Helpdesk.pdf`](docs/final-report/23IT723_Final_Project_Report_IT_Helpdesk.pdf)
  - Architecture Diagram: [`docs/final-report/figures/fig_architecture_diagram.png`](docs/final-report/figures/fig_architecture_diagram.png)
  - Screenshot Checklist: [`docs/final-report/screenshot_checklist.md`](docs/final-report/screenshot_checklist.md)
  - Evidence Audit: [`docs/final-report/unverifiable_claims_and_evidence_report.md`](docs/final-report/unverifiable_claims_and_evidence_report.md)
- **DevOps Roadmap**: [docs/devops-roadmap.md](docs/devops-roadmap.md) — Phase status matrix (All 6 Phases Completed)

---

## 5. Security & Licensing
- `.env` files, passwords, and signing secrets are strictly git-ignored.
- Multi-stage Docker containers execute as non-root users (`spring:spring` UID 1000).
- Generated configuration files on the host are restricted to owner read/write permissions (`0600`).
