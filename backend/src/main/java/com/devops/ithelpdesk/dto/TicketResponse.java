package com.devops.ithelpdesk.dto;

import com.devops.ithelpdesk.entity.Ticket;
import com.devops.ithelpdesk.entity.TicketCategory;
import com.devops.ithelpdesk.entity.TicketPriority;
import com.devops.ithelpdesk.entity.TicketStatus;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class TicketResponse {

    private Long id;
    private String ticketCode;
    private String title;
    private String description;
    private TicketCategory category;
    private TicketPriority priority;
    private TicketStatus status;
    private String resolutionNotes;
    private UserResponse createdBy;
    private UserResponse assignedTo;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime resolvedAt;
    private int commentCount;
    private List<CommentResponse> comments = new ArrayList<>();

    public TicketResponse() {}

    public static TicketResponse fromEntity(Ticket ticket, boolean includeComments) {
        if (ticket == null) {
            return null;
        }

        TicketResponse res = new TicketResponse();
        res.setId(ticket.getId());
        res.setTicketCode(ticket.getTicketCode());
        res.setTitle(ticket.getTitle());
        res.setDescription(ticket.getDescription());
        res.setCategory(ticket.getCategory());
        res.setPriority(ticket.getPriority());
        res.setStatus(ticket.getStatus());
        res.setResolutionNotes(ticket.getResolutionNotes());
        res.setCreatedBy(UserResponse.fromEntity(ticket.getCreatedBy()));
        res.setAssignedTo(UserResponse.fromEntity(ticket.getAssignedTo()));
        res.setCreatedAt(ticket.getCreatedAt());
        res.setUpdatedAt(ticket.getUpdatedAt());
        res.setResolvedAt(ticket.getResolvedAt());

        if (ticket.getComments() != null) {
            res.setCommentCount(ticket.getComments().size());
            if (includeComments) {
                res.setComments(ticket.getComments().stream()
                        .map(CommentResponse::fromEntity)
                        .collect(Collectors.toList()));
            }
        }
        return res;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTicketCode() {
        return ticketCode;
    }

    public void setTicketCode(String ticketCode) {
        this.ticketCode = ticketCode;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public TicketCategory getCategory() {
        return category;
    }

    public void setCategory(TicketCategory category) {
        this.category = category;
    }

    public TicketPriority getPriority() {
        return priority;
    }

    public void setPriority(TicketPriority priority) {
        this.priority = priority;
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

    public UserResponse getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(UserResponse createdBy) {
        this.createdBy = createdBy;
    }

    public UserResponse getAssignedTo() {
        return assignedTo;
    }

    public void setAssignedTo(UserResponse assignedTo) {
        this.assignedTo = assignedTo;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    public LocalDateTime getResolvedAt() {
        return resolvedAt;
    }

    public void setResolvedAt(LocalDateTime resolvedAt) {
        this.resolvedAt = resolvedAt;
    }

    public int getCommentCount() {
        return commentCount;
    }

    public void setCommentCount(int commentCount) {
        this.commentCount = commentCount;
    }

    public List<CommentResponse> getComments() {
        return comments;
    }

    public void setComments(List<CommentResponse> comments) {
        this.comments = comments;
    }
}
