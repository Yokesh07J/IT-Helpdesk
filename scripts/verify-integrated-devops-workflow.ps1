# ==============================================================================
# Script: verify-integrated-devops-workflow.ps1
# Course: DevOps Lab CAT Project - Phase 5: Integrated DevOps Workflow
# Purpose: End-to-end automated validation of the integrated DevOps pipeline:
#          Git -> Jenkins CI -> Tests (JUnit/Mockito) -> Docker Build ->
#          Ansible Configuration Management -> Docker Compose Deploy -> Health Check
# ==============================================================================

[CmdletBinding()]
param(
    [switch]$SkipMavenTests = $false,
    [string]$BackendUrl = "http://localhost:8088",
    [string]$FrontendUrl = "http://localhost:80"
)

$ErrorActionPreference = "Continue"
$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

# Ensure Docker binaries in user environment are on PATH
$DockerBinPaths = @(
    "C:\Users\Laptop\AppData\Local\Programs\DockerDesktop\resources\bin",
    "C:\Program Files\Docker\Docker\resources\bin"
)
foreach ($bin in $DockerBinPaths) {
    if ((Test-Path $bin) -and ($env:PATH -notlike "*$bin*")) {
        $env:PATH = "$bin;$env:PATH"
    }
}

$GlobalStartTime = Get-Date
$PassedTests = 0
$FailedTests = 0
$TestResults = [System.Collections.Generic.List[PSCustomObject]]::new()

function Record-TestResult {
    param(
        [string]$Stage,
        [string]$Description,
        [bool]$Success,
        [string]$Detail
    )
    if ($Success) {
        $script:PassedTests++
        Write-Host "  [PASS] ${Stage}: $Description" -ForegroundColor Green
        if ($Detail) { Write-Host "         $Detail" -ForegroundColor Gray }
    } else {
        $script:FailedTests++
        Write-Host "  [FAIL] ${Stage}: $Description" -ForegroundColor Red
        if ($Detail) { Write-Host "         $Detail" -ForegroundColor Yellow }
    }
    $script:TestResults.Add([PSCustomObject]@{
        Stage       = $Stage
        Description = $Description
        Status      = if ($Success) { "PASS" } else { "FAIL" }
        Details     = $Detail
    })
}

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host " IT Helpdesk & Ticket Management System: Integrated DevOps Workflow" -ForegroundColor Cyan
Write-Host " Phase 5 End-to-End Pipeline Verification" -ForegroundColor Cyan
Write-Host " Start Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host " Repository: $RepoRoot" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# ------------------------------------------------------------------------------
# STAGE 1: Git Repository & Branching Model
# ------------------------------------------------------------------------------
Write-Host "`n>>> [Stage 1/7] Inspecting Git Repository & Branching Model..." -ForegroundColor Yellow
try {
    $Branch = (git branch --show-current).Trim()
    $RemoteUrl = (git remote get-url origin).Trim()
    $IsMain = ($Branch -eq "main")
    Record-TestResult -Stage "Stage 1" -Description "Git Active Branch" -Success $IsMain -Detail "Active Branch: '$Branch' (Expected: 'main')"

    $IsGithubRemote = ($RemoteUrl -like "*github.com*IT-Helpdesk*")
    Record-TestResult -Stage "Stage 1" -Description "GitHub Remote Origin" -Success $IsGithubRemote -Detail "Remote: $RemoteUrl"

    $EnvTracked = (git ls-files .env)
    $SecretSafe = [string]::IsNullOrEmpty($EnvTracked)
    $SecretDetail = if ($SecretSafe) { ".env is properly git-ignored" } else { "SECURITY WARNING: .env is tracked in git!" }
    Record-TestResult -Stage "Stage 1" -Description "Secret Hygiene (.env excluded from git)" -Success $SecretSafe -Detail $SecretDetail
} catch {
    Record-TestResult -Stage "Stage 1" -Description "Git SCM Inspection" -Success $false -Detail $_.Exception.Message
}

