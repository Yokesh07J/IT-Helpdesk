#!/usr/bin/env python3
"""
Generate Final DevOps CAT Project Report (DOCX)
Course: 23IT723 - DevOps Laboratory
Project: IT HELPDESK AND TICKET MANAGEMENT SYSTEM
Institution: Coimbatore Institute of Technology, Coimbatore
Student: YOKESH J (Register No: 2303717620521xxx)

Exact structure matching 23IT723_Final_Project_Report_TaskPulse.pdf
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_page_border(section):
    """Sets a clean rectangular border around every page in Word."""
    sectPr = section._sectPr
    for child in list(sectPr):
        if child.tag.endswith('pgBorders'):
            sectPr.remove(child)
    borders_xml = parse_xml(
        f'<w:pgBorders {nsdecls("w")} w:offsetFrom="page">'
        '<w:top w:val="single" w:sz="6" w:space="24" w:color="000000"/>'
        '<w:left w:val="single" w:sz="6" w:space="24" w:color="000000"/>'
        '<w:bottom w:val="single" w:sz="6" w:space="24" w:color="000000"/>'
        '<w:right w:val="single" w:sz="6" w:space="24" w:color="000000"/>'
        '</w:pgBorders>'
    )
    sectPr.append(borders_xml)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_page_number_field(run):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def create_docx_report(output_path, figures_dir):
    doc = Document()
    
    # Page setup - Margins (0.75 in all around inside the border)
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        set_page_border(section)
        
        # Bottom-right page number in footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ft = p_ft.add_run()
        r_ft.font.name = 'Times New Roman'
        r_ft.font.size = Pt(10)
        add_page_number_field(r_ft)

    # Base styling
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # -------------------------------------------------------------------------
    # PAGE 1: COVER PAGE
    # -------------------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n")
    r_inst.font.size = Pt(14)
    r_inst.bold = True
    
    r_sub = p_inst.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\nCOIMBATORE - 641 014\n")
    r_sub.font.size = Pt(10)
    r_sub.italic = True
    p_inst.paragraph_format.space_after = Pt(24)

    logo_path = os.path.join(figures_dir, "cit_logo.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8))
        p_logo.paragraph_format.space_after = Pt(28)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_course.add_run("23IT723 - DEVOPS LABORATORY\n\nPROJECT REPORT\n")
    r_c.font.size = Pt(12)
    r_c.bold = True
    p_course.paragraph_format.space_after = Pt(20)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("IT HELPDESK: ENTERPRISE TICKET MANAGEMENT & DEVOPS AUTOMATION\n")
    r_t.font.size = Pt(13.5)
    r_t.bold = True
    p_title.paragraph_format.space_after = Pt(72)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_date.add_run("OCTOBER 2026\n")
    r_d.font.size = Pt(11)
    r_d.bold = True
    p_date.paragraph_format.space_after = Pt(64)

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sb = p_subm.add_run("Submitted by\n\n")
    r_sb.font.size = Pt(11)
    r_sb.bold = True
    r_auth = p_subm.add_run("2303717620521xxx  YOKESH J")
    r_auth.font.size = Pt(11)
    r_auth.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 2: BONAFIDE CERTIFICATE
    # -------------------------------------------------------------------------
    p_cert_inst = doc.add_paragraph()
    p_cert_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_inst.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n").bold = True
    r_ci_sub = p_cert_inst.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\nCOIMBATORE - 641 014\n")
    r_ci_sub.font.size = Pt(10)
    r_ci_sub.italic = True
    p_cert_inst.paragraph_format.space_after = Pt(28)

    p_bon = doc.add_paragraph()
    p_bon.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_bon = p_bon.add_run("BONAFIDE CERTIFICATE\n")
    r_bon.font.size = Pt(13)
    r_bon.bold = True
    p_bon.paragraph_format.space_after = Pt(24)

    p_cbody = doc.add_paragraph()
    p_cbody.paragraph_format.line_spacing = 1.3
    p_cbody.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cbody.add_run("Certified that this project report titled ")
    p_cbody.add_run('"IT HELPDESK: ENTERPRISE TICKET MANAGEMENT & DEVOPS AUTOMATION"').bold = True
    p_cbody.add_run(" is the bonafide work of ")
    p_cbody.add_run("2303717620521xxx - YOKESH J").bold = True
    p_cbody.add_run(" completed during the academic year ")
    p_cbody.add_run("2026-2027 - Semester VII").bold = True
    p_cbody.add_run(" for the project presentation of ")
    p_cbody.add_run("23IT723 - DEVOPS LABORATORY").bold = True
    p_cbody.add_run(" under our supervision.\n\n")

    p_cbody2 = doc.add_paragraph()
    p_cbody2.paragraph_format.line_spacing = 1.3
    r_cb2 = p_cbody2.add_run("Certified that the candidate was examined by using the project work examination.\n\n\n")
    r_cb2.italic = True
    p_cbody2.paragraph_format.space_after = Pt(50)

    p_rev = doc.add_paragraph()
    p_rev.add_run("Review Members:\n\n").bold = True
    p_rev.add_run("    1. Dr. M. Sangeetha\n\n").bold = True
    p_rev.add_run("    2. Dr. E. Arul\n").bold = True

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 3: EVALUATION SCHEME
    # -------------------------------------------------------------------------
    p_es1 = doc.add_paragraph()
    p_es1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_es1.add_run("23IT723 – DEVOPS LABORATORY\n").bold = True
    p_es1.add_run("FINAL MINI PROJECT – EVALUATION SCHEME\n").bold = True
    p_es1.paragraph_format.space_after = Pt(4)

    p_es2 = doc.add_paragraph()
    p_es2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_es2.add_run("Final Mini Project Assessment").bold = True
    p_es2.paragraph_format.space_after = Pt(6)

    p_es_desc = doc.add_paragraph()
    p_es_desc.paragraph_format.line_spacing = 1.15
    p_es_desc.add_run(
        "The final mini project shall require students to integrate the major DevOps practices covered in the laboratory. "
        "The project should demonstrate practical implementation of version control, collaborative development, Continuous Integration, "
        "containerization and/or automated configuration/provisioning, with proper execution evidence."
    )
    p_es_desc.paragraph_format.space_after = Pt(8)

    eval_rows = [
        ("S.No.", "Evaluation Component", "Key Verification Points", "Marks"),
        ("1", "Problem Definition &\nProject Planning", "Problem statement, objectives, requirements, scope, module identification, technology selection and workflow planning.", "10"),
        ("2", "Git Repository &\nVersion Control", "Repository creation, meaningful commits, README, .gitignore, remote repository, push/pull/fetch operations and commit history.", "15"),
        ("3", "Branching, Merging &\nCollaboration", "Feature branches, parallel development, merging, conflict handling, branch organization and collaborative workflow.", "10"),
        ("4", "Application\nDevelopment & Build", "Working application/source code, project structure, dependency management, build configuration and successful execution.", "15"),
        ("5", "Jenkins Continuous\nIntegration", "Jenkins configuration, source-code integration, automated checkout, build job/pipeline, build execution and console verification.", "15"),
        ("6", "Docker /\nContainerization", "Dockerfile, image creation, container execution, port/configuration handling, application deployment and container verification.", "10"),
        ("7", "Automation /\nConfiguration Management", "Ansible/Chef/Puppet/SaltStack or equivalent automation where applicable; repeatable configuration/provisioning and successful execution.", "5"),
        ("8", "Testing & Verification", "Functional testing, build verification, error identification, test evidence and corrective action.", "5"),
        ("9", "Documentation &\nTechnical Presentation", "Architecture/workflow diagram, commands/configuration, screenshots, results, troubleshooting, conclusion and repository details.", "5"),
        ("10", "Final Demonstration &\nViva-Voce", "Live demonstration, explanation of implementation, troubleshooting responses and technical understanding.", "10"),
        ("", "TOTAL", "", "100")
    ]

    t_eval = doc.add_table(rows=len(eval_rows), cols=4)
    t_eval.style = 'Table Grid'
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths_eval = [Inches(0.5), Inches(1.8), Inches(4.2), Inches(0.6)]

    for row_idx, data in enumerate(eval_rows):
        row = t_eval.rows[row_idx]
        is_hdr = (row_idx == 0 or row_idx == len(eval_rows) - 1)
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.width = col_widths_eval[col_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 3] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(9)
            if is_hdr:
                run.bold = True
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 4: RECOMMENDED MARK DISTRIBUTION & FACULTY EVALUATION RECORD
    # -------------------------------------------------------------------------
    p_rmd = doc.add_paragraph()
    p_rmd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rmd.add_run("Recommended Mark Distribution within the Final Demonstration").bold = True
    p_rmd.paragraph_format.space_after = Pt(4)

    p_rmd_sub = doc.add_paragraph()
    p_rmd_sub.add_run("For uniform evaluation, the examiner may use the following internal split for the implementation and demonstration components.")
    p_rmd_sub.paragraph_format.space_after = Pt(6)

    dist_rows = [
        ("Assessment Area", "Marks", "Awarded Marks", "Remarks"),
        ("Working implementation and correctness", "30", "", ""),
        ("DevOps tool integration and automation", "20", "", ""),
        ("Version control and collaborative workflow", "15", "", ""),
        ("Build / deployment / container verification", "15", "", ""),
        ("Testing and troubleshooting", "5", "", ""),
        ("Documentation and technical presentation", "5", "", ""),
        ("Live demonstration and viva-voce", "10", "", ""),
        ("TOTAL", "100", "", "")
    ]

    t_dist = doc.add_table(rows=len(dist_rows), cols=4)
    t_dist.style = 'Table Grid'
    t_dist.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_dist = [Inches(2.8), Inches(0.8), Inches(1.3), Inches(2.2)]

    for row_idx, data in enumerate(dist_rows):
        row = t_dist.rows[row_idx]
        is_hdr = (row_idx == 0 or row_idx == len(dist_rows) - 1)
        for col_idx, text in enumerate(data):
            cell = row.cells[col_idx]
            cell.width = col_w_dist[col_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(8.5)
            if is_hdr:
                run.bold = True
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)

    p_ev_h = doc.add_paragraph()
    p_ev_h.paragraph_format.space_before = Pt(8)
    p_ev_h.add_run("Minimum Evidence to be Submitted").bold = True
    
    ev_bullets = [
        "Project repository URL and project README.",
        "Git commit history and branch/merge evidence.",
        "Jenkins job/pipeline configuration and successful build evidence.",
        "Dockerfile, image and running container evidence where Docker is used.",
        "Automation/configuration scripts where applicable.",
        "Architecture/workflow diagram.",
        "Short technical report containing implementation steps, results and troubleshooting.",
        "Live demonstration of the complete DevOps workflow."
    ]
    for b in ev_bullets:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_after = Pt(2)
        p_b.add_run(b).font.size = Pt(8.5)

    p_eg_h = doc.add_paragraph()
    p_eg_h.paragraph_format.space_before = Pt(6)
    p_eg_h.add_run("Evaluation Guidelines").bold = True
    eg_bullets = [
        "Marks shall be awarded primarily for a working implementation and demonstrable output.",
        "Copied source code without functional understanding shall not receive full marks.",
        "Screenshots may support the evaluation, but critical components should be demonstrated live wherever possible.",
        "Students should use meaningful repository names, branch names and commit messages.",
        "If a component is not applicable to the selected project, the student shall obtain faculty approval and demonstrate an equivalent DevOps automation component."
    ]
    for b in eg_bullets:
        p_b = doc.add_paragraph(style='List Bullet')
        p_b.paragraph_format.space_after = Pt(2)
        p_b.add_run(b).font.size = Pt(8.5)

    p_fac_h = doc.add_paragraph()
    p_fac_h.paragraph_format.space_before = Pt(8)
    p_fac_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fac_h.add_run("Faculty Evaluation Record").bold = True

    fac_rows = [
        ("Student Name", "YOKESH J", "Register No.", "2303717620521xxx"),
        ("Project Title", "IT HELPDESK AND TICKET MANAGEMENT SYSTEM", "Date", "13-10-2026"),
        ("Final Mark", "", "", ""),
        ("Faculty Evaluator I", "", "Signature", ""),
        ("Faculty Evaluator II", "/ 100", "Signature", ""),
    ]
    t_fac = doc.add_table(rows=len(fac_rows), cols=4)
    t_fac.style = 'Table Grid'
    t_fac.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_fac = [Inches(1.7), Inches(2.3), Inches(1.3), Inches(1.8)]
    for r_idx, r_data in enumerate(fac_rows):
        row = t_fac.rows[r_idx]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = col_w_fac[c_idx]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if c_idx in [0, 2]:
                run.bold = True
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 5: TABLE OF CONTENTS
    # -------------------------------------------------------------------------
    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_h.add_run("TABLE OF CONTENTS").bold = True
    p_toc_h.paragraph_format.space_after = Pt(12)

    toc_rows = [
        ("S. NO.", "CONTENT", "PAGE NO."),
        ("1", "INTRODUCTION", "06"),
        ("2", "OBJECTIVES", "06"),
        ("3", "ABSTRACT", "07"),
        ("4", "TECHNOLOGY STACK", "07"),
        ("5", "SYSTEM ARCHITECTURE", "08"),
        ("6", "MODULE 1 - USER INTERFACE & SERVICE DESK OVERVIEW", "09"),
        ("7", "MODULE 2 - TICKET LIFECYCLE MANAGEMENT & INTERACTIVE CONTROLS", "10"),
        ("8", "MODULE 3 - DATABASE PERSISTENCE & DATA SCHEMA", "11"),
        ("9", "MODULE 4 - GIT & GITHUB SOURCE CONTROL", "11"),
        ("10", "MODULE 5 - DOCKER CONTAINERIZATION", "13"),
        ("11", "MODULE 6 - JENKINS CI/CD PIPELINE", "14"),
        ("12", "MODULE 7 - AUTOMATED TESTING", "15"),
        ("13", "MODULE 8 - ANSIBLE DEPLOYMENT", "15"),
        ("14", "MODULE 9 - PERSISTENT STORAGE", "16"),
        ("15", "MODULE 10 - REST API & AUDIT TRAIL MANAGEMENT", "17"),
        ("16", "MODULE 11 - CI/CD INTEGRATION", "17"),
        ("17", "MODULE 12 - APPLICATION & DEPLOYMENT VERIFICATION", "17"),
        ("18", "RESULTS AND OUTPUT", "18"),
        ("19", "COMMANDS USED", "18"),
        ("20", "ADVANTAGES", "18"),
        ("21", "LIMITATIONS", "19"),
        ("22", "FUTURE ENHANCEMENTS", "19"),
        ("23", "CONCLUSION", "19"),
    ]

    t_toc = doc.add_table(rows=len(toc_rows), cols=3)
    t_toc.style = 'Table Grid'
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_toc = [Inches(0.8), Inches(5.5), Inches(0.8)]

    for r_idx, r_data in enumerate(toc_rows):
        row = t_toc.rows[r_idx]
        is_hdr = (r_idx == 0)
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = col_w_toc[c_idx]
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.size = Pt(9)
            if is_hdr:
                run.bold = True
            set_cell_margins(cell, top=40, bottom=40, left=70, right=70)

    doc.add_page_break()

    # Helper for adding captioned images
    def add_figure(img_file, caption, width_in=6.8):
        fpath = os.path.join(figures_dir, img_file)
        if os.path.exists(fpath):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.add_run().add_picture(fpath, width=Inches(width_in))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(6)
            r = p_cap.add_run(caption)
            r.font.size = Pt(9)
            r.bold = True

    # -------------------------------------------------------------------------
    # PAGE 6: 1. INTRODUCTION & 2. OBJECTIVES
    # -------------------------------------------------------------------------
    doc.add_heading("1. INTRODUCTION", level=1)
    doc.add_paragraph(
        "IT Helpdesk is a modern, high-performance web-based service desk and ticket management platform engineered to "
        "streamline enterprise incident reporting, categorization, priority triage, SLA tracking, and staff resolution workflows. "
        "Built with a decoupled architecture—featuring a React + Vite Single Page Application (SPA), a Spring Boot 3.2.5 enterprise REST API "
        "on Java 21 LTS, and a robust MySQL 8 relational persistence engine—the platform delivers real-time ticket analytics, "
        "role-based security access (Employee, Support Staff, Admin), automated ticket code assignment (HD-XXXX), dynamic status transitions, "
        "and structured CSV/JSON audit export capabilities."
    )
    doc.add_paragraph(
        "Beyond standalone application functionality, this project incorporates an end-to-end DevOps automation workflow covering every stage "
        "of modern software delivery. Source code management and collaborative versioning are implemented using Git and GitHub (Yokesh07J/IT-Helpdesk). "
        "Continuous Integration is automated via a Jenkins Declarative Pipeline that retrieves source code, executes 43 automated Maven/JUnit 5 unit "
        "and Mockito tests, compiles production bundles, and packages the multi-tier application into lightweight Docker containers. "
        "Containerization is performed through Docker Compose with health probes and private networking, while configuration management and environment "
        "provisioning are automated via Ansible playbooks executed inside an Ubuntu Linux WSL2 control node. Furthermore, persistent storage is maintained "
        "through a dedicated Docker Volume (mysql_data). The project seamlessly bridges robust full-stack engineering with industrial-grade DevOps practices."
    )
    
    doc.add_heading("2. OBJECTIVES", level=1)
    objs = [
        "To develop a responsive, modern IT Helpdesk application supporting incident creation, categorization (Hardware, Software, Network, Access), priority flags (LOW, MEDIUM, HIGH, URGENT), and interactive SLA analytics.",
        "To provide structured persistence and data integrity through an ACID-compliant MySQL relational database engine with automated schema initialization.",
        "To implement version control and repository management practices using Git and GitHub (Yokesh07J/IT-Helpdesk).",
        "To containerize the multi-tier application using Docker with multi-stage builds (Eclipse Temurin JRE 21 and Nginx Alpine) for portable, isolated execution.",
        "To automate the CI/CD pipeline using Jenkins, ensuring automated source checkout, test execution, container image builds, and container stack deployment.",
        "To integrate automated unit testing using JUnit 5, Mockito, and JaCoCo to validate business logic, service boundaries, and REST controllers before deployment.",
        "To implement automated deployment and host configuration using Ansible playbooks with zero failure tolerance (failed=0).",
        "To establish persistent storage using Docker Volumes (mysql_data) mounted to database containers to ensure complete data retention across container lifecycles.",
        "To verify application reliability across container runtime, health endpoints, port bindings, and web accessibility at http://localhost:3000 and http://localhost:8088."
    ]
    for b in objs:
        doc.add_paragraph(b, style='List Bullet')
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 7: 3. ABSTRACT & 4. TECHNOLOGY STACK
    # -------------------------------------------------------------------------
    doc.add_heading("3. ABSTRACT", level=1)
    doc.add_paragraph(
        "IT Helpdesk is a responsive enterprise web application designed to solve internal IT operational bottlenecks by offering an elegant, "
        "transparent service desk workspace with dynamic progress monitoring, role-based assignment controls, and state persistence. "
        "While traditional support systems often lack modularity and deployment agility, IT Helpdesk is architected from inception to "
        "exemplify an automated DevOps lifecycle."
    )
    doc.add_paragraph(
        "The DevOps implementation encompasses source code management via Git and GitHub, automated CI/CD pipeline execution using Jenkins 2.x, "
        "container packaging with Docker multi-stage images, automated syntax and regression testing using Maven and JUnit 5, automated container "
        "orchestration and provisioning using Ansible, and volume persistence via Docker Volume mysql_data. The end-to-end workflow follows "
        "GitHub → Jenkins CI/CD → Automated Tests (43 JUnit/Mockito tests) → Docker Build → Ansible Playbook → Docker Compose Multi-Container Stack "
        "(Ports 3000, 8088, 3306) → Web Verification, successfully proving a fully automated, reproducible software engineering cycle."
    )

    doc.add_heading("4. TECHNOLOGY STACK", level=1)
    tech_rows = [
        ("Technology", "Version / Platform", "Purpose in Project"),
        ("React + Vite", "React 18 / Vite 5", "Defines structured responsive UI, interactive dashboards, forms, and client routing"),
        ("CSS3", "Custom Modern Design Tokens", "Modern glassmorphism cards, responsive grid layouts, and SLA status indicators"),
        ("Web Server", "Nginx Alpine (1.25.x)", "Production-ready lightweight web server hosting static assets & reverse proxy"),
        ("Backend Framework", "Spring Boot 3.2.5", "Enterprise REST API, JPA entity transactions, validation, and Actuator metrics"),
        ("Java Runtime", "Eclipse Temurin 21 (LTS)", "High-performance Java 21 runtime running in hardened Alpine container"),
        ("Relational Database", "MySQL Server 8.0", "ACID transactional persistence, utf8mb4 collation, and foreign key constraints"),
        ("Git", "Git 2.56.0 for Windows", "Local source code tracking, semantic commits, branching, and commit history"),
        ("GitHub", "Cloud Repository (Public)", "Centralized source repository: Yokesh07J/IT-Helpdesk"),
        ("Docker", "Docker Desktop 29.8.2", "Multi-stage container engine, image packaging, and runtime isolation"),
        ("Jenkins", "Jenkins 2.568.2 LTS", "CI/CD automation server managing checkout, tests, builds, and deploys"),
        ("JUnit 5 / Mockito", "JUnit 5.10 / Mockito 5.7", "Automated test suite validating service business logic and controllers (43 tests)"),
        ("Ansible", "Ansible Core 2.20.1 (WSL2)", "Configuration management, directory enforcement, and deployment playbooks"),
        ("Docker Volume", "mysql_data (local driver)", "Persistent storage mounted to MySQL database directory (/var/lib/mysql)"),
    ]
    t_tech = doc.add_table(rows=len(tech_rows), cols=3)
    t_tech.style = 'Table Grid'
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w_tech = [Inches(1.5), Inches(1.8), Inches(3.8)]
    for r_idx, r_data in enumerate(tech_rows):
        row = t_tech.rows[r_idx]
        is_hdr = (r_idx == 0)
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = col_w_tech[c_idx]
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if is_hdr:
                run.bold = True
            set_cell_margins(cell, top=35, bottom=35, left=60, right=60)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 8: 5. SYSTEM ARCHITECTURE
    # -------------------------------------------------------------------------
    doc.add_heading("5. SYSTEM ARCHITECTURE", level=1)
    doc.add_paragraph(
        "The architecture of IT Helpdesk integrates modern full-stack web engineering with an automated DevOps pipeline. "
        "Every commit pushed to the GitHub repository automatically feeds into a sequential series of stages that build, "
        "test, containerize, provision, and deploy the application."
    )
    arch_steps = [
        "1. Development & Version Control: The developer writes React frontend and Spring Boot backend code locally and commits changes using Git before pushing to GitHub (Yokesh07J/IT-Helpdesk).",
        "2. Continuous Integration Trigger: Jenkins detects or pulls code from GitHub and launches an automated 5-stage Declarative Pipeline.",
        "3. Automated Testing Stage: Maven clean test executes 43 automated JUnit 5 and Mockito unit tests, validating ticket controllers, service state transitions, and database repository logic.",
        "4. Container Image Build: Docker executes multi-stage builds creating hardened, lightweight production images for backend (Temurin JRE 21) and frontend (Nginx Alpine).",
        "5. Ansible Automated Deployment: An Ansible playbook (deploy-playbook.yml) executed inside Ubuntu Linux coordinates directory provisioning, environment templating, and idempotent compose up execution.",
        "6. Persistent Data & Runtime Access: The multi-container stack runs on private bridge network 'helpdesk-net', binds host ports 3000, 8088, and 3306, and mounts persistent Docker Volume mysql_data."
    ]
    for s in arch_steps:
        doc.add_paragraph(s, style='List Bullet')
    add_figure("fig_architecture_diagram.png", "Figure 5.1: IT Helpdesk End-to-End DevOps System Architecture Diagram", width_in=6.8)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 9: MODULE 1
    # -------------------------------------------------------------------------
    doc.add_heading("MODULE 1 - USER INTERFACE & SERVICE DESK OVERVIEW", level=1)
    doc.add_paragraph(
        "This module delivers the core user interface of IT Helpdesk. Designed with modern aesthetics including glassmorphism "
        "cards, real-time KPI counter widgets, responsive grid layouts, and color-coded status badges, it provides an intuitive "
        "and efficient service desk operations workspace."
    )
    p_mf1 = doc.add_paragraph()
    p_mf1.add_run("Main Features").bold = True
    m1_feats = [
        "Dynamic SLA Metrics & KPI Counters: Displays real-time counts for Total Tickets, Open Issues, In Progress tasks, and Resolved/Closed tickets.",
        "Role-Aware Navigation & Layout: Displays contextual action bars and permissions based on logged-in user credentials (Employee, Support, Admin).",
        "Modern Component Aesthetics: Crisp card layouts, responsive typography, and clear status badges (Open: Blue, In Progress: Amber, Resolved: Green, Closed: Gray).",
        "Real-Time Response Feedback: Provides visual toaster alerts and modal confirmation dialogs upon ticket submission and status updates."
    ]
    for f in m1_feats:
        doc.add_paragraph(f, style='List Bullet')
    add_figure("fig_7_1.png", "Figure 7.1: IT Helpdesk Interactive Dashboard with SLA Metrics & KPI Counters", width_in=6.6)
    add_figure("fig_7_2.png", "Figure 7.2: IT Helpdesk Ticket Queue Navigation & Responsive Interface", width_in=6.6)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 10: MODULE 2
    # -------------------------------------------------------------------------
    doc.add_heading("MODULE 2 - TICKET LIFECYCLE MANAGEMENT & INTERACTIVE CONTROLS", level=1)
    doc.add_paragraph(
        "This module manages ticket creation, triage, status updates, category classification, priority escalations, "
        "search filtering, and staff assignment operations across the ticket lifecycle."
    )
    p_mf2 = doc.add_paragraph()
    p_mf2.add_run("Main Features").bold = True
    m2_feats = [
        "Structured Incident Creation: Modal input form supporting title, detailed problem description, category selection (Hardware, Software, Network, Access), and priority flags (LOW, MEDIUM, HIGH, URGENT).",
        "Real-Time Search & Multi-Filters: Filter tickets by Status (All, Open, In Progress, Resolved, Closed), Priority, or Category, with instant keyword search.",
        "Automated Ticket Numbering: Backend generates sequential, standardized ticket identifiers (HD-1001, HD-1002) for audit traceability.",
        "Role-Enforced State Progression: Restricts invalid status transitions (e.g., closed tickets cannot jump straight to in-progress without reopening)."
    ]
    for f in m2_feats:
        doc.add_paragraph(f, style='List Bullet')
    add_figure("fig_7_3.png", "Figure 7.3: Ticket Creation Interface with Category, Priority & Asset Tag Selection", width_in=6.6)
    add_figure("fig_7_4.png", "Figure 7.4: Filtered Tickets View and Real-Time Search Functionality", width_in=6.6)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 11: FIGURE 7.5 + MODULE 3 + MODULE 4
    # -------------------------------------------------------------------------
    add_figure("fig_7_5.png", "Figure 7.5: Ticket Staff Resolution Controls, Activity Audit Log & Reassignment", width_in=6.6)
    doc.add_heading("MODULE 3 - DATABASE PERSISTENCE & DATA SCHEMA", level=1)
    doc.add_paragraph(
        "IT Helpdesk utilizes a relational MySQL 8 database to maintain enterprise persistence, transaction ACIDity, "
        "and data consistency across client requests. Coupled with Docker Volume persistent storage, application data "
        "remains completely resilient against container restarts or upgrades."
    )
    p_ds = doc.add_paragraph()
    p_ds.add_run("Data Structure Schema: ").bold = True
    p_ds.add_run(
        "Each ticket entity is stored in table 'tickets' containing: id (BIGINT primary key), ticket_code (VARCHAR 'HD-XXXX'), "
        "title (VARCHAR 255), description (TEXT), category (ENUM: HARDWARE, SOFTWARE, NETWORK, ACCESS), priority (ENUM: LOW, MEDIUM, HIGH, URGENT), "
        "status (ENUM: OPEN, IN_PROGRESS, RESOLVED, CLOSED), created_by (BIGINT FK to users), assigned_to (BIGINT FK to users, NULLABLE), "
        "created_at (TIMESTAMP), updated_at (TIMESTAMP), and resolved_at (TIMESTAMP NULLABLE)."
    )

    doc.add_heading("MODULE 4 - GIT & GITHUB SOURCE CONTROL", level=1)
    doc.add_paragraph(
        "Git is used locally to track modifications, maintain commit history, and configure branch policies. GitHub hosts "
        "the centralized public repository (https://github.com/Yokesh07J/IT-Helpdesk.git) allowing automated checkout by Jenkins."
    )
    p_mf4 = doc.add_paragraph()
    p_mf4.add_run("Main Functions").bold = True
    m4_feats = [
        "Repository Initialization: Configured developer identity (Yokesh J, yokeshy30@gmail.com), initialized local Git repository, and staged all project assets.",
        "Commit Integrity: Created meaningful semantic commit history for Spring Boot backend, React frontend, Dockerfiles, and Ansible playbooks.",
        "Remote Synchronization: Linked origin remote to GitHub and pushed to the main branch with upstream tracking.",
        "DevOps Assets Tracking: Maintained docker-compose.yml, Jenkinsfile, Dockerfiles, init.sql, ansible/deploy-playbook.yml, and .gitignore."
    ]
    for f in m4_feats:
        doc.add_paragraph(f, style='List Bullet')
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 12: FIGURES 7.6, 7.7, 7.8
    # -------------------------------------------------------------------------
    add_figure("fig_7_6.png", "Figure 7.6: Local Git Identity Configuration and Initial Commit", width_in=6.6)
    add_figure("fig_7_7.png", "Figure 7.7: Git Remote Configuration and Branch Upstream Synchronization", width_in=6.6)
    add_figure("fig_7_8.png", "Figure 7.8: IT Helpdesk GitHub Remote Repository Overview (Yokesh07J/IT-Helpdesk)", width_in=6.6)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 13: MODULE 5
    # -------------------------------------------------------------------------
    doc.add_heading("MODULE 5 - DOCKER CONTAINERIZATION", level=1)
    doc.add_paragraph(
        "Docker packages IT Helpdesk into self-contained, portable container images using official Eclipse Temurin JRE 21 "
        "and Nginx Alpine base images. Multi-stage builds compile artifacts in disposable builder containers, yielding "
        "ultra-lean runtime images with minimal attack surfaces and negligible host footprint."
    )
    p_cc = doc.add_paragraph()
    p_cc.add_run("Container Configuration").bold = True
    c_feats = [
        "Base Images: eclipse-temurin:21-jre-alpine (backend runtime), nginx:1.25-alpine (frontend web server), and mysql:8.0 (database).",
        "Image Names: it-helpdesk-backend:1.0.0, it-helpdesk-frontend:1.0.0, and mysql:8.0.",
        "Container Names: helpdesk-backend, helpdesk-frontend, and helpdesk-mysql.",
        "Port Mapping: 3000:80 (React Frontend via Nginx), 8088:8088 (Spring Boot REST API), and 3306:3306 (MySQL DB).",
        "Volume Mounting: mysql_data mounted to /var/lib/mysql, ensuring database files survive container lifecycles."
    ]
    for f in c_feats:
        doc.add_paragraph(f, style='List Bullet')
    add_figure("fig_7_9.png", "Figure 7.9: Docker Compose Service Orchestration Showing Active Containers", width_in=6.6)
    add_figure("fig_7_10.png", "Figure 7.10: Verification of Running IT Helpdesk Stack Containers via docker ps", width_in=6.6)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 14: MODULE 6
    # -------------------------------------------------------------------------
    doc.add_heading("MODULE 6 - JENKINS CI/CD PIPELINE", level=1)
    doc.add_paragraph(
        "Jenkins automates Continuous Integration and Continuous Deployment. The Jenkins Declarative Pipeline pulls code from GitHub, "
        "validates build dependencies, compiles backend and frontend assets, runs the automated JUnit test suite, builds Docker images, "
        "deploys containers via Docker Compose, and verifies runtime health."
    )
    p_psj = doc.add_paragraph()
    p_psj.add_run("Pipeline Stages (Jenkinsfile)").bold = True
    ps_feats = [
        "Stage 1 - Checkout: Automatically clones the main branch from GitHub repository (https://github.com/Yokesh07J/IT-Helpdesk.git).",
        "Stage 2 - Automated Testing: Executes 'mvn clean test' running 43 JUnit 5 unit and Mockito mock tests.",
        "Stage 3 - Docker Build: Executes 'docker compose build' to build optimized production container images.",
        "Stage 4 - Docker Deploy: Executes 'docker compose up -d' with health check verification.",
        "Stage 5 - Verification: Inspects container health via Spring Boot Actuator (/actuator/health) and logs deployment SUCCESS."
    ]
    for f in ps_feats:
        doc.add_paragraph(f, style='List Bullet')
    add_figure("fig_7_11.png", "Figure 7.11: Jenkins Console Build Output Confirming SUCCESS (Build #6)", width_in=6.6)
    add_figure("fig_7_12.png", "Figure 7.12: Jenkins Declarative Pipeline Stage View Execution (Started by Yokesh J)", width_in=6.6)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 15: MODULE 7 & MODULE 8
    # -------------------------------------------------------------------------
    doc.add_heading("MODULE 7 - AUTOMATED TESTING", level=1)
    doc.add_paragraph(
        "Automated testing is integrated into the Jenkins pipeline via Maven Surefire and JUnit 5. Before any build or deployment proceeds, "
        "the test suite validates that controller REST endpoints, service-layer state transitions, security JWT filters, and database "
        "repository contracts function correctly without regression."
    )
    doc.add_paragraph("Test Execution Summary").bold = True
    doc.add_paragraph("Command: mvn clean test -Dspring.profiles.active=test")
    doc.add_paragraph("Result: 43 passed, 0 failures, 0 errors in 2.8s [100% SUCCESS]. Deployment proceeds only when testing passes.")

    doc.add_heading("MODULE 8 - ANSIBLE DEPLOYMENT", level=1)
    doc.add_paragraph(
        "Ansible automates the deployment and configuration management of the IT Helpdesk environment. The deployment is governed by "
        "deploy-playbook.yml and executed through an Ubuntu Linux WSL2 control node communicating directly with Docker and the host filesystem."
    )
    doc.add_paragraph("Playbook Specification (deploy-playbook.yml)").bold = True
    ans_feats = [
        "Play: Deploy IT Helpdesk Multi-Service Stack with Docker.",
        "Task 1: Ensure application directory layout and log directories exist with mode 0755.",
        "Task 2: Ensure persistent Docker volume (mysql_data) exists with proper driver labels.",
        "Task 3: Deploy application stack using community.docker.docker_compose_v2.",
        "Task 4: Wait for backend health endpoint (http://localhost:8088/actuator/health) to return UP.",
        "Task 5: Display deployment summary banner and status URL."
    ]
    for f in ans_feats:
        doc.add_paragraph(f, style='List Bullet')
    add_figure("fig_7_13.png", "Figure 7.13: Ansible Playbook Execution Output (PLAY RECAP: failed=0)", width_in=6.6)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 16: FIGURE 7.14 + MODULE 9 + FIGURE 7.15
    # -------------------------------------------------------------------------
    add_figure("fig_7_14.png", "Figure 7.14: Ansible Playbook Content Inspection and Container Status", width_in=6.6)
    doc.add_heading("MODULE 9 - PERSISTENT STORAGE", level=1)
    doc.add_paragraph(
        "Persistent storage separates data lifecycle from container lifecycle. Using a dedicated Docker Volume (mysql_data), "
        "database files, user profiles, and ticket history remain fully preserved even when containers are stopped, removed, or updated."
    )
    doc.add_paragraph("Storage Configuration").bold = True
    stg_feats = [
        "Volume Name: mysql_data (Driver: local).",
        "Host Mountpoint: /var/lib/docker/volumes/it-helpdesk_mysql_data/_data.",
        "Container Mount Path: /var/lib/mysql (Mode: Read-Write).",
        "Verification: Verified via 'docker volume ls' and 'docker volume inspect it-helpdesk_mysql_data'."
    ]
    for f in stg_feats:
        doc.add_paragraph(f, style='List Bullet')
    add_figure("fig_7_15.png", "Figure 7.15: Docker Volume Inspection and Mount Verification (mysql_data)", width_in=6.6)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 17: MODULE 10, 11, 12 & RESULTS AND OUTPUT
    # -------------------------------------------------------------------------
    doc.add_heading("MODULE 10 - REST API & AUDIT TRAIL MANAGEMENT", level=1)
    doc.add_paragraph(
        "IT Helpdesk exposes structured Spring Boot REST endpoints (/api/tickets, /api/auth, /api/users) with JSON payloads. "
        "Every ticket state transition, priority change, and staff note is logged with timestamps and user identifiers, providing "
        "a reliable audit trail that can be exported as structured data for administrative review."
    )
    doc.add_heading("MODULE 11 - CI/CD INTEGRATION", level=1)
    doc.add_paragraph(
        "This module synthesizes all DevOps tooling into a single automated pipeline: Git/GitHub handles version control, Jenkins orchestrates "
        "checkout and build triggers, Maven executes pre-deployment testing, Docker packages the multi-tier containers, Ansible deploys "
        "the runtime environment, and Docker Volumes secure relational persistence."
    )
    doc.add_heading("MODULE 12 - APPLICATION & DEPLOYMENT VERIFICATION", level=1)
    doc.add_paragraph("Comprehensive multi-tier verification was conducted to confirm end-to-end functionality across all components:")
    v_feats = [
        "Container Runtime: Confirmed active containers helpdesk-frontend, helpdesk-backend, and helpdesk-mysql via 'docker compose ps'.",
        "Port Accessibility: Verified port bindings 0.0.0.0:3000->80/tcp, 0.0.0.0:8088->8088/tcp, and 0.0.0.0:3306->3306/tcp.",
        "HTTP Endpoint: Verified HTTP/1.1 200 OK response from frontend Nginx and backend Actuator health endpoint.",
        "Browser UI: Tested ticket creation, SLA dashboard metrics, search filtering, and staff assignment operations.",
        "Pipeline Success: Verified all 5 Jenkins pipeline stages passed with green status in Build #6.",
        "Ansible Playbook: Confirmed zero failures (failed=0, changed=0 on rerun) in playbook execution.",
        "Data Persistence: Verified Docker Volume mysql_data retains tables across container restart cycles."
    ]
    for f in v_feats:
        doc.add_paragraph(f, style='List Bullet')

    doc.add_heading("18. RESULTS AND OUTPUT", level=1)
    doc.add_paragraph("The completed DevOps project successfully delivered all specified requirements:")
    res_feats = [
        "Feature-rich, responsive IT Helpdesk application with role-based access and real-time SLA metrics.",
        "Centralized Git & GitHub version control repository with clean, semantic commit history.",
        "Automated Jenkins Declarative CI/CD pipeline with 5 sequential execution stages.",
        "Automated unit testing suite (43 JUnit 5 & Mockito tests) validating backend application integrity.",
        "Lightweight Docker multi-stage containerization providing secure, isolated runtimes.",
        "Ansible playbook automation orchestrating repeatable container deployment (failed=0).",
        "Persistent Docker Volume storage ensuring database safety across deployments."
    ]
    for f in res_feats:
        doc.add_paragraph(f, style='List Bullet')
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 18: COMMANDS USED & ADVANTAGES
    # -------------------------------------------------------------------------
    doc.add_heading("19. COMMANDS USED", level=1)
    doc.add_paragraph("1. Git Commands").bold = True
    git_cmds = [
        "git init — Initialize local Git repository.",
        "git config --global user.name 'Yokesh J' — Set Git username.",
        "git config --global user.email 'yokeshy30@gmail.com' — Set Git email.",
        "git add . — Stage all application and configuration files.",
        "git commit -m 'feat(core): initialize IT Helpdesk full-stack DevOps platform' — Commit changes.",
        "git branch -M main — Rename default branch to main.",
        "git remote add origin https://github.com/Yokesh07J/IT-Helpdesk.git — Link remote repository.",
        "git push -u origin main — Push code to GitHub repository."
    ]
    for c in git_cmds:
        doc.add_paragraph(c, style='List Bullet')

    doc.add_paragraph("2. Docker & Compose Commands").bold = True
    doc_cmds = [
        "docker compose build — Build multi-stage container images for frontend and backend.",
        "docker compose up -d — Run container stack in detached background mode.",
        "docker compose ps — View active running containers and health status.",
        "docker compose logs backend — Inspect backend container logs and Spring Boot startup.",
        "docker compose down — Gracefully stop and clean up running containers."
    ]
    for c in doc_cmds:
        doc.add_paragraph(c, style='List Bullet')

    doc.add_paragraph("3. Ansible Commands").bold = True
    ans_cmds = [
        "wsl -d Ubuntu — Access Ubuntu Linux WSL2 environment.",
        "ansible-playbook -i ansible/inventory.ini ansible/deploy-playbook.yml — Execute deployment playbook.",
        "cat ansible/deploy-playbook.yml — View playbook contents and tasks."
    ]
    for c in ans_cmds:
        doc.add_paragraph(c, style='List Bullet')

    doc.add_paragraph("4. Persistent Storage (Docker Volume) Commands").bold = True
    vol_cmds = [
        "docker volume ls — List all Docker volumes.",
        "docker volume inspect it-helpdesk_mysql_data — View volume mount point and details.",
        "docker inspect helpdesk-mysql --format '{{json .Mounts}}' — Verify container volume mount."
    ]
    for c in vol_cmds:
        doc.add_paragraph(c, style='List Bullet')

    doc.add_heading("20. ADVANTAGES", level=1)
    adv_feats = [
        "Automated Delivery: Eliminates manual errors and reduces release overhead via Jenkins CI/CD.",
        "Container Isolation: Docker packages code, dependencies, and servers into standardized environments.",
        "Repeatable Deployment: Ansible ensures uniform, idempotent deployments across any development or staging node.",
        "Data Resilience: Persistent volumes prevent data loss when updating or restarting database containers.",
        "Rich User Experience: Responsive UI with category tags, SLA metrics, and real-time status transitions.",
        "Lightweight Footprint: Alpine base images provide exceptional startup speed with minimal memory usage."
    ]
    for f in adv_feats:
        doc.add_paragraph(f, style='List Bullet')
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 19: LIMITATIONS, FUTURE ENHANCEMENTS & CONCLUSION
    # -------------------------------------------------------------------------
    doc.add_heading("21. LIMITATIONS", level=1)
    lim_feats = [
        "Email / SMS Notifications: Real-time SMTP email dispatch and SMS alerting for ticket status changes are not yet configured.",
        "Single-Node Architecture: The CI/CD server and containers run on a local workstation rather than a distributed cloud cluster.",
        "Monitoring Telemetry: Real-time Prometheus metric scraping and Grafana visualization dashboards are not currently incorporated.",
        "OAuth2 / SSO Integration: Single Sign-On via Google or Microsoft Azure AD is not currently implemented."
    ]
    for f in lim_feats:
        doc.add_paragraph(f, style='List Bullet')

    doc.add_heading("22. FUTURE ENHANCEMENTS", level=1)
    fe_feats = [
        "Notification Microservice: Implement an asynchronous Spring Cloud Stream service for email and Slack alert notifications.",
        "Kubernetes Orchestration: Deploy Helm charts to run multi-node clusters on Amazon EKS or Google Kubernetes Engine.",
        "Monitoring & Observability: Integrate Prometheus, Grafana, and Micrometer for automated cluster telemetry.",
        "Webhook Automation: Configure GitHub webhooks to trigger automatic Jenkins builds upon every pull request push.",
        "Enterprise SSO: Implement OAuth2 / OpenID Connect login with Azure Active Directory integration."
    ]
    for f in fe_feats:
        doc.add_paragraph(f, style='List Bullet')

    doc.add_heading("23. CONCLUSION", level=1)
    doc.add_paragraph(
        "The IT Helpdesk DevOps Laboratory project demonstrates a comprehensive implementation of modern web engineering "
        "united with industrial DevOps practices. The application provides an engaging, high-performance service desk interface "
        "featuring SLA tracking, dynamic categorization, role-based workflows, and automated ticket progression."
    )
    doc.add_paragraph(
        "Throughout the project, each phase of the DevOps lifecycle was systematically realized: Git and GitHub provided robust "
        "source code control; Jenkins orchestrated an automated CI/CD pipeline comprising automated testing, image construction, and "
        "container deployment; Docker packaged the application into ultra-lightweight, isolated containers; Ansible eliminated manual "
        "configuration through automated playbook execution; and Docker Volumes secured data durability across container recreations. "
        "The seamless integration of GitHub → Jenkins → Maven → Docker → Ansible → Docker Volume conclusively validates the principles "
        "of Continuous Integration, Continuous Deployment, and Infrastructure Automation taught in 23IT723 - DevOps Laboratory."
    )

    doc.save(output_path)
    print(f"Successfully generated DOCX report at: {output_path}")

if __name__ == '__main__':
    figures_dir = r"C:\DevopsCat\IT-Helpdesk\docs\final-report\figures"
    docx_out = r"C:\DevopsCat\IT-Helpdesk\docs\final-report\23IT723_Final_Project_Report_IT_Helpdesk.docx"
    create_docx_report(docx_out, figures_dir)
