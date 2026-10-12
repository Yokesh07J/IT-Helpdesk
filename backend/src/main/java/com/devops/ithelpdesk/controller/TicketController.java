package com.devops.ithelpdesk.controller;

import com.devops.ithelpdesk.dto.AssignTicketRequest;
import com.devops.ithelpdesk.dto.StatusUpdateRequest;
import com.devops.ithelpdesk.dto.TicketRequest;
import com.devops.ithelpdesk.dto.TicketResponse;
import com.devops.ithelpdesk.entity.TicketCategory;
import com.devops.ithelpdesk.entity.TicketPriority;
import com.devops.ithelpdesk.entity.TicketStatus;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.service.AuthService;
import com.devops.ithelpdesk.service.TicketService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/tickets")
public class TicketController {

    private final TicketService ticketService;
    private final AuthService authService;

    public TicketController(TicketService ticketService, AuthService authService) {
        this.ticketService = ticketService;
        this.authService = authService;
    }

    @PostMapping
    public ResponseEntity<TicketResponse> createTicket(@Valid @RequestBody TicketRequest request) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        TicketResponse response = ticketService.createTicket(request, currentUser);
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }

    @GetMapping
    public ResponseEntity<List<TicketResponse>> getTickets(
            @RequestParam(required = false) TicketStatus status,
            @RequestParam(required = false) TicketPriority priority,
            @RequestParam(required = false) TicketCategory category,
            @RequestParam(required = false) String search) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        List<TicketResponse> tickets = ticketService.getTickets(status, priority, category, search, currentUser);
        return ResponseEntity.ok(tickets);
    }

    @GetMapping("/{id}")
    public ResponseEntity<TicketResponse> getTicketById(@PathVariable Long id) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        TicketResponse ticket = ticketService.getTicketById(id, currentUser);
        return ResponseEntity.ok(ticket);
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<TicketResponse> updateStatus(
            @PathVariable Long id,
            @Valid @RequestBody StatusUpdateRequest request) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        TicketResponse updated = ticketService.updateTicketStatus(id, request, currentUser);
        return ResponseEntity.ok(updated);
    }

    @PutMapping("/{id}/assign")
    @PreAuthorize("hasAnyRole('ADMIN', 'SUPPORT')")
    public ResponseEntity<TicketResponse> assignTicket(
            @PathVariable Long id,
            @Valid @RequestBody AssignTicketRequest request) {
        User currentUser = authService.getCurrentAuthenticatedUser();
        TicketResponse updated = ticketService.assignTicket(id, request, currentUser);
        return ResponseEntity.ok(updated);
    }
}
