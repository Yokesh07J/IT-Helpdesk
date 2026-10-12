package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.AssignTicketRequest;
import com.devops.ithelpdesk.dto.StatusUpdateRequest;
import com.devops.ithelpdesk.dto.TicketRequest;
import com.devops.ithelpdesk.dto.TicketResponse;
import com.devops.ithelpdesk.entity.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.access.AccessDeniedException;
import com.devops.ithelpdesk.repository.TicketRepository;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class TicketServiceTest {

    @Mock
    private TicketRepository ticketRepository;

    @Mock
    private UserService userService;

    @InjectMocks
    private TicketService ticketService;

    private User employee;
    private User otherEmployee;
    private User supportUser;
    private Ticket sampleTicket;

    @BeforeEach
    void setUp() {
        employee = new User("John Doe", "john.doe@company.com", "hash", "Engineering", Role.ROLE_EMPLOYEE);
        employee.setId(10L);

        otherEmployee = new User("Jane Roe", "jane.roe@company.com", "hash", "Sales", Role.ROLE_EMPLOYEE);
        otherEmployee.setId(15L);

        supportUser = new User("Alex Vance", "alex@helpdesk.com", "hash", "Support", Role.ROLE_SUPPORT);
        supportUser.setId(20L);

        sampleTicket = new Ticket("HD-1001", "Printer offline", "Printer on 2nd floor offline",
                TicketCategory.HARDWARE, TicketPriority.HIGH, employee);
        sampleTicket.setId(100L);
    }

    @Test
    void createTicket_GeneratesUniqueTicketCodeAndSetsOpenStatus() {
        TicketRequest request = new TicketRequest("Printer offline", "Printer on 2nd floor offline",
                TicketCategory.HARDWARE, TicketPriority.HIGH);

        when(ticketRepository.findByTicketCode(anyString())).thenReturn(Optional.empty());
        when(ticketRepository.save(any(Ticket.class))).thenAnswer(invocation -> {
            Ticket t = invocation.getArgument(0);
            t.setId(101L);
            return t;
        });

        TicketResponse response = ticketService.createTicket(request, employee);

        assertNotNull(response);
        assertNotNull(response.getTicketCode());
        assertTrue(response.getTicketCode().startsWith("HD-"));
        assertEquals(TicketStatus.OPEN, response.getStatus());
        assertEquals("Printer offline", response.getTitle());
        verify(ticketRepository, times(1)).save(any(Ticket.class));
    }

    @Test
    void updateTicketStatus_ResolvesTicketAndSetsResolvedAt() {
        when(ticketRepository.findById(100L)).thenReturn(Optional.of(sampleTicket));
        when(ticketRepository.save(any(Ticket.class))).thenAnswer(invocation -> invocation.getArgument(0));

        StatusUpdateRequest request = new StatusUpdateRequest(TicketStatus.RESOLVED, "Replaced toner cartridge");
        TicketResponse response = ticketService.updateTicketStatus(100L, request, supportUser);

        assertEquals(TicketStatus.RESOLVED, response.getStatus());
        assertEquals("Replaced toner cartridge", response.getResolutionNotes());
        assertNotNull(response.getResolvedAt());
    }

    @Test
    void updateTicketStatus_AllowsEmployeeToCloseOwnResolvedTicket() {
        sampleTicket.setStatus(TicketStatus.RESOLVED);
        when(ticketRepository.findById(100L)).thenReturn(Optional.of(sampleTicket));
        when(ticketRepository.save(any(Ticket.class))).thenAnswer(invocation -> invocation.getArgument(0));

        StatusUpdateRequest request = new StatusUpdateRequest(TicketStatus.CLOSED, "Confirmed fixed");
        TicketResponse response = ticketService.updateTicketStatus(100L, request, employee);

        assertEquals(TicketStatus.CLOSED, response.getStatus());
    }

    @Test
    void updateTicketStatus_ThrowsAccessDeniedWhenEmployeeChangesToInProgress() {
        when(ticketRepository.findById(100L)).thenReturn(Optional.of(sampleTicket));

        StatusUpdateRequest request = new StatusUpdateRequest(TicketStatus.IN_PROGRESS, null);
        assertThrows(AccessDeniedException.class, () -> ticketService.updateTicketStatus(100L, request, employee));
    }

    @Test
    void assignTicket_UpdatesAssignedStaffAndTransitionsOpenToInProgress() {
        when(ticketRepository.findById(100L)).thenReturn(Optional.of(sampleTicket));
        when(userService.findEntityById(20L)).thenReturn(supportUser);
        when(ticketRepository.save(any(Ticket.class))).thenAnswer(invocation -> invocation.getArgument(0));

        AssignTicketRequest request = new AssignTicketRequest(20L);
        TicketResponse response = ticketService.assignTicket(100L, request, supportUser);

        assertEquals(TicketStatus.IN_PROGRESS, response.getStatus());
        assertEquals("Alex Vance", response.getAssignedTo().getFullName());
    }

    @Test
    void assignTicket_ThrowsAccessDeniedWhenAttemptedByEmployee() {
        AssignTicketRequest request = new AssignTicketRequest(20L);
        assertThrows(AccessDeniedException.class, () -> ticketService.assignTicket(100L, request, employee));
    }

    @Test
    void getTicketById_ThrowsAccessDeniedWhenEmployeeViewsOtherEmployeeTicket() {
        when(ticketRepository.findById(100L)).thenReturn(Optional.of(sampleTicket));
        assertThrows(AccessDeniedException.class, () -> ticketService.getTicketById(100L, otherEmployee));
    }

    @Test
    void getTicketById_ReturnsTicketWhenAdminOrSupportViewsAnyTicket() {
        when(ticketRepository.findById(100L)).thenReturn(Optional.of(sampleTicket));

        TicketResponse response = ticketService.getTicketById(100L, supportUser);
        assertNotNull(response);
        assertEquals("HD-1001", response.getTicketCode());
    }

    @Test
    void getTicketById_ThrowsResourceNotFoundWhenIdDoesNotExist() {
        when(ticketRepository.findById(999L)).thenReturn(Optional.empty());

        assertThrows(com.devops.ithelpdesk.exception.ResourceNotFoundException.class,
                () -> ticketService.getTicketById(999L, supportUser));
    }

    @Test
    void getTickets_PassesUserIdFilterForEmployee() {
        when(ticketRepository.searchTickets(isNull(), isNull(), isNull(), isNull(), eq(10L)))
                .thenReturn(java.util.List.of(sampleTicket));

        java.util.List<TicketResponse> result = ticketService.getTickets(null, null, null, null, employee);
        assertEquals(1, result.size());
        verify(ticketRepository).searchTickets(isNull(), isNull(), isNull(), isNull(), eq(10L));
    }

    @Test
    void getTickets_PassesNullUserIdFilterForAdmin() {
        User admin = new User("Admin", "admin@helpdesk.com", "hash", "IT", Role.ROLE_ADMIN);
        admin.setId(1L);

        when(ticketRepository.searchTickets(isNull(), isNull(), isNull(), isNull(), isNull()))
                .thenReturn(java.util.List.of(sampleTicket));

        java.util.List<TicketResponse> result = ticketService.getTickets(null, null, null, null, admin);
        assertEquals(1, result.size());
        verify(ticketRepository).searchTickets(isNull(), isNull(), isNull(), isNull(), isNull());
    }

    @Test
    void updateTicketStatus_ReopeningTicketClearsResolvedAt() {
        sampleTicket.setStatus(TicketStatus.RESOLVED);
        sampleTicket.setResolvedAt(java.time.LocalDateTime.now());
        when(ticketRepository.findById(100L)).thenReturn(Optional.of(sampleTicket));
        when(ticketRepository.save(any(Ticket.class))).thenAnswer(i -> i.getArgument(0));

        StatusUpdateRequest request = new StatusUpdateRequest(TicketStatus.IN_PROGRESS, null);
        TicketResponse response = ticketService.updateTicketStatus(100L, request, supportUser);

        assertEquals(TicketStatus.IN_PROGRESS, response.getStatus());
        assertNull(response.getResolvedAt());
    }

    @Test
    void assignTicket_PreservesStatusWhenTicketAlreadyInProgress() {
        sampleTicket.setStatus(TicketStatus.IN_PROGRESS);
        when(ticketRepository.findById(100L)).thenReturn(Optional.of(sampleTicket));
        when(userService.findEntityById(20L)).thenReturn(supportUser);
        when(ticketRepository.save(any(Ticket.class))).thenAnswer(i -> i.getArgument(0));

        AssignTicketRequest request = new AssignTicketRequest(20L);
        TicketResponse response = ticketService.assignTicket(100L, request, supportUser);

        assertEquals(TicketStatus.IN_PROGRESS, response.getStatus());
        assertEquals("Alex Vance", response.getAssignedTo().getFullName());
    }
}
