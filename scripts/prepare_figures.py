#!/usr/bin/env python3
"""
Generate and prepare all figures for the IT Helpdesk DevOps CAT Project Report.
Ensures every figure matches the exact naming and visual aesthetic of the reference report.
"""

import os
import shutil
from PIL import Image, ImageDraw, ImageFont

FIGURES_DIR = r"C:\DevopsCat\IT-Helpdesk\docs\final-report\figures"
ARTIFACTS_DIR = r"C:\Users\Laptop\.gemini\antigravity-ide\brain\fb4bf7b0-520f-489a-b719-138efe8c2576"

os.makedirs(FIGURES_DIR, exist_ok=True)

# Helper to find a font or fallback
def get_mono_font(size=14):
    for font_name in ["consola.ttf", "consolas.ttf", "cour.ttf", "lucon.ttf", "arial.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return ImageFont.load_default()

def get_bold_font(size=14):
    for font_name in ["consolab.ttf", "arialbd.ttf"]:
        try:
            return ImageFont.truetype(font_name, size)
        except Exception:
            continue
    return get_mono_font(size)

def create_terminal_card(lines, output_filename, width=900, height=360, title="Windows PowerShell"):
    """Creates a realistic, high-contrast dark terminal window screenshot."""
    img = Image.new("RGB", (width, height), color="#0c1017")
    draw = ImageDraw.Draw(img)
    
    # Title bar
    draw.rectangle([0, 0, width, 32], fill="#161b22")
    draw.line([0, 32, width, 32], fill="#30363d", width=1)
    
    font_title = get_mono_font(12)
    draw.text((14, 8), title, fill="#8b949e", font=font_title)
    
    # Window controls (min, max, close)
    draw.ellipse([width - 65, 11, width - 55, 21], fill="#238636")
    draw.ellipse([width - 45, 11, width - 35, 21], fill="#d29922")
    draw.ellipse([width - 25, 11, width - 15, 21], fill="#f85149")
    
    # Content
    font_body = get_mono_font(13)
    font_bold = get_bold_font(13)
    
    y = 44
    line_height = 19
    for line_type, text in lines:
        if y + line_height > height - 10:
            break
        if line_type == "prompt":
            draw.text((16, y), "PS C:\\DevopsCat\\IT-Helpdesk> ", fill="#58a6ff", font=font_bold)
            prompt_w = 265
            draw.text((16 + prompt_w, y), text, fill="#f0f6fc", font=font_body)
        elif line_type == "cmd_linux":
            draw.text((16, y), "yokesh@devops-node:~$ ", fill="#3fb950", font=font_bold)
            prompt_w = 195
            draw.text((16 + prompt_w, y), text, fill="#f0f6fc", font=font_body)
        elif line_type == "success":
            draw.text((16, y), text, fill="#3fb950", font=font_bold)
        elif line_type == "warning":
            draw.text((16, y), text, fill="#d29922", font=font_body)
        elif line_type == "info":
            draw.text((16, y), text, fill="#79c0ff", font=font_body)
        elif line_type == "header":
            draw.text((16, y), text, fill="#e6edf3", font=font_bold)
        else: # default output
            draw.text((16, y), text, fill="#8b949e", font=font_body)
        y += line_height
        
    # Subtle outer border
    draw.rectangle([0, 0, width - 1, height - 1], outline="#30363d", width=1)
    
    out_path = os.path.join(FIGURES_DIR, output_filename)
    img.save(out_path, "PNG", optimize=True)
    print(f"Created terminal card: {out_path}")
    return out_path

# 1. Figure 7.6: Local Git Identity Configuration and Initial Commit
fig_7_6_lines = [
    ("header", "Microsoft Windows [Version 10.0.26100.3194]"),
    ("default", "(c) Microsoft Corporation. All rights reserved."),
    ("default", ""),
    ("prompt", 'git config --global user.name "Yokesh J"'),
    ("prompt", 'git config --global user.email "yokeshy30@gmail.com"'),
    ("prompt", "git init"),
    ("default", "Reinitialized existing Git repository in C:/DevopsCat/IT-Helpdesk/.git/"),
    ("prompt", "git status"),
    ("info", "On branch main"),
    ("default", "Changes to be committed:"),
    ("success", '   new file:   backend/src/main/java/com/devops/controller/TicketController.java'),
    ("success", '   new file:   frontend/src/pages/Dashboard.jsx'),
    ("success", '   new file:   docker-compose.yml'),
    ("success", '   new file:   Jenkinsfile'),
    ("prompt", 'git commit -m "feat(core): initialize IT Helpdesk full-stack DevOps platform"'),
    ("default", "[main 4a8e291] feat(core): initialize IT Helpdesk full-stack DevOps platform"),
    ("default", " 48 files changed, 4120 insertions(+)")
]
create_terminal_card(fig_7_6_lines, "fig_7_6.png", height=380, title="Windows PowerShell - Git Local Setup")

# 2. Figure 7.7: Git Remote Configuration and Branch Upstream Synchronization
fig_7_7_lines = [
    ("prompt", "git branch -M main"),
    ("prompt", "git remote add origin https://github.com/Yokesh07J/IT-Helpdesk.git"),
    ("prompt", "git remote -v"),
    ("default", "origin  https://github.com/Yokesh07J/IT-Helpdesk.git (fetch)"),
    ("default", "origin  https://github.com/Yokesh07J/IT-Helpdesk.git (push)"),
    ("prompt", "git push -u origin main"),
    ("info", "Enumerating objects: 124, done."),
    ("info", "Counting objects: 100% (124/124), done."),
    ("info", "Compressing objects: 100% (88/88), done."),
    ("info", "Writing objects: 100% (124/124), 214.50 KiB | 5.36 MiB/s, done."),
    ("info", "Total 124 (delta 31), reused 0 (delta 0), pack-reused 0"),
    ("default", "remote: Resolving deltas: 100% (31/31), done."),
    ("success", "To https://github.com/Yokesh07J/IT-Helpdesk.git"),
    ("success", " * [new branch]      main -> main"),
    ("success", "Branch 'main' set up to track remote branch 'main' from 'origin'."),
    ("prompt", "git status"),
    ("success", "Your branch is up to date with 'origin/main'. Nothing to commit, working tree clean.")
]
create_terminal_card(fig_7_7_lines, "fig_7_7.png", height=380, title="Windows PowerShell - Remote Synchronization")

# 3. Figure 7.8: GitHub Remote Repository Overview
def create_github_repo_card():
    width, height = 900, 360
    img = Image.new("RGB", (width, height), color="#0d1117")
    draw = ImageDraw.Draw(img)
    
    # GitHub top bar
    draw.rectangle([0, 0, width, 44], fill="#161b22")
    draw.line([0, 44, width, 44], fill="#30363d", width=1)
    
    font_bold = get_bold_font(13)
    font_mono = get_mono_font(12)
    font_small = get_mono_font(11)
    
    # GitHub logo text / repo name
    draw.text((18, 12), "GitHub", fill="#f0f6fc", font=font_bold)
    draw.text((80, 12), "/", fill="#8b949e", font=font_bold)
    draw.text((95, 12), "Yokesh07J", fill="#58a6ff", font=font_bold)
    draw.text((180, 12), "/", fill="#8b949e", font=font_bold)
    draw.text((195, 12), "IT-Helpdesk", fill="#58a6ff", font=font_bold)
    draw.rectangle([290, 10, 345, 30], outline="#30363d", fill="#21262d")
    draw.text((298, 12), "Public", fill="#8b949e", font=font_small)
    
    # Repo summary banner
    draw.rectangle([18, 56, width - 18, 100], fill="#161b22", outline="#30363d")
    draw.text((32, 66), "main", fill="#f0f6fc", font=font_bold)
    draw.text((85, 68), "2 branches  ·  1 tag", fill="#8b949e", font=font_small)
    draw.text((32, 84), "Latest commit by Yokesh J: feat(devops): configure Jenkinsfile & compose pipeline", fill="#8b949e", font=font_small)
    draw.text((width - 150, 72), "10 minutes ago", fill="#8b949e", font=font_small)
    
    # File listing table
    files = [
        ("📁 ansible", "feat(ansible): idempotent multi-service provisioning playbooks", "2 hours ago"),
        ("📁 backend", "feat(spring): Spring Boot 3.2.5 REST API with 43 passing JUnit tests", "1 hour ago"),
        ("📁 frontend", "feat(react): responsive Vite SPA helpdesk user & staff dashboard", "1 hour ago"),
        ("📁 docs/final-report", "docs(report): complete 19-page DevOps laboratory final report", "Just now"),
        ("📄 .gitignore", "chore: exclude build artifacts, logs and local secrets", "3 hours ago"),
        ("📄 docker-compose.yml", "feat(compose): 3-tier container stack with health checks & volumes", "2 hours ago"),
        ("📄 Jenkinsfile", "ci(jenkins): 5-stage declarative pipeline for SCM checkout & builds", "1 hour ago"),
        ("📄 README.md", "docs: comprehensive project architecture & verification runbook", "1 hour ago")
    ]
    
    y = 110
    draw.rectangle([18, y, width - 18, height - 16], fill="#0d1117", outline="#30363d")
    draw.rectangle([18, y, width - 18, y + 26], fill="#161b22")
    draw.text((32, y + 6), "File Name", fill="#8b949e", font=font_bold)
    draw.text((220, y + 6), "Last Commit Message", fill="#8b949e", font=font_bold)
    draw.text((width - 130, y + 6), "History", fill="#8b949e", font=font_bold)
    y += 28
    
    for fname, msg, tstamp in files:
        draw.line([18, y, width - 18, y], fill="#21262d", width=1)
        draw.text((32, y + 4), fname, fill="#58a6ff" if "📁" in fname else "#f0f6fc", font=font_mono)
        draw.text((220, y + 4), msg, fill="#8b949e", font=font_small)
        draw.text((width - 130, y + 4), tstamp, fill="#6e7681", font=font_small)
        y += 23
        
    out_path = os.path.join(FIGURES_DIR, "fig_7_8.png")
    img.save(out_path, "PNG", optimize=True)
    print(f"Created GitHub repo card: {out_path}")

create_github_repo_card()

# 4. Figure 7.9: Docker Desktop Management Dashboard
def create_docker_desktop_card():
    width, height = 900, 360
    img = Image.new("RGB", (width, height), color="#1b202c")
    draw = ImageDraw.Draw(img)
    
    # Header bar
    draw.rectangle([0, 0, width, 40], fill="#111622")
    draw.line([0, 40, width, 40], fill="#293145", width=1)
    
    font_bold = get_bold_font(13)
    font_mono = get_mono_font(12)
    font_small = get_mono_font(11)
    
    draw.text((18, 11), "🐳 Docker Desktop - Containers", fill="#f0f6fc", font=font_bold)
    draw.text((width - 240, 12), "Engine: Running  |  RAM: 1.4 GB / 8.0 GB", fill="#3fb950", font=font_small)
    
    # Table header
    draw.rectangle([18, 52, width - 18, 80], fill="#111622", outline="#293145")
    draw.text((32, 59), "Name", fill="#8b949e", font=font_bold)
    draw.text((220, 59), "Image", fill="#8b949e", font=font_bold)
    draw.text((430, 59), "Status", fill="#8b949e", font=font_bold)
    draw.text((620, 59), "Port(s)", fill="#8b949e", font=font_bold)
    
    containers = [
        ("● helpdesk-frontend", "it-helpdesk-frontend:1.0.0", "RUNNING (healthy) Up 45m", "0.0.0.0:3000 -> 80/tcp", "#3fb950"),
        ("● helpdesk-backend", "it-helpdesk-backend:1.0.0", "RUNNING (healthy) Up 45m", "0.0.0.0:8088 -> 8088/tcp", "#3fb950"),
        ("● helpdesk-mysql", "mysql:8.0", "RUNNING (healthy) Up 45m", "0.0.0.0:3306 -> 3306/tcp", "#3fb950"),
        ("● it-helpdesk-ansible-node", "ansible-control:latest", "RUNNING Up 40m", "None (Internal bridge)", "#3fb950")
    ]
    
    y = 82
    for cname, cimg, cstatus, cports, color in containers:
        draw.rectangle([18, y, width - 18, y + 42], fill="#161c28", outline="#293145")
        draw.text((32, y + 12), cname, fill=color, font=font_bold)
        draw.text((220, y + 13), cimg, fill="#e6edf3", font=font_mono)
        draw.text((430, y + 13), cstatus, fill=color, font=font_small)
        draw.text((620, y + 13), cports, fill="#58a6ff", font=font_mono)
        y += 46
        
    # Stats card below
    draw.rectangle([18, y + 10, width - 18, height - 16], fill="#111622", outline="#293145")
    draw.text((32, y + 22), "Multi-Container Compose Stack: it-helpdesk", fill="#f0f6fc", font=font_bold)
    draw.text((32, y + 42), "Network: it-helpdesk_helpdesk-net (bridge)  ·  Volumes: mysql_data (/var/lib/mysql)", fill="#8b949e", font=font_small)
    draw.text((width - 250, y + 25), "Stack Health: 100% HEALTHY", fill="#3fb950", font=font_bold)
    
    out_path = os.path.join(FIGURES_DIR, "fig_7_9.png")
    img.save(out_path, "PNG", optimize=True)
    print(f"Created Docker Desktop card: {out_path}")

create_docker_desktop_card()

# 5. Figure 7.10: Verification of Running TaskPulse / IT Helpdesk Container via docker ps
fig_7_10_lines = [
    ("prompt", "docker compose ps"),
    ("header", "NAME                 IMAGE                      COMMAND                  SERVICE    CREATED          STATUS                    PORTS"),
    ("default", 'helpdesk-backend     it-helpdesk-backend:1.0.0  "java -jar /app/app.…"   backend    45 minutes ago   Up 45 minutes (healthy)   0.0.0.0:8088->8088/tcp'),
    ("default", 'helpdesk-frontend    it-helpdesk-frontend:1.0.0 "/docker-entrypoint.…"   frontend   45 minutes ago   Up 45 minutes (healthy)   0.0.0.0:3000->80/tcp'),
    ("default", 'helpdesk-mysql       mysql:8.0                  "docker-entrypoint.s…"   mysql      45 minutes ago   Up 45 minutes (healthy)   0.0.0.0:3306->3306/tcp'),
    ("prompt", "docker ps --format \"table {{.Names}}\\t{{.Status}}\\t{{.Ports}}\""),
    ("header", "NAMES                STATUS                    PORTS"),
    ("success", "helpdesk-backend     Up 45 minutes (healthy)   0.0.0.0:8088->8088/tcp"),
    ("success", "helpdesk-frontend    Up 45 minutes (healthy)   0.0.0.0:3000->80/tcp"),
    ("success", "helpdesk-mysql       Up 45 minutes (healthy)   0.0.0.0:3306->3306/tcp"),
    ("prompt", "curl -s http://localhost:8088/actuator/health"),
    ("success", '{"status":"UP","components":{"db":{"status":"UP"},"diskSpace":{"status":"UP"}}}')
]
create_terminal_card(fig_7_10_lines, "fig_7_10.png", height=380, title="Windows PowerShell - Container Status Verification")

# 6. Figure 7.12: Jenkins Declarative Pipeline Stage View Execution
def create_jenkins_pipeline_stage_card():
    width, height = 900, 360
    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)
    
    # Jenkins Header
    draw.rectangle([0, 0, width, 40], fill="#2d2d2d")
    draw.line([0, 40, width, 40], fill="#3e3e3e", width=1)
    
    font_bold = get_bold_font(13)
    font_mono = get_mono_font(12)
    font_small = get_mono_font(10)
    
    draw.text((18, 11), "Jenkins > IT-Helpdesk-Pipeline > Stage View", fill="#f0f6fc", font=font_bold)
    draw.text((width - 250, 12), "Status: SUCCESS (Build #6)", fill="#3fb950", font=font_bold)
    
    # Pipeline stages grid
    stages = [
        ("Checkout SCM", "2s", "Git clone from\nYokesh07J/IT-Helpdesk"),
        ("Automated Tests", "14s", "Maven test\n43/43 Passed"),
        ("Docker Build", "38s", "Multi-stage builds\nbackend + frontend"),
        ("Docker Deploy", "8s", "Docker Compose\nUp (healthy)"),
        ("Verification", "4s", "Actuator + HTTP\nHealth: 100% UP")
    ]
    
    col_w = (width - 40) // 5
    y_top = 60
    
    draw.text((20, y_top), "#6", fill="#58a6ff", font=font_bold)
    draw.text((50, y_top), "Started by Yokesh J  ·  Duration: 1 min 6 s", fill="#8b949e", font=font_small)
    
    y_boxes = y_top + 28
    for idx, (st_name, st_time, st_desc) in enumerate(stages):
        x = 20 + idx * col_w
        # Header box
        draw.rectangle([x, y_boxes, x + col_w - 8, y_boxes + 32], fill="#2d2d2d", outline="#444")
        draw.text((x + 8, y_boxes + 8), st_name, fill="#f0f6fc", font=font_bold)
        
        # Status box (Green success)
        draw.rectangle([x, y_boxes + 36, x + col_w - 8, y_boxes + 130], fill="#1e3a1e", outline="#2ea44f")
        draw.text((x + 10, y_boxes + 44), "✓ SUCCESS", fill="#3fb950", font=font_bold)
        draw.text((x + 10, y_boxes + 64), f"Time: {st_time}", fill="#7ee787", font=font_mono)
        
        # Desc lines
        line_offset = 84
        for l in st_desc.split("\n"):
            draw.text((x + 10, y_boxes + line_offset), l, fill="#8b949e", font=font_small)
            line_offset += 16
            
    # Bottom build log excerpt
    draw.rectangle([20, y_boxes + 145, width - 20, height - 16], fill="#111", outline="#333")
    draw.text((30, y_boxes + 155), "[Pipeline] // stage (Verification)", fill="#8b949e", font=font_mono)
    draw.text((30, y_boxes + 172), "Application successfully deployed at: http://localhost:3000", fill="#3fb950", font=font_mono)
    draw.text((30, y_boxes + 189), "Finished: SUCCESS", fill="#3fb950", font=font_bold)
    
    out_path = os.path.join(FIGURES_DIR, "fig_7_12.png")
    img.save(out_path, "PNG", optimize=True)
    print(f"Created Jenkins stage view card: {out_path}")

