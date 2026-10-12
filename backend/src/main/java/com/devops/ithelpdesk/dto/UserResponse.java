package com.devops.ithelpdesk.dto;

import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.User;

public class UserResponse {

    private Long id;
    private String fullName;
    private String email;
    private Role role;
    private String department;

    public UserResponse() {}

    public UserResponse(Long id, String fullName, String email, Role role, String department) {
        this.id = id;
        this.fullName = fullName;
        this.email = email;
        this.role = role;
        this.department = department;
    }

    public static UserResponse fromEntity(User user) {
        if (user == null) {
            return null;
        }
        return new UserResponse(
                user.getId(),
                user.getFullName(),
                user.getEmail(),
                user.getRole(),
                user.getDepartment()
        );
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }
}
