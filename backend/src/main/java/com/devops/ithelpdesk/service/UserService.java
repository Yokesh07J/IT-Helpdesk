package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.UserResponse;
import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.exception.ResourceNotFoundException;
import com.devops.ithelpdesk.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<UserResponse> getSupportStaff() {
        List<User> staff = userRepository.findByRoleIn(Arrays.asList(Role.ROLE_ADMIN, Role.ROLE_SUPPORT));
        return staff.stream()
                .map(UserResponse::fromEntity)
                .collect(Collectors.toList());
    }

    public UserResponse getUserById(Long id) {
        User user = findEntityById(id);
        return UserResponse.fromEntity(user);
    }

    public User findEntityById(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("User not found with id: " + id));
    }
}
