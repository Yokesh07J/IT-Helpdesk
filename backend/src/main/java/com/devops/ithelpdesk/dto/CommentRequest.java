package com.devops.ithelpdesk.dto;

import jakarta.validation.constraints.NotBlank;

public class CommentRequest {

    @NotBlank(message = "Comment message cannot be empty")
    private String message;

    private boolean internalNote = false;

    public CommentRequest() {}

    public CommentRequest(String message, boolean internalNote) {
        this.message = message;
        this.internalNote = internalNote;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public boolean isInternalNote() {
        return internalNote;
    }

    public void setInternalNote(boolean internalNote) {
        this.internalNote = internalNote;
    }
}
