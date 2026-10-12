package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.DashboardStatsResponse;
import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.TicketStatus;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.repository.TicketRepository;
import org.springframework.stereotype.Service;

@Service
public class DashboardService {

    private final TicketRepository ticketRepository;

    public DashboardService(TicketRepository ticketRepository) {
        this.ticketRepository = ticketRepository;
    }

    public DashboardStatsResponse getStats(User currentUser) {
        if (currentUser.getRole() == Role.ROLE_EMPLOYEE) {
            long total = ticketRepository.countByCreatedBy(currentUser);
            long open = ticketRepository.countByCreatedByAndStatus(currentUser, TicketStatus.OPEN);
            long inProgress = ticketRepository.countByCreatedByAndStatus(currentUser, TicketStatus.IN_PROGRESS);
            long resolved = ticketRepository.countByCreatedByAndStatus(currentUser, TicketStatus.RESOLVED);
            long closed = ticketRepository.countByCreatedByAndStatus(currentUser, TicketStatus.CLOSED);

            return new DashboardStatsResponse(total, open, inProgress, resolved, closed);
        } else {
            long total = ticketRepository.count();
            long open = ticketRepository.countByStatus(TicketStatus.OPEN);
            long inProgress = ticketRepository.countByStatus(TicketStatus.IN_PROGRESS);
            long resolved = ticketRepository.countByStatus(TicketStatus.RESOLVED);
            long closed = ticketRepository.countByStatus(TicketStatus.CLOSED);

            return new DashboardStatsResponse(total, open, inProgress, resolved, closed);
        }
    }
}
