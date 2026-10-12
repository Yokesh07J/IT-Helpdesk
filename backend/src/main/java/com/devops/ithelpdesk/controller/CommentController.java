package com.devops.ithelpdesk.controller;

import com.devops.ithelpdesk.dto.CommentRequest;
import com.devops.ithelpdesk.dto.CommentResponse;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.service.AuthService;
import com.devops.ithelpdesk.service.CommentService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tickets/{ticketId}/comments")
public class CommentController {

    private final CommentService commentService;
    private final AuthService authService;

    public CommentController(CommentService commentService, AuthService authService) {
        this.commentService = commentService;
        this.authService = authService;
    }

    @PostMapping
    public ResponseEntity<CommentResponse> addComment(
            @PathVariable Long ticketId,
            @Valid @RequestBody CommentRequest request) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        CommentResponse response = commentService.addComment(ticketId, request, currentUser);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    @GetMapping
    public ResponseEntity<List<CommentResponse>> getComments(@PathVariable Long ticketId) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        List<CommentResponse> comments = commentService.getComments(ticketId, currentUser);
        return ResponseEntity.ok(comments);
    }
}
