package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.CommentRequest;
import com.devops.ithelpdesk.dto.CommentResponse;
import com.devops.ithelpdesk.entity.*;
import com.devops.ithelpdesk.repository.CommentRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.access.AccessDeniedException;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class CommentServiceTest {

    @Mock
    private CommentRepository commentRepository;

    @Mock
    private TicketService ticketService;

    @InjectMocks
    private CommentService commentService;

    private User employee;
    private User otherEmployee;
    private User supportStaff;
    private Ticket sampleTicket;

    @BeforeEach
    void setUp() {
        employee = new User("Alice Developer", "alice@company.com", "hash", "Eng", Role.ROLE_EMPLOYEE);
        employee.setId(10L);

        otherEmployee = new User("Bob Manager", "bob@company.com", "hash", "Mgmt", Role.ROLE_EMPLOYEE);
        otherEmployee.setId(15L);

        supportStaff = new User("Rachel Green", "rachel@helpdesk.com", "hash", "Support", Role.ROLE_SUPPORT);
        supportStaff.setId(25L);

        sampleTicket = new Ticket("HD-5001", "Database timeout", "Query timeout on replica",
                TicketCategory.SOFTWARE, TicketPriority.HIGH, employee);
        sampleTicket.setId(100L);
    }

    @Test
    void addComment_SuccessfullyAddsPublicCommentForOwnerEmployee() {
        CommentRequest request = new CommentRequest("Checking connection pool settings", false);

        when(ticketService.findEntityById(100L)).thenReturn(sampleTicket);
        when(commentRepository.save(any(Comment.class))).thenAnswer(invocation -> {
            Comment c = invocation.getArgument(0);
            c.setId(201L);
            return c;
        });

        CommentResponse response = commentService.addComment(100L, request, employee);

        assertNotNull(response);
        assertEquals(201L, response.getId());
        assertEquals("Checking connection pool settings", response.getMessage());
        assertFalse(response.isInternalNote());
        assertEquals("Alice Developer", response.getAuthor().getFullName());
        verify(commentRepository).save(any(Comment.class));
    }

    @Test
    void addComment_ThrowsAccessDeniedWhenEmployeeCommentsOnAnotherEmployeesTicket() {
        CommentRequest request = new CommentRequest("Unauthorized comment", false);
        when(ticketService.findEntityById(100L)).thenReturn(sampleTicket);

        assertThrows(AccessDeniedException.class, () -> commentService.addComment(100L, request, otherEmployee));
        verify(commentRepository, never()).save(any());
    }

    @Test
    void addComment_AllowsStaffToCreateInternalNote() {
        CommentRequest request = new CommentRequest("Internal note: Escalated to DBA team", true);

        when(ticketService.findEntityById(100L)).thenReturn(sampleTicket);
        when(commentRepository.save(any(Comment.class))).thenAnswer(invocation -> {
            Comment c = invocation.getArgument(0);
            c.setId(202L);
            return c;
        });

        CommentResponse response = commentService.addComment(100L, request, supportStaff);

        assertNotNull(response);
        assertTrue(response.isInternalNote());
        assertEquals("Rachel Green", response.getAuthor().getFullName());
    }

    @Test
    void addComment_ForcesInternalNoteFalseWhenAuthorIsEmployee() {
        CommentRequest request = new CommentRequest("Employee tried to set internal note", true);

        when(ticketService.findEntityById(100L)).thenReturn(sampleTicket);
        when(commentRepository.save(any(Comment.class))).thenAnswer(invocation -> {
            Comment c = invocation.getArgument(0);
            c.setId(203L);
            return c;
        });

        CommentResponse response = commentService.addComment(100L, request, employee);

        assertNotNull(response);
        assertFalse(response.isInternalNote(), "Employees must never be allowed to create internal-only notes");
    }

    @Test
    void getComments_FiltersOutInternalNotesWhenCurrentUserIsEmployee() {
        Comment publicComment = new Comment(sampleTicket, employee, "Public message", false);
        publicComment.setId(1L);

        Comment internalComment = new Comment(sampleTicket, supportStaff, "Secret diagnosis", true);
        internalComment.setId(2L);

        when(ticketService.findEntityById(100L)).thenReturn(sampleTicket);
        when(commentRepository.findByTicketOrderByCreatedAtAsc(sampleTicket))
                .thenReturn(Arrays.asList(publicComment, internalComment));

        List<CommentResponse> comments = commentService.getComments(100L, employee);

        assertEquals(1, comments.size());
        assertEquals("Public message", comments.get(0).getMessage());
        assertFalse(comments.get(0).isInternalNote());
    }

    @Test
    void getComments_IncludesInternalNotesWhenCurrentUserIsStaff() {
        Comment publicComment = new Comment(sampleTicket, employee, "Public message", false);
        publicComment.setId(1L);

        Comment internalComment = new Comment(sampleTicket, supportStaff, "Secret diagnosis", true);
        internalComment.setId(2L);

        when(ticketService.findEntityById(100L)).thenReturn(sampleTicket);
        when(commentRepository.findByTicketOrderByCreatedAtAsc(sampleTicket))
                .thenReturn(Arrays.asList(publicComment, internalComment));

        List<CommentResponse> comments = commentService.getComments(100L, supportStaff);

        assertEquals(2, comments.size());
    }

    @Test
    void getComments_ThrowsAccessDeniedWhenEmployeeViewsAnotherEmployeesComments() {
        when(ticketService.findEntityById(100L)).thenReturn(sampleTicket);

        assertThrows(AccessDeniedException.class, () -> commentService.getComments(100L, otherEmployee));
        verify(commentRepository, never()).findByTicketOrderByCreatedAtAsc(any());
    }
}
