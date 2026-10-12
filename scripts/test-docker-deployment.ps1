# ==============================================================================
# Script: test-docker-deployment.ps1
# Description: Automated verification script for Phase 2 Docker Compose Deployment
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " [PHASE 2] IT HELPDESK DOCKER DEPLOYMENT VERIFICATION" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$baseUrl = "http://localhost"
$headers = @{ "Content-Type" = "application/json" }

# Test 1: Frontend HTTP availability
Write-Host "`n[TEST 1] Verifying Frontend Web Server (Nginx on Port 80)..." -NoNewline
try {
    $frontendResp = Invoke-WebRequest -Uri "$baseUrl/" -UseBasicParsing -TimeoutSec 10
    if ($frontendResp.StatusCode -eq 200) {
        Write-Host " [PASS] HTTP 200 OK" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Status: $($frontendResp.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 2: Backend Health Endpoint via Nginx Reverse Proxy
Write-Host "[TEST 2] Verifying Backend Health (/api/health)..." -NoNewline
try {
    $healthResp = Invoke-RestMethod -Uri "$baseUrl/api/health" -Method Get -TimeoutSec 10
    if ($healthResp.status -eq "UP") {
        Write-Host " [PASS] Status: $($healthResp.status)" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Status: $($healthResp.status)" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 3: Spring Boot Actuator Health Check (Database status)
Write-Host "[TEST 3] Verifying Spring Boot Actuator (/actuator/health)..." -NoNewline
try {
    $actuatorResp = Invoke-RestMethod -Uri "$baseUrl/actuator/health" -Method Get -TimeoutSec 10
    if ($actuatorResp.status -eq "UP") {
        Write-Host " [PASS] Actuator Status: $($actuatorResp.status)" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Actuator Status: $($actuatorResp.status)" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 4: Admin Authentication
Write-Host "[TEST 4] Authenticating as Administrator (admin@helpdesk.com)..." -NoNewline
$adminToken = $null
try {
    $adminBody = @{
        email = "admin@helpdesk.com"
        password = "Admin@123"
    } | ConvertTo-Json

    $adminAuth = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method Post -Body $adminBody -Headers $headers
    if ($adminAuth.token -and $adminAuth.role -eq "ROLE_ADMIN") {
        $adminToken = $adminAuth.token
        Write-Host " [PASS] Token acquired (Role: $($adminAuth.role))" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Unexpected response: $($adminAuth | ConvertTo-Json -Compress)" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 5: Employee Authentication
Write-Host "[TEST 5] Authenticating as Employee (john.doe@company.com)..." -NoNewline
$empToken = $null
try {
    $empBody = @{
        email = "john.doe@company.com"
        password = "Pass@123"
    } | ConvertTo-Json

    $empAuth = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method Post -Body $empBody -Headers $headers
    if ($empAuth.token -and $empAuth.role -eq "ROLE_EMPLOYEE") {
        $empToken = $empAuth.token
        Write-Host " [PASS] Token acquired (Role: $($empAuth.role))" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Unexpected response: $($empAuth | ConvertTo-Json -Compress)" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 6: Ticket Creation by Employee
Write-Host "[TEST 6] Creating Ticket as Employee..." -NoNewline
$createdTicketId = $null
try {
    $empHeaders = @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $empToken"
    }
    $newTicketBody = @{
        title = "Docker Compose Automated Pipeline Verification Ticket"
        description = "Validating automated containerized end-to-end ticketing workflow with MySQL persistence."
        category = "SOFTWARE"
        priority = "HIGH"
    } | ConvertTo-Json

    $createdTicket = Invoke-RestMethod -Uri "$baseUrl/api/tickets" -Method Post -Body $newTicketBody -Headers $empHeaders
    if ($createdTicket.id -and $createdTicket.ticketCode) {
        $createdTicketId = $createdTicket.id
        Write-Host " [PASS] Ticket Code: $($createdTicket.ticketCode) (ID: $($createdTicket.id))" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Could not create ticket: $($createdTicket | ConvertTo-Json -Compress)" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 7: Admin Ticket Assignment to Support Staff
Write-Host "[TEST 7] Assigning Ticket to Support Staff (Alex Vance) as Admin..." -NoNewline
try {
    $adminHeaders = @{
        "Content-Type" = "application/json"
        "Authorization" = "Bearer $adminToken"
    }
    $assignBody = @{
        assignedToUserId = 2
    } | ConvertTo-Json

    $assignedTicket = Invoke-RestMethod -Uri "$baseUrl/api/tickets/$createdTicketId/assign" -Method Put -Body $assignBody -Headers $adminHeaders
    if ($assignedTicket.assignedTo.fullName -eq "Alex Vance") {
        Write-Host " [PASS] Assigned to: $($assignedTicket.assignedTo.fullName)" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Assignment result: $($assignedTicket.assignedTo.fullName)" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 8: Ticket Status Update to IN_PROGRESS
Write-Host "[TEST 8] Updating Ticket Status to IN_PROGRESS..." -NoNewline
try {
    $statusBody = @{
        status = "IN_PROGRESS"
    } | ConvertTo-Json

    $statusTicket = Invoke-RestMethod -Uri "$baseUrl/api/tickets/$createdTicketId/status" -Method Put -Body $statusBody -Headers $adminHeaders
    if ($statusTicket.status -eq "IN_PROGRESS") {
        Write-Host " [PASS] Status updated to: $($statusTicket.status)" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Status update failed: $($statusTicket.status)" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 9: Adding Comment
Write-Host "[TEST 9] Adding Public Comment to Ticket..." -NoNewline
try {
    $commentBody = @{
        message = "Verified ticket resolution flow running inside Dockerized Spring Boot and MySQL containers."
        internalNote = $false
    } | ConvertTo-Json

    $commentResp = Invoke-RestMethod -Uri "$baseUrl/api/tickets/$createdTicketId/comments" -Method Post -Body $commentBody -Headers $adminHeaders
    if ($commentResp.id) {
        Write-Host " [PASS] Comment added (ID: $($commentResp.id))" -ForegroundColor Green
    } else {
        Write-Host " [FAIL] Comment addition failed" -ForegroundColor Red
    }
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

# Test 10: Dashboard Analytics Check
Write-Host "[TEST 10] Fetching Dashboard Metrics..." -NoNewline
try {
    $stats = Invoke-RestMethod -Uri "$baseUrl/api/dashboard/stats" -Method Get -Headers $adminHeaders
    Write-Host " [PASS] Total: $($stats.totalTickets), Open: $($stats.openTickets), In Progress: $($stats.inProgressTickets), Resolved: $($stats.resolvedTickets)" -ForegroundColor Green
} catch {
    Write-Host " [FAIL] $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " ALL PHASE 2 DOCKER DEPLOYMENT TESTS COMPLETED" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
