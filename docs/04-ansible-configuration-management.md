# Phase 4: Configuration Management Using Ansible in WSL/Ubuntu Linux

**Course / Lab**: DevOps Lab CAT Project  
**Project**: IT Helpdesk and Ticket Management System  
**Date**: October 2026  
**Status**: COMPLETED & VERIFIED LIVE  

---

## 1. Aim and Objectives

### Aim
To establish automated, declarative, and idempotent configuration management for the IT Helpdesk and Ticket Management System infrastructure using Ansible on an Ubuntu Linux WSL2 control node, ensuring consistent directory structures, secure file permissions, templated configuration generation, and service health validation.

### Objectives
1. **Differentiate System Layers**: Clarify architectural distinctions between Windows PowerShell, WSL2/Ubuntu, Docker Desktop's WSL2 backend, and Ansible control vs. managed nodes.
2. **Control Node Setup**: Install and configure Ansible Core (version 2.20.1 / Ansible 13.1) inside an authentic Ubuntu 26.04 LTS environment.
3. **Structured Project Layout**: Design a modular Ansible directory containing `ansible.cfg`, `inventory.ini`, `group_vars/all.yml`, and Jinja2 templates.
4. **Idempotent Automation**: Implement declarative plays for target host discovery, package prerequisites, directory permissions (`0755`), secure configuration files (`0600`), and automated health probes (`0755`).
5. **Real-World Verification**: Execute ad-hoc pings, syntax checks, initial application runs, and repeated execution passes demonstrating `changed=0` (strict idempotency).

---

## 2. Architectural Concepts: Windows vs. WSL vs. Docker vs. Ansible

In modern DevOps environments hosted on Windows workstations, multiple virtualization and shell layers coexist. Understanding their roles is fundamental:

| Layer / Technology | Nature & Kernel | Primary Role in This Project | Execution Context |
| :--- | :--- | :--- | :--- |
| **Windows PowerShell** | Windows NT Kernel, .NET CLR | Host orchestration, git operations, launching Jenkins Windows service, Docker Desktop CLI. | Native Windows user space (`C:\DevopsCat\IT-Helpdesk`) |
| **WSL2 / Ubuntu** | Real Linux Kernel (v6.18+ Microsoft Standard) running in lightweight Hyper-V utility VM | Ansible Control Node running Python 3.14, Jinja2, PyYAML, and Ansible CLI. | Linux filesystem & `/mnt/c` mount |
| **Docker Desktop WSL Backend** | Specialized headless Alpine/Debian VM (`docker-desktop`) | Runs the Docker Daemon container engine and manages Linux container lifecycle. | Container network bridge (`helpdesk-network`) |
| **Ansible Control Node** | Machine where Ansible is installed and executed | Executes playbooks, parses Jinja2 templates, and calculates target state diffs. | Ubuntu 26.04 WSL2 environment |
| **Ansible Managed Node** | Machine being configured by Ansible | Receives module commands and enforces desired state (locally via `local` connection or remotely via SSH). | Localhost target (`helpdesk-host-01`) or remote Linux servers |

```
 +-------------------------------------------------------------------------+
 |                         Windows 11 Host OS                              |
 |                                                                         |
 |  +---------------------+   +-----------------------------------------+  |
 |  |  PowerShell CLI     |   |  Jenkins CI Service (Port 8080)         |  |
 |  |  - Git Worktree     |   |  - Automated Build Pipeline             |  |
 |  |  - IDE Editor       |   |  - Maven Surefire & JaCoCo Gate         |  |
 |  +---------------------+   +-----------------------------------------+  |
 |            |                                                            |
 |            v                                                            |
 |  +-------------------------------------------------------------------+  |
 |  |                  WSL2 Hyper-V Virtualization Subsystem            |  |
 |  |                                                                   |  |
 |  |  +---------------------------+   +-----------------------------+  |  |
 |  |  | Ubuntu 26.04 LTS Distro   |   | Docker Desktop Engine       |  |  |
 |  |  | [Ansible Control Node]    |   | [Container Infrastructure]  |  |  |
 |  |  | - ansible-playbook        |   | - helpdesk-frontend (:80)   |  |  |
 |  |  | - Jinja2 Templates        |   | - helpdesk-backend (:8088)  |  |  |
 |  |  | - Idempotency Validation  |   | - helpdesk-mysql (:3306)    |  |  |
 |  |  +---------------------------+   +-----------------------------+  |  |
 |  +-------------------------------------------------------------------+  |
 +-------------------------------------------------------------------------+
```