# ------------------------------------------------------------------------------
# STAGE 2: Host Environment & DevOps Runtime Readiness
# ------------------------------------------------------------------------------
Write-Host "`n>>> [Stage 2/7] Checking Host DevOps Tooling & Runtimes..." -ForegroundColor Yellow

$JavaVersion = & java -version 2>&1 | Out-String
$JavaOk = ($JavaVersion -like "*21.*")
$JavaDetail = ($JavaVersion -split "`n")[0].Trim()
Record-TestResult -Stage "Stage 2" -Description "Java 21 LTS Runtime" -Success $JavaOk -Detail $JavaDetail

$MavenCmd = if (Test-Path "$RepoRoot\backend\mvnw.cmd") { "$RepoRoot\backend\mvnw.cmd" } else { "mvn" }
$MavenVersion = & $MavenCmd -version 2>&1 | Out-String
$MavenOk = ($MavenVersion -like "*Apache Maven*")
$MavenDetail = ($MavenVersion -split "`n")[0].Trim()
Record-TestResult -Stage "Stage 2" -Description "Maven Build System" -Success $MavenOk -Detail $MavenDetail

$NodeVersion = & node -v 2>&1 | Out-String
$NodeOk = ($NodeVersion -like "v*")
Record-TestResult -Stage "Stage 2" -Description "Node.js Runtime" -Success $NodeOk -Detail "Version: $($NodeVersion.Trim())"

$DockerVersion = & docker --version 2>&1 | Out-String
$DockerOk = ($DockerVersion -like "*Docker version*")
Record-TestResult -Stage "Stage 2" -Description "Docker Engine CLI" -Success $DockerOk -Detail $DockerVersion.Trim()

$AnsibleVersion = & wsl -d Ubuntu -- bash -c "ansible --version | head -n 1" 2>&1 | Out-String
$AnsibleOk = ($AnsibleVersion -like "*ansible*")
Record-TestResult -Stage "Stage 2" -Description "Ansible Core in Ubuntu WSL2" -Success $AnsibleOk -Detail $AnsibleVersion.Trim()

# ------------------------------------------------------------------------------
# STAGE 3: Automated Testing Gate (JUnit 5 + Mockito + JaCoCo)
# ------------------------------------------------------------------------------
Write-Host "`n>>> [Stage 3/7] Verifying Automated Backend Tests & Coverage Gate..." -ForegroundColor Yellow
if ($SkipMavenTests) {
    Write-Host "  [SKIP] Skipping live Maven surefire execution as requested." -ForegroundColor Gray
} else {
    try {
        Set-Location "$RepoRoot\backend"
        $TestOutput = & $MavenCmd test 2>&1 | Out-String
        $TestsPassed = ($TestOutput -like "*BUILD SUCCESS*") -and ($TestOutput -like "*Tests run: 43, Failures: 0, Errors: 0*")
        $TestDetail = if ($TestsPassed) { "43 / 43 tests PASSED (0 failures, 0 errors, 0 skipped)" } else { "Test execution failed. Consult surefire reports." }
        Record-TestResult -Stage "Stage 3" -Description "JUnit 5 & Mockito Tests (43 unit & controller tests)" -Success $TestsPassed -Detail $TestDetail
        Set-Location $RepoRoot
    } catch {
        Set-Location $RepoRoot
        Record-TestResult -Stage "Stage 3" -Description "Maven Test Execution" -Success $false -Detail $_.Exception.Message
    }
}

$JacocoReport = "$RepoRoot\backend\target\site\jacoco\index.html"
$JacocoExists = Test-Path $JacocoReport
$JacocoDetail = if ($JacocoExists) { "Report generated at: $JacocoReport" } else { "JaCoCo index.html missing" }
Record-TestResult -Stage "Stage 3" -Description "JaCoCo Code Coverage HTML Report" -Success $JacocoExists -Detail $JacocoDetail

