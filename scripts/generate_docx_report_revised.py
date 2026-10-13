#!/usr/bin/env python3
"""
Generate Revised Final DevOps CAT Project Report (DOCX)
Course: 23IT723 - DevOps Laboratory
Project: IT HELPDESK AND TICKET MANAGEMENT SYSTEM
Institution: Coimbatore Institute of Technology, Coimbatore
Student: YOKESH J (Register No: 2303717620521xxx)

Exact structure matching 23IT723_Final_Project_Report_TaskPulse.pdf.
Strict Requirements:
- Pure black text (#000000) throughout.
- White backgrounds on all tables.
- Natural aspect ratios preserved on all figures (zero distortion).
- Clean rectangular outer border and exact page numbers.
"""

import os
import sys
from PIL import Image as PILImage
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_page_border(section):
    """Sets a clean rectangular black border around every page in Word."""
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

def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_page_number_field(run):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def add_proportional_figure(doc, img_path, max_w_in, max_h_in, caption):
    """Adds a figure centered with its natural aspect ratio strictly preserved."""
    if not os.path.exists(img_path):
        return
    im = PILImage.open(img_path)
    orig_w, orig_h = im.size
    aspect = orig_w / orig_h

    target_w = max_w_in
    target_h = target_w / aspect

    if target_h > max_h_in:
        target_h = max_h_in
        target_w = target_h * aspect

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(3)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.add_run().add_picture(img_path, width=Inches(target_w), height=Inches(target_h))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_after = Pt(5)
    r = p_cap.add_run(caption)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00) # Pure black
    r.bold = True

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
        
        # Bottom-right page number in footer (pure black)
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_ft = p_ft.add_run()
        r_ft.font.name = 'Times New Roman'
        r_ft.font.size = Pt(10)
        r_ft.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        add_page_number_field(r_ft)

    # Base styling - 100% Pure Black Text
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
    r_inst.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_inst.bold = True
    
    r_sub = p_inst.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\nCOIMBATORE - 641 014\n")
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_sub.italic = True
    p_inst.paragraph_format.space_after = Pt(24)

    logo_path = os.path.join(figures_dir, "cit_logo_enhanced.png")
    if not os.path.exists(logo_path):
        logo_path = os.path.join(figures_dir, "cit_logo.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.add_run().add_picture(logo_path, width=Inches(1.8), height=Inches(1.8))
        p_logo.paragraph_format.space_after = Pt(28)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_course.add_run("23IT723 - DEVOPS LABORATORY\n\nPROJECT REPORT\n")
    r_c.font.size = Pt(12)
    r_c.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_c.bold = True
    p_course.paragraph_format.space_after = Pt(20)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("IT HELPDESK AND TICKET MANAGEMENT SYSTEM\n")
    r_t.font.size = Pt(13.5)
    r_t.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_t.bold = True
    p_title.paragraph_format.space_after = Pt(72)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_date.add_run("OCTOBER 2026\n")
    r_d.font.size = Pt(11)
    r_d.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_d.bold = True
    p_date.paragraph_format.space_after = Pt(64)

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sb = p_subm.add_run("Submitted by\n\n")
    r_sb.font.size = Pt(11)
    r_sb.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_sb.bold = True
    r_auth = p_subm.add_run("2303717620521xxx  YOKESH J")
    r_auth.font.size = Pt(11)
    r_auth.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_auth.bold = True

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 2: BONAFIDE CERTIFICATE
    # -------------------------------------------------------------------------
    p_cert_inst = doc.add_paragraph()
    p_cert_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ci = p_cert_inst.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n")
    r_ci.bold = True
    r_ci.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_ci_sub = p_cert_inst.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\nCOIMBATORE - 641 014\n")
    r_ci_sub.font.size = Pt(10)
    r_ci_sub.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_ci_sub.italic = True
    p_cert_inst.paragraph_format.space_after = Pt(28)

    p_bon = doc.add_paragraph()
    p_bon.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_bon = p_bon.add_run("BONAFIDE CERTIFICATE\n")
    r_bon.font.size = Pt(13)
    r_bon.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_bon.bold = True
    p_bon.paragraph_format.space_after = Pt(24)

    p_cbody = doc.add_paragraph()
    p_cbody.paragraph_format.line_spacing = 1.3
    p_cbody.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r1 = p_cbody.add_run("Certified that this project report titled ")
    r1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r2 = p_cbody.add_run('"IT HELPDESK AND TICKET MANAGEMENT SYSTEM"')
    r2.bold = True
    r2.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r3 = p_cbody.add_run(" is the bonafide work of ")
    r3.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r4 = p_cbody.add_run("2303717620521xxx - YOKESH J")
    r4.bold = True
    r4.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r5 = p_cbody.add_run(" completed during the academic year ")
    r5.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r6 = p_cbody.add_run("2026-2027 - Semester VII")
    r6.bold = True
    r6.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r7 = p_cbody.add_run(" for the project presentation of ")
    r7.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r8 = p_cbody.add_run("23IT723 - DEVOPS LABORATORY")
    r8.bold = True
    r8.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r9 = p_cbody.add_run(" under our supervision.\n\n")
    r9.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_cbody2 = doc.add_paragraph()
    p_cbody2.paragraph_format.line_spacing = 1.3
    r_cb2 = p_cbody2.add_run("Certified that the candidate was examined by using the project work examination.\n\n\n")
    r_cb2.italic = True
    r_cb2.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    p_cbody2.paragraph_format.space_after = Pt(50)

    p_rev = doc.add_paragraph()
    r_rvh = p_rev.add_run("Review Members:\n\n")
    r_rvh.bold = True
    r_rvh.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_rv1 = p_rev.add_run("    1. Dr. M. Sangeetha\n\n")
    r_rv1.bold = True
    r_rv1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_rv2 = p_rev.add_run("    2. Dr. E. Arul\n")
    r_rv2.bold = True
    r_rv2.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 3: EVALUATION SCHEME
    # -------------------------------------------------------------------------
    p_es1 = doc.add_paragraph()
    p_es1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_e1 = p_es1.add_run("23IT723 – DEVOPS LABORATORY\n")
    r_e1.bold = True
    r_e1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_e2 = p_es1.add_run("FINAL MINI PROJECT – EVALUATION SCHEME\n")
    r_e2.bold = True
    r_e2.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    p_es1.paragraph_format.space_after = Pt(4)

    p_es2 = doc.add_paragraph()
    p_es2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_e3 = p_es2.add_run("Final Mini Project Assessment")
    r_e3.bold = True
    r_e3.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    p_es2.paragraph_format.space_after = Pt(6)

    p_es_desc = doc.add_paragraph()
    p_es_desc.paragraph_format.line_spacing = 1.15
    r_ed = p_es_desc.add_run(
        "The final mini project shall require students to integrate the major DevOps practices covered in the laboratory. "
        "The project should demonstrate practical implementation of version control, collaborative development, Continuous Integration, "
        "containerization and/or automated configuration/provisioning, with proper execution evidence."
    )
    r_ed.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
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
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00) # Pure black
            if is_hdr:
                run.bold = True
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 4: RECOMMENDED MARK DISTRIBUTION & FACULTY EVALUATION RECORD
    # -------------------------------------------------------------------------
    p_rmd = doc.add_paragraph()
    p_rmd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rmd = p_rmd.add_run("Recommended Mark Distribution within the Final Demonstration")
    r_rmd.bold = True
    r_rmd.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    p_rmd.paragraph_format.space_after = Pt(4)

    p_rmd_sub = doc.add_paragraph()
    r_rs = p_rmd_sub.add_run("For uniform evaluation, the examiner may use the following internal split for the implementation and demonstration components.")
    r_rs.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
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
            run.font.name = 'Times New Roman'
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            if is_hdr:
                run.bold = True
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)

    p_ev_h = doc.add_paragraph()
    p_ev_h.paragraph_format.space_before = Pt(8)
    r_evh = p_ev_h.add_run("Minimum Evidence to be Submitted")
    r_evh.bold = True
    r_evh.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    
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
        r = p_b.add_run(b)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_eg_h = doc.add_paragraph()
    p_eg_h.paragraph_format.space_before = Pt(6)
    r_egh = p_eg_h.add_run("Evaluation Guidelines")
    r_egh.bold = True
    r_egh.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
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
        r = p_b.add_run(b)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_fac_h = doc.add_paragraph()
    p_fac_h.paragraph_format.space_before = Pt(8)
    p_fac_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_fh = p_fac_h.add_run("Faculty Evaluation Record")
    r_fh.bold = True
    r_fh.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

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
            run.font.name = 'Times New Roman'
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            if c_idx in [0, 2]:
                run.bold = True
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 5: TABLE OF CONTENTS
    # -------------------------------------------------------------------------
    p_toc_h = doc.add_paragraph()
    p_toc_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_th = p_toc_h.add_run("TABLE OF CONTENTS")
    r_th.bold = True
    r_th.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
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
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            if is_hdr:
                run.bold = True
            set_cell_margins(cell, top=40, bottom=40, left=70, right=70)

    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 6: 1. INTRODUCTION & 2. OBJECTIVES
    # -------------------------------------------------------------------------
    p_h1 = doc.add_paragraph()
    r = p_h1.add_run("1. INTRODUCTION")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_p1 = doc.add_paragraph()
    r = p_p1.add_run(
        "IT Helpdesk is a modern, high-performance web-based service desk and ticket management platform engineered to "
        "streamline enterprise incident reporting, categorization, priority triage, SLA tracking, and staff resolution workflows. "
        "Built with a decoupled architecture—featuring a React + Vite Single Page Application (SPA), a Spring Boot 3.2.5 enterprise REST API "
        "on Java 21 LTS, and a robust MySQL 8 relational persistence engine—the platform delivers real-time ticket analytics, "
        "role-based security access (Employee, Support Staff, Admin), automated ticket code assignment (HD-XXXX), dynamic status transitions, "
        "and structured CSV/JSON audit export capabilities."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_p2 = doc.add_paragraph()
    r = p_p2.add_run(
        "Beyond standalone application functionality, this project incorporates an end-to-end DevOps automation workflow covering every stage "
        "of modern software delivery. Source code management and collaborative versioning are implemented using Git and GitHub (Yokesh07J/IT-Helpdesk). "
        "Continuous Integration is automated via a Jenkins Declarative Pipeline that retrieves source code, executes 43 automated Maven/JUnit 5 unit "
        "and Mockito tests, compiles production bundles, and packages the multi-tier application into lightweight Docker containers. "
        "Containerization is performed through Docker Compose with health probes and private networking, while configuration management and environment "
        "provisioning are automated via Ansible playbooks executed inside an Ubuntu Linux WSL2 control node. Furthermore, persistent storage is maintained "
        "through a dedicated Docker Volume (mysql_data). The project seamlessly bridges robust full-stack engineering with industrial-grade DevOps practices."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    
    p_h2 = doc.add_paragraph()
    r = p_h2.add_run("2. OBJECTIVES")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

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
        p_b = doc.add_paragraph(style='List Bullet')
        r = p_b.add_run(b)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 7: 3. ABSTRACT & 4. TECHNOLOGY STACK
    # -------------------------------------------------------------------------
    p_h3 = doc.add_paragraph()
    r = p_h3.add_run("3. ABSTRACT")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_a1 = doc.add_paragraph()
    r = p_a1.add_run(
        "IT Helpdesk is a responsive enterprise web application designed to solve internal IT operational bottlenecks by offering an elegant, "
        "transparent service desk workspace with dynamic progress monitoring, role-based assignment controls, and state persistence. "
        "While traditional support systems often lack modularity and deployment agility, IT Helpdesk is architected from inception to "
        "exemplify an automated DevOps lifecycle."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_a2 = doc.add_paragraph()
    r = p_a2.add_run(
        "The DevOps implementation encompasses source code management via Git and GitHub, automated CI/CD pipeline execution using Jenkins 2.x, "
        "container packaging with Docker multi-stage images, automated syntax and regression testing using Maven and JUnit 5, automated container "
        "orchestration and provisioning using Ansible, and volume persistence via Docker Volume mysql_data. The end-to-end workflow follows "
        "GitHub → Jenkins CI/CD → Automated Tests (43 JUnit/Mockito tests) → Docker Build → Ansible Playbook → Docker Compose Multi-Container Stack "
        "(Ports 3000, 8088, 3306) → Web Verification, successfully proving a fully automated, reproducible software engineering cycle."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_h4 = doc.add_paragraph()
    r = p_h4.add_run("4. TECHNOLOGY STACK")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

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
            run.font.name = 'Times New Roman'
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
            if is_hdr:
                run.bold = True
            set_cell_margins(cell, top=35, bottom=35, left=60, right=60)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 8: 5. SYSTEM ARCHITECTURE
    # -------------------------------------------------------------------------
    p_h5 = doc.add_paragraph()
    r = p_h5.add_run("5. SYSTEM ARCHITECTURE")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_arch = doc.add_paragraph()
    r = p_arch.add_run(
        "The architecture of IT Helpdesk integrates modern full-stack web engineering with an automated DevOps pipeline. "
        "Every commit pushed to the GitHub repository automatically feeds into a sequential series of stages that build, "
        "test, containerize, provision, and deploy the application."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    arch_steps = [
        "1. Development & Version Control: The developer writes React frontend and Spring Boot backend code locally and commits changes using Git before pushing to GitHub (Yokesh07J/IT-Helpdesk).",
        "2. Continuous Integration Trigger: Jenkins detects or pulls code from GitHub and launches an automated 5-stage Declarative Pipeline.",
        "3. Automated Testing Stage: Maven clean test executes 43 automated JUnit 5 and Mockito unit tests, validating ticket controllers, service state transitions, and database repository logic.",
        "4. Container Image Build: Docker executes multi-stage builds creating hardened, lightweight production images for backend (Temurin JRE 21) and frontend (Nginx Alpine).",
        "5. Ansible Automated Deployment: An Ansible playbook (deploy-playbook.yml) executed inside Ubuntu Linux coordinates directory provisioning, environment templating, and idempotent compose up execution.",
        "6. Persistent Data & Runtime Access: The multi-container stack runs on private bridge network 'helpdesk-net', binds host ports 3000, 8088, and 3306, and mounts persistent Docker Volume mysql_data."
    ]
    for s in arch_steps:
        p_s = doc.add_paragraph(style='List Bullet')
        r = p_s.add_run(s)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    add_proportional_figure(
        doc,
        os.path.join(figures_dir, "fig_architecture_diagram.png"),
        max_w_in=6.2, max_h_in=3.55,
        caption="Figure 5.1: IT Helpdesk End-to-End DevOps System Architecture Diagram"
    )
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 9: MODULE 1
    # -------------------------------------------------------------------------
    p_m1 = doc.add_paragraph()
    r = p_m1.add_run("MODULE 1 - USER INTERFACE & SERVICE DESK OVERVIEW")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m1_desc = doc.add_paragraph()
    r = p_m1_desc.add_run(
        "This module delivers the core user interface of IT Helpdesk. Designed with modern aesthetics including glassmorphism "
        "cards, real-time KPI counter widgets, responsive grid layouts, and color-coded status badges, it provides an intuitive "
        "and efficient service desk operations workspace."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_mf1 = doc.add_paragraph()
    r = p_mf1.add_run("Main Features")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    m1_feats = [
        "Dynamic SLA Metrics & KPI Counters: Displays real-time counts for Total Tickets, Open Issues, In Progress tasks, and Resolved/Closed tickets.",
        "Role-Aware Navigation & Layout: Displays contextual action bars and permissions based on logged-in user credentials (Employee, Support, Admin).",
        "Modern Component Aesthetics: Crisp card layouts, responsive typography, and clear status badges (Open: Blue, In Progress: Amber, Resolved: Green, Closed: Gray).",
        "Real-Time Response Feedback: Provides visual toaster alerts and modal confirmation dialogs upon ticket submission and status updates."
    ]
    for f in m1_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_1.png"),
        max_w_in=5.5, max_h_in=2.85,
        caption="Figure 7.1: IT Helpdesk Interactive Dashboard with SLA Metrics & KPI Counters"
    )
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_2.png"),
        max_w_in=5.5, max_h_in=2.85,
        caption="Figure 7.2: IT Helpdesk Ticket Queue Navigation & Responsive Interface"
    )
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 10: MODULE 2
    # -------------------------------------------------------------------------
    p_m2 = doc.add_paragraph()
    r = p_m2.add_run("MODULE 2 - TICKET LIFECYCLE MANAGEMENT & INTERACTIVE CONTROLS")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m2_desc = doc.add_paragraph()
    r = p_m2_desc.add_run(
        "This module manages ticket creation, triage, status updates, category classification, priority escalations, "
        "search filtering, and staff assignment operations across the ticket lifecycle."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_mf2 = doc.add_paragraph()
    r = p_mf2.add_run("Main Features")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    m2_feats = [
        "Structured Incident Creation: Modal input form supporting title, detailed problem description, category selection (Hardware, Software, Network, Access), and priority flags (LOW, MEDIUM, HIGH, URGENT).",
        "Real-Time Search & Multi-Filters: Filter tickets by Status (All, Open, In Progress, Resolved, Closed), Priority, or Category, with instant keyword search.",
        "Automated Ticket Numbering: Backend generates sequential, standardized ticket identifiers (HD-1001, HD-1002) for audit traceability.",
        "Role-Enforced State Progression: Restricts invalid status transitions (e.g., closed tickets cannot jump straight to in-progress without reopening)."
    ]
    for f in m2_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_3.png"),
        max_w_in=5.5, max_h_in=2.80,
        caption="Figure 7.3: Ticket Creation Interface with Category, Priority & Asset Tag Selection"
    )
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_4.png"),
        max_w_in=5.5, max_h_in=2.85,
        caption="Figure 7.4: Filtered Tickets View and Real-Time Search Functionality"
    )
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 11: FIGURE 7.5 + MODULE 3 + MODULE 4
    # -------------------------------------------------------------------------
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_5.png"),
        max_w_in=5.5, max_h_in=2.80,
        caption="Figure 7.5: Ticket Staff Resolution Controls, Activity Audit Log & Reassignment"
    )

    p_m3 = doc.add_paragraph()
    r = p_m3.add_run("MODULE 3 - DATABASE PERSISTENCE & DATA SCHEMA")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m3_desc = doc.add_paragraph()
    r = p_m3_desc.add_run(
        "IT Helpdesk utilizes a relational MySQL 8 database to maintain enterprise persistence, transaction ACIDity, "
        "and data consistency across client requests. Coupled with Docker Volume persistent storage, application data "
        "remains completely resilient against container restarts or upgrades."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_ds = doc.add_paragraph()
    r_dsh = p_ds.add_run("Data Structure Schema: ")
    r_dsh.bold = True
    r_dsh.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r_dsd = p_ds.add_run(
        "Each ticket entity is stored in table 'tickets' containing: id (BIGINT primary key), ticket_code (VARCHAR 'HD-XXXX'), "
        "title (VARCHAR 255), description (TEXT), category (ENUM: HARDWARE, SOFTWARE, NETWORK, ACCESS), priority (ENUM: LOW, MEDIUM, HIGH, URGENT), "
        "status (ENUM: OPEN, IN_PROGRESS, RESOLVED, CLOSED), created_by (BIGINT FK to users), assigned_to (BIGINT FK to users, NULLABLE), "
        "created_at (TIMESTAMP), updated_at (TIMESTAMP), and resolved_at (TIMESTAMP NULLABLE)."
    )
    r_dsd.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m4 = doc.add_paragraph()
    r = p_m4.add_run("MODULE 4 - GIT & GITHUB SOURCE CONTROL")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m4_desc = doc.add_paragraph()
    r = p_m4_desc.add_run(
        "Git is used locally to track modifications, maintain commit history, and configure branch policies. GitHub hosts "
        "the centralized public repository (https://github.com/Yokesh07J/IT-Helpdesk.git) allowing automated checkout by Jenkins."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_mf4 = doc.add_paragraph()
    r = p_mf4.add_run("Main Functions")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    m4_feats = [
        "Repository Initialization: Configured developer identity (Yokesh J, yokeshy30@gmail.com), initialized local Git repository, and staged all project assets.",
        "Commit Integrity: Created meaningful semantic commit history for Spring Boot backend, React frontend, Dockerfiles, and Ansible playbooks.",
        "Remote Synchronization: Linked origin remote to GitHub and pushed to the main branch with upstream tracking.",
        "DevOps Assets Tracking: Maintained docker-compose.yml, Jenkinsfile, Dockerfiles, init.sql, ansible/deploy-playbook.yml, and .gitignore."
    ]
    for f in m4_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 12: FIGURES 7.6, 7.7, 7.8
    # -------------------------------------------------------------------------
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_6.png"),
        max_w_in=5.6, max_h_in=2.35,
        caption="Figure 7.6: Local Git Identity Configuration and Initial Commit"
    )
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_7.png"),
        max_w_in=5.6, max_h_in=2.35,
        caption="Figure 7.7: Git Remote Configuration and Branch Upstream Synchronization"
    )
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_8.png"),
        max_w_in=5.6, max_h_in=2.25,
        caption="Figure 7.8: IT Helpdesk GitHub Remote Repository Overview (Yokesh07J/IT-Helpdesk)"
    )
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 13: MODULE 5
    # -------------------------------------------------------------------------
    p_m5 = doc.add_paragraph()
    r = p_m5.add_run("MODULE 5 - DOCKER CONTAINERIZATION")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m5_desc = doc.add_paragraph()
    r = p_m5_desc.add_run(
        "Docker packages IT Helpdesk into self-contained, portable container images using official Eclipse Temurin JRE 21 "
        "and Nginx Alpine base images. Multi-stage builds compile artifacts in disposable builder containers, yielding "
        "ultra-lean runtime images with minimal attack surfaces and negligible host footprint."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_cc = doc.add_paragraph()
    r = p_cc.add_run("Container Configuration")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    c_feats = [
        "Base Images: eclipse-temurin:21-jre-alpine (backend runtime), nginx:1.25-alpine (frontend web server), and mysql:8.0 (database).",
        "Image Names: it-helpdesk-backend:1.0.0, it-helpdesk-frontend:1.0.0, and mysql:8.0.",
        "Container Names: helpdesk-backend, helpdesk-frontend, and helpdesk-mysql.",
        "Port Mapping: 3000:80 (React Frontend via Nginx), 8088:8088 (Spring Boot REST API), and 3306:3306 (MySQL DB).",
        "Volume Mounting: mysql_data mounted to /var/lib/mysql, ensuring database files survive container lifecycles."
    ]
    for f in c_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_9.png"),
        max_w_in=5.6, max_h_in=2.25,
        caption="Figure 7.9: Docker Desktop Management Dashboard Showing Active Containers"
    )
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_10.png"),
        max_w_in=5.6, max_h_in=2.35,
        caption="Figure 7.10: Verification of Running IT Helpdesk Stack Containers via docker ps"
    )
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 14: MODULE 6
    # -------------------------------------------------------------------------
    p_m6 = doc.add_paragraph()
    r = p_m6.add_run("MODULE 6 - JENKINS CI/CD PIPELINE")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m6_desc = doc.add_paragraph()
    r = p_m6_desc.add_run(
        "Jenkins automates Continuous Integration and Continuous Deployment. The Jenkins Declarative Pipeline pulls code from GitHub, "
        "validates build dependencies, compiles backend and frontend assets, runs the automated JUnit test suite, builds Docker images, "
        "deploys containers via Docker Compose, and verifies runtime health."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_psj = doc.add_paragraph()
    r = p_psj.add_run("Pipeline Stages (Jenkinsfile)")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    ps_feats = [
        "Stage 1 - Checkout: Automatically clones the main branch from GitHub repository (https://github.com/Yokesh07J/IT-Helpdesk.git).",
        "Stage 2 - Automated Testing: Executes 'mvn clean test' running 43 JUnit 5 unit and Mockito mock tests.",
        "Stage 3 - Docker Build: Executes 'docker compose build' to build optimized production container images.",
        "Stage 4 - Docker Deploy: Executes 'docker compose up -d' with health check verification.",
        "Stage 5 - Verification: Inspects container health via Spring Boot Actuator (/actuator/health) and logs deployment SUCCESS."
    ]
    for f in ps_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_11.png"),
        max_w_in=5.6, max_h_in=2.35,
        caption="Figure 7.11: Jenkins Console Build Output Confirming SUCCESS (Build #6)"
    )
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_12.png"),
        max_w_in=5.6, max_h_in=2.25,
        caption="Figure 7.12: Jenkins Declarative Pipeline Stage View Execution (Started by Yokesh J)"
    )
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 15: MODULE 7 & MODULE 8
    # -------------------------------------------------------------------------
    p_m7 = doc.add_paragraph()
    r = p_m7.add_run("MODULE 7 - AUTOMATED TESTING")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m7_desc = doc.add_paragraph()
    r = p_m7_desc.add_run(
        "Automated testing is integrated into the Jenkins pipeline via Maven Surefire and JUnit 5. Before any build or deployment proceeds, "
        "the test suite validates that controller REST endpoints, service-layer state transitions, security JWT filters, and database "
        "repository contracts function correctly without regression."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_tes = doc.add_paragraph()
    r = p_tes.add_run("Test Execution Summary\n")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r1 = p_tes.add_run("Command: mvn clean test -Dspring.profiles.active=test\n")
    r1.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    r2 = p_tes.add_run("Result: 43 passed, 0 failures, 0 errors in 2.8s [100% SUCCESS]. Deployment proceeds only when testing passes.")
    r2.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m8 = doc.add_paragraph()
    r = p_m8.add_run("MODULE 8 - ANSIBLE DEPLOYMENT")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m8_desc = doc.add_paragraph()
    r = p_m8_desc.add_run(
        "Ansible automates the deployment and configuration management of the IT Helpdesk environment. The deployment is governed by "
        "deploy-playbook.yml and executed through an Ubuntu Linux WSL2 control node communicating directly with Docker and the host filesystem."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_psp = doc.add_paragraph()
    r = p_psp.add_run("Playbook Specification (deploy-playbook.yml)")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    ans_feats = [
        "Play: Deploy IT Helpdesk Multi-Service Stack with Docker.",
        "Task 1: Ensure application directory layout and log directories exist with mode 0755.",
        "Task 2: Ensure persistent Docker volume (mysql_data) exists with proper driver labels.",
        "Task 3: Deploy application stack using community.docker.docker_compose_v2.",
        "Task 4: Wait for backend health endpoint (http://localhost:8088/actuator/health) to return UP.",
        "Task 5: Display deployment summary banner and status URL."
    ]
    for f in ans_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_13.png"),
        max_w_in=5.6, max_h_in=2.55,
        caption="Figure 7.13: Ansible Playbook Execution Output (PLAY RECAP: failed=0)"
    )
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 16: FIGURE 7.14 + MODULE 9 + FIGURE 7.15
    # -------------------------------------------------------------------------
    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_14.png"),
        max_w_in=5.6, max_h_in=2.35,
        caption="Figure 7.14: Ansible Playbook Content Inspection and Container Status"
    )

    p_m9 = doc.add_paragraph()
    r = p_m9.add_run("MODULE 9 - PERSISTENT STORAGE")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m9_desc = doc.add_paragraph()
    r = p_m9_desc.add_run(
        "Persistent storage separates data lifecycle from container lifecycle. Using a dedicated Docker Volume (mysql_data), "
        "database files, user profiles, and ticket history remain fully preserved even when containers are stopped, removed, or updated."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_sc = doc.add_paragraph()
    r = p_sc.add_run("Storage Configuration")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    stg_feats = [
        "Volume Name: mysql_data (Driver: local).",
        "Host Mountpoint: /var/lib/docker/volumes/it-helpdesk_mysql_data/_data.",
        "Container Mount Path: /var/lib/mysql (Mode: Read-Write).",
        "Verification: Verified via 'docker volume ls' and 'docker volume inspect it-helpdesk_mysql_data'."
    ]
    for f in stg_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    add_proportional_figure(
        doc, os.path.join(figures_dir, "fig_7_15.png"),
        max_w_in=5.6, max_h_in=2.35,
        caption="Figure 7.15: Docker Volume Inspection and Mount Verification (mysql_data)"
    )
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 17: MODULE 10, 11, 12 & RESULTS AND OUTPUT
    # -------------------------------------------------------------------------
    p_m10 = doc.add_paragraph()
    r = p_m10.add_run("MODULE 10 - REST API & AUDIT TRAIL MANAGEMENT")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m10_desc = doc.add_paragraph()
    r = p_m10_desc.add_run(
        "IT Helpdesk exposes structured Spring Boot REST endpoints (/api/tickets, /api/auth, /api/users) with JSON payloads. "
        "Every ticket state transition, priority change, and staff note is logged with timestamps and user identifiers, providing "
        "a reliable audit trail that can be exported as structured data for administrative review."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m11 = doc.add_paragraph()
    r = p_m11.add_run("MODULE 11 - CI/CD INTEGRATION")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m11_desc = doc.add_paragraph()
    r = p_m11_desc.add_run(
        "This module synthesizes all DevOps tooling into a single automated pipeline: Git/GitHub handles version control, Jenkins orchestrates "
        "checkout and build triggers, Maven executes pre-deployment testing, Docker packages the multi-tier containers, Ansible deploys "
        "the runtime environment, and Docker Volumes secure relational persistence."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m12 = doc.add_paragraph()
    r = p_m12.add_run("MODULE 12 - APPLICATION & DEPLOYMENT VERIFICATION")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_m12_desc = doc.add_paragraph()
    r = p_m12_desc.add_run("Comprehensive multi-tier verification was conducted to confirm end-to-end functionality across all components:")
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
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
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_res = doc.add_paragraph()
    r = p_res.add_run("18. RESULTS AND OUTPUT")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_res_desc = doc.add_paragraph()
    r = p_res_desc.add_run("The completed DevOps project successfully delivered all specified requirements:")
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
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
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 18: COMMANDS USED & ADVANTAGES
    # -------------------------------------------------------------------------
    p_cmd = doc.add_paragraph()
    r = p_cmd.add_run("19. COMMANDS USED")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_cg = doc.add_paragraph()
    r = p_cg.add_run("1. Git Commands")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
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
        p_c = doc.add_paragraph(style='List Bullet')
        r = p_c.add_run(c)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_cd = doc.add_paragraph()
    r = p_cd.add_run("2. Docker & Compose Commands")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    doc_cmds = [
        "docker compose build — Build multi-stage container images for frontend and backend.",
        "docker compose up -d — Run container stack in detached background mode.",
        "docker compose ps — View active running containers and health status.",
        "docker compose logs backend — Inspect backend container logs and Spring Boot startup.",
        "docker compose down — Gracefully stop and clean up running containers."
    ]
    for c in doc_cmds:
        p_c = doc.add_paragraph(style='List Bullet')
        r = p_c.add_run(c)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_ca = doc.add_paragraph()
    r = p_ca.add_run("3. Ansible Commands")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    ans_cmds = [
        "wsl -d Ubuntu — Access Ubuntu Linux WSL2 environment.",
        "ansible-playbook -i ansible/inventory.ini ansible/deploy-playbook.yml — Execute deployment playbook.",
        "cat ansible/deploy-playbook.yml — View playbook contents and tasks."
    ]
    for c in ans_cmds:
        p_c = doc.add_paragraph(style='List Bullet')
        r = p_c.add_run(c)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_cv = doc.add_paragraph()
    r = p_cv.add_run("4. Persistent Storage (Docker Volume) Commands")
    r.bold = True
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    vol_cmds = [
        "docker volume ls — List all Docker volumes.",
        "docker volume inspect it-helpdesk_mysql_data — View volume mount point and details.",
        "docker inspect helpdesk-mysql --format '{{json .Mounts}}' — Verify container volume mount."
    ]
    for c in vol_cmds:
        p_c = doc.add_paragraph(style='List Bullet')
        r = p_c.add_run(c)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_adv = doc.add_paragraph()
    r = p_adv.add_run("20. ADVANTAGES")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    adv_feats = [
        "Automated Delivery: Eliminates manual errors and reduces release overhead via Jenkins CI/CD.",
        "Container Isolation: Docker packages code, dependencies, and servers into standardized environments.",
        "Repeatable Deployment: Ansible ensures uniform, idempotent deployments across any development or staging node.",
        "Data Resilience: Persistent volumes prevent data loss when updating or restarting database containers.",
        "Rich User Experience: Responsive UI with category tags, SLA metrics, and real-time status transitions.",
        "Lightweight Footprint: Alpine base images provide exceptional startup speed with minimal memory usage."
    ]
    for f in adv_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    doc.add_page_break()

    # -------------------------------------------------------------------------
    # PAGE 19: LIMITATIONS, FUTURE ENHANCEMENTS & CONCLUSION
    # -------------------------------------------------------------------------
    p_lim = doc.add_paragraph()
    r = p_lim.add_run("21. LIMITATIONS")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    lim_feats = [
        "Email / SMS Notifications: Real-time SMTP email dispatch and SMS alerting for ticket status changes are not yet configured.",
        "Single-Node Architecture: The CI/CD server and containers run on a local workstation rather than a distributed cloud cluster.",
        "Monitoring Telemetry: Real-time Prometheus metric scraping and Grafana visualization dashboards are not currently incorporated.",
        "OAuth2 / SSO Integration: Single Sign-On via Google or Microsoft Azure AD is not currently implemented."
    ]
    for f in lim_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_fe = doc.add_paragraph()
    r = p_fe.add_run("22. FUTURE ENHANCEMENTS")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    fe_feats = [
        "Notification Microservice: Implement an asynchronous Spring Cloud Stream service for email and Slack alert notifications.",
        "Kubernetes Orchestration: Deploy Helm charts to run multi-node clusters on Amazon EKS or Google Kubernetes Engine.",
        "Monitoring & Observability: Integrate Prometheus, Grafana, and Micrometer for automated cluster telemetry.",
        "Webhook Automation: Configure GitHub webhooks to trigger automatic Jenkins builds upon every pull request push.",
        "Enterprise SSO: Implement OAuth2 / OpenID Connect login with Azure Active Directory integration."
    ]
    for f in fe_feats:
        p_f = doc.add_paragraph(style='List Bullet')
        r = p_f.add_run(f)
        r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_con = doc.add_paragraph()
    r = p_con.add_run("23. CONCLUSION")
    r.bold = True
    r.font.size = Pt(12)
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_c1 = doc.add_paragraph()
    r = p_c1.add_run(
        "The IT Helpdesk DevOps Laboratory project demonstrates a comprehensive implementation of modern web engineering "
        "united with industrial DevOps practices. The application provides an engaging, high-performance service desk interface "
        "featuring SLA tracking, dynamic categorization, role-based workflows, and automated ticket progression."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    p_c2 = doc.add_paragraph()
    r = p_c2.add_run(
        "Throughout the project, each phase of the DevOps lifecycle was systematically realized: Git and GitHub provided robust "
        "source code control; Jenkins orchestrated an automated CI/CD pipeline comprising automated testing, image construction, and "
        "container deployment; Docker packaged the application into ultra-lightweight, isolated containers; Ansible eliminated manual "
        "configuration through automated playbook execution; and Docker Volumes secured data durability across container recreations. "
        "The seamless integration of GitHub → Jenkins → Maven → Docker → Ansible → Docker Volume conclusively validates the principles "
        "of Continuous Integration, Continuous Deployment, and Infrastructure Automation taught in 23IT723 - DevOps Laboratory."
    )
    r.font.color.rgb = RGBColor(0x00, 0x00, 0x00)

    doc.save(output_path)
    print(f"Successfully generated Revised DOCX report at: {output_path}")

if __name__ == '__main__':
    figures_dir = r"C:\DevopsCat\IT-Helpdesk\docs\final-report\figures"
    docx_out = r"C:\DevopsCat\IT-Helpdesk\docs\final-report\23IT723_Final_Project_Report_IT_Helpdesk_Revised.docx"
    create_docx_report(docx_out, figures_dir)
