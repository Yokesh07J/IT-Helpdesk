package com.devops.ithelpdesk.controller;

import com.devops.ithelpdesk.dto.AuthRequest;
import com.devops.ithelpdesk.dto.AuthResponse;
import com.devops.ithelpdesk.dto.RegisterRequest;
import com.devops.ithelpdesk.dto.UserResponse;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@Valid @RequestBody AuthRequest request) {
        AuthResponse response = authService.login(request);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/register")
    public ResponseEntity<UserResponse> register(@Valid @RequestBody RegisterRequest request) {
        UserResponse response = authService.register(request);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    @GetMapping("/me")
    public ResponseEntity<UserResponse> getCurrentUser() {
        User currentUser = authService.getCurrentAuthenticatedUser();
        return ResponseEntity.ok(UserResponse.fromEntity(currentUser));
    }
}