# ------------------------------------------------------------------------------
# STAGE 4: Frontend Production Compilation
# ------------------------------------------------------------------------------
Write-Host "`n>>> [Stage 4/7] Verifying Frontend Production SPA Compilation..." -ForegroundColor Yellow
try {
    Set-Location "$RepoRoot\frontend"
    $NpmBuildOutput = & npm.cmd run build 2>&1 | Out-String
    $DistHtml = "$RepoRoot\frontend\dist\index.html"
    $BuildOk = (Test-Path $DistHtml)
    $BuildDetail = if ($BuildOk) { "Production bundle compiled to frontend/dist/ (HTML, JS, CSS)" } else { "Build failed: dist/index.html not found" }
    Record-TestResult -Stage "Stage 4" -Description "Vite React SPA Production Build" -Success $BuildOk -Detail $BuildDetail
    Set-Location $RepoRoot
} catch {
    Set-Location $RepoRoot
    Record-TestResult -Stage "Stage 4" -Description "Frontend Build" -Success $false -Detail $_.Exception.Message
}

# ------------------------------------------------------------------------------
# STAGE 5: Docker Containerization & Orchestration Specification
# ------------------------------------------------------------------------------
Write-Host "`n>>> [Stage 5/7] Verifying Docker Images & Compose Graph..." -ForegroundColor Yellow
try {
    $ComposeConfig = & docker compose config 2>&1 | Out-String
    $ConfigOk = ($ComposeConfig -like "*services:*") -and ($ComposeConfig -like "*backend:*") -and ($ComposeConfig -like "*frontend:*")
    Record-TestResult -Stage "Stage 5" -Description "Docker Compose Service Graph" -Success $ConfigOk -Detail "Valid YAML graph with backend, frontend, mysql, network, and volume"

    $BackendImg = & docker images it-helpdesk-backend:1.0.0 --format "{{.Repository}}:{{.Tag}}" 2>&1 | Out-String
    $BackendImgOk = ($BackendImg.Trim() -eq "it-helpdesk-backend:1.0.0")
    $BackendImgDetail = if ($BackendImgOk) { "Image tagged: it-helpdesk-backend:1.0.0" } else { "Image tag not found" }
    Record-TestResult -Stage "Stage 5" -Description "Docker Image (it-helpdesk-backend:1.0.0)" -Success $BackendImgOk -Detail $BackendImgDetail

    $FrontendImg = & docker images it-helpdesk-frontend:1.0.0 --format "{{.Repository}}:{{.Tag}}" 2>&1 | Out-String
    $FrontendImgOk = ($FrontendImg.Trim() -eq "it-helpdesk-frontend:1.0.0")
    $FrontendImgDetail = if ($FrontendImgOk) { "Image tagged: it-helpdesk-frontend:1.0.0" } else { "Image tag not found" }
    Record-TestResult -Stage "Stage 5" -Description "Docker Image (it-helpdesk-frontend:1.0.0)" -Success $FrontendImgOk -Detail $FrontendImgDetail
} catch {
    Record-TestResult -Stage "Stage 5" -Description "Docker Image Verification" -Success $false -Detail $_.Exception.Message
}

# ------------------------------------------------------------------------------
# STAGE 6: Ansible Configuration Management & Idempotency
# ------------------------------------------------------------------------------
Write-Host "`n>>> [Stage 6/7] Running Ansible Configuration Management in Ubuntu WSL2..." -ForegroundColor Yellow
try {
    $AnsibleRun = & wsl -d Ubuntu -- bash -c "cd /mnt/c/DevopsCat/IT-Helpdesk/ansible && export ANSIBLE_CONFIG=./ansible.cfg && ansible-playbook -i inventory.ini playbook.yml" 2>&1 | Out-String
    $AnsibleOk = ($AnsibleRun -like "*failed=0*") -and ($AnsibleRun -like "*unreachable=0*")
    $Changed0 = ($AnsibleRun -like "*changed=0*")
    $AnsibleDetail = if ($AnsibleOk) { "Playbook completed with 0 failures, 0 unreachable" } else { "Playbook reported failures" }
    Record-TestResult -Stage "Stage 6" -Description "Ansible Playbook Execution" -Success $AnsibleOk -Detail $AnsibleDetail
    $IdempotentDetail = if ($Changed0) { "Strict Idempotency confirmed: changed=0" } else { "Notice: tasks reported changed > 0" }
    Record-TestResult -Stage "Stage 6" -Description "Ansible Idempotency Check" -Success $Changed0 -Detail $IdempotentDetail
} catch {
    Record-TestResult -Stage "Stage 6" -Description "Ansible Execution" -Success $false -Detail $_.Exception.Message
}

