package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.config.JwtTokenProvider;
import com.devops.ithelpdesk.dto.AuthRequest;
import com.devops.ithelpdesk.dto.AuthResponse;
import com.devops.ithelpdesk.dto.RegisterRequest;
import com.devops.ithelpdesk.dto.UserResponse;
import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.exception.BadRequestException;
import com.devops.ithelpdesk.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AuthServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    @Mock
    private AuthenticationManager authenticationManager;

    @Mock
    private JwtTokenProvider tokenProvider;

    @InjectMocks
    private AuthService authService;

    private User sampleUser;

    @BeforeEach
    void setUp() {
        sampleUser = new User("Jane Smith", "jane.smith@company.com", "encodedPass", "HR", Role.ROLE_EMPLOYEE);
        sampleUser.setId(1L);
    }

    @Test
    void register_SuccessfullyCreatesEmployeeAccount() {
        RegisterRequest request = new RegisterRequest("Jane Smith", "jane.smith@company.com", "secret123", "HR");

        when(userRepository.existsByEmail("jane.smith@company.com")).thenReturn(false);
        when(passwordEncoder.encode("secret123")).thenReturn("encodedPass");
        when(userRepository.save(any(User.class))).thenReturn(sampleUser);

        UserResponse response = authService.register(request);

        assertNotNull(response);
        assertEquals("Jane Smith", response.getFullName());
        assertEquals("jane.smith@company.com", response.getEmail());
        assertEquals(Role.ROLE_EMPLOYEE, response.getRole());
        verify(userRepository, times(1)).save(any(User.class));
    }

    @Test
    void register_ThrowsExceptionWhenEmailAlreadyExists() {
        RegisterRequest request = new RegisterRequest("Jane Smith", "jane.smith@company.com", "secret123", "HR");
        when(userRepository.existsByEmail("jane.smith@company.com")).thenReturn(true);

        assertThrows(BadRequestException.class, () -> authService.register(request));
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    void login_ReturnsJwtTokenForValidCredentials() {
        AuthRequest request = new AuthRequest("jane.smith@company.com", "secret123");
        Authentication auth = mock(Authentication.class);

        when(authenticationManager.authenticate(any(UsernamePasswordAuthenticationToken.class))).thenReturn(auth);
        when(userRepository.findByEmail("jane.smith@company.com")).thenReturn(Optional.of(sampleUser));
        when(tokenProvider.generateToken(sampleUser)).thenReturn("jwt.token.mock");

        AuthResponse response = authService.login(request);

        assertNotNull(response);
        assertEquals("jwt.token.mock", response.getToken());
        assertEquals("jane.smith@company.com", response.getEmail());
        assertEquals(Role.ROLE_EMPLOYEE, response.getRole());
    }

    @Test
    void login_ThrowsBadCredentialsExceptionWhenPasswordIsInvalid() {
        AuthRequest request = new AuthRequest("jane.smith@company.com", "wrongpassword");
        when(authenticationManager.authenticate(any(UsernamePasswordAuthenticationToken.class)))
                .thenThrow(new org.springframework.security.authentication.BadCredentialsException("Bad credentials"));

        assertThrows(org.springframework.security.authentication.BadCredentialsException.class,
                () -> authService.login(request));
        verify(tokenProvider, never()).generateToken(any());
    }

    @Test
    void login_ThrowsUnauthorizedExceptionWhenUserNotFoundInRepository() {
        AuthRequest request = new AuthRequest("unknown@company.com", "pass123");
        Authentication auth = mock(Authentication.class);
        when(authenticationManager.authenticate(any(UsernamePasswordAuthenticationToken.class))).thenReturn(auth);
        when(userRepository.findByEmail("unknown@company.com")).thenReturn(Optional.empty());

        assertThrows(com.devops.ithelpdesk.exception.UnauthorizedException.class,
                () -> authService.login(request));
    }

    @Test
    void getCurrentAuthenticatedUser_ReturnsUserWhenAuthenticated() {
        Authentication auth = mock(Authentication.class);
        when(auth.isAuthenticated()).thenReturn(true);
        when(auth.getName()).thenReturn("jane.smith@company.com");
        when(auth.getPrincipal()).thenReturn("jane.smith@company.com");
        org.springframework.security.core.context.SecurityContextHolder.getContext().setAuthentication(auth);

        when(userRepository.findByEmail("jane.smith@company.com")).thenReturn(Optional.of(sampleUser));

        User current = authService.getCurrentAuthenticatedUser();
        assertNotNull(current);
        assertEquals("Jane Smith", current.getFullName());
    }

    @Test
    void getCurrentAuthenticatedUser_ThrowsUnauthorizedExceptionWhenNotAuthenticated() {
        org.springframework.security.core.context.SecurityContextHolder.getContext().setAuthentication(null);

        assertThrows(com.devops.ithelpdesk.exception.UnauthorizedException.class,
                () -> authService.getCurrentAuthenticatedUser());
    }

    @Test
    void getCurrentAuthenticatedUser_ThrowsUnauthorizedExceptionWhenAnonymous() {
        Authentication auth = mock(Authentication.class);
        when(auth.isAuthenticated()).thenReturn(true);
        when(auth.getPrincipal()).thenReturn("anonymousUser");
        org.springframework.security.core.context.SecurityContextHolder.getContext().setAuthentication(auth);

        assertThrows(com.devops.ithelpdesk.exception.UnauthorizedException.class,
                () -> authService.getCurrentAuthenticatedUser());
    }
}