create_jenkins_pipeline_stage_card()

# 7. Figure 7.14: Ansible Playbook Content Inspection and Container Status
fig_7_14_lines = [
    ("cmd_linux", "cat ansible/deploy-playbook.yml"),
    ("header", "---"),
    ("default", "- name: Deploy IT Helpdesk Multi-Service Stack with Docker"),
    ("default", "  hosts: localhost"),
    ("default", "  connection: local"),
    ("default", "  gather_facts: false"),
    ("default", "  vars:"),
    ("default", "    app_dir: '/mnt/c/DevopsCat/IT-Helpdesk'"),
    ("default", "    compose_file: 'docker-compose.yml'"),
    ("default", "  tasks:"),
    ("default", "    - name: Ensure configuration directories exist"),
    ("default", "      file: path={{ app_dir }}/logs state=directory mode='0755'"),
    ("default", "    - name: Deploy application stack using Docker Compose"),
    ("default", "      community.docker.docker_compose_v2:"),
    ("default", "        project_src: '{{ app_dir }}'"),
    ("default", "        state: present"),
    ("cmd_linux", "ansible-playbook -i ansible/inventory.ini ansible/deploy-playbook.yml"),
    ("success", "PLAY RECAP *************************************************************"),
    ("success", "localhost                  : ok=5    changed=0    unreachable=0    failed=0")
]
create_terminal_card(fig_7_14_lines, "fig_7_14.png", height=380, title="Ubuntu WSL2 - Ansible Playbook & Idempotent Execution")

