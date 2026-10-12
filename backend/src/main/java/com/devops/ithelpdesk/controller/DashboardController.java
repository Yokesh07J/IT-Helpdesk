package com.devops.ithelpdesk.controller;

import com.devops.ithelpdesk.dto.DashboardStatsResponse;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.service.AuthService;
import com.devops.ithelpdesk.service.DashboardService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {

    private final DashboardService dashboardService;
    private final AuthService authService;

    public DashboardController(DashboardService dashboardService, AuthService authService) {
        this.dashboardService = dashboardService;
        this.authService = authService;
    }

    @GetMapping("/stats")
    public ResponseEntity<DashboardStatsResponse> getStats() {
        User currentUser = authService.getCurrentAuthenticatedUser();
        DashboardStatsResponse stats = dashboardService.getStats(currentUser);
        return ResponseEntity.ok(stats);
    }
}
