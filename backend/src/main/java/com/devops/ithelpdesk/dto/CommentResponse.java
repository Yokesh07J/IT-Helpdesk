package com.devops.ithelpdesk.dto;

import com.devops.ithelpdesk.entity.Comment;
import java.time.LocalDateTime;

public class CommentResponse {

    private Long id;
    private String message;
    private boolean internalNote;
    private UserResponse author;
    private LocalDateTime createdAt;

    public CommentResponse() {}

    public CommentResponse(Long id, String message, boolean internalNote, UserResponse author, LocalDateTime createdAt) {
        this.id = id;
        this.message = message;
        this.internalNote = internalNote;
        this.author = author;
        this.createdAt = createdAt;
    }

    public static CommentResponse fromEntity(Comment comment) {
        if (comment == null) {
            return null;
        }
        return new CommentResponse(
                comment.getId(),
                comment.getMessage(),
                comment.isInternalNote(),
                UserResponse.fromEntity(comment.getAuthor()),
                comment.getCreatedAt()
        );
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
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

    public UserResponse getAuthor() {
        return author;
    }

    public void setAuthor(UserResponse author) {
        this.author = author;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }
}
