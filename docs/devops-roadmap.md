# IT Helpdesk & Ticket Management System — DevOps Lab Syllabus Roadmap

This roadmap tracks the implementation, status, and verification of the 6 phases required by the DevOps Lab syllabus.

---

## Progress Overview

| Phase | Description | Deliverables | Status |
|---|---|---|---|
| **Phase 1** | **Docker Basics** | Installation guide, verification script, core command exercises (`pull`, `images`, `run`, `ps`, `stop`, `rm`, `logs`, `exec`, `inspect`), lab record, viva Q&A | **COMPLETED** |
| **Phase 2** | **Java/Web App Deployment** | Multi-stage backend `Dockerfile` (Java 21), multi-stage frontend `Dockerfile` (Vite + Nginx), `docker-compose.yml`, MySQL persistent storage, networking, health checks | **COMPLETED** |
| **Phase 3** | **Continuous Testing** | JUnit 5 + Mockito test suite (43 tests), JaCoCo coverage, declarative Jenkinsfile, GitHub SCM pipeline, test report publishing | **COMPLETED** |
| **Phase 4** | **Configuration Management** | Ansible inventory, playbooks for environment configuration (WSL/Ubuntu Linux), idempotency verification | **COMPLETED** |
| **Phase 5** | **Integrated DevOps Workflow** | Complete Git ➔ Jenkins ➔ Test ➔ Containerization ➔ Ansible deployment pipeline documentation and verification | **PENDING** |
| **Phase 6** | **CAT Submission & Viva Preparation**| Project abstract, architecture diagrams, testing results checklist, viva voce question bank across all DevOps tools | **PENDING** |

---

## Detailed Phase Documentation Links
- [Phase 0: Project Audit & Environment Baseline](file:///c:/DevopsCat/IT-Helpdesk/docs/00-project-audit.md)
- [Phase 1: Docker Basics & Lifecycle Management](file:///c:/DevopsCat/IT-Helpdesk/docs/01-docker-basics.md) (Script: [scripts/verify-docker-basics.ps1](file:///c:/DevopsCat/IT-Helpdesk/scripts/verify-docker-basics.ps1))
- [Phase 2: Multi-Container Docker Deployment](file:///c:/DevopsCat/IT-Helpdesk/docs/02-docker-deployment.md) (Script: [scripts/test-docker-deployment.ps1](file:///c:/DevopsCat/IT-Helpdesk/scripts/test-docker-deployment.ps1))
- [Phase 3: Continuous Testing Using JUnit 5, Mockito, Maven, and Jenkins](file:///c:/DevopsCat/IT-Helpdesk/docs/03-continuous-testing-jenkins.md)
- [Phase 4: Configuration Management Using Ansible in WSL/Ubuntu Linux](file:///c:/DevopsCat/IT-Helpdesk/docs/04-ansible-configuration-management.md) (Script: [ansible/verify-ansible.sh](file:///c:/DevopsCat/IT-Helpdesk/ansible/verify-ansible.sh))
