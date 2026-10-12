package com.devops.ithelpdesk.dto;

import jakarta.validation.constraints.NotNull;

public class AssignTicketRequest {

    @NotNull(message = "Assigned user ID is required")
    private Long assignedToUserId;

    public AssignTicketRequest() {}

    public AssignTicketRequest(Long assignedToUserId) {
        this.assignedToUserId = assignedToUserId;
    }

    public Long getAssignedToUserId() {
        return assignedToUserId;
    }

    public void setAssignedToUserId(Long assignedToUserId) {
        this.assignedToUserId = assignedToUserId;
    }
}
