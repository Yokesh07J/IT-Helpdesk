package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.UserResponse;
import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.exception.ResourceNotFoundException;
import com.devops.ithelpdesk.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    private User admin;
    private User support;

    @BeforeEach
    void setUp() {
        admin = new User("System Admin", "admin@helpdesk.com", "hash", "IT", Role.ROLE_ADMIN);
        admin.setId(1L);

        support = new User("Alex Vance", "alex@helpdesk.com", "hash", "Support", Role.ROLE_SUPPORT);
        support.setId(2L);
    }

    @Test
    void getSupportStaff_ReturnsOnlyAdminAndSupportUsers() {
        when(userRepository.findByRoleIn(anyList())).thenReturn(Arrays.asList(admin, support));

        List<UserResponse> staff = userService.getSupportStaff();

        assertEquals(2, staff.size());
        assertEquals("System Admin", staff.get(0).getFullName());
        assertEquals(Role.ROLE_ADMIN, staff.get(0).getRole());
        assertEquals("Alex Vance", staff.get(1).getFullName());
        assertEquals(Role.ROLE_SUPPORT, staff.get(1).getRole());
        verify(userRepository, times(1)).findByRoleIn(anyList());
    }

    @Test
    void getUserById_ReturnsUserResponseWhenUserExists() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(admin));

        UserResponse response = userService.getUserById(1L);

        assertNotNull(response);
        assertEquals(1L, response.getId());
        assertEquals("admin@helpdesk.com", response.getEmail());
    }

    @Test
    void findEntityById_ThrowsResourceNotFoundExceptionWhenUserNotFound() {
        when(userRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> userService.findEntityById(999L));
    }
}
