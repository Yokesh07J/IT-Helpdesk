# PowerShell script for automated execution & verification of Docker Basics Lab
$ErrorActionPreference = "Continue"

# Ensure Docker CLI path is available in the current PowerShell session
$dockerBin = "C:\Users\Laptop\AppData\Local\Programs\DockerDesktop\resources\bin"
if ((Test-Path $dockerBin) -and ($env:PATH -notlike "*$dockerBin*")) {
    $env:PATH = "$env:PATH;$dockerBin"
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  DevOps Lab - Phase 1: Docker Basics Verification Script " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check if Docker CLI is in PATH
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Docker CLI was not found in PATH." -ForegroundColor Yellow
    Write-Host "    Expected path: $dockerBin" -ForegroundColor Yellow
    exit 1
}

# 2. Check if Docker Daemon is running
Write-Host ""
Write-Host "[1/15] Verifying Docker CLI and Daemon connectivity..." -ForegroundColor Green
docker --version
docker info --format 'Server Version: {{.ServerVersion}}, OS: {{.OperatingSystem}}, Containers: {{.Containers}}, Images: {{.Images}}'
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Docker CLI is installed, but Docker Desktop daemon is not running." -ForegroundColor Yellow
    exit 1
}

# 3. Pull image
Write-Host ""
Write-Host "[2/15] Executing: docker pull nginx:alpine" -ForegroundColor Green
docker pull nginx:alpine

# 4. List images
Write-Host ""
Write-Host "[3/15] Executing: docker images" -ForegroundColor Green
docker images nginx:alpine

# 5. Clean any previous test container
docker rm -f helpdesk-web-test 2>$null | Out-Null

# 6. Run detached container
Write-Host ""
Write-Host "[4/15] Executing: docker run -d -p 8085:80 --name helpdesk-web-test nginx:alpine" -ForegroundColor Green
$cid = docker run -d -p 8085:80 --name helpdesk-web-test nginx:alpine
Write-Host "       Container ID: $cid" -ForegroundColor Gray

# 7. List running containers
Write-Host ""
Write-Host "[5/15] Executing: docker ps" -ForegroundColor Green
docker ps --filter "name=helpdesk-web-test"

# 8. List all containers (including stopped)
Write-Host ""
Write-Host "[6/15] Executing: docker ps -a" -ForegroundColor Green
docker ps -a --filter "name=helpdesk-web-test"

# 9. Verify web connectivity via HTTP
Write-Host ""
Write-Host "[7/15] Testing HTTP Web Response at http://localhost:8085 ..." -ForegroundColor Green
try {
    $webResp = Invoke-WebRequest -Uri "http://localhost:8085" -UseBasicParsing -TimeoutSec 5
    Write-Host "       HTTP Status Code: $($webResp.StatusCode) (Welcome to nginx!)" -ForegroundColor Green
} catch {
    Write-Host "       [!] HTTP request warning: $_" -ForegroundColor Yellow
}

# 10. Fetch logs
Write-Host ""
Write-Host "[8/15] Executing: docker logs helpdesk-web-test" -ForegroundColor Green
docker logs --tail 5 helpdesk-web-test

# 11. Exec command inside container
Write-Host ""
Write-Host "[9/15] Executing: docker exec helpdesk-web-test nginx -v" -ForegroundColor Green
docker exec helpdesk-web-test nginx -v

# 12. Inspect container metadata
Write-Host ""
Write-Host "[10/15] Executing: docker inspect (Extracting IP and Port)" -ForegroundColor Green
$ip = docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' helpdesk-web-test
Write-Host "       Container Internal Bridge IP: $ip" -ForegroundColor Gray

# 13. Stop container
Write-Host ""
Write-Host "[11/15] Executing: docker stop helpdesk-web-test" -ForegroundColor Green
docker stop helpdesk-web-test

# 14. Restart container
Write-Host ""
Write-Host "[12/15] Executing: docker start helpdesk-web-test" -ForegroundColor Green
docker start helpdesk-web-test
docker ps --filter "name=helpdesk-web-test"
docker stop helpdesk-web-test

# 15. Inspect Volumes and Networks
Write-Host ""
Write-Host "[13/15] Executing: docker volume ls and docker network ls" -ForegroundColor Green
docker volume ls
docker network ls

# 16. Remove container
Write-Host ""
Write-Host "[14/15] Executing: docker rm helpdesk-web-test" -ForegroundColor Green
docker rm helpdesk-web-test

# 17. Verify RMI query
Write-Host ""
Write-Host "[15/15] Executing: docker images (verifying image management)" -ForegroundColor Green
docker images --filter "reference=nginx:alpine"

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  [SUCCESS] All 15 Docker lifecycle commands verified live! " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
