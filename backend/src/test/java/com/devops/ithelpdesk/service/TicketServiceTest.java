package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.AssignTicketRequest;
import com.devops.ithelpdesk.dto.StatusUpdateRequest;
import com.devops.ithelpdesk.dto.TicketRequest;
import com.devops.ithelpdesk.dto.TicketResponse;
import com.devops.ithelpdesk.entity.*;
import com.devops.ithelpdesk.exception.UnauthorizedException;
import com.devops.ithelpdesk.repository.TicketRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

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
    private User supportUser;
    private Ticket sampleTicket;

    @BeforeEach
    void setUp() {
        employee = new User("John Doe", "john.doe@company.com", "hash", "Engineering", Role.ROLE_EMPLOYEE);
        employee.setId(10L);

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
    void assignTicket_ThrowsUnauthorizedWhenAttemptedByEmployee() {
        AssignTicketRequest request = new AssignTicketRequest(20L);
        assertThrows(UnauthorizedException.class, () -> ticketService.assignTicket(100L, request, employee));
    }
}
