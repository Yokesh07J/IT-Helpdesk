package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.CommentRequest;
import com.devops.ithelpdesk.dto.CommentResponse;
import com.devops.ithelpdesk.entity.Comment;
import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.Ticket;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.exception.UnauthorizedException;
import com.devops.ithelpdesk.repository.CommentRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class CommentService {

    private final CommentRepository commentRepository;
    private final TicketService ticketService;

    public CommentService(CommentRepository commentRepository, TicketService ticketService) {
        this.commentRepository = commentRepository;
        this.ticketService = ticketService;
    }

    @Transactional
    public CommentResponse addComment(Long ticketId, CommentRequest request, User currentUser) {
        Ticket ticket = ticketService.findEntityById(ticketId);

        boolean isEmployee = currentUser.getRole() == Role.ROLE_EMPLOYEE;
        if (isEmployee && !ticket.getCreatedBy().getId().equals(currentUser.getId())) {
            throw new UnauthorizedException("You cannot comment on this ticket");
        }

        // Only staff can mark internal notes
        boolean internalNote = !isEmployee && request.isInternalNote();

        Comment comment = new Comment();
        comment.setTicket(ticket);
        comment.setAuthor(currentUser);
        comment.setMessage(request.getMessage().trim());
        comment.setInternalNote(internalNote);

        Comment saved = commentRepository.save(comment);
        return CommentResponse.fromEntity(saved);
    }

    public List<CommentResponse> getComments(Long ticketId, User currentUser) {
        Ticket ticket = ticketService.findEntityById(ticketId);

        boolean isEmployee = currentUser.getRole() == Role.ROLE_EMPLOYEE;
        if (isEmployee && !ticket.getCreatedBy().getId().equals(currentUser.getId())) {
            throw new UnauthorizedException("You cannot view comments on this ticket");
        }

        List<Comment> comments = commentRepository.findByTicketOrderByCreatedAtAsc(ticket);
        return comments.stream()
                .filter(c -> !isEmployee || !c.isInternalNote())
                .map(CommentResponse::fromEntity)
                .collect(Collectors.toList());
    }
}
