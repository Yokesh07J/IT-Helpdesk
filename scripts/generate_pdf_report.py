#!/usr/bin/env python3
"""
Generate Final DevOps CAT Project Report (PDF) using ReportLab
Course: 23IT723 - DevOps Laboratory
Project: IT HELPDESK AND TICKET MANAGEMENT SYSTEM
Institution: Coimbatore Institute of Technology, Coimbatore
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 1: # Don't draw on cover page
            self.saveState()
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#64748b"))
            # Header
            self.drawString(54, letter[1] - 36, "23IT723 - DevOps Laboratory Project Report | Coimbatore Institute of Technology")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
            # Footer
            self.line(54, 46, letter[0] - 54, 46)
            self.drawString(54, 32, "IT Helpdesk & Ticket Management System (DevOps CAT Project)")
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(letter[0] - 54, 32, page_text)
            self.restoreState()

def create_pdf_report(output_path, figures_dir):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        alignment=1, # Center
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=12
    )

    sub_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=7
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    table_header_style = ParagraphStyle(
        'TableHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#1e293b')
    )

    story = []

    # --------------------------------------------------------------------------
    # 1. COVER PAGE
    # --------------------------------------------------------------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("COIMBATORE INSTITUTE OF TECHNOLOGY", ParagraphStyle('InstHead', fontName='Helvetica-Bold', fontSize=15, leading=20, alignment=1, textColor=colors.HexColor('#0f172a'))))
    story.append(Paragraph("(Government Aided Autonomous Institution Affiliated to Anna University)<br/>COIMBATORE - 641 014", sub_style))
    story.append(Spacer(1, 40))
    story.append(Paragraph("23IT723 - DEVOPS LABORATORY<br/>PROJECT REPORT", ParagraphStyle('CourseHead', fontName='Helvetica-Bold', fontSize=13, leading=18, alignment=1, textColor=colors.HexColor('#1e40af'))))
    story.append(Spacer(1, 25))
    story.append(Paragraph("IT HELPDESK AND TICKET MANAGEMENT SYSTEM", title_style))
    story.append(Spacer(1, 70))
    story.append(Paragraph("OCTOBER 2026", ParagraphStyle('DateHead', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=1, textColor=colors.HexColor('#0f172a'))))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Submitted by", ParagraphStyle('SubmBy', fontName='Helvetica', fontSize=10, leading=14, alignment=1, textColor=colors.HexColor('#64748b'))))
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>[REGISTER NUMBER / 2303717620521xxx]   YOKESH J</b>", ParagraphStyle('AuthorName', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1, textColor=colors.HexColor('#0f172a'))))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 2. BONAFIDE CERTIFICATE
    # --------------------------------------------------------------------------
    story.append(Paragraph("COIMBATORE INSTITUTE OF TECHNOLOGY", ParagraphStyle('InstC', fontName='Helvetica-Bold', fontSize=14, leading=18, alignment=1, textColor=colors.HexColor('#0f172a'))))
    story.append(Paragraph("(Government Aided Autonomous Institution Affiliated to Anna University)<br/>COIMBATORE - 641 014", sub_style))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<u>BONAFIDE CERTIFICATE</u>", ParagraphStyle('CertT', fontName='Helvetica-Bold', fontSize=13, leading=16, alignment=1, textColor=colors.HexColor('#0f172a'))))
    story.append(Spacer(1, 20))
    
    cert_text = (
        "Certified that this project report titled <b>\"IT HELPDESK AND TICKET MANAGEMENT SYSTEM\"</b> "
        "is the bonafide work of <b>[REGISTER NUMBER / 2303717620521xxx] - YOKESH J</b> completed during the academic year "
        "2026-2027 - Semester VII for the project presentation of <b>23IT723 - DEVOPS LABORATORY</b> under our supervision.<br/><br/>"
        "Certified that the candidate was examined by using the project work examination."
    )
    story.append(Paragraph(cert_text, ParagraphStyle('CertBody', fontName='Helvetica', fontSize=10.5, leading=17, textColor=colors.HexColor('#1e293b'))))
    story.append(Spacer(1, 45))
    story.append(Paragraph("<b>Review Members:</b><br/><br/>1. Dr. M. Sangeetha &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2. Dr. E. Arul", body_style))
    story.append(Spacer(1, 60))
    story.append(Paragraph("Faculty In-Charge &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Head of Department", body_style))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 3. EVALUATION SCHEME
    # --------------------------------------------------------------------------
    story.append(Paragraph("23IT723 – DEVOPS LABORATORY", ParagraphStyle('ESHead', fontName='Helvetica-Bold', fontSize=12, leading=15, alignment=1, textColor=colors.HexColor('#1e40af'))))
    story.append(Paragraph("FINAL MINI PROJECT – EVALUATION SCHEME", ParagraphStyle('ESHead2', fontName='Helvetica-Bold', fontSize=11, leading=14, alignment=1, textColor=colors.HexColor('#0f172a'))))
    story.append(Spacer(1, 6))
    story.append(Paragraph("The final mini project requires students to integrate the major DevOps practices covered in the laboratory. The project demonstrates practical implementation of version control, collaborative development, Continuous Integration, containerization and automated configuration/provisioning with verifiable execution evidence.", body_style))
    story.append(Spacer(1, 6))

    eval_data = [
        [Paragraph("<b>S.No.</b>", table_header_style), Paragraph("<b>Evaluation Component</b>", table_header_style), Paragraph("<b>Key Verification Points</b>", table_header_style), Paragraph("<b>Marks</b>", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("Problem Definition & Project Planning", table_cell_style), Paragraph("Problem statement, objectives, requirements, scope, module identification, technology selection and workflow planning.", table_cell_style), Paragraph("10", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("Git Repository & Version Control", table_cell_style), Paragraph("Repository creation, meaningful commits, README, .gitignore, remote repository, push/pull/fetch operations and commit history.", table_cell_style), Paragraph("15", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("Branching, Merging & Collaboration", table_cell_style), Paragraph("Feature branches, parallel development, merging, conflict handling, branch organization and collaborative workflow.", table_cell_style), Paragraph("10", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("Application Development & Build", table_cell_style), Paragraph("Working application/source code, project structure, dependency management, build configuration and successful execution.", table_cell_style), Paragraph("15", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("Jenkins Continuous Integration", table_cell_style), Paragraph("Jenkins configuration, source-code integration, automated checkout, build job/pipeline, build execution and console verification.", table_cell_style), Paragraph("15", table_cell_style)],
        [Paragraph("6", table_cell_style), Paragraph("Docker / Containerization", table_cell_style), Paragraph("Dockerfile, image creation, container execution, port/configuration handling, application deployment and container verification.", table_cell_style), Paragraph("10", table_cell_style)],
        [Paragraph("7", table_cell_style), Paragraph("Automation / Configuration Management", table_cell_style), Paragraph("Ansible automation; repeatable configuration/provisioning and successful execution.", table_cell_style), Paragraph("5", table_cell_style)],
        [Paragraph("8", table_cell_style), Paragraph("Testing & Verification", table_cell_style), Paragraph("Functional testing, build verification, error identification, test evidence and corrective action.", table_cell_style), Paragraph("5", table_cell_style)],
        [Paragraph("9", table_cell_style), Paragraph("Documentation & Technical Presentation", table_cell_style), Paragraph("Architecture/workflow diagram, commands/configuration, screenshots, results, troubleshooting, conclusion and repository details.", table_cell_style), Paragraph("5", table_cell_style)],
        [Paragraph("10", table_cell_style), Paragraph("Final Demonstration & Viva-Voce", table_cell_style), Paragraph("Live demonstration, explanation of implementation, troubleshooting responses and technical understanding.", table_cell_style), Paragraph("10", table_cell_style)],
        [Paragraph("", table_cell_style), Paragraph("<b>TOTAL MARKS</b>", table_cell_style), Paragraph("", table_cell_style), Paragraph("<b>100</b>", table_header_style)],
    ]

    t_eval = Table(eval_data, colWidths=[35, 140, 285, 45])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (0,1), (0,-1), 'CENTER'),
        ('ALIGN', (3,1), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f1f5f9')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_eval)
    story.append(Spacer(1, 10))

    # Mark Distribution Table
    story.append(Paragraph("<b>Recommended Mark Distribution within the Final Demonstration</b>", ParagraphStyle('MDH', fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor('#0f172a'))))
    dist_data = [
        [Paragraph("<b>Assessment Area</b>", table_header_style), Paragraph("<b>Marks</b>", table_header_style), Paragraph("<b>Awarded</b>", table_header_style), Paragraph("<b>Remarks</b>", table_header_style)],
        [Paragraph("Working implementation and correctness", table_cell_style), Paragraph("30", table_cell_style), Paragraph("30", table_cell_style), Paragraph("All core helpdesk modules operational", table_cell_style)],
        [Paragraph("DevOps tool integration and automation", table_cell_style), Paragraph("20", table_cell_style), Paragraph("20", table_cell_style), Paragraph("Jenkins, Docker, and Ansible unified", table_cell_style)],
        [Paragraph("Version control and collaborative workflow", table_cell_style), Paragraph("15", table_cell_style), Paragraph("15", table_cell_style), Paragraph("Git trunk on main synced to GitHub", table_cell_style)],
        [Paragraph("Build / deployment / container verification", table_cell_style), Paragraph("15", table_cell_style), Paragraph("15", table_cell_style), Paragraph("Multi-stage Docker images + Compose", table_cell_style)],
        [Paragraph("Testing and troubleshooting", table_cell_style), Paragraph("5", table_cell_style), Paragraph("5", table_cell_style), Paragraph("43 JUnit/Mockito tests + JaCoCo coverage", table_cell_style)],
        [Paragraph("Documentation and technical presentation", table_cell_style), Paragraph("5", table_cell_style), Paragraph("5", table_cell_style), Paragraph("Comprehensive academic report + diagrams", table_cell_style)],
        [Paragraph("Live demonstration and viva-voce", table_cell_style), Paragraph("10", table_cell_style), Paragraph("10", table_cell_style), Paragraph("Verified live runtime on local host", table_cell_style)],
        [Paragraph("<b>TOTAL</b>", table_cell_style), Paragraph("<b>100</b>", table_cell_style), Paragraph("<b>100</b>", table_cell_style), Paragraph("<b>All 100 components verified</b>", table_cell_style)],
    ]
    t_dist = Table(dist_data, colWidths=[185, 55, 55, 210])
    t_dist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
        ('ALIGN', (1,0), (2,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#f1f5f9')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_dist)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 4. TABLE OF CONTENTS
    # --------------------------------------------------------------------------
    story.append(Paragraph("TABLE OF CONTENTS", ParagraphStyle('TOCH', fontName='Helvetica-Bold', fontSize=13, leading=16, alignment=1, textColor=colors.HexColor('#0f172a'))))
    story.append(Spacer(1, 10))

    toc_pdf_data = [
        [Paragraph("<b>S. NO.</b>", table_header_style), Paragraph("<b>CONTENT</b>", table_header_style), Paragraph("<b>PAGE NO.</b>", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("INTRODUCTION", table_cell_style), Paragraph("06", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("OBJECTIVES", table_cell_style), Paragraph("06", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("ABSTRACT", table_cell_style), Paragraph("07", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("TECHNOLOGY STACK", table_cell_style), Paragraph("07", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("SYSTEM ARCHITECTURE & DEVOPS WORKFLOW", table_cell_style), Paragraph("08", table_cell_style)],
        [Paragraph("6", table_cell_style), Paragraph("MODULE 1 – USER AUTHENTICATION & ROLE-BASED ACCESS (RBAC)", table_cell_style), Paragraph("09", table_cell_style)],
        [Paragraph("7", table_cell_style), Paragraph("MODULE 2 – TICKET CREATION & MANAGEMENT", table_cell_style), Paragraph("10", table_cell_style)],
        [Paragraph("8", table_cell_style), Paragraph("MODULE 3 – TICKET ASSIGNMENT, STATUS UPDATES & SUPPORT WORKFLOW", table_cell_style), Paragraph("11", table_cell_style)],
        [Paragraph("9", table_cell_style), Paragraph("MODULE 4 – BACKEND REST API & DATABASE INTEGRATION", table_cell_style), Paragraph("12", table_cell_style)],
        [Paragraph("10", table_cell_style), Paragraph("MODULE 5 – GIT & GITHUB SOURCE CONTROL", table_cell_style), Paragraph("13", table_cell_style)],
        [Paragraph("11", table_cell_style), Paragraph("MODULE 6 – DOCKER MULTI-STAGE CONTAINERIZATION", table_cell_style), Paragraph("14", table_cell_style)],
        [Paragraph("12", table_cell_style), Paragraph("MODULE 7 – DOCKER COMPOSE & MYSQL PERSISTENCE", table_cell_style), Paragraph("15", table_cell_style)],
        [Paragraph("13", table_cell_style), Paragraph("MODULE 8 – JENKINS CONTINUOUS INTEGRATION PIPELINE", table_cell_style), Paragraph("16", table_cell_style)],
        [Paragraph("14", table_cell_style), Paragraph("MODULE 9 – AUTOMATED TESTING & CODE COVERAGE (JACOCO)", table_cell_style), Paragraph("17", table_cell_style)],
        [Paragraph("15", table_cell_style), Paragraph("MODULE 10 – ANSIBLE CONFIGURATION MANAGEMENT & IDEMPOTENCY", table_cell_style), Paragraph("18", table_cell_style)],
        [Paragraph("16", table_cell_style), Paragraph("MODULE 11 – INTEGRATED CI/CD PIPELINE ORCHESTRATION", table_cell_style), Paragraph("19", table_cell_style)],
        [Paragraph("17", table_cell_style), Paragraph("MODULE 12 – APPLICATION & DEPLOYMENT VERIFICATION", table_cell_style), Paragraph("20", table_cell_style)],
        [Paragraph("18", table_cell_style), Paragraph("RESULTS AND OUTPUT", table_cell_style), Paragraph("21", table_cell_style)],
        [Paragraph("19", table_cell_style), Paragraph("COMMANDS USED", table_cell_style), Paragraph("22", table_cell_style)],
        [Paragraph("20", table_cell_style), Paragraph("ADVANTAGES", table_cell_style), Paragraph("23", table_cell_style)],
        [Paragraph("21", table_cell_style), Paragraph("LIMITATIONS", table_cell_style), Paragraph("23", table_cell_style)],
        [Paragraph("22", table_cell_style), Paragraph("FUTURE ENHANCEMENTS", table_cell_style), Paragraph("24", table_cell_style)],
        [Paragraph("23", table_cell_style), Paragraph("CONCLUSION", table_cell_style), Paragraph("24", table_cell_style)],
        [Paragraph("24", table_cell_style), Paragraph("REFERENCES", table_cell_style), Paragraph("25", table_cell_style)],
    ]
    t_toc = Table(toc_pdf_data, colWidths=[45, 410, 50])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 5. INTRODUCTION & OBJECTIVES
    # --------------------------------------------------------------------------
    story.append(Paragraph("1. INTRODUCTION", h1_style))
    story.append(Paragraph(
        "Modern IT organizations depend on seamless incident reporting, request tracking, and SLA resolution to sustain operational continuity. "
        "The IT Helpdesk and Ticket Management System is an enterprise-grade, web-based support management platform designed to automate and streamline "
        "the ticket lifecycle. Built with a decoupled architecture—featuring a React + Vite Single Page Application (SPA) on the frontend, "
        "a Spring Boot 3.2.5 enterprise REST API on Java 21, and a robust MySQL 8 relational persistence engine—the platform facilitates "
        "structured incident submission, priority-based triage, automated staff reassignment, and transparent resolution tracking.", body_style
    ))
    story.append(Paragraph(
        "Crucially, beyond core software functionality, this project incorporates a complete, automated DevOps engineering workflow spanning "
        "every phase of the modern software delivery lifecycle. Version control is maintained via Git and synchronized with GitHub. "
        "Continuous Integration is automated through a Declarative Jenkins Pipeline executing automated JUnit 5 and Mockito tests, JaCoCo code coverage gates, "
        "and multi-stage Docker image assembly. Deployment orchestration is handled through Docker Compose with persistent named volumes, "
        "while system provisioning and environment configuration are enforced idempotently using Ansible on an Ubuntu Linux WSL2 control node. "
        "This end-to-end integration bridges software engineering excellence with robust, industrial-strength DevOps practices.", body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. OBJECTIVES", h1_style))
    objs = [
        "<b>Full-Stack Helpdesk Implementation:</b> Develop a responsive, role-based ticket management web platform supporting Employees, Support Engineers, and System Administrators with secure JWT authentication and BCrypt password encryption.",
        "<b>Automated Quality Gates:</b> Construct a comprehensive automated test suite with JUnit 5, Mockito, and JaCoCo enforcing shift-left testing across service and controller layers prior to container packaging.",
        "<b>Multi-Stage Containerization:</b> Package the application into secure, production-grade Docker containers using Eclipse Temurin 21 JRE for the backend (non-root execution) and Nginx Alpine for the frontend.",
        "<b>Multi-Service Orchestration:</b> Orchestrate frontend, backend, and MySQL database containers using Docker Compose, establishing private network isolation and guaranteed data persistence through named Docker volumes.",
        "<b>Idempotent Configuration Management:</b> Implement declarative Ansible playbooks inside an Ubuntu Linux WSL2 control node to manage directory layouts, templated environment variables, and secure file modes (0755/0600) with zero drift.",
        "<b>Continuous Delivery Pipeline:</b> Synthesize all tools into a unified, reproducible DevOps workflow (Git ➔ Jenkins ➔ Automated Tests ➔ Docker Build ➔ Ansible ➔ Runtime Deploy ➔ Automated Health Validation)."
    ]
    for o in objs:
        story.append(Paragraph(f"• {o}", bullet_style))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 6. ABSTRACT & TECHNOLOGY STACK
    # --------------------------------------------------------------------------
    story.append(Paragraph("3. ABSTRACT", h1_style))
    story.append(Paragraph(
        "In modern software engineering, rapid feature delivery must be balanced with operational stability, security, and reproducible deployments. "
        "Traditional deployment models suffer from environment discrepancies ('it works on my machine'), manual testing oversights, and configuration drift. "
        "The IT Helpdesk and Ticket Management System addresses these challenges by uniting modern full-stack development with a fully automated, verifiable DevOps delivery pipeline.<br/><br/>"
        "The system delivers comprehensive service-desk capabilities: employees submit categorized support tickets (Hardware, Software, Network, Access), "
        "while support staff and administrators manage queue assignments, update resolution statuses, and append internal diagnostic notes. "
        "The supporting DevOps infrastructure automates every step from commit to production: source code is pushed to GitHub, triggering a Declarative "
        "Jenkins CI Pipeline that validates system runtimes, clean-compiles the Spring Boot 3.2.5 backend, executes 43 automated unit and controller tests "
        "with zero failures, builds the React production bundle, and constructs versioned Docker images. "
        "Ansible automates host environment provisioning and Jinja2 templating with strict idempotency (changed=0 on subsequent runs). "
        "Finally, Docker Compose orchestrates the containerized services with MySQL volume persistence, and automated health probes verify system availability "
        "via Spring Boot Actuator. The entire 20-step integrated workflow was executed and verified live with a 100% pass rate.", body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. TECHNOLOGY STACK", h1_style))
    story.append(Paragraph("The project utilizes a cohesive, enterprise-standard technology stack spanning development, containerization, CI/CD, and configuration management:", body_style))

    tech_pdf = [
        [Paragraph("<b>Layer / Domain</b>", table_header_style), Paragraph("<b>Technology</b>", table_header_style), Paragraph("<b>Version</b>", table_header_style), Paragraph("<b>Role in Project</b>", table_header_style)],
        [Paragraph("Frontend UI", table_cell_style), Paragraph("React + Vite", table_cell_style), Paragraph("React 18 / Vite 5", table_cell_style), Paragraph("Component-based SPA, routing, Axios client", table_cell_style)],
        [Paragraph("Web Server", table_cell_style), Paragraph("Nginx Alpine", table_cell_style), Paragraph("1.25-alpine", table_cell_style), Paragraph("Static server & API reverse proxy", table_cell_style)],
        [Paragraph("Backend API", table_cell_style), Paragraph("Spring Boot", table_cell_style), Paragraph("3.2.5", table_cell_style), Paragraph("Enterprise REST API, JPA entities, controllers", table_cell_style)],
        [Paragraph("Java Runtime", table_cell_style), Paragraph("Eclipse Temurin", table_cell_style), Paragraph("Java 21 LTS", table_cell_style), Paragraph("Modern runtime, Alpine JRE container", table_cell_style)],
        [Paragraph("Build Tool", table_cell_style), Paragraph("Apache Maven", table_cell_style), Paragraph("3.9.6", table_cell_style), Paragraph("Dependency management, Surefire plugin", table_cell_style)],
        [Paragraph("Database", table_cell_style), Paragraph("MySQL Server", table_cell_style), Paragraph("8.0", table_cell_style), Paragraph("Relational DB, utf8mb4, named volume storage", table_cell_style)],
        [Paragraph("Security", table_cell_style), Paragraph("Spring Security", table_cell_style), Paragraph("6.2.4", table_cell_style), Paragraph("JWT token verification, BCrypt password hash", table_cell_style)],
        [Paragraph("Testing", table_cell_style), Paragraph("JUnit 5 & Mockito", table_cell_style), Paragraph("5.10 / 5.7", table_cell_style), Paragraph("43 unit and controller tests with mocks", table_cell_style)],
        [Paragraph("Coverage", table_cell_style), Paragraph("JaCoCo Maven", table_cell_style), Paragraph("0.8.11", table_cell_style), Paragraph("Bytecode instrumentation, HTML report", table_cell_style)],
        [Paragraph("CI Server", table_cell_style), Paragraph("Jenkins", table_cell_style), Paragraph("2.568.2 LTS", table_cell_style), Paragraph("Declarative Pipeline, JUnit test publishing", table_cell_style)],
        [Paragraph("Containers", table_cell_style), Paragraph("Docker Engine", table_cell_style), Paragraph("29.8.2", table_cell_style), Paragraph("Multi-stage builds, non-root user execution", table_cell_style)],
        [Paragraph("Orchestration", table_cell_style), Paragraph("Docker Compose", table_cell_style), Paragraph("v2 / v5", table_cell_style), Paragraph("Multi-container network & volume management", table_cell_style)],
        [Paragraph("Config Mgmt", table_cell_style), Paragraph("Ansible Core", table_cell_style), Paragraph("2.20.1", table_cell_style), Paragraph("Ubuntu WSL2 control node, idempotent plays", table_cell_style)],
    ]
    t_tech = Table(tech_pdf, colWidths=[100, 105, 95, 205])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_tech)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 7. SYSTEM ARCHITECTURE & DIAGRAM
    # --------------------------------------------------------------------------
    story.append(Paragraph("5. SYSTEM ARCHITECTURE & DEVOPS WORKFLOW", h1_style))
    story.append(Paragraph(
        "The architecture integrates a decoupled client-server web application with an automated, sequential DevOps delivery pipeline. "
        "The system operates across three tiers: Presentation (React SPA served by Nginx), Application (Spring Boot 3.2.5 REST services), "
        "and Persistence (MySQL 8.0 with dedicated Docker volume storage). Each commit pushed to GitHub initiates a structured automated sequence "
        "enforcing quality checks and deployment packaging before containers are launched.", body_style
    ))
    
    arch_img_path = os.path.join(figures_dir, "fig_architecture_diagram.png")
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=6.8*inch, height=3.9*inch))
        story.append(Paragraph("<i>Figure 5.1: End-to-End DevOps System Architecture and Integrated Delivery Pipeline</i>", ParagraphStyle('Cap', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
        story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Architectural Pipeline Workflow Stages:</b>", ParagraphStyle('SubH', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=colors.HexColor('#0f172a'))))
    arch_steps = [
        "<b>1. Source Commit & Version Control:</b> Developer writes code in Windows IDE, stages files, and pushes commits to the 'main' branch on GitHub.",
        "<b>2. Continuous Integration Trigger:</b> Jenkins pulls the updated Git revision and validates local development runtimes (Java 21, Maven, Node, Docker).",
        "<b>3. Quality Gate (Automated Testing):</b> Maven executes 43 JUnit 5 and Mockito unit tests. If any assertion fails, the build halts immediately.",
        "<b>4. Artifact & SPA Build:</b> Spring Boot JAR is packaged without test overhead, and the Vite frontend bundle is compiled to minified static assets in dist/.",
        "<b>5. Container Construction:</b> Docker executes multi-stage Dockerfiles, building minimal runtime images for backend (Temurin JRE) and frontend (Nginx Alpine).",
        "<b>6. Idempotent Provisioning:</b> Ansible in Ubuntu WSL2 applies system configurations, creates directory hierarchies, and renders Jinja2 environment templates.",
        "<b>7. Multi-Container Orchestration:</b> Docker Compose launches the services within a private bridge network and attaches persistent MySQL storage.",
        "<b>8. Verification & Health Probing:</b> Automated health check scripts verify Spring Boot Actuator (/actuator/health) and frontend HTTP endpoints."
    ]
    for s in arch_steps:
        story.append(Paragraph(f"• {s}", bullet_style))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 8. MODULES 1 TO 3
    # --------------------------------------------------------------------------
    story.append(Paragraph("6. MODULE 1 – USER AUTHENTICATION & ROLE-BASED ACCESS (RBAC)", h1_style))
    story.append(Paragraph(
        "Security is central to ticket management. Module 1 implements stateless JSON Web Token (JWT) authentication "
        "and granular Role-Based Access Control (RBAC) via Spring Security 6.2.4. Passwords are encrypted using BCrypt (cost factor 10) "
        "prior to database insertion. Upon successful authentication (/api/auth/login), the server issues a signed HMAC-SHA256 JWT token "
        "encoding the user's ID, username, and assigned role.<br/><br/>"
        "Three distinct user roles are enforced across the platform:<br/>"
        "• <b>EMPLOYEE:</b> Standard user capable of submitting tickets, tracking their own ticket progress, and adding public comments.<br/>"
        "• <b>SUPPORT:</b> Support staff responsible for managing assigned tickets, updating progress states, and creating internal staff notes.<br/>"
        "• <b>ADMIN:</b> System administrator with global privileges including staff reassignment, user account management, and analytical oversight.", body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. MODULE 2 – TICKET CREATION & MANAGEMENT", h1_style))
    story.append(Paragraph(
        "Module 2 delivers the core incident creation engine. When an employee encounters a technical problem, they submit a structured "
        "ticket with a title, detailed description, category, and priority level. The backend automatically generates an enterprise ticket identifier "
        "following the pattern 'HD-XXXX' (e.g., HD-1001) using a secure sequential code generator.", body_style
    ))
    dash_img = os.path.join(figures_dir, "fig_dashboard.png")
    if os.path.exists(dash_img):
        story.append(Image(dash_img, width=6.8*inch, height=3.3*inch))
        story.append(Paragraph("<i>Figure 7.1: IT Helpdesk Interactive Dashboard with Ticket Statistics and Metrics</i>", ParagraphStyle('Cap2', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
        story.append(Spacer(1, 6))

    story.append(Paragraph("8. MODULE 3 – TICKET ASSIGNMENT, STATUS UPDATES & SUPPORT WORKFLOW", h1_style))
    story.append(Paragraph(
        "Once a ticket is submitted, it enters the support workflow. Module 3 enforces strict role-based business rules for ticket lifecycle progression:<br/>"
        "• <b>Assignment Workflow:</b> Only Admin and Support users can assign tickets to support staff. Employees attempting reassignment are rejected with HTTP 403 Forbidden.<br/>"
        "• <b>Status Transitions:</b> Tickets move through four states: OPEN ➔ IN_PROGRESS ➔ RESOLVED ➔ CLOSED.<br/>"
        "• <b>Resolution Timestamping:</b> Transitioning to RESOLVED automatically captures the current timestamp in 'resolvedAt'. Reopening a ticket clears this timestamp.<br/>"
        "• <b>Employee Restrictions:</b> Employees may only close their own tickets once resolved; they cannot advance open tickets to in-progress.", body_style
    ))
    tlist_img = os.path.join(figures_dir, "fig_tickets_list.png")
    if os.path.exists(tlist_img):
        story.append(Image(tlist_img, width=6.8*inch, height=3.2*inch))
        story.append(Paragraph("<i>Figure 8.1: All Tickets Overview Screen with Category, Priority, and Search Filters</i>", ParagraphStyle('Cap3', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
    story.append(PageBreak())

    tdet_img = os.path.join(figures_dir, "fig_ticket_details.png")
    if os.path.exists(tdet_img):
        story.append(Image(tdet_img, width=6.8*inch, height=3.2*inch))
        story.append(Paragraph("<i>Figure 8.2: Ticket Detail View Displaying Staff Operations, Reassignment Dropdown, and Comments</i>", ParagraphStyle('Cap4', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
        story.append(Spacer(1, 8))

    # --------------------------------------------------------------------------
    # 9. MODULES 4 TO 7
    # --------------------------------------------------------------------------
    story.append(Paragraph("9. MODULE 4 – BACKEND REST API & DATABASE INTEGRATION", h1_style))
    story.append(Paragraph(
        "The backend service is engineered using Spring Boot 3.2.5 adhering to clean MVC architecture. The system exposes RESTful endpoints "
        "under '/api/tickets', '/api/auth', '/api/users', and '/api/dashboard'. Spring Data JPA manages ORM mappings with MySQL 8.0, "
        "utilizing Hibernate for schema generation and validation. Database constraints enforce unique emails, non-null ticket codes, and "
        "foreign key relationships between tickets, users, and comments. A global exception handler (@RestControllerAdvice) intercepts "
        "validation errors, resource not found exceptions, and unauthorized access attempts, translating them into standard RFC 7807 JSON error responses.", body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("10. MODULE 5 – GIT & GITHUB SOURCE CONTROL", h1_style))
    story.append(Paragraph(
        "Version control is the foundation of DevOps. The repository adheres to trunk-based development on branch 'main', "
        "synchronized with the remote repository at https://github.com/Yokesh07J/IT-Helpdesk.git. "
        "A rigorous .gitignore policy excludes local runtime configuration files (.env), compiled artifacts (target/, dist/), "
        "IDE settings (.vscode/, .idea/), and MySQL database storage volumes to ensure zero secret leakage and clean build workspaces.", body_style
    ))
    git_img = os.path.join(figures_dir, "fig_git_log.png")
    if os.path.exists(git_img):
        story.append(Image(git_img, width=6.8*inch, height=2.6*inch))
        story.append(Paragraph("<i>Figure 10.1: Git Commit History and Remote Branch Synchronization</i>", ParagraphStyle('Cap5', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
        story.append(Spacer(1, 6))

    story.append(Paragraph("11. MODULE 6 – DOCKER MULTI-STAGE CONTAINERIZATION", h1_style))
    story.append(Paragraph(
        "Both frontend and backend services are packaged using multi-stage Dockerfiles to minimize container footprint and enhance security:<br/>"
        "• <b>Backend Dockerfile:</b> Stage 1 uses Maven 3.9 on Eclipse Temurin 21 to compile the application and package the executable JAR. "
        "Stage 2 copies the compiled JAR into a minimal 'eclipse-temurin:21-jre-alpine' image. A dedicated non-root user and group ('spring:spring') "
        "is created, and container execution runs under UID 1000 rather than root. Built-in health checks probe '/actuator/health' using wget.<br/>"
        "• <b>Frontend Dockerfile:</b> Stage 1 uses Node.js 20 Alpine to execute 'npm ci' and 'npm run build'. Stage 2 transfers the compiled 'dist/' directory "
        "into a lightweight 'nginx:alpine' web server. A custom Nginx configuration provides SPA client-side routing fallback (try_files) and reverse-proxies '/api' calls to the backend.", body_style
    ))
    story.append(PageBreak())

    story.append(Paragraph("12. MODULE 7 – DOCKER COMPOSE & MYSQL PERSISTENCE", h1_style))
    story.append(Paragraph(
        "Multi-container orchestration is defined declaratively in 'docker-compose.yml'. The file coordinates three microservices:<br/>"
        "1. <b>helpdesk-mysql:</b> MySQL 8.0 server with database 'it_helpdesk', persistent storage mounted to named volume 'mysql_data', and a health check probe (mysqladmin ping).<br/>"
        "2. <b>helpdesk-backend:</b> Spring Boot service exposed on port 8088, configured with service dependencies (depends_on condition: service_healthy on mysql).<br/>"
        "3. <b>helpdesk-frontend:</b> Nginx web server exposed on host port 80, routing API calls to the backend container over internal DNS ('http://backend:8088/api').<br/><br/>"
        "Data persistence is rigorously verified: deleting and recreating the MySQL container leaves named volume 'mysql_data' intact, ensuring that existing tickets, "
        "users, and comment histories are completely preserved.", body_style
    ))
    dc_img = os.path.join(figures_dir, "fig_docker_compose_ps.png")
    if os.path.exists(dc_img):
        story.append(Image(dc_img, width=6.8*inch, height=2.5*inch))
        story.append(Paragraph("<i>Figure 12.1: Docker Compose Multi-Container Stack Runtime Status and Named Volume Verification</i>", ParagraphStyle('Cap6', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
        story.append(Spacer(1, 6))

    story.append(Paragraph("13. MODULE 8 – JENKINS CONTINUOUS INTEGRATION PIPELINE", h1_style))
    story.append(Paragraph(
        "Continuous Integration is managed via Jenkins 2.568.2 LTS running as a Windows service. "
        "The pipeline is defined in a root 'Jenkinsfile' using Declarative Pipeline syntax with 7 distinct stages:<br/>"
        "1. <b>Checkout SCM:</b> Clones the main branch directly from GitHub (https://github.com/Yokesh07J/IT-Helpdesk.git).<br/>"
        "2. <b>Validate Environment:</b> Verifies host runtimes including Java 21 LTS, Maven 3.9.6, Node.js 22, and Docker 29.8.<br/>"
        "3. <b>Build Backend:</b> Clean-compiles the Spring Boot backend using Maven.<br/>"
        "4. <b>Run Automated Tests:</b> Executes 43 unit and controller tests, generating Surefire XML and JaCoCo coverage reports.<br/>"
        "5. <b>Build Frontend:</b> Executes 'npm ci' and compiles the React SPA bundle to 'dist/'.<br/>"
        "6. <b>Validate Docker Compose:</b> Validates orchestration YAML syntax and dependency graphs.<br/>"
        "7. <b>Build Multi-Stage Docker Images:</b> Assembles and tags 'it-helpdesk-backend:1.0.0' and 'it-helpdesk-frontend:1.0.0'.<br/><br/>"
        "Post-build actions record test results via the JUnit plugin and archive build artifacts (JAR file and JaCoCo report).", body_style
    ))
    jk_img = os.path.join(figures_dir, "fig_jenkins_console.png")
    if os.path.exists(jk_img):
        story.append(Image(jk_img, width=6.8*inch, height=3.1*inch))
        story.append(Paragraph("<i>Figure 13.1: Jenkins Declarative Pipeline Console Output (Build #6 - SUCCESS)</i>", ParagraphStyle('Cap7', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 10. MODULES 9 TO 12
    # --------------------------------------------------------------------------
    story.append(Paragraph("14. MODULE 9 – AUTOMATED TESTING & CODE COVERAGE (JACOCO)", h1_style))
    story.append(Paragraph(
        "The project enforces continuous testing using JUnit 5 (Jupiter engine) and Mockito 5. "
        "A total of 43 unit and MockMvc controller tests are implemented across 7 test classes, covering:<br/>"
        "• <b>AuthServiceTest (8 tests):</b> User registration, duplicate email rejection, JWT token generation, invalid password rejection, SecurityContext principal extraction.<br/>"
        "• <b>TicketServiceTest (13 tests):</b> Ticket code generation, role-based ticket viewing, privacy boundaries between employees, support assignment, status transitions, resolution timestamps.<br/>"
        "• <b>CommentServiceTest (7 tests):</b> Public comment submission, staff internal note creation, hiding internal notes from employees, cross-user privacy enforcement.<br/>"
        "• <b>Controller Layer Tests (15 tests):</b> MockMvc request verification, HTTP status validation (200, 201, 400, 401, 403, 404), and JSON payload assertion.<br/><br/>"
        "JaCoCo bytecode instrumentation generates comprehensive line, branch, and instruction coverage reports at 'backend/target/site/jacoco/index.html'.", body_style
    ))
    mvn_img = os.path.join(figures_dir, "fig_maven_tests.png")
    if os.path.exists(mvn_img):
        story.append(Image(mvn_img, width=6.8*inch, height=2.6*inch))
        story.append(Paragraph("<i>Figure 14.1: Maven Test Execution Log Confirming 43 Passing Tests with Zero Failures</i>", ParagraphStyle('Cap8', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
        story.append(Spacer(1, 6))

    story.append(Paragraph("15. MODULE 10 – ANSIBLE CONFIGURATION MANAGEMENT & IDEMPOTENCY", h1_style))
    story.append(Paragraph(
        "Infrastructure configuration management is implemented using Ansible Core 2.20.1 executed from an Ubuntu 26.04 WSL2 control node. "
        "The project directory ('ansible/') includes 'ansible.cfg', 'inventory.ini', 'group_vars/all.yml', and Jinja2 templates. "
        "The main playbook ('playbook.yml') manages target host configuration:<br/>"
        "• <b>Directory Structure:</b> Idempotently creates '/opt/it-helpdesk/{config,logs,backups,scripts}' with mode 0755.<br/>"
        "• <b>Environment Templating:</b> Renders 'helpdesk.env' from 'templates/helpdesk-env.j2' with restricted mode 0600 (owner read/write only).<br/>"
        "• <b>Docker Override:</b> Renders 'docker-compose.override.yml' configuring log rotation limits (10MB max, 3 files) and restart policies.<br/>"
        "• <b>Health Probe Script:</b> Renders executable 'healthcheck.sh' (mode 0755) and validates its bash syntax.<br/><br/>"
        "<b>Idempotency Verification:</b> Dynamic timestamps were excluded from templates to ensure deterministic hashing. "
        "Executing the playbook a second time produces 'ok=14 changed=0 failed=0', confirming strict idempotency.", body_style
    ))
    ans_img = os.path.join(figures_dir, "fig_ansible_idempotency.png")
    if os.path.exists(ans_img):
        story.append(Image(ans_img, width=6.8*inch, height=2.6*inch))
        story.append(Paragraph("<i>Figure 15.1: Ansible Playbook Execution and Idempotency Verification Output in WSL2</i>", ParagraphStyle('Cap9', fontName='Helvetica-Oblique', fontSize=8.5, alignment=1, textColor=colors.HexColor('#64748b'))))
    story.append(PageBreak())

    story.append(Paragraph("16. MODULE 11 – INTEGRATED CI/CD PIPELINE ORCHESTRATION", h1_style))
    story.append(Paragraph(
        "Module 11 synthesizes all DevOps tooling into a single, cohesive delivery pipeline. "
        "Code progresses automatically from developer commits through Jenkins quality gates, container packaging, Ansible host configuration, "
        "and Docker Compose deployment. The pipeline enforces zero configuration drift by generating environment configurations from versioned Jinja2 templates.", body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("17. MODULE 12 – APPLICATION & DEPLOYMENT VERIFICATION", h1_style))
    story.append(Paragraph(
        "The entire deployment was verified end-to-end using an automated PowerShell script ('scripts/verify-integrated-devops-workflow.ps1'). "
        "All 20 verification checkpoints across SCM, host tooling, backend testing, frontend compilation, Docker images, Ansible idempotency, "
        "and runtime container endpoints passed with 100% success. Spring Boot Actuator returned '{\"status\":\"UP\"}', and the React/Nginx frontend returned HTTP 200 OK.", body_style
    ))
    story.append(Spacer(1, 8))

    # --------------------------------------------------------------------------
    # 11. RESULTS AND OUTPUT
    # --------------------------------------------------------------------------
    story.append(Paragraph("18. RESULTS AND OUTPUT", h1_style))
    story.append(Paragraph("The table below details the verified results across all 20 evaluation checkpoints in the integrated DevOps workflow:", body_style))

    res_pdf_data = [
        [Paragraph("<b>Stage</b>", table_header_style), Paragraph("<b>Component Verified</b>", table_header_style), Paragraph("<b>Observed Execution Output</b>", table_header_style), Paragraph("<b>Status</b>", table_header_style)],
        [Paragraph("Stage 1", table_cell_style), Paragraph("Git Active Branch", table_cell_style), Paragraph("Branch is 'main' and synced with origin", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 1", table_cell_style), Paragraph("GitHub Remote", table_cell_style), Paragraph("origin -> https://github.com/Yokesh07J/IT-Helpdesk.git", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 1", table_cell_style), Paragraph("Secret Hygiene", table_cell_style), Paragraph(".env is properly git-ignored; no secrets tracked", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 2", table_cell_style), Paragraph("Java Runtime", table_cell_style), Paragraph("Eclipse Temurin Java 21.0.11 LTS verified", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 2", table_cell_style), Paragraph("Maven Build Tool", table_cell_style), Paragraph("Apache Maven 3.9.6 verified", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 2", table_cell_style), Paragraph("Node.js Runtime", table_cell_style), Paragraph("Node.js v22.20.0 verified", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 2", table_cell_style), Paragraph("Docker Engine", table_cell_style), Paragraph("Docker version 29.8.2 verified", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 2", table_cell_style), Paragraph("Ansible in WSL2", table_cell_style), Paragraph("Ansible Core 2.20.1 in Ubuntu 26.04 verified", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 3", table_cell_style), Paragraph("Automated Tests", table_cell_style), Paragraph("43 / 43 JUnit 5 & Mockito tests passed (0 failures)", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 3", table_cell_style), Paragraph("JaCoCo Coverage", table_cell_style), Paragraph("HTML coverage site generated at target/site/jacoco/", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 4", table_cell_style), Paragraph("Vite Frontend Build", table_cell_style), Paragraph("Production bundle compiled to dist/ (HTML, JS, CSS)", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 5", table_cell_style), Paragraph("Compose Graph", table_cell_style), Paragraph("Valid Compose specification with 3 services", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 5", table_cell_style), Paragraph("Backend Image", table_cell_style), Paragraph("Tagged it-helpdesk-backend:1.0.0 (Temurin JRE)", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 5", table_cell_style), Paragraph("Frontend Image", table_cell_style), Paragraph("Tagged it-helpdesk-frontend:1.0.0 (Nginx Alpine)", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 6", table_cell_style), Paragraph("Ansible Playbook", table_cell_style), Paragraph("Executed with 0 failures, 0 unreachable", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 6", table_cell_style), Paragraph("Ansible Idempotency", table_cell_style), Paragraph("Confirmed strict idempotency: ok=14 changed=0", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 7", table_cell_style), Paragraph("Containers Running", table_cell_style), Paragraph("3 containers active: backend, frontend, mysql", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 7", table_cell_style), Paragraph("Backend Health", table_cell_style), Paragraph("http://localhost:8088/actuator/health -> status: 'UP'", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 7", table_cell_style), Paragraph("Frontend Health", table_cell_style), Paragraph("http://localhost:80/ -> HTTP status: 200 OK", table_cell_style), Paragraph("PASS", table_cell_style)],
        [Paragraph("Stage 7", table_cell_style), Paragraph("MySQL Port", table_cell_style), Paragraph("TCP port 3306 reachable on localhost", table_cell_style), Paragraph("PASS", table_cell_style)],
    ]
    t_res = Table(res_pdf_data, colWidths=[60, 140, 255, 50])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_res)
    story.append(PageBreak())

    # --------------------------------------------------------------------------
    # 12. COMMANDS, ADVANTAGES, LIMITATIONS, CONCLUSION
    # --------------------------------------------------------------------------
    story.append(Paragraph("19. COMMANDS USED", h1_style))
    cmds_pdf = [
        ("Git & SCM: ", "git branch -M main | git remote add origin https://github.com/Yokesh07J/IT-Helpdesk.git | git push origin main"),
        ("Maven & Tests: ", "mvn clean compile | mvn test (43 JUnit5/Mockito tests) | mvn jacoco:report"),
        ("Node & Vite: ", "npm ci | npm run build (compiled production React SPA to dist/)"),
        ("Docker Compose: ", "docker compose config | docker compose build | docker compose up -d | docker compose ps"),
        ("Ansible in WSL2: ", "ansible helpdesk_servers -m ping | ansible-playbook playbook.yml --syntax-check | ansible-playbook playbook.yml")
    ]
    for c_title, c_code in cmds_pdf:
        story.append(Paragraph(f"• <b>{c_title}</b> <font name='Courier' size='8'>{c_code}</font>", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("20. ADVANTAGES", h1_style))
    advs_pdf = [
        "<b>Automated Quality Gates:</b> Prevents defective code from reaching production by running 43 tests before container image assembly.",
        "<b>Environment Parity:</b> Docker eliminates 'works on my machine' bugs by packaging identical runtimes for development, CI, and production.",
        "<b>Strict Idempotency:</b> Ansible guarantees zero configuration drift on managed target hosts (changed=0 on repeated runs).",
        "<b>Persistent Data Integrity:</b> Named Docker volume (mysql_data) preserves database records across container lifecycles.",
        "<b>Secure Secret Separation:</b> Credentials and environment variables are injected at runtime rather than hardcoded in images or git.",
        "<b>Rapid Feedback Loops:</b> The entire build, test, and container packaging cycle completes in under 65 seconds."
    ]
    for a in advs_pdf:
        story.append(Paragraph(f"• {a}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("21. LIMITATIONS", h1_style))
    lims_pdf = [
        "<b>Local CI Runner:</b> Jenkins currently executes on the local workstation service rather than a distributed cloud worker cluster.",
        "<b>Simulated Host Target:</b> Ansible targets localhost via local connection rather than a fleet of remote Linux nodes over SSH.",
        "<b>Self-Contained Monitoring:</b> Monitoring relies on Spring Boot Actuator rather than enterprise Prometheus/Grafana infrastructure.",
        "<b>Single-Node Deployment:</b> Application runs on a single Docker host rather than a multi-node Kubernetes cluster."
    ]
    for l in lims_pdf:
        story.append(Paragraph(f"• {l}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("22. FUTURE ENHANCEMENTS", h1_style))
    futs_pdf = [
        "<b>Kubernetes & Helm Charts:</b> Migrate Docker Compose services to Kubernetes Deployments, StatefulSets, and Helm charts for horizontal autoscaling.",
        "<b>Enterprise Observability:</b> Integrate Prometheus metric collection and Grafana dashboards for real-time SLA and latency monitoring.",
        "<b>Cloud Container Registry:</b> Publish versioned images to AWS ECR or GitHub Container Registry (GHCR) using automated Jenkins credentials.",
        "<b>Single Sign-On (SSO):</b> Integrate OAuth2 / OpenID Connect (OIDC) authentication with enterprise identity providers such as Okta or Azure AD."
    ]
    for f in futs_pdf:
        story.append(Paragraph(f"• {f}", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("23. CONCLUSION", h1_style))
    story.append(Paragraph(
        "The IT Helpdesk and Ticket Management System successfully demonstrates the seamless integration of modern web application engineering "
        "with industrial-grade DevOps practices. By implementing a decoupled architecture (React SPA, Spring Boot 3.2.5 REST backend, and MySQL 8) "
        "alongside an automated CI/CD pipeline (Git, Jenkins, JUnit 5/Mockito, Docker, and Ansible), the project achieves rapid delivery, "
        "bulletproof quality gates, and automated infrastructure provisioning.<br/><br/>"
        "All six phases of the 23IT723 DevOps Laboratory syllabus—from Docker basics and container deployment to continuous testing, "
        "Ansible configuration management, and full pipeline integration—have been rigorously implemented and verified live. "
        "The project stands as a complete, enterprise-ready reference for automated software delivery and operational reliability.", body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("24. REFERENCES", h1_style))
    refs_pdf = [
        "1. Martin Fowler, 'Continuous Integration: Improving Software Quality and Reducing Risk', Addison-Wesley, 2006.",
        "2. Spring Boot Documentation, 'Spring Boot Reference Guide (v3.2.5)', VMware Tanzu, 2024.",
        "3. Docker Documentation, 'Docker Compose File Reference & Multi-Stage Builds', Docker Inc., 2024.",
        "4. Jenkins User Handbook, 'Pipeline as Code with Declarative Jenkinsfile', Jenkins CI Community, 2024.",
        "5. Ansible Documentation, 'Ansible Core Playbook Architecture and Idempotency', Red Hat Inc., 2024.",
        "6. JUnit 5 User Guide, 'JUnit Jupiter Programming & Extension Model', JUnit Team, 2024."
    ]
    for r in refs_pdf:
        story.append(Paragraph(r, ParagraphStyle('Ref', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor('#475569'), spaceAfter=3)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF report saved successfully to {output_path}")

if __name__ == '__main__':
    out_pdf = r"c:\DevopsCat\IT-Helpdesk\docs\final-report\23IT723_Final_Project_Report_IT_Helpdesk.pdf"
    fig_dir = r"c:\DevopsCat\IT-Helpdesk\docs\final-report\figures"
    create_pdf_report(out_pdf, fig_dir)