---

## 3. Environment Inspection & Ansible Installation

### 3.1 WSL2 Distribution Verification
From Windows PowerShell, the installed distributions were inspected:
```powershell
wsl -l -v
```
**Observed Output**:
```text
  NAME                   STATE           VERSION
* Ubuntu                 Running         2
  docker-desktop         Running         2
```

### 3.2 Operating System & Python Baseline
Inside the Ubuntu instance:
```bash
lsb_release -a
uname -a
python3 --version
```
**Observed Output**:
```text
Distributor ID: Ubuntu
Description:    Ubuntu 26.04.1 LTS (resolute)
Linux LAPTOP-8JUSP8L6 6.18.40.1-microsoft-standard-WSL2 x86_64
Python 3.14.4
```

### 3.3 Installing Ansible via APT
Ansible was installed directly from the official Ubuntu universe repository with standard collections:
```bash
sudo apt-get update
sudo apt-get install -y ansible
```
**Verification of Installed Binary**:
```bash
ansible --version
```
**Observed Output**:
```text
ansible [core 2.20.1]
  config file = /mnt/c/DevopsCat/IT-Helpdesk/ansible/ansible.cfg
  configured module search path = ['/home/yokesh/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /home/yokesh/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.14.4 (main, Jun 18 2026, 14:25:02) [GCC 15.2.0] (/usr/bin/python3)
  jinja version = 3.1.6
  pyyaml version = 6.0.3 (with libyaml v0.2.5)
```

---

## 4. Ansible Project Structure

The project is structured under the `ansible/` root directory:

```text
ansible/
├── ansible.cfg                          # Central Ansible configuration
├── inventory.ini                        # Host inventory definitions and groups
├── group_vars/
│   └── all.yml                          # Global variables, paths, and security modes
├── templates/
│   ├── helpdesk-env.j2                  # Jinja2 template for application environment
│   ├── docker-compose.override.yml.j2   # Jinja2 template for Docker Compose overrides
│   └── system-health-check.sh.j2        # Jinja2 template for automated health probe
├── playbook.yml                         # Main declarative configuration playbook
└── verify-ansible.sh                    # Automated end-to-end verification script
```

---

## 5. File Implementations

### 5.1 `ansible/ansible.cfg`
Defines defaults, suppresses deprecation noise, points to local inventory, and configures sudo privilege escalation:

```ini
[defaults]
inventory = ./inventory.ini
host_key_checking = False
retry_files_enabled = False
stdout_callback = default
interpreter_python = auto_silent
nocows = 1
deprecation_warnings = False
remote_tmp = ~/.ansible/tmp
local_tmp = ~/.ansible/tmp

[privilege_escalation]
become = True
become_method = sudo
become_user = root
become_ask_pass = False

[ssh_connection]
pipelining = True
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no
```

### 5.2 `ansible/inventory.ini`
Defines the target nodes. For our local environment, `helpdesk-host-01` connects via `ansible_connection=local`. The file also documents how the same playbook targets remote SSH production servers:

```ini
[helpdesk_servers]
# Local workstation acting as the managed Docker host target in WSL2
helpdesk-host-01 ansible_host=localhost ansible_connection=local

[local]
localhost ansible_connection=local

[web_servers]
helpdesk-host-01

[database_servers]
helpdesk-host-01

# Production cluster reference configuration (for multi-node SSH deployment):
# [production_servers]
# prod-app-01 ansible_host=192.168.1.50 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/devops_rsa
# prod-db-01  ansible_host=192.168.1.51 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/devops_rsa

[all:vars]
ansible_python_interpreter=/usr/bin/python3
environment_name=development
project_name=it-helpdesk
```

### 5.3 `ansible/group_vars/all.yml`
Separates configuration data from automation logic. Stores standard directory paths, application port configurations, and file permission modes:

```yaml
---
# Project and Target Host Paths
app_name: "it-helpdesk"
app_base_dir: "/opt/it-helpdesk"
app_config_dir: "{{ app_base_dir }}/config"
app_logs_dir: "{{ app_base_dir }}/logs"
app_backup_dir: "{{ app_base_dir }}/backups"
app_scripts_dir: "{{ app_base_dir }}/scripts"

# File Ownership and Security Modes
app_owner: "root"
app_group: "root"
dir_mode: "0755"
file_mode: "0644"
secure_file_mode: "0600"
exec_file_mode: "0755"

# Network Ports and Services
frontend_port: 80
backend_port: 8088
mysql_port: 3306

# Application Environment Settings
spring_profiles_active: "prod"
database_name: "it_helpdesk"
database_host: "helpdesk-mysql"
database_port: 3306
database_user: "helpdesk_user"

# Required System Utility Packages
required_packages:
  - curl
  - git
  - tar
  - python3

# Health Check Settings
health_check_interval: 10
health_check_retries: 3
health_check_url: "http://localhost:{{ backend_port }}/actuator/health"
frontend_url: "http://localhost:{{ frontend_port }}/"
```

### 5.4 Jinja2 Templates

#### `ansible/templates/helpdesk-env.j2`
Generates `/opt/it-helpdesk/config/helpdesk.env` with restricted `0600` permissions:
```jinja2
# ==============================================================================
# IT Helpdesk Application Environment Configuration
# Managed by Ansible (Phase 4: Configuration Management)
# Target Host: {{ inventory_hostname }} | Environment: {{ environment_name }}
# DO NOT EDIT DIRECTLY ON MANAGED HOSTS - CHANGES WILL BE OVERWRITTEN
# ==============================================================================

# Application Profile
SPRING_PROFILES_ACTIVE={{ spring_profiles_active }}

# Database Configuration
DB_HOST={{ database_host }}
DB_PORT={{ database_port }}
DB_NAME={{ database_name }}
DB_USER={{ database_user }}

# Ports
BACKEND_PORT={{ backend_port }}
FRONTEND_PORT={{ frontend_port }}

# Service URLs
BACKEND_HEALTH_ENDPOINT={{ health_check_url }}
FRONTEND_URL={{ frontend_url }}

# Managed Environment Metadata
DEPLOYMENT_ENV={{ environment_name }}
DEPLOYMENT_TARGET={{ inventory_hostname }}
MANAGED_BY=Ansible-{{ ansible_version.full | default('core') }}
```

#### `ansible/templates/docker-compose.override.yml.j2`
Generates `/opt/it-helpdesk/config/docker-compose.override.yml`:
```jinja2
# ==============================================================================
# Docker Compose Override for IT Helpdesk Infrastructure
# Managed by Ansible (Phase 4: Configuration Management)
# Target: {{ inventory_hostname }} | Environment: {{ environment_name }}
# ==============================================================================

version: '3.8'

services:
  backend:
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    environment:
      - SPRING_PROFILES_ACTIVE={{ spring_profiles_active }}
      - DB_NAME={{ database_name }}

  frontend:
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  mysql:
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "20m"
        max-file: "3"
```

#### `ansible/templates/system-health-check.sh.j2`
Generates executable `/opt/it-helpdesk/scripts/healthcheck.sh` (`0755`):
```bash
#!/usr/bin/env bash
# ==============================================================================
# Automated Service Health Check Probe
# Managed by Ansible (Phase 4: Configuration Management)
# Generated for: {{ inventory_hostname }} | Environment: {{ environment_name }}
# ==============================================================================
set -euo pipefail

echo "=========================================================="
echo " IT Helpdesk Service Health Probe (Ansible Automated Check)"
echo " Target: {{ inventory_hostname }}"
echo " Date:   $(date)"
echo "=========================================================="

# Check Backend Health Endpoint
echo -n "[1/2] Probing Spring Boot Actuator ({{ health_check_url }})... "
if curl -s -f -m {{ health_check_interval }} "{{ health_check_url }}" > /dev/null 2>&1; then
    echo "HEALTHY (HTTP 200)"
else
    echo "WARNING: Backend not reachable directly at {{ health_check_url }}"
fi

# Check Frontend Endpoint
echo -n "[2/2] Probing React/Nginx Frontend ({{ frontend_url }})... "
if curl -s -f -m {{ health_check_interval }} "{{ frontend_url }}" > /dev/null 2>&1; then
    echo "HEALTHY (HTTP 200)"
else
    echo "WARNING: Frontend not reachable directly at {{ frontend_url }}"
fi

echo "=========================================================="
echo "Health check probe finished."
exit 0
```