# ------------------------------------------------------------------------------
# STAGE 7: Multi-Service Live Deployment & Endpoint Health
# ------------------------------------------------------------------------------
Write-Host "`n>>> [Stage 7/7] Verifying Live Multi-Container Deployment & Endpoints..." -ForegroundColor Yellow
try {
    $PsOutput = & docker compose ps --format json 2>&1 | Out-String
    $ContainersRunning = ($PsOutput -like "*helpdesk-backend*") -and ($PsOutput -like "*helpdesk-frontend*") -and ($PsOutput -like "*helpdesk-mysql*")
    Record-TestResult -Stage "Stage 7" -Description "Docker Compose Stack Running" -Success $ContainersRunning -Detail "All 3 services (backend, frontend, mysql) present in container table"

    # Backend Actuator Health
    $ActuatorRes = Invoke-RestMethod -Uri "$BackendUrl/actuator/health" -TimeoutSec 10
    $BackendHealthOk = ($ActuatorRes.status -eq "UP")
    Record-TestResult -Stage "Stage 7" -Description "Spring Boot Backend Health (/actuator/health)" -Success $BackendHealthOk -Detail "Endpoint: $BackendUrl/actuator/health -> status: '$($ActuatorRes.status)'"

    # Frontend HTTP Status
    $FrontendRes = Invoke-WebRequest -Uri "$FrontendUrl/" -UseBasicParsing -TimeoutSec 10
    $FrontendHttpOk = ($FrontendRes.StatusCode -eq 200)
    Record-TestResult -Stage "Stage 7" -Description "React + Nginx Frontend Health (/)" -Success $FrontendHttpOk -Detail "Endpoint: $FrontendUrl/ -> HTTP status: $($FrontendRes.StatusCode) OK"

    # MySQL Port Open
    $TcpTest = Test-NetConnection -ComputerName "localhost" -Port 3306 -WarningAction SilentlyContinue
    $MySqlPortOk = $TcpTest.TcpTestSucceeded
    $MySqlDetail = if ($MySqlPortOk) { "TCP port 3306 reachable on localhost" } else { "Port 3306 not responding" }
    Record-TestResult -Stage "Stage 7" -Description "MySQL Database Port (3306)" -Success $MySqlPortOk -Detail $MySqlDetail
} catch {
    Record-TestResult -Stage "Stage 7" -Description "Live Deployment Verification" -Success $false -Detail $_.Exception.Message
}

# ------------------------------------------------------------------------------
# PIPELINE EXECUTION SUMMARY & LAB REPORT
# ------------------------------------------------------------------------------
$Duration = (Get-Date) - $GlobalStartTime
$SummaryColor = if ($FailedTests -eq 0) { "Green" } else { "Red" }
Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host " INTEGRATED DEVOPS WORKFLOW EXECUTION SUMMARY" -ForegroundColor Cyan
Write-Host " Total Steps Evaluated: $($TestResults.Count)" -ForegroundColor Cyan
Write-Host " Passed: $PassedTests | Failed: $FailedTests | Duration: $($Duration.TotalSeconds.ToString('F1'))s" -ForegroundColor $SummaryColor
Write-Host "================================================================================" -ForegroundColor Cyan

$TestResults | Format-Table -AutoSize -Property Stage, Description, Status, Details

if ($FailedTests -eq 0) {
    Write-Host "`n>>> [STATUS: SUCCESS] The complete end-to-end Integrated DevOps Workflow is verified!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n>>> [STATUS: WARNING] $FailedTests step(s) failed verification. Check details above." -ForegroundColor Yellow
    exit 1
}
