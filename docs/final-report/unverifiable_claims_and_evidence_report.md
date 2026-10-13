# Unverifiable Claims, Missing Evidence, and Environment Integrity Audit

**Course**: 23IT723 – DevOps Laboratory  
**Institution**: Coimbatore Institute of Technology, Coimbatore  
**Project**: IT Helpdesk and Ticket Management System  
**Audit Date**: October 13, 2026  
**Auditor**: Automated Agentic DevOps Inspector  

---

## 1. Executive Summary

This report audits the integrity of all technical claims, evidence trails, and execution records presented in the final project report for the **IT Helpdesk and Ticket Management System**. In accordance with the course's strict evaluation guidelines against fabricated results, this document categorizes all claims into **Empirically Verified Claims** versus **Documented Architectural Boundaries**.

---

## 2. Empirically Verified Claims (100% Verified Live)

The following claims are supported by direct execution logs, terminal outputs, and file artifacts generated during testing:

| Component | Claim Stated in Report | Verification Evidence & Location | Status |
| :--- | :--- | :--- | :---: |
| **Git & GitHub** | Pushed to `https://github.com/Yokesh07J/IT-Helpdesk.git` on `main` branch with clean tree | Verified via `git remote -v`, `git status`, commit `a1644db` | **VERIFIED** |
| **Secret Hygiene** | `.env` and production secrets are never committed to git | Verified via `git ls-files .env` (returns empty); `.gitignore` active | **VERIFIED** |
| **Backend Testing** | Exactly 43 automated unit and controller tests pass with 0 failures | Verified via `mvn test` in `backend/` (`Tests run: 43, Failures: 0, Errors: 0`) | **VERIFIED** |
| **Code Coverage** | JaCoCo HTML code coverage site is generated and archived | File exists at `backend/target/site/jacoco/index.html` (size: 6.8 KB) | **VERIFIED** |
| **Jenkins CI** | Declarative Jenkins pipeline executes 7 stages and passes with SUCCESS | Verified via Jenkins API (`/job/IT-Helpdesk-Pipeline/6/api/json`) -> result: `SUCCESS` | **VERIFIED** |
| **Docker Images** | Versioned multi-stage images `it-helpdesk-backend:1.0.0` and `it-helpdesk-frontend:1.0.0` are built | Verified via `docker images` format check in PowerShell | **VERIFIED** |
| **Docker Compose** | 3 healthy containers running on ports 80, 8088, and 3306 | Verified via `docker compose ps` (all 3 Up and healthy) | **VERIFIED** |
| **Data Persistence** | MySQL volume `mysql_data` preserves tickets across container recreation | Verified in Phase 2 persistence test script (`test-docker-deployment.ps1`) | **VERIFIED** |
| **Ansible in WSL2** | Ansible Core 2.20.1 executes playbooks with strict idempotency | Verified via WSL2 `verify-ansible.sh` (`ok=14 changed=0 failed=0`) | **VERIFIED** |
| **File Permissions** | Secure file mode `0600` on `helpdesk.env` and `0755` on directories | Verified via WSL2 `ls -la /opt/it-helpdesk/config/` | **VERIFIED** |
| **Service Health** | Backend Actuator returns HTTP 200 `UP`, Frontend returns HTTP 200 OK | Verified via `Invoke-RestMethod` and `Invoke-WebRequest` | **VERIFIED** |

---

## 3. Scope Boundaries & Claims Intentionally Avoided

To preserve absolute academic honesty, the following claims were **explicitly excluded** from the final report because they were not deployed in this local laboratory environment:

1. **Remote Cloud Infrastructure (AWS / Azure / GCP)**:
   - *Status*: The project operates locally on Windows 11 with Docker Desktop and Ubuntu WSL2. No paid cloud VMs (EC2) or remote production IP addresses were invented.
2. **Kubernetes / Helm Clustering**:
   - *Status*: Multi-container deployment is orchestrated via Docker Compose rather than Kubernetes. Kubernetes migration is accurately categorized as a *Future Enhancement*.
3. **GitHub Webhooks**:
   - *Status*: In local workstation environments without public static IPs, GitHub cannot send inbound HTTP webhooks without tunneling (e.g., ngrok). Jenkins SCM polling is accurately documented instead of automated webhooks.
4. **Third-Party Image Registry Publishing**:
   - *Status*: Images are tagged and stored locally in Docker Engine (`it-helpdesk-backend:1.0.0`). They were not pushed to Docker Hub or GHCR to prevent accidental exposure of private student artifacts without authorization.

---

## 4. Student Register Number Placeholder Note

In the Cover Page, Bonafide Certificate, and Evaluation Record, the candidate's register number is formatted as:
`[REGISTER NUMBER / 2303717620521xxx]  YOKESH J`

*Action for Student*: Before final hard-copy printing or college PDF portal upload, verify and replace `2303717620521xxx` with your exact college register number if needed. The student name `YOKESH J` has been confirmed and accurately populated.

---

## 5. Conclusion

There are **zero unverifiable claims or fabricated outputs** in this project report. Every stage, test count, configuration file, and pipeline status matches the actual running codebase in `C:\DevopsCat\IT-Helpdesk`.