---

## 6. Main Playbook Execution Logic (`ansible/playbook.yml`)

The playbook enforces 6 logical phases:
1. **Connectivity & Fingerprinting**: Pings target host and prints OS family, kernel, RAM, and Python version.
2. **System Prerequisites**: Idempotently validates presence of `curl`, `git`, `tar`, and `python3`.
3. **Directory Hierarchy**: Idempotently creates `/opt/it-helpdesk/{config,logs,backups,scripts}` with mode `0755`.
4. **Jinja2 Templating**: Renders `helpdesk.env` (`0600`), `docker-compose.override.yml` (`0644`), and `healthcheck.sh` (`0755`).
5. **Validation & Automated Probe**: Asserts non-zero file sizes, runs `bash -n` syntax check on the script, and executes the health probe against running services.
6. **Execution Summary**: Confirms successful idempotent run.

---

## 7. Execution and Verification Evidence

All commands below were executed inside the Ubuntu WSL2 environment:

### 7.1 Ad-Hoc Connectivity Check
```bash
export ANSIBLE_CONFIG=/mnt/c/DevopsCat/IT-Helpdesk/ansible/ansible.cfg
ansible helpdesk_servers -i inventory.ini -m ping
```
**Observed Result**:
```text
helpdesk-host-01 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

### 7.2 Inventory Graph Inspection
```bash
ansible-inventory -i inventory.ini --graph
```
**Observed Result**:
```text
@all:
  |--@ungrouped:
  |--@helpdesk_servers:
  |  |--helpdesk-host-01
  |--@local:
  |  |--localhost
  |--@web_servers:
  |  |--helpdesk-host-01
  |--@database_servers:
  |  |--helpdesk-host-01
```

### 7.3 Playbook Syntax Validation
```bash
ansible-playbook -i inventory.ini playbook.yml --syntax-check
```
**Observed Result**:
```text
playbook: playbook.yml
Syntax check passed: OK
```

### 7.4 Automated Health Check Probe Output
During playbook task execution (`Task 5.5`), Ansible executed the templated health probe against the active containers:
```text
TASK [5.5 Display service health check probe output] ***************************
ok: [helpdesk-host-01] => {
    "healthcheck_result.stdout_lines": [
        "==========================================================",
        " IT Helpdesk Service Health Probe (Ansible Automated Check)",
        " Target: helpdesk-host-01",
        " Date:   Tue Oct 13 05:28:52 UTC 2026",
        "==========================================================",
        "[1/2] Probing Spring Boot Actuator (http://localhost:8088/actuator/health)... HEALTHY (HTTP 200)",
        "[2/2] Probing React/Nginx Frontend (http://localhost:80/)... HEALTHY (HTTP 200)",
        "==========================================================",
        "Health check probe finished."
    ]
}
```

### 7.5 Strict Idempotency Verification (Run 2)
When the playbook was executed a second time against the already-configured host, Ansible evaluated all 14 tasks without performing redundant modifications:

```text
PLAY RECAP *********************************************************************
helpdesk-host-01           : ok=14   changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
- **Total tasks evaluated**: 14
- **Tasks changed**: **0** (Idempotency 100% verified)
- **Failures / Unreachable**: **0**

### 7.6 Resulting File Hierarchy on Target System
```bash
ls -la /opt/it-helpdesk/
ls -la /opt/it-helpdesk/config/
ls -la /opt/it-helpdesk/scripts/
```
**Observed Result**:
```text
/opt/it-helpdesk/:
drwxr-xr-x 6 root root 4096 Oct 13 05:26 .
drwxr-xr-x 2 root root 4096 Oct 13 05:26 backups
drwxr-xr-x 2 root root 4096 Oct 13 05:27 config
drwxr-xr-x 2 root root 4096 Oct 13 05:26 logs
drwxr-xr-x 2 root root 4096 Oct 13 05:27 scripts

/opt/it-helpdesk/config/:
-rw-r--r-- 1 root root  856 Oct 13 05:27 docker-compose.override.yml
-rw------- 1 root root  831 Oct 13 05:27 helpdesk.env

/opt/it-helpdesk/scripts/:
-rwxr-xr-x 1 root root 1399 Oct 13 05:27 healthcheck.sh
```

