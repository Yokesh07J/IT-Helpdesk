package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.DashboardStatsResponse;
import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.TicketStatus;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.repository.TicketRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class DashboardServiceTest {

    @Mock
    private TicketRepository ticketRepository;

    @InjectMocks
    private DashboardService dashboardService;

    private User employee;
    private User admin;

    @BeforeEach
    void setUp() {
        employee = new User("John Doe", "john@company.com", "hash", "Eng", Role.ROLE_EMPLOYEE);
        employee.setId(10L);

        admin = new User("Admin", "admin@helpdesk.com", "hash", "IT", Role.ROLE_ADMIN);
        admin.setId(1L);
    }

    @Test
    void getStats_ReturnsEmployeeSpecificMetricsWhenRoleIsEmployee() {
        when(ticketRepository.countByCreatedBy(employee)).thenReturn(5L);
        when(ticketRepository.countByCreatedByAndStatus(employee, TicketStatus.OPEN)).thenReturn(2L);
        when(ticketRepository.countByCreatedByAndStatus(employee, TicketStatus.IN_PROGRESS)).thenReturn(1L);
        when(ticketRepository.countByCreatedByAndStatus(employee, TicketStatus.RESOLVED)).thenReturn(1L);
        when(ticketRepository.countByCreatedByAndStatus(employee, TicketStatus.CLOSED)).thenReturn(1L);

        DashboardStatsResponse stats = dashboardService.getStats(employee);

        assertNotNull(stats);
        assertEquals(5L, stats.getTotalTickets());
        assertEquals(2L, stats.getOpenTickets());
        assertEquals(1L, stats.getInProgressTickets());
        assertEquals(1L, stats.getResolvedTickets());
        assertEquals(1L, stats.getClosedTickets());
        verify(ticketRepository).countByCreatedBy(employee);
    }

    @Test
    void getStats_ReturnsGlobalSystemMetricsWhenRoleIsAdminOrSupport() {
        when(ticketRepository.count()).thenReturn(20L);
        when(ticketRepository.countByStatus(TicketStatus.OPEN)).thenReturn(8L);
        when(ticketRepository.countByStatus(TicketStatus.IN_PROGRESS)).thenReturn(5L);
        when(ticketRepository.countByStatus(TicketStatus.RESOLVED)).thenReturn(4L);
        when(ticketRepository.countByStatus(TicketStatus.CLOSED)).thenReturn(3L);

        DashboardStatsResponse stats = dashboardService.getStats(admin);

        assertNotNull(stats);
        assertEquals(20L, stats.getTotalTickets());
        assertEquals(8L, stats.getOpenTickets());
        assertEquals(5L, stats.getInProgressTickets());
        assertEquals(4L, stats.getResolvedTickets());
        assertEquals(3L, stats.getClosedTickets());
        verify(ticketRepository).count();
    }
}
