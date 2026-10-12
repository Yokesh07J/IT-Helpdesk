package com.devops.ithelpdesk.service;

import com.devops.ithelpdesk.dto.AssignTicketRequest;
import com.devops.ithelpdesk.dto.StatusUpdateRequest;
import com.devops.ithelpdesk.dto.TicketRequest;
import com.devops.ithelpdesk.dto.TicketResponse;
import com.devops.ithelpdesk.entity.*;
import com.devops.ithelpdesk.exception.ResourceNotFoundException;
import com.devops.ithelpdesk.exception.UnauthorizedException;
import com.devops.ithelpdesk.repository.TicketRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Random;
import java.util.stream.Collectors;

@Service
public class TicketService {

    private final TicketRepository ticketRepository;
    private final UserService userService;
    private final Random random = new Random();

    public TicketService(TicketRepository ticketRepository, UserService userService) {
        this.ticketRepository = ticketRepository;
        this.userService = userService;
    }

    @Transactional
    public TicketResponse createTicket(TicketRequest request, User currentUser) {
        String ticketCode = generateUniqueTicketCode();

        Ticket ticket = new Ticket();
        ticket.setTicketCode(ticketCode);
        ticket.setTitle(request.getTitle().trim());
        ticket.setDescription(request.getDescription().trim());
        ticket.setCategory(request.getCategory());
        ticket.setPriority(request.getPriority());
        ticket.setStatus(TicketStatus.OPEN);
        ticket.setCreatedBy(currentUser);

        Ticket saved = ticketRepository.save(ticket);
        return TicketResponse.fromEntity(saved, false);
    }

    public List<TicketResponse> getTickets(TicketStatus status, TicketPriority priority,
                                          TicketCategory category, String search, User currentUser) {
        Long userId = null;
        if (currentUser.getRole() == Role.ROLE_EMPLOYEE) {
            userId = currentUser.getId();
        }

        String searchParam = (search != null && !search.trim().isEmpty()) ? search.trim() : null;

        List<Ticket> tickets = ticketRepository.searchTickets(status, priority, category, searchParam, userId);
        return tickets.stream()
                .map(t -> TicketResponse.fromEntity(t, false))
                .collect(Collectors.toList());
    }

    public TicketResponse getTicketById(Long id, User currentUser) {
        Ticket ticket = findEntityById(id);
        verifyAccess(ticket, currentUser);
        return TicketResponse.fromEntity(ticket, true);
    }

    @Transactional
    public TicketResponse updateTicketStatus(Long id, StatusUpdateRequest request, User currentUser) {
        Ticket ticket = findEntityById(id);

        if (currentUser.getRole() == Role.ROLE_EMPLOYEE) {
            // Employees may only close tickets that belong to them if already resolved
            if (request.getStatus() == TicketStatus.CLOSED && ticket.getCreatedBy().getId().equals(currentUser.getId())) {
                ticket.setStatus(TicketStatus.CLOSED);
            } else {
                throw new UnauthorizedException("Employees cannot modify ticket status directly");
            }
        } else {
            // Admin and Support can transition statuses
            ticket.setStatus(request.getStatus());
            if (request.getStatus() == TicketStatus.RESOLVED || request.getStatus() == TicketStatus.CLOSED) {
                if (ticket.getResolvedAt() == null) {
                    ticket.setResolvedAt(LocalDateTime.now());
                }
            } else {
                ticket.setResolvedAt(null);
            }
        }

        if (request.getResolutionNotes() != null && !request.getResolutionNotes().trim().isEmpty()) {
            ticket.setResolutionNotes(request.getResolutionNotes().trim());
        }

        Ticket saved = ticketRepository.save(ticket);
        return TicketResponse.fromEntity(saved, true);
    }

    @Transactional
    public TicketResponse assignTicket(Long id, AssignTicketRequest request, User currentUser) {
        if (currentUser.getRole() == Role.ROLE_EMPLOYEE) {
            throw new UnauthorizedException("Only Support staff and Administrators can assign tickets");
        }

        Ticket ticket = findEntityById(id);
        User assignedStaff = userService.findEntityById(request.getAssignedToUserId());

        ticket.setAssignedTo(assignedStaff);
        if (ticket.getStatus() == TicketStatus.OPEN) {
            ticket.setStatus(TicketStatus.IN_PROGRESS);
        }

        Ticket saved = ticketRepository.save(ticket);
        return TicketResponse.fromEntity(saved, true);
    }

    public Ticket findEntityById(Long id) {
        return ticketRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Ticket not found with id: " + id));
    }

    private void verifyAccess(Ticket ticket, User currentUser) {
        if (currentUser.getRole() == Role.ROLE_EMPLOYEE &&
                !ticket.getCreatedBy().getId().equals(currentUser.getId())) {
            throw new UnauthorizedException("You are not authorized to view this ticket");
        }
    }

    private synchronized String generateUniqueTicketCode() {
        while (true) {
            int num = 1000 + random.nextInt(9000);
            String code = "HD-" + num;
            if (ticketRepository.findByTicketCode(code).isEmpty()) {
                return code;
            }
        }
    }
}
