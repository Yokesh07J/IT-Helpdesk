package com.devops.ithelpdesk.dto;

import com.devops.ithelpdesk.entity.TicketStatus;
import jakarta.validation.constraints.NotNull;

public class StatusUpdateRequest {

    @NotNull(message = "Ticket status is required")
    private TicketStatus status;

    private String resolutionNotes;

    public StatusUpdateRequest() {}

    public StatusUpdateRequest(TicketStatus status, String resolutionNotes) {
        this.status = status;
        this.resolutionNotes = resolutionNotes;
    }

    public TicketStatus getStatus() {
        return status;
    }

    public void setStatus(TicketStatus status) {
        this.status = status;
    }

    public String getResolutionNotes() {
        return resolutionNotes;
    }

    public void setResolutionNotes(String resolutionNotes) {
        this.resolutionNotes = resolutionNotes;
    }
}
