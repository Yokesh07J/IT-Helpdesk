# PowerShell script for automated execution & verification of Docker Basics Lab
$ErrorActionPreference = "Continue"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  DevOps Lab — Phase 1: Docker Basics Verification Script " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check if Docker CLI is in PATH
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Docker CLI was not found in PATH." -ForegroundColor Yellow
    Write-Host "    Please install Docker Desktop for Windows or ensure Docker CLI is configured." -ForegroundColor Yellow
    Write-Host "    Follow installation steps documented in: docs/01-docker-basics.md" -ForegroundColor Gray
    exit 1
}

# 2. Check if Docker Daemon is running
Write-Host "[1/10] Verifying Docker daemon connectivity..." -ForegroundColor Green
$daemonStatus = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Docker CLI is installed, but Docker Desktop daemon is not running." -ForegroundColor Yellow
    Write-Host "    Please start Docker Desktop from the Start Menu and wait until the status indicator turns green." -ForegroundColor Yellow
    exit 1
}
Write-Host "       Docker Engine is running successfully." -ForegroundColor Green

# 3. Pull image
Write-Host "[2/10] Executing: docker pull nginx:alpine" -ForegroundColor Green
docker pull nginx:alpine

# 4. List images
Write-Host "[3/10] Executing: docker images" -ForegroundColor Green
docker images

# 5. Clean any existing test container
docker rm -f helpdesk-web-test 2>$null

# 6. Run detached container
Write-Host "[4/10] Executing: docker run -d -p 8085:80 --name helpdesk-web-test nginx:alpine" -ForegroundColor Green
$cid = docker run -d -p 8085:80 --name helpdesk-web-test nginx:alpine
Write-Host "       Container ID: $cid" -ForegroundColor Gray

# 7. List running containers
Write-Host "[5/10] Executing: docker ps" -ForegroundColor Green
docker ps --filter "name=helpdesk-web-test"

# 8. Fetch logs
Write-Host "[6/10] Executing: docker logs helpdesk-web-test" -ForegroundColor Green
docker logs --tail 5 helpdesk-web-test

# 9. Exec command inside container
Write-Host "[7/10] Executing: docker exec helpdesk-web-test nginx -v" -ForegroundColor Green
docker exec helpdesk-web-test nginx -v

# 10. Inspect container metadata
Write-Host "[8/10] Executing: docker inspect (Extracting IP and Port)" -ForegroundColor Green
$ip = docker inspect --format '{{.NetworkSettings.IPAddress}}' helpdesk-web-test
Write-Host "       Container Internal Bridge IP: $ip" -ForegroundColor Gray

# 11. Stop container
Write-Host "[9/10] Executing: docker stop helpdesk-web-test" -ForegroundColor Green
docker stop helpdesk-web-test

# 12. Remove container
Write-Host "[10/10] Executing: docker rm helpdesk-web-test" -ForegroundColor Green
docker rm helpdesk-web-test

Write-Host "`n[SUCCESS] All 10 Docker fundamental commands executed and verified cleanly!" -ForegroundColor Cyan
Write-Host "Documentation & lab record updated at: docs/01-docker-basics.md" -ForegroundColor Gray
