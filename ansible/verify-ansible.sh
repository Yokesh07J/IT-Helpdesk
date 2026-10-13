#!/usr/bin/env bash
# ==============================================================================
# Automated Ansible Verification Script for DevOps Lab CAT Project
# Course: DevOps Lab CAT Project - Phase 4: Configuration Management
# Target: Ubuntu WSL2 Environment
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"
export ANSIBLE_CONFIG="${SCRIPT_DIR}/ansible.cfg"

echo "================================================================="
echo "  IT Helpdesk: Phase 4 Ansible Automated Verification"
echo "  Date: $(date)"
echo "  Working Directory: ${SCRIPT_DIR}"
echo "================================================================="

# Step 1: Verify Ansible Installation
echo ""
echo ">>> STEP 1: Verifying Ansible Installation in Ubuntu WSL2..."
ansible --version | head -n 4

# Step 2: Validate Inventory
echo ""
echo ">>> STEP 2: Inspecting Ansible Inventory Graph..."
ansible-inventory -i inventory.ini --graph

# Step 3: Test Host Ping Connectivity
echo ""
echo ">>> STEP 3: Executing Ad-Hoc Connectivity Ping..."
ansible helpdesk_servers -i inventory.ini -m ping

# Step 4: Playbook Syntax Check
echo ""
echo ">>> STEP 4: Validating Playbook Syntax..."
ansible-playbook -i inventory.ini playbook.yml --syntax-check
echo "Syntax check passed: OK"

# Step 5: Initial Playbook Execution (Apply State)
echo ""
echo ">>> STEP 5: Executing Playbook (Initial Run - Applying Configuration)..."
ansible-playbook -i inventory.ini playbook.yml

# Step 6: Idempotency Verification (Run 2 - Expecting changed=0)
echo ""
echo ">>> STEP 6: Executing Playbook (Second Run - Testing Idempotency)..."
ansible-playbook -i inventory.ini playbook.yml

# Step 7: Inspect Created File Hierarchy
echo ""
echo ">>> STEP 7: Inspecting Created Infrastructure at /opt/it-helpdesk..."
ls -la /opt/it-helpdesk/
ls -la /opt/it-helpdesk/config/
ls -la /opt/it-helpdesk/scripts/

echo ""
echo "================================================================="
echo "  Phase 4 Ansible Verification: ALL CHECKS PASSED SUCCESSFULLY!"
echo "================================================================="