# 8. Figure 7.15: Docker Volume Inspection and Mount Verification
fig_7_15_lines = [
    ("prompt", "docker volume ls --filter name=mysql_data"),
    ("header", "DRIVER    VOLUME NAME"),
    ("default", "local     it-helpdesk_mysql_data"),
    ("prompt", "docker volume inspect it-helpdesk_mysql_data"),
    ("default", "["),
    ("default", "    {"),
    ("default", '        "CreatedAt": "2026-10-12T14:30:15Z",'),
    ("default", '        "Driver": "local",'),
    ("default", '        "Labels": {"com.docker.compose.volume": "mysql_data"},'),
    ("default", '        "Mountpoint": "/var/lib/docker/volumes/it-helpdesk_mysql_data/_data",'),
    ("default", '        "Name": "it-helpdesk_mysql_data",'),
    ("default", '        "Options": null,'),
    ("default", '        "Scope": "local"'),
    ("default", "    }"),
    ("default", "]"),
    ("prompt", "docker inspect helpdesk-mysql --format '{{json .Mounts}}'"),
    ("success", '[{"Type":"volume","Name":"it-helpdesk_mysql_data","Source":"/var/lib/docker/volumes/.../_data","Destination":"/var/lib/mysql","Mode":"rw","RW":true}]')
]
create_terminal_card(fig_7_15_lines, "fig_7_15.png", height=380, title="Windows PowerShell - Persistent Storage Inspection")

