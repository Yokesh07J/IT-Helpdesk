#!/usr/bin/env python3
"""
Generate Final DevOps CAT Project Report (PDF)
Course: 23IT723 - DevOps Laboratory
Project: IT HELPDESK AND TICKET MANAGEMENT SYSTEM
Institution: Coimbatore Institute of Technology, Coimbatore
Student: YOKESH J (Register No: 2303717620521xxx)

Exact 19-page format matching 23IT723_Final_Project_Report_TaskPulse.pdf
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
)
from reportlab.pdfgen import canvas
import pypdf

class BorderAndNumberedCanvas(canvas.Canvas):
    """
    Draws a crisp outer border rectangle and the exact page number (1, 2, ..., 19)
    at the bottom right corner of each page, matching the CIT TaskPulse reference.
    """
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
            self.draw_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_decorations(self, total_pages):
        self.saveState()
        # Outer rectangular border around the entire page
        self.setStrokeColor(colors.black)
        self.setLineWidth(0.8)
        self.rect(28, 28, letter[0] - 56, letter[1] - 56, stroke=1, fill=0)

        # Page number at bottom right inside the border
        self.setFont("Helvetica", 10)
        self.setFillColor(colors.black)
        self.drawRightString(letter[0] - 40, 36, str(self._pageNumber))
        self.restoreState()


def build_pdf_report(output_path, figures_dir):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=44,
        rightMargin=44,
        topMargin=40,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Academic Typography Styles matching the CIT TaskPulse format
    center_inst_style = ParagraphStyle(
        'InstHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        alignment=1,
        textColor=colors.black,
        spaceAfter=4
    )

    sub_inst_style = ParagraphStyle(
        'InstSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.black,
        spaceAfter=3
    )

    city_style = ParagraphStyle(
        'InstCity',
        parent=styles['Normal'],
        fontName='Helvetica-BoldOblique',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.black,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.black,
        spaceBefore=7,
        spaceAfter=5
    )

    h1_center_style = ParagraphStyle(
        'SectionH1Center',
        parent=h1_style,
        alignment=1
    )

    body_style = ParagraphStyle(
        'BodyAcademic',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.2,
        leading=13.2,
        textColor=colors.black,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'BulletAcademic',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3.5
    )

    caption_style = ParagraphStyle(
        'FigCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        alignment=1,
        textColor=colors.black,
        spaceBefore=3,
        spaceAfter=5
    )

    tbl_hdr_style = ParagraphStyle(
        'TblHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.black
    )

    tbl_body_style = ParagraphStyle(
        'TblBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.black
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("COIMBATORE INSTITUTE OF TECHNOLOGY", center_inst_style))
    story.append(Paragraph("(Government Aided Autonomous Institution Affiliated to Anna University)", sub_inst_style))
    story.append(Paragraph("COIMBATORE - 641 014", city_style))
    story.append(Spacer(1, 35))

    logo_path = os.path.join(figures_dir, "cit_logo.png")
    if os.path.exists(logo_path):
        story.append(Image(logo_path, width=1.7*inch, height=1.7*inch))
    story.append(Spacer(1, 40))

    story.append(Paragraph("23IT723 - DEVOPS LABORATORY", ParagraphStyle('CoverCourse', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 12))
    story.append(Paragraph("PROJECT REPORT", ParagraphStyle('CoverPR', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("IT HELPDESK: ENTERPRISE TICKET MANAGEMENT & DEVOPS AUTOMATION", ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=13.5, leading=18, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 65))
    story.append(Paragraph("OCTOBER 2026", ParagraphStyle('CoverDate', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 60))

    subm_block = [
        [Paragraph("", body_style), Paragraph("<b>Submitted by</b>", ParagraphStyle('SubmBy', fontName='Helvetica-Bold', fontSize=10.5, leading=14, alignment=2))],
        [Paragraph("", body_style), Spacer(1, 6)],
        [Paragraph("", body_style), Paragraph("<b>2303717620521xxx  YOKESH J</b>", ParagraphStyle('SubmName', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=2))]
    ]
    t_subm = Table(subm_block, colWidths=[240, 280])
    t_subm.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_subm)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: BONAFIDE CERTIFICATE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("COIMBATORE INSTITUTE OF TECHNOLOGY", center_inst_style))
    story.append(Paragraph("(Government Aided Autonomous Institution Affiliated to Anna University)", sub_inst_style))
    story.append(Paragraph("COIMBATORE - 641 014", city_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph("BONAFIDE CERTIFICATE", ParagraphStyle('CertHeading', fontName='Helvetica-Bold', fontSize=13, leading=17, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 25))

    cert_text = (
        "Certified that this project report titled <b>\"IT HELPDESK: ENTERPRISE TICKET MANAGEMENT & DEVOPS AUTOMATION\"</b> "
        "is the bonafide work of <b>2303717620521xxx - YOKESH J</b> completed during the academic year "
        "<b>2026-2027 - Semester VII</b> for the project presentation of <b>23IT723 - DEVOPS LABORATORY</b> "
        "under our supervision."
    )
    story.append(Paragraph(cert_text, ParagraphStyle('CertP1', parent=body_style, fontSize=10.5, leading=18, alignment=4))) # Justified
    story.append(Spacer(1, 25))

    story.append(Paragraph("<i>Certified that the candidate was examined by using the project work examination.</i>", ParagraphStyle('CertP2', fontName='Helvetica-Oblique', fontSize=10.5, leading=16)))
    story.append(Spacer(1, 65))

    story.append(Paragraph("<b>Review Members:</b>", ParagraphStyle('RevMem', fontName='Helvetica-Bold', fontSize=11, leading=16)))
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>1. Dr. M. Sangeetha</b>", ParagraphStyle('Rev1', fontName='Helvetica-Bold', fontSize=11, leading=16, leftIndent=25)))
    story.append(Spacer(1, 25))
    story.append(Paragraph("<b>2. Dr. E. Arul</b>", ParagraphStyle('Rev2', fontName='Helvetica-Bold', fontSize=11, leading=16, leftIndent=25)))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: EVALUATION SCHEME
    # =========================================================================
    story.append(Paragraph("23IT723 – DEVOPS LABORATORY", ParagraphStyle('ESHdr1', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1, textColor=colors.black)))
    story.append(Paragraph("FINAL MINI PROJECT – EVALUATION SCHEME", ParagraphStyle('ESHdr2', fontName='Helvetica-Bold', fontSize=11, leading=15, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Final Mini Project Assessment</b>", ParagraphStyle('ESHdr3', fontName='Helvetica-Bold', fontSize=10, leading=14, alignment=1, textColor=colors.black)))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "The final mini project shall require students to integrate the major DevOps practices covered in the laboratory. "
        "The project should demonstrate practical implementation of version control, collaborative development, Continuous Integration, "
        "containerization and/or automated configuration/provisioning, with proper execution evidence.",
        body_style
    ))
    story.append(Spacer(1, 6))

    eval_data = [
        [Paragraph("<b>S.No.</b>", tbl_hdr_style), Paragraph("<b>Evaluation<br/>Component</b>", tbl_hdr_style), Paragraph("<b>Key Verification Points</b>", tbl_hdr_style), Paragraph("<b>Marks</b>", tbl_hdr_style)],
        [Paragraph("1", tbl_body_style), Paragraph("Problem Definition &<br/>Project Planning", tbl_body_style), Paragraph("Problem statement, objectives, requirements, scope, module identification, technology selection and workflow planning.", tbl_body_style), Paragraph("10", tbl_body_style)],
        [Paragraph("2", tbl_body_style), Paragraph("Git Repository &<br/>Version Control", tbl_body_style), Paragraph("Repository creation, meaningful commits, README, .gitignore, remote repository, push/pull/fetch operations and commit history.", tbl_body_style), Paragraph("15", tbl_body_style)],
        [Paragraph("3", tbl_body_style), Paragraph("Branching, Merging &<br/>Collaboration", tbl_body_style), Paragraph("Feature branches, parallel development, merging, conflict handling, branch organization and collaborative workflow.", tbl_body_style), Paragraph("10", tbl_body_style)],
        [Paragraph("4", tbl_body_style), Paragraph("Application<br/>Development & Build", tbl_body_style), Paragraph("Working application/source code, project structure, dependency management, build configuration and successful execution.", tbl_body_style), Paragraph("15", tbl_body_style)],
        [Paragraph("5", tbl_body_style), Paragraph("Jenkins Continuous<br/>Integration", tbl_body_style), Paragraph("Jenkins configuration, source-code integration, automated checkout, build job/pipeline, build execution and console verification.", tbl_body_style), Paragraph("15", tbl_body_style)],
        [Paragraph("6", tbl_body_style), Paragraph("Docker /<br/>Containerization", tbl_body_style), Paragraph("Dockerfile, image creation, container execution, port/configuration handling, application deployment and container verification.", tbl_body_style), Paragraph("10", tbl_body_style)],
        [Paragraph("7", tbl_body_style), Paragraph("Automation /<br/>Configuration<br/>Management", tbl_body_style), Paragraph("Ansible/Chef/Puppet/SaltStack or equivalent automation where applicable; repeatable configuration/provisioning and successful execution.", tbl_body_style), Paragraph("5", tbl_body_style)],
        [Paragraph("8", tbl_body_style), Paragraph("Testing & Verification", tbl_body_style), Paragraph("Functional testing, build verification, error identification, test evidence and corrective action.", tbl_body_style), Paragraph("5", tbl_body_style)],
        [Paragraph("9", tbl_body_style), Paragraph("Documentation &<br/>Technical Presentation", tbl_body_style), Paragraph("Architecture/workflow diagram, commands/configuration, screenshots, results, troubleshooting, conclusion and repository details.", tbl_body_style), Paragraph("5", tbl_body_style)],
        [Paragraph("10", tbl_body_style), Paragraph("Final Demonstration &<br/>Viva-Voce", tbl_body_style), Paragraph("Live demonstration, explanation of implementation, troubleshooting responses and technical understanding.", tbl_body_style), Paragraph("10", tbl_body_style)],
        [Paragraph("", tbl_body_style), Paragraph("<b>TOTAL</b>", tbl_hdr_style), Paragraph("", tbl_body_style), Paragraph("<b>100</b>", tbl_hdr_style)],
    ]
    t_eval = Table(eval_data, colWidths=[35, 125, 325, 40])
    t_eval.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_eval)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: RECOMMENDED MARK DISTRIBUTION & FACULTY EVALUATION RECORD
    # =========================================================================
    story.append(Paragraph("<b>Recommended Mark Distribution within the Final Demonstration</b>", ParagraphStyle('RMDHdr', fontName='Helvetica-Bold', fontSize=10.5, leading=14, alignment=1)))
    story.append(Spacer(1, 3))
    story.append(Paragraph("For uniform evaluation, the examiner may use the following internal split for the implementation and demonstration components.", body_style))
    story.append(Spacer(1, 3))

    dist_data = [
        [Paragraph("<b>Assessment Area</b>", tbl_hdr_style), Paragraph("<b>Marks</b>", tbl_hdr_style), Paragraph("<b>Awarded Marks</b>", tbl_hdr_style), Paragraph("<b>Remarks</b>", tbl_hdr_style)],
        [Paragraph("Working implementation and correctness", tbl_body_style), Paragraph("30", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("DevOps tool integration and automation", tbl_body_style), Paragraph("20", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("Version control and collaborative workflow", tbl_body_style), Paragraph("15", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("Build / deployment / container verification", tbl_body_style), Paragraph("15", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("Testing and troubleshooting", tbl_body_style), Paragraph("5", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("Documentation and technical presentation", tbl_body_style), Paragraph("5", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("Live demonstration and viva-voce", tbl_body_style), Paragraph("10", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("<b>TOTAL</b>", tbl_hdr_style), Paragraph("<b>100</b>", tbl_hdr_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
    ]
    t_dist = Table(dist_data, colWidths=[180, 50, 90, 205])
    t_dist.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (1,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_dist)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Minimum Evidence to be Submitted</b>", ParagraphStyle('EvidHdr', fontName='Helvetica-Bold', fontSize=10, leading=13)))
    evid_bullets = [
        "Project repository URL and project README.",
        "Git commit history and branch/merge evidence.",
        "Jenkins job/pipeline configuration and successful build evidence.",
        "Dockerfile, image and running container evidence where Docker is used.",
        "Automation/configuration scripts where applicable.",
        "Architecture/workflow diagram.",
        "Short technical report containing implementation steps, results and troubleshooting.",
        "Live demonstration of the complete DevOps workflow."
    ]
    for b in evid_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 5))

    story.append(Paragraph("<b>Evaluation Guidelines</b>", ParagraphStyle('GuideHdr', fontName='Helvetica-Bold', fontSize=10, leading=13)))
    guide_bullets = [
        "Marks shall be awarded primarily for a working implementation and demonstrable output.",
        "Copied source code without functional understanding shall not receive full marks.",
        "Screenshots may support the evaluation, but critical components should be demonstrated live wherever possible.",
        "Students should use meaningful repository names, branch names and commit messages.",
        "If a component is not applicable to the selected project, the student shall obtain faculty approval and demonstrate an equivalent DevOps automation component."
    ]
    for b in guide_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 6))

    fac_data = [
        [Paragraph("<b>Faculty Evaluation Record</b>", ParagraphStyle('FEH', fontName='Helvetica-Bold', fontSize=9, alignment=1)), "", "", ""],
        [Paragraph("<b>Student Name</b>", tbl_body_style), Paragraph("YOKESH J", tbl_body_style), Paragraph("<b>Register No.</b>", tbl_body_style), Paragraph("2303717620521xxx", tbl_body_style)],
        [Paragraph("<b>Project Title</b>", tbl_body_style), Paragraph("IT HELPDESK AND TICKET MANAGEMENT SYSTEM", tbl_body_style), Paragraph("<b>Date</b>", tbl_body_style), Paragraph("13-10-2026", tbl_body_style)],
        [Paragraph("<b>Final Mark</b>", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("<b>Faculty Evaluator I</b>", tbl_body_style), Paragraph("", tbl_body_style), Paragraph("<b>Signature</b>", tbl_body_style), Paragraph("", tbl_body_style)],
        [Paragraph("<b>Faculty Evaluator II</b>", tbl_body_style), Paragraph("/ 100", tbl_body_style), Paragraph("<b>Signature</b>", tbl_body_style), Paragraph("", tbl_body_style)],
    ]
    t_fac = Table(fac_data, colWidths=[120, 160, 100, 145])
    t_fac.setStyle(TableStyle([
        ('SPAN', (0,0), (3,0)),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_fac)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: TABLE OF CONTENTS
    # =========================================================================
    story.append(Spacer(1, 5))
    story.append(Paragraph("TABLE OF CONTENTS", ParagraphStyle('TOCHdr', fontName='Helvetica-Bold', fontSize=12, leading=16, alignment=1)))
    story.append(Spacer(1, 8))

    toc_items = [
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

    toc_table_data = [
        [Paragraph("<b>S. NO.</b>", tbl_hdr_style), Paragraph("<b>CONTENT</b>", tbl_hdr_style), Paragraph("<b>PAGE NO.</b>", tbl_hdr_style)]
    ]
    for sno, content, pg in toc_items:
        toc_table_data.append([
            Paragraph(sno, tbl_body_style),
            Paragraph(content, tbl_body_style),
            Paragraph(pg, tbl_body_style)
        ])

    t_toc = Table(toc_table_data, colWidths=[45, 420, 60])
    t_toc.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: 1. INTRODUCTION & 2. OBJECTIVES
    # =========================================================================
    story.append(Paragraph("1. INTRODUCTION", h1_style))
    story.append(Paragraph(
        "IT Helpdesk is a modern, high-performance web-based service desk and ticket management platform engineered to "
        "streamline enterprise incident reporting, categorization, priority triage, SLA tracking, and staff resolution workflows. "
        "Built with a decoupled architecture—featuring a React + Vite Single Page Application (SPA), a Spring Boot 3.2.5 enterprise REST API "
        "on Java 21 LTS, and a robust MySQL 8 relational persistence engine—the platform delivers real-time ticket analytics, "
        "role-based security access (Employee, Support Staff, Admin), automated ticket code assignment (HD-XXXX), dynamic status transitions, "
        "and structured CSV/JSON audit export capabilities.",
        body_style
    ))
    story.append(Paragraph(
        "Beyond standalone application functionality, this project incorporates an end-to-end DevOps automation workflow covering every stage "
        "of modern software delivery. Source code management and collaborative versioning are implemented using Git and GitHub (Yokesh07J/IT-Helpdesk). "
        "Continuous Integration is automated via a Jenkins Declarative Pipeline that retrieves source code, executes 43 automated Maven/JUnit 5 unit "
        "and Mockito tests, compiles production bundles, and packages the multi-tier application into lightweight Docker containers. "
        "Containerization is performed through Docker Compose with health probes and private networking, while configuration management and environment "
        "provisioning are automated via Ansible playbooks executed inside an Ubuntu Linux WSL2 control node. Furthermore, persistent storage is maintained "
        "through a dedicated Docker Volume (mysql_data). The project seamlessly bridges robust full-stack engineering with industrial-grade DevOps practices.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("2. OBJECTIVES", h1_style))
    obj_bullets = [
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
    for b in obj_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: 3. ABSTRACT & 4. TECHNOLOGY STACK
    # =========================================================================
    story.append(Paragraph("3. ABSTRACT", h1_style))
    story.append(Paragraph(
        "IT Helpdesk is a responsive enterprise web application designed to solve internal IT operational bottlenecks by offering an elegant, "
        "transparent service desk workspace with dynamic progress monitoring, role-based assignment controls, and state persistence. "
        "While traditional support systems often lack modularity and deployment agility, IT Helpdesk is architected from inception to "
        "exemplify an automated DevOps lifecycle.",
        body_style
    ))
    story.append(Paragraph(
        "The DevOps implementation encompasses source code management via Git and GitHub, automated CI/CD pipeline execution using Jenkins 2.x, "
        "container packaging with Docker multi-stage images, automated syntax and regression testing using Maven and JUnit 5, automated container "
        "orchestration and provisioning using Ansible, and volume persistence via Docker Volume mysql_data. The end-to-end workflow follows "
        "GitHub → Jenkins CI/CD → Automated Tests (43 JUnit/Mockito tests) → Docker Build → Ansible Playbook → Docker Compose Multi-Container Stack "
        "(Ports 3000, 8088, 3306) → Web Verification, successfully proving a fully automated, reproducible software engineering cycle.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. TECHNOLOGY STACK", h1_style))
    tech_data = [
        [Paragraph("<b>Technology</b>", tbl_hdr_style), Paragraph("<b>Version / Platform</b>", tbl_hdr_style), Paragraph("<b>Purpose in Project</b>", tbl_hdr_style)],
        [Paragraph("React + Vite", tbl_body_style), Paragraph("React 18 / Vite 5", tbl_body_style), Paragraph("Defines structured responsive UI, interactive dashboards, forms, and client routing", tbl_body_style)],
        [Paragraph("CSS3", tbl_body_style), Paragraph("Custom Modern Design Tokens", tbl_body_style), Paragraph("Modern glassmorphism cards, responsive grid layouts, and SLA status indicators", tbl_body_style)],
        [Paragraph("Web Server", tbl_body_style), Paragraph("Nginx Alpine (1.25.x)", tbl_body_style), Paragraph("Production-ready lightweight web server hosting static assets & reverse proxy", tbl_body_style)],
        [Paragraph("Backend Framework", tbl_body_style), Paragraph("Spring Boot 3.2.5", tbl_body_style), Paragraph("Enterprise REST API, JPA entity transactions, validation, and Actuator metrics", tbl_body_style)],
        [Paragraph("Java Runtime", tbl_body_style), Paragraph("Eclipse Temurin 21 (LTS)", tbl_body_style), Paragraph("High-performance Java 21 runtime running in hardened Alpine container", tbl_body_style)],
        [Paragraph("Relational Database", tbl_body_style), Paragraph("MySQL Server 8.0", tbl_body_style), Paragraph("ACID transactional persistence, utf8mb4 collation, and foreign key constraints", tbl_body_style)],
        [Paragraph("Git", tbl_body_style), Paragraph("Git 2.56.0 for Windows", tbl_body_style), Paragraph("Local source code tracking, semantic commits, branching, and commit history", tbl_body_style)],
        [Paragraph("GitHub", tbl_body_style), Paragraph("Cloud Repository (Public)", tbl_body_style), Paragraph("Centralized source repository: Yokesh07J/IT-Helpdesk", tbl_body_style)],
        [Paragraph("Docker", tbl_body_style), Paragraph("Docker Desktop 29.8.2", tbl_body_style), Paragraph("Multi-stage container engine, image packaging, and runtime isolation", tbl_body_style)],
        [Paragraph("Jenkins", tbl_body_style), Paragraph("Jenkins 2.568.2 LTS", tbl_body_style), Paragraph("CI/CD automation server managing checkout, tests, builds, and deploys", tbl_body_style)],
        [Paragraph("JUnit 5 / Mockito", tbl_body_style), Paragraph("JUnit 5.10 / Mockito 5.7", tbl_body_style), Paragraph("Automated test suite validating service business logic and controllers (43 tests)", tbl_body_style)],
        [Paragraph("Ansible", tbl_body_style), Paragraph("Ansible Core 2.20.1 (WSL2)", tbl_body_style), Paragraph("Configuration management, directory enforcement, and deployment playbooks", tbl_body_style)],
        [Paragraph("Docker Volume", tbl_body_style), Paragraph("mysql_data (local driver)", tbl_body_style), Paragraph("Persistent storage mounted to MySQL database directory (/var/lib/mysql)", tbl_body_style)],
    ]
    t_tech = Table(tech_data, colWidths=[110, 135, 280])
    t_tech.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
    ]))
    story.append(t_tech)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: 5. SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("5. SYSTEM ARCHITECTURE", h1_style))
    story.append(Paragraph(
        "The architecture of IT Helpdesk integrates modern full-stack web engineering with an automated DevOps pipeline. "
        "Every commit pushed to the GitHub repository automatically feeds into a sequential series of stages that build, "
        "test, containerize, provision, and deploy the application.",
        body_style
    ))
    arch_steps = [
        "<b>1. Development & Version Control:</b> The developer writes React frontend and Spring Boot backend code locally and commits changes using Git before pushing to GitHub (Yokesh07J/IT-Helpdesk).",
        "<b>2. Continuous Integration Trigger:</b> Jenkins detects or pulls code from GitHub and launches an automated 5-stage Declarative Pipeline.",
        "<b>3. Automated Testing Stage:</b> Maven clean test executes 43 automated JUnit 5 and Mockito unit tests, validating ticket controllers, service state transitions, and database repository logic.",
        "<b>4. Container Image Build:</b> Docker executes multi-stage builds creating hardened, lightweight production images for backend (Temurin JRE 21) and frontend (Nginx Alpine).",
        "<b>5. Ansible Automated Deployment:</b> An Ansible playbook (deploy-playbook.yml) executed inside Ubuntu Linux coordinates directory provisioning, environment templating, and idempotent compose up execution.",
        "<b>6. Persistent Data & Runtime Access:</b> The multi-container stack runs on private bridge network 'helpdesk-net', binds host ports 3000, 8088, and 3306, and mounts persistent Docker Volume mysql_data."
    ]
    for s in arch_steps:
        story.append(Paragraph(f"• {s}", bullet_style))
    story.append(Spacer(1, 5))

    arch_fig = os.path.join(figures_dir, "fig_architecture_diagram.png")
    if os.path.exists(arch_fig):
        story.append(Image(arch_fig, width=7.1*inch, height=3.6*inch))
        story.append(Paragraph("Figure 5.1: IT Helpdesk End-to-End DevOps System Architecture Diagram", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: MODULE 1 - USER INTERFACE & SERVICE DESK OVERVIEW
    # =========================================================================
    story.append(Paragraph("MODULE 1 - USER INTERFACE & SERVICE DESK OVERVIEW", h1_style))
    story.append(Paragraph(
        "This module delivers the core user interface of IT Helpdesk. Designed with modern aesthetics including glassmorphism "
        "cards, real-time KPI counter widgets, responsive grid layouts, and color-coded status badges, it provides an intuitive "
        "and efficient service desk operations workspace.",
        body_style
    ))
    story.append(Paragraph("<b>Main Features</b>", ParagraphStyle('MFH', fontName='Helvetica-Bold', fontSize=9.5, leading=13)))
    m1_bullets = [
        "Dynamic SLA Metrics & KPI Counters: Displays real-time counts for Total Tickets, Open Issues, In Progress tasks, and Resolved/Closed tickets.",
        "Role-Aware Navigation & Layout: Displays contextual action bars and permissions based on logged-in user credentials (Employee, Support, Admin).",
        "Modern Component Aesthetics: Crisp card layouts, responsive typography, and clear status badges (Open: Blue, In Progress: Amber, Resolved: Green, Closed: Gray).",
        "Real-Time Response Feedback: Provides visual toaster alerts and modal confirmation dialogs upon ticket submission and status updates."
    ]
    for b in m1_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 4))

    fig_7_1 = os.path.join(figures_dir, "fig_7_1.png")
    if os.path.exists(fig_7_1):
        story.append(Image(fig_7_1, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.1: IT Helpdesk Interactive Dashboard with SLA Metrics & KPI Counters", caption_style))

    fig_7_2 = os.path.join(figures_dir, "fig_7_2.png")
    if os.path.exists(fig_7_2):
        story.append(Image(fig_7_2, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.2: IT Helpdesk Ticket Queue Navigation & Responsive Interface", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: MODULE 2 - TICKET LIFECYCLE MANAGEMENT & INTERACTIVE CONTROLS
    # =========================================================================
    story.append(Paragraph("MODULE 2 - TICKET LIFECYCLE MANAGEMENT & INTERACTIVE CONTROLS", h1_style))
    story.append(Paragraph(
        "This module manages ticket creation, triage, status updates, category classification, priority escalations, "
        "search filtering, and staff assignment operations across the ticket lifecycle.",
        body_style
    ))
    story.append(Paragraph("<b>Main Features</b>", ParagraphStyle('MFH2', fontName='Helvetica-Bold', fontSize=9.5, leading=13)))
    m2_bullets = [
        "Structured Incident Creation: Modal input form supporting title, detailed problem description, category selection (Hardware, Software, Network, Access), and priority flags (LOW, MEDIUM, HIGH, URGENT).",
        "Real-Time Search & Multi-Filters: Filter tickets by Status (All, Open, In Progress, Resolved, Closed), Priority, or Category, with instant keyword search.",
        "Automated Ticket Numbering: Backend generates sequential, standardized ticket identifiers (HD-1001, HD-1002) for audit traceability.",
        "Role-Enforced State Progression: Restricts invalid status transitions (e.g., closed tickets cannot jump straight to in-progress without reopening)."
    ]
    for b in m2_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 4))

    fig_7_3 = os.path.join(figures_dir, "fig_7_3.png")
    if os.path.exists(fig_7_3):
        story.append(Image(fig_7_3, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.3: Ticket Creation Interface with Category, Priority & Asset Tag Selection", caption_style))

    fig_7_4 = os.path.join(figures_dir, "fig_7_4.png")
    if os.path.exists(fig_7_4):
        story.append(Image(fig_7_4, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.4: Filtered Tickets View and Real-Time Search Functionality", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: FIGURE 7.5 + MODULE 3 + MODULE 4
    # =========================================================================
    fig_7_5 = os.path.join(figures_dir, "fig_7_5.png")
    if os.path.exists(fig_7_5):
        story.append(Image(fig_7_5, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.5: Ticket Staff Resolution Controls, Activity Audit Log & Reassignment", caption_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph("MODULE 3 - DATABASE PERSISTENCE & DATA SCHEMA", h1_style))
    story.append(Paragraph(
        "IT Helpdesk utilizes a relational MySQL 8 database to maintain enterprise persistence, transaction ACIDity, "
        "and data consistency across client requests. Coupled with Docker Volume persistent storage, application data "
        "remains completely resilient against container restarts or upgrades.",
        body_style
    ))
    story.append(Paragraph("<b>Data Structure Schema</b>", ParagraphStyle('DSS', fontName='Helvetica-Bold', fontSize=9, leading=12)))
    story.append(Paragraph(
        "Each ticket entity is stored in table 'tickets' containing: id (BIGINT primary key), ticket_code (VARCHAR 'HD-XXXX'), "
        "title (VARCHAR 255), description (TEXT), category (ENUM: HARDWARE, SOFTWARE, NETWORK, ACCESS), priority (ENUM: LOW, MEDIUM, HIGH, URGENT), "
        "status (ENUM: OPEN, IN_PROGRESS, RESOLVED, CLOSED), created_by (BIGINT FK to users), assigned_to (BIGINT FK to users, NULLABLE), "
        "created_at (TIMESTAMP), updated_at (TIMESTAMP), and resolved_at (TIMESTAMP NULLABLE).",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("MODULE 4 - GIT & GITHUB SOURCE CONTROL", h1_style))
    story.append(Paragraph(
        "Git is used locally to track modifications, maintain commit history, and configure branch policies. GitHub hosts "
        "the centralized public repository (https://github.com/Yokesh07J/IT-Helpdesk.git) allowing automated checkout by Jenkins.",
        body_style
    ))
    story.append(Paragraph("<b>Main Functions</b>", ParagraphStyle('MF4', fontName='Helvetica-Bold', fontSize=9, leading=12)))
    m4_bullets = [
        "Repository Initialization: Configured developer identity (Yokesh J, yokeshy30@gmail.com), initialized local Git repository, and staged all project assets.",
        "Commit Integrity: Created meaningful semantic commit history for Spring Boot backend, React frontend, Dockerfiles, and Ansible playbooks.",
        "Remote Synchronization: Linked origin remote to GitHub and pushed to the main branch with upstream tracking.",
        "DevOps Assets Tracking: Maintained docker-compose.yml, Jenkinsfile, Dockerfiles, init.sql, ansible/deploy-playbook.yml, and .gitignore."
    ]
    for b in m4_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: GIT & GITHUB EVIDENCE FIGURES (7.6, 7.7, 7.8)
    # =========================================================================
    fig_7_6 = os.path.join(figures_dir, "fig_7_6.png")
    if os.path.exists(fig_7_6):
        story.append(Image(fig_7_6, width=7.1*inch, height=2.45*inch))
        story.append(Paragraph("Figure 7.6: Local Git Identity Configuration and Initial Commit", caption_style))
        story.append(Spacer(1, 4))

    fig_7_7 = os.path.join(figures_dir, "fig_7_7.png")
    if os.path.exists(fig_7_7):
        story.append(Image(fig_7_7, width=7.1*inch, height=2.45*inch))
        story.append(Paragraph("Figure 7.7: Git Remote Configuration and Branch Upstream Synchronization", caption_style))
        story.append(Spacer(1, 4))

    fig_7_8 = os.path.join(figures_dir, "fig_7_8.png")
    if os.path.exists(fig_7_8):
        story.append(Image(fig_7_8, width=7.1*inch, height=2.45*inch))
        story.append(Paragraph("Figure 7.8: IT Helpdesk GitHub Remote Repository Overview (Yokesh07J/IT-Helpdesk)", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: MODULE 5 - DOCKER CONTAINERIZATION
    # =========================================================================
    story.append(Paragraph("MODULE 5 - DOCKER CONTAINERIZATION", h1_style))
    story.append(Paragraph(
        "Docker packages IT Helpdesk into self-contained, portable container images using official Eclipse Temurin JRE 21 "
        "and Nginx Alpine base images. Multi-stage builds compile artifacts in disposable builder containers, yielding "
        "ultra-lean runtime images with minimal attack surfaces and negligible host footprint.",
        body_style
    ))
    story.append(Paragraph("<b>Container Configuration</b>", ParagraphStyle('CC', fontName='Helvetica-Bold', fontSize=9.5, leading=13)))
    c_bullets = [
        "Base Images: eclipse-temurin:21-jre-alpine (backend runtime), nginx:1.25-alpine (frontend web server), and mysql:8.0 (database).",
        "Image Names: it-helpdesk-backend:1.0.0, it-helpdesk-frontend:1.0.0, and mysql:8.0.",
        "Container Names: helpdesk-backend, helpdesk-frontend, and helpdesk-mysql.",
        "Port Mapping: 3000:80 (React Frontend via Nginx), 8088:8088 (Spring Boot REST API), and 3306:3306 (MySQL DB).",
        "Volume Mounting: mysql_data mounted to /var/lib/mysql, ensuring database files survive container lifecycles."
    ]
    for b in c_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 4))

    fig_7_9 = os.path.join(figures_dir, "fig_7_9.png")
    if os.path.exists(fig_7_9):
        story.append(Image(fig_7_9, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.9: Docker Compose Service Orchestration Showing Active Containers", caption_style))

    fig_7_10 = os.path.join(figures_dir, "fig_7_10.png")
    if os.path.exists(fig_7_10):
        story.append(Image(fig_7_10, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.10: Verification of Running IT Helpdesk Stack Containers via docker ps", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: MODULE 6 - JENKINS CI/CD PIPELINE
    # =========================================================================
    story.append(Paragraph("MODULE 6 - JENKINS CI/CD PIPELINE", h1_style))
    story.append(Paragraph(
        "Jenkins automates Continuous Integration and Continuous Deployment. The Jenkins Declarative Pipeline pulls code from GitHub, "
        "validates build dependencies, compiles backend and frontend assets, runs the automated JUnit test suite, builds Docker images, "
        "deploys containers via Docker Compose, and verifies runtime health.",
        body_style
    ))
    story.append(Paragraph("<b>Pipeline Stages (Jenkinsfile)</b>", ParagraphStyle('PSJ', fontName='Helvetica-Bold', fontSize=9.5, leading=13)))
    ps_bullets = [
        "Stage 1 - Checkout: Automatically clones the main branch from GitHub repository (https://github.com/Yokesh07J/IT-Helpdesk.git).",
        "Stage 2 - Automated Testing: Executes 'mvn clean test' running 43 JUnit 5 unit and Mockito mock tests.",
        "Stage 3 - Docker Build: Executes 'docker compose build' to build optimized production container images.",
        "Stage 4 - Docker Deploy: Executes 'docker compose up -d' with health check verification.",
        "Stage 5 - Verification: Inspects container health via Spring Boot Actuator (/actuator/health) and logs deployment SUCCESS."
    ]
    for b in ps_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 4))

    fig_7_11 = os.path.join(figures_dir, "fig_7_11.png")
    if os.path.exists(fig_7_11):
        story.append(Image(fig_7_11, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.11: Jenkins Console Build Output Confirming SUCCESS (Build #6)", caption_style))

    fig_7_12 = os.path.join(figures_dir, "fig_7_12.png")
    if os.path.exists(fig_7_12):
        story.append(Image(fig_7_12, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.12: Jenkins Declarative Pipeline Stage View Execution (Started by Yokesh J)", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: MODULE 7 & MODULE 8
    # =========================================================================
    story.append(Paragraph("MODULE 7 - AUTOMATED TESTING", h1_style))
    story.append(Paragraph(
        "Automated testing is integrated into the Jenkins pipeline via Maven Surefire and JUnit 5. Before any build or deployment proceeds, "
        "the test suite validates that controller REST endpoints, service-layer state transitions, security JWT filters, and database "
        "repository contracts function correctly without regression.",
        body_style
    ))
    story.append(Paragraph("<b>Test Execution Summary</b>", ParagraphStyle('TES', fontName='Helvetica-Bold', fontSize=9.5, leading=13)))
    story.append(Paragraph("<b>Command:</b> mvn clean test -Dspring.profiles.active=test", body_style))
    story.append(Paragraph("<b>Result:</b> 43 passed, 0 failures, 0 errors in 2.8s [100% SUCCESS]. Deployment proceeds only when testing passes.", body_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("MODULE 8 - ANSIBLE DEPLOYMENT", h1_style))
    story.append(Paragraph(
        "Ansible automates the deployment and configuration management of the IT Helpdesk environment. The deployment is governed by "
        "deploy-playbook.yml and executed through an Ubuntu Linux WSL2 control node communicating directly with Docker and the host filesystem.",
        body_style
    ))
    story.append(Paragraph("<b>Playbook Specification (deploy-playbook.yml)</b>", ParagraphStyle('PSP', fontName='Helvetica-Bold', fontSize=9.5, leading=13)))
    ans_bullets = [
        "Play: Deploy IT Helpdesk Multi-Service Stack with Docker.",
        "Task 1: Ensure application directory layout and log directories exist with mode 0755.",
        "Task 2: Ensure persistent Docker volume (mysql_data) exists with proper driver labels.",
        "Task 3: Deploy application stack using community.docker.docker_compose_v2.",
        "Task 4: Wait for backend health endpoint (http://localhost:8088/actuator/health) to return UP.",
        "Task 5: Display deployment summary banner and status URL."
    ]
    for b in ans_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 4))

    fig_7_13 = os.path.join(figures_dir, "fig_7_13.png")
    if os.path.exists(fig_7_13):
        story.append(Image(fig_7_13, width=7.0*inch, height=2.45*inch))
        story.append(Paragraph("Figure 7.13: Ansible Playbook Execution Output (PLAY RECAP: failed=0)", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: FIGURE 7.14 + MODULE 9 + FIGURE 7.15
    # =========================================================================
    fig_7_14 = os.path.join(figures_dir, "fig_7_14.png")
    if os.path.exists(fig_7_14):
        story.append(Image(fig_7_14, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.14: Ansible Playbook Content Inspection and Container Status", caption_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph("MODULE 9 - PERSISTENT STORAGE", h1_style))
    story.append(Paragraph(
        "Persistent storage separates data lifecycle from container lifecycle. Using a dedicated Docker Volume (mysql_data), "
        "database files, user profiles, and ticket history remain fully preserved even when containers are stopped, removed, or updated.",
        body_style
    ))
    story.append(Paragraph("<b>Storage Configuration</b>", ParagraphStyle('SC', fontName='Helvetica-Bold', fontSize=9.5, leading=13)))
    stg_bullets = [
        "Volume Name: mysql_data (Driver: local).",
        "Host Mountpoint: /var/lib/docker/volumes/it-helpdesk_mysql_data/_data.",
        "Container Mount Path: /var/lib/mysql (Mode: Read-Write).",
        "Verification: Verified via 'docker volume ls' and 'docker volume inspect it-helpdesk_mysql_data'."
    ]
    for b in stg_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 4))

    fig_7_15 = os.path.join(figures_dir, "fig_7_15.png")
    if os.path.exists(fig_7_15):
        story.append(Image(fig_7_15, width=7.0*inch, height=2.4*inch))
        story.append(Paragraph("Figure 7.15: Docker Volume Inspection and Mount Verification (mysql_data)", caption_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: MODULE 10, 11, 12 & RESULTS AND OUTPUT
    # =========================================================================
    story.append(Paragraph("MODULE 10 - REST API & AUDIT TRAIL MANAGEMENT", h1_style))
    story.append(Paragraph(
        "IT Helpdesk exposes structured Spring Boot REST endpoints (/api/tickets, /api/auth, /api/users) with JSON payloads. "
        "Every ticket state transition, priority change, and staff note is logged with timestamps and user identifiers, providing "
        "a reliable audit trail that can be exported as structured data for administrative review.",
        body_style
    ))
    story.append(Paragraph("MODULE 11 - CI/CD INTEGRATION", h1_style))
    story.append(Paragraph(
        "This module synthesizes all DevOps tooling into a single automated pipeline: Git/GitHub handles version control, Jenkins orchestrates "
        "checkout and build triggers, Maven executes pre-deployment testing, Docker packages the multi-tier containers, Ansible deploys "
        "the runtime environment, and Docker Volumes secure relational persistence.",
        body_style
    ))
    story.append(Paragraph("MODULE 12 - APPLICATION & DEPLOYMENT VERIFICATION", h1_style))
    story.append(Paragraph("Comprehensive multi-tier verification was conducted to confirm end-to-end functionality across all components:", body_style))
    v_bullets = [
        "Container Runtime: Confirmed active containers helpdesk-frontend, helpdesk-backend, and helpdesk-mysql via 'docker compose ps'.",
        "Port Accessibility: Verified port bindings 0.0.0.0:3000->80/tcp, 0.0.0.0:8088->8088/tcp, and 0.0.0.0:3306->3306/tcp.",
        "HTTP Endpoint: Verified HTTP/1.1 200 OK response from frontend Nginx and backend Actuator health endpoint.",
        "Browser UI: Tested ticket creation, SLA dashboard metrics, search filtering, and staff assignment operations.",
        "Pipeline Success: Verified all 5 Jenkins pipeline stages passed with green status in Build #6.",
        "Ansible Playbook: Confirmed zero failures (failed=0, changed=0 on rerun) in playbook execution.",
        "Data Persistence: Verified Docker Volume mysql_data retains tables across container restart cycles."
    ]
    for b in v_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("18. RESULTS AND OUTPUT", h1_style))
    story.append(Paragraph("The completed DevOps project successfully delivered all specified requirements:", body_style))
    res_bullets = [
        "Feature-rich, responsive IT Helpdesk application with role-based access and real-time SLA metrics.",
        "Centralized Git & GitHub version control repository with clean, semantic commit history.",
        "Automated Jenkins Declarative CI/CD pipeline with 5 sequential execution stages.",
        "Automated unit testing suite (43 JUnit 5 & Mockito tests) validating backend application integrity.",
        "Lightweight Docker multi-stage containerization providing secure, isolated runtimes.",
        "Ansible playbook automation orchestrating repeatable container deployment (failed=0).",
        "Persistent Docker Volume storage ensuring database safety across deployments."
    ]
    for b in res_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: COMMANDS USED & ADVANTAGES
    # =========================================================================
    story.append(Paragraph("19. COMMANDS USED", h1_style))
    story.append(Paragraph("<b>1. Git Commands</b>", ParagraphStyle('CGH', fontName='Helvetica-Bold', fontSize=9, leading=12)))
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
        story.append(Paragraph(f"• {c}", bullet_style))

    story.append(Paragraph("<b>2. Docker & Compose Commands</b>", ParagraphStyle('CDH', fontName='Helvetica-Bold', fontSize=9, leading=12)))
    doc_cmds = [
        "docker compose build — Build multi-stage container images for frontend and backend.",
        "docker compose up -d — Run container stack in detached background mode.",
        "docker compose ps — View active running containers and health status.",
        "docker compose logs backend — Inspect backend container logs and Spring Boot startup.",
        "docker compose down — Gracefully stop and clean up running containers."
    ]
    for c in doc_cmds:
        story.append(Paragraph(f"• {c}", bullet_style))

    story.append(Paragraph("<b>3. Ansible Commands</b>", ParagraphStyle('CAH', fontName='Helvetica-Bold', fontSize=9, leading=12)))
    ans_cmds = [
        "wsl -d Ubuntu — Access Ubuntu Linux WSL2 environment.",
        "ansible-playbook -i ansible/inventory.ini ansible/deploy-playbook.yml — Execute deployment playbook.",
        "cat ansible/deploy-playbook.yml — View playbook contents and tasks."
    ]
    for c in ans_cmds:
        story.append(Paragraph(f"• {c}", bullet_style))

    story.append(Paragraph("<b>4. Persistent Storage (Docker Volume) Commands</b>", ParagraphStyle('CVH', fontName='Helvetica-Bold', fontSize=9, leading=12)))
    vol_cmds = [
        "docker volume ls — List all Docker volumes.",
        "docker volume inspect it-helpdesk_mysql_data — View volume mount point and details.",
        "docker inspect helpdesk-mysql --format '{{json .Mounts}}' — Verify container volume mount."
    ]
    for c in vol_cmds:
        story.append(Paragraph(f"• {c}", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("20. ADVANTAGES", h1_style))
    adv_bullets = [
        "Automated Delivery: Eliminates manual errors and reduces release overhead via Jenkins CI/CD.",
        "Container Isolation: Docker packages code, dependencies, and servers into standardized environments.",
        "Repeatable Deployment: Ansible ensures uniform, idempotent deployments across any development or staging node.",
        "Data Resilience: Persistent volumes prevent data loss when updating or restarting database containers.",
        "Rich User Experience: Responsive UI with category tags, SLA metrics, and real-time status transitions.",
        "Lightweight Footprint: Alpine base images provide exceptional startup speed with minimal memory usage."
    ]
    for b in adv_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 19: LIMITATIONS, FUTURE ENHANCEMENTS & CONCLUSION
    # =========================================================================
    story.append(Paragraph("21. LIMITATIONS", h1_style))
    lim_bullets = [
        "Email / SMS Notifications: Real-time SMTP email dispatch and SMS alerting for ticket status changes are not yet configured.",
        "Single-Node Architecture: The CI/CD server and containers run on a local workstation rather than a distributed cloud cluster.",
        "Monitoring Telemetry: Real-time Prometheus metric scraping and Grafana visualization dashboards are not currently incorporated.",
        "OAuth2 / SSO Integration: Single Sign-On via Google or Microsoft Azure AD is not currently implemented."
    ]
    for b in lim_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("22. FUTURE ENHANCEMENTS", h1_style))
    fe_bullets = [
        "Notification Microservice: Implement an asynchronous Spring Cloud Stream service for email and Slack alert notifications.",
        "Kubernetes Orchestration: Deploy Helm charts to run multi-node clusters on Amazon EKS or Google Kubernetes Engine.",
        "Monitoring & Observability: Integrate Prometheus, Grafana, and Micrometer for automated cluster telemetry.",
        "Webhook Automation: Configure GitHub webhooks to trigger automatic Jenkins builds upon every pull request push.",
        "Enterprise SSO: Implement OAuth2 / OpenID Connect login with Azure Active Directory integration."
    ]
    for b in fe_bullets:
        story.append(Paragraph(f"• {b}", bullet_style))
    story.append(Spacer(1, 5))

    story.append(Paragraph("23. CONCLUSION", h1_style))
    story.append(Paragraph(
        "The IT Helpdesk DevOps Laboratory project demonstrates a comprehensive implementation of modern web engineering "
        "united with industrial DevOps practices. The application provides an engaging, high-performance service desk interface "
        "featuring SLA tracking, dynamic categorization, role-based workflows, and automated ticket progression.",
        body_style
    ))
    story.append(Paragraph(
        "Throughout the project, each phase of the DevOps lifecycle was systematically realized: Git and GitHub provided robust "
        "source code control; Jenkins orchestrated an automated CI/CD pipeline comprising automated testing, image construction, and "
        "container deployment; Docker packaged the application into ultra-lightweight, isolated containers; Ansible eliminated manual "
        "configuration through automated playbook execution; and Docker Volumes secured data durability across container recreations. "
        "The seamless integration of GitHub → Jenkins → Maven → Docker → Ansible → Docker Volume conclusively validates the principles "
        "of Continuous Integration, Continuous Deployment, and Infrastructure Automation taught in 23IT723 - DevOps Laboratory.",
        body_style
    ))

    # Build PDF
    doc.build(story, canvasmaker=BorderAndNumberedCanvas)
    print(f"Successfully generated PDF report at: {output_path}")

if __name__ == '__main__':
    figures_dir = r"C:\DevopsCat\IT-Helpdesk\docs\final-report\figures"
    pdf_out = r"C:\DevopsCat\IT-Helpdesk\docs\final-report\23IT723_Final_Project_Report_IT_Helpdesk.pdf"
    build_pdf_report(pdf_out, figures_dir)
    
    # Verify page count
    reader = pypdf.PdfReader(pdf_out)
    print(f"Total pages generated: {len(reader.pages)}")