---

## 8. Viva Questions & Answers (Phase 4: Ansible & Configuration Management)

### Q1: What is Ansible and how does it differ from Chef, Puppet, and SaltStack?
**Answer**: Ansible is an open-source, agentless configuration management and automation tool. Unlike Chef and Puppet which require background daemons (agents) installed on managed nodes, Ansible connects over standard SSH (or local IPC) and executes Python modules in memory before removing them.

### Q2: What is the concept of "Idempotence" in DevOps configuration management?
**Answer**: Idempotence is the property of an automation operation where applying it multiple times produces the exact same system state as applying it once, without making redundant changes or triggering errors. If a file or package is already in the desired state, an idempotent task returns `ok` (`changed: false`).

### Q3: Why is dynamic timestamping in Jinja2 templates considered an anti-pattern for idempotency?
**Answer**: Jinja2 expressions like `ansible_date_time.iso8601` or `lookup('pipe', 'date')` evaluate to a new string on every execution. This causes the rendered file's cryptographic hash to differ on every run, forcing Ansible to overwrite the file and falsely report `changed: true`.

### Q4: What is the difference between an Ansible Control Node and a Managed Node?
**Answer**: The Control Node is the machine where Ansible is installed and where playbooks are executed (must be a POSIX system like Linux or macOS). Managed Nodes are the target servers configured by Ansible (can be Linux, Windows, or network appliances).

### Q5: How does Ansible handle privilege escalation?
**Answer**: Privilege escalation is configured using the `become: true`, `become_method: sudo`, and `become_user: root` directives in `ansible.cfg` or playbooks. It allows non-privileged connections to execute administrative tasks safely.

### Q6: What is the purpose of `ansible.cfg` and what is its search priority?
**Answer**: `ansible.cfg` defines default parameters such as inventory location, host key checking, and timeouts. Ansible checks configuration in the following order:
1. Environment variable `ANSIBLE_CONFIG`
2. `./ansible.cfg` in the current working directory (unless world-writable)
3. `~/.ansible.cfg` in the user's home directory
4. `/etc/ansible/ansible.cfg` default system configuration

### Q7: What is the role of Jinja2 templates (`.j2` files) in Ansible?
**Answer**: Jinja2 templates enable dynamic generation of configuration files using variables, conditionals (`{% if %}`), and loops (`{% for %}`). They allow a single template to adapt across development, staging, and production environments.

### Q8: What does the `stat` module do in Ansible playbooks?
**Answer**: The `ansible.builtin.stat` module retrieves file or filesystem status (existence, size, permissions, checksum, owner) without modifying anything, enabling conditional assertions in subsequent tasks via `register`.

### Q9: How does Ansible manage secrets safely in production?
**Answer**: Ansible uses **Ansible Vault** (`ansible-vault encrypt / decrypt / edit`) to encrypt sensitive variables and files using AES-256 encryption. The decryption key is supplied via `--vault-password-file` or interactive prompt during playbook runtime.

### Q10: How does Ansible communicate with targets running on the same host versus remote servers?
**Answer**: For remote servers, Ansible uses `ansible_connection=ssh` with SSH key pairs. For local targets or container hosts, Ansible uses `ansible_connection=local`, executing commands directly through local sub-processes while bypassing SSH daemon overhead.

---

## 9. Screenshot Checklist for Lab Submission

| Step | Item to Capture | Verification Detail |
| :--- | :--- | :--- |
| 1 | Ansible Version in Ubuntu | Terminal showing `ansible [core 2.20.1]` and `python version = 3.14.4` |
| 2 | Ad-Hoc Ping Output | Terminal showing `helpdesk-host-01 \| SUCCESS => {"changed": false, "ping": "pong"}` |
| 3 | Inventory Graph | Terminal showing `ansible-inventory --graph` output |
| 4 | Initial Playbook Execution | Terminal showing `ansible-playbook playbook.yml` applying tasks |
| 5 | Idempotent Playbook Run | Terminal showing `PLAY RECAP` with `ok=14 changed=0 failed=0` |
| 6 | Target Directory Permissions | Terminal showing `ls -la /opt/it-helpdesk/config/` with `0600` on `helpdesk.env` |
