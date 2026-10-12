package com.devops.ithelpdesk.controller;

import com.devops.ithelpdesk.dto.UserResponse;
import com.devops.ithelpdesk.service.UserService;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/staff")
    @PreAuthorize("hasAnyRole('ADMIN', 'SUPPORT')")
    public ResponseEntity<List<UserResponse>> getSupportStaff() {
        List<UserResponse> staff = userService.getSupportStaff();
        return ResponseEntity.ok(staff);
    }
}
