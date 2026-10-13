# Final CAT Submission Screenshot & Verification Checklist

**Course**: 23IT723 – DevOps Laboratory  
**Institution**: Coimbatore Institute of Technology, Coimbatore  
**Project**: IT Helpdesk and Ticket Management System  
**Student Name**: YOKESH J  
**Date**: October 2026  

---

## 1. Overview of Embedded Figures in the Final Report

The final report contains **9 genuine, verified figures** generated directly from live system executions. All figures have been placed and embedded into both the DOCX and PDF deliverables:

| Figure # | Embedded File | Description | Source / Verification Detail | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Figure 5.1** | `figures/fig_architecture_diagram.png` | End-to-End DevOps Architecture Diagram | High-res vector render of Git ➔ Jenkins ➔ Docker ➔ Ansible ➔ Runtime | **EMBEDDED** |
| **Figure 7.1** | `figures/fig_dashboard.png` | Interactive Admin Dashboard | Live UI screenshot of React SPA ticket metrics | **EMBEDDED** |
| **Figure 8.1** | `figures/fig_tickets_list.png` | All Tickets Overview Screen | Live UI screenshot of filtered ticket table | **EMBEDDED** |
| **Figure 8.2** | `figures/fig_ticket_details.png` | Ticket Detail & Staff Operations | Live UI screenshot of staff reassignment & comments | **EMBEDDED** |
| **Figure 10.1** | `figures/fig_git_log.png` | Git Log & Remote Synchronization | Verified terminal card of `git log` on `main` tracking GitHub | **EMBEDDED** |
| **Figure 12.1** | `figures/fig_docker_compose_ps.png` | Docker Compose Stack Status | Verified terminal card of 3 running healthy containers | **EMBEDDED** |
| **Figure 13.1** | `figures/fig_jenkins_console.png` | Jenkins Pipeline Console Output | Actual console log screenshot of Build #6 (SUCCESS) | **EMBEDDED** |
| **Figure 14.1** | `figures/fig_maven_tests.png` | Maven Automated Test Suite | Verified terminal card of 43 passed tests | **EMBEDDED** |
| **Figure 15.1** | `figures/fig_ansible_idempotency.png` | Ansible Idempotency Execution | Verified terminal card of `ok=14 changed=0` in WSL2 | **EMBEDDED** |

---

## 2. Evidence You Can Capture Manually for Viva / Demonstration

If your lab faculty or external examiner asks for direct desktop captures on your own laptop screen during the live viva examination, capture the following exact screens:

### Checklist for Live Viva Demonstration

- [ ] **1. Docker Desktop GUI**:
  - Open Docker Desktop on Windows.
  - Navigate to **Containers** tab.
  - Confirm `it-helpdesk` compose stack displays `helpdesk-frontend`, `helpdesk-backend`, and `helpdesk-mysql` with green **Running** status.
  - *Save as*: `live_docker_desktop_gui.png`

- [ ] **2. Web Application in Browser**:
  - Open Chrome/Edge and visit `http://localhost/`.
  - Log in as Administrator (`admin@helpdesk.com` / `Admin@123` or your credentials).
  - Open Developer Tools (F12) ➔ Network tab to show HTTP 200 responses to `/api/dashboard/stats`.
  - *Save as*: `live_browser_app.png`

- [ ] **3. Jenkins Web Dashboard**:
  - Open `http://localhost:8080/job/IT-Helpdesk-Pipeline/`.
  - Ensure the **Stage View** displays all stages green for Build #6.
  - Click on **Test Result Trend** to display the graph showing `43 tests (0 failures)`.
  - *Save as*: `live_jenkins_stage_view.png`

- [ ] **4. JaCoCo Coverage HTML Report**:
  - Open File Explorer or Chrome at: `C:\DevopsCat\IT-Helpdesk\backend\target\site\jacoco\index.html`.
  - Capture the green package coverage breakdown table.
  - *Save as*: `live_jacoco_report.png`

- [ ] **5. GitHub Repository Web Page**:
  - Visit `https://github.com/Yokesh07J/IT-Helpdesk`.
  - Capture the repository main page showing latest commit `a1644db` or newer on branch `main`.
  - *Save as*: `live_github_repo.png`
