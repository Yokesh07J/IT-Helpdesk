package com.devops.ithelpdesk.controller;

import com.devops.ithelpdesk.dto.AuthRequest;
import com.devops.ithelpdesk.dto.AuthResponse;
import com.devops.ithelpdesk.dto.RegisterRequest;
import com.devops.ithelpdesk.dto.UserResponse;
import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.exception.GlobalExceptionHandler;
import com.devops.ithelpdesk.service.AuthService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@ExtendWith(MockitoExtension.class)
class AuthControllerTest {

    private MockMvc mockMvc;

    @Mock
    private AuthService authService;

    @InjectMocks
    private AuthController authController;

    private final ObjectMapper objectMapper = new ObjectMapper();

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(authController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .build();
    }

    @Test
    void login_Returns200AndTokenForValidPayload() throws Exception {
        AuthRequest request = new AuthRequest("john@company.com", "Password@123");
        AuthResponse response = new AuthResponse("mock.jwt.token", 1L, "John Doe", "john@company.com", Role.ROLE_EMPLOYEE, "Engineering");

        when(authService.login(any(AuthRequest.class))).thenReturn(response);

        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token").value("mock.jwt.token"))
                .andExpect(jsonPath("$.email").value("john@company.com"))
                .andExpect(jsonPath("$.role").value("ROLE_EMPLOYEE"));

        verify(authService, times(1)).login(any(AuthRequest.class));
    }

    @Test
    void login_Returns400BadRequestWhenEmailIsInvalid() throws Exception {
        AuthRequest request = new AuthRequest("invalid-email-format", "Password@123");

        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Validation Error"));

        verify(authService, never()).login(any());
    }

    @Test
    void login_Returns400BadRequestWhenPasswordIsBlank() throws Exception {
        AuthRequest request = new AuthRequest("john@company.com", "");

        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Validation Error"));

        verify(authService, never()).login(any());
    }

    @Test
    void register_Returns201CreatedForValidPayload() throws Exception {
        RegisterRequest request = new RegisterRequest("Jane Smith", "jane@company.com", "Secret@123", "HR");
        UserResponse response = new UserResponse(2L, "Jane Smith", "jane@company.com", Role.ROLE_EMPLOYEE, "HR");

        when(authService.register(any(RegisterRequest.class))).thenReturn(response);

        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.fullName").value("Jane Smith"))
                .andExpect(jsonPath("$.email").value("jane@company.com"));

        verify(authService, times(1)).register(any(RegisterRequest.class));
    }

    @Test
    void register_Returns400BadRequestWhenFullNameIsBlank() throws Exception {
        RegisterRequest request = new RegisterRequest("", "jane@company.com", "Secret@123", "HR");

        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Validation Error"));

        verify(authService, never()).register(any());
    }
}
