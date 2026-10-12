# IT Helpdesk & Ticket Management System — DevOps Lab Syllabus Roadmap

This roadmap tracks the implementation, status, and verification of the 6 phases required by the DevOps Lab syllabus.

---

## Progress Overview

| Phase | Description | Deliverables | Status |
|---|---|---|---|
| **Phase 1** | **Docker Basics** | Installation guide, verification script, core command exercises (`pull`, `images`, `run`, `ps`, `stop`, `rm`, `logs`, `exec`, `inspect`), lab record, viva Q&A | **COMPLETED** |
| **Phase 2** | **Java/Web App Deployment** | Multi-stage backend `Dockerfile` (Java 21), multi-stage frontend `Dockerfile` (Vite + Nginx), `docker-compose.yml`, MySQL persistent storage, networking, health checks | **READY TO IMPLEMENT** |
| **Phase 3** | **Continuous Testing** | JUnit 5 + Mockito test suite, Jenkinsfile, Maven automated test execution, test report publishing | **PENDING** |
| **Phase 4** | **Configuration Management** | Ansible inventory, playbooks for environment configuration (WSL/Ubuntu Linux), idempotency verification | **PENDING** |
| **Phase 5** | **Integrated DevOps Workflow** | Complete Git ➔ Jenkins ➔ Test ➔ Containerization ➔ Ansible deployment pipeline documentation and verification | **PENDING** |
| **Phase 6** | **CAT Submission & Viva Preparation**| Project abstract, architecture diagrams, testing results checklist, viva voce question bank across all DevOps tools | **PENDING** |

---

## Detailed Phase Documentation Links
- [Phase 1: Docker Basics & Lifecycle Management](file:///c:/DevopsCat/IT-Helpdesk/docs/01-docker-basics.md)
- Automated verification script: [scripts/verify-docker-basics.ps1](file:///c:/DevopsCat/IT-Helpdesk/scripts/verify-docker-basics.ps1)