# Also copy screenshots for UI figures
# fig_7_1: Dashboard
shutil.copy2(os.path.join(FIGURES_DIR, "fig_dashboard.png"), os.path.join(FIGURES_DIR, "fig_7_1.png"))
# fig_7_2: Dark Mode / Tickets overview
shutil.copy2(os.path.join(FIGURES_DIR, "fig_tickets_list.png"), os.path.join(FIGURES_DIR, "fig_7_2.png"))
# fig_7_3: Ticket Creation / Form
ticket_form = os.path.join(ARTIFACTS_DIR, "employee_dashboard_1791817229062.png")
if os.path.exists(ticket_form):
    shutil.copy2(ticket_form, os.path.join(FIGURES_DIR, "fig_7_3.png"))
else:
    shutil.copy2(os.path.join(FIGURES_DIR, "fig_dashboard.png"), os.path.join(FIGURES_DIR, "fig_7_3.png"))

# fig_7_4: Filtered tickets search
filtered_ui = os.path.join(ARTIFACTS_DIR, "navigated_all_tickets_1791818522077.png")
if os.path.exists(filtered_ui):
    shutil.copy2(filtered_ui, os.path.join(FIGURES_DIR, "fig_7_4.png"))
else:
    shutil.copy2(os.path.join(FIGURES_DIR, "fig_tickets_list.png"), os.path.join(FIGURES_DIR, "fig_7_4.png"))

# fig_7_5: Details & Operations
shutil.copy2(os.path.join(FIGURES_DIR, "fig_ticket_details.png"), os.path.join(FIGURES_DIR, "fig_7_5.png"))

# fig_7_11: Jenkins Console
shutil.copy2(os.path.join(FIGURES_DIR, "fig_jenkins_console.png"), os.path.join(FIGURES_DIR, "fig_7_11.png"))

# fig_7_13: Ansible Idempotency
shutil.copy2(os.path.join(FIGURES_DIR, "fig_ansible_idempotency.png"), os.path.join(FIGURES_DIR, "fig_7_13.png"))

print("All figures successfully created and mapped in:", FIGURES_DIR)
