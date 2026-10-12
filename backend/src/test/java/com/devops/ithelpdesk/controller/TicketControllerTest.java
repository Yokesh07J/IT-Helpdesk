package com.devops.ithelpdesk.controller;

import com.devops.ithelpdesk.dto.AssignTicketRequest;
import com.devops.ithelpdesk.dto.StatusUpdateRequest;
import com.devops.ithelpdesk.dto.TicketRequest;
import com.devops.ithelpdesk.dto.TicketResponse;
import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.TicketCategory;
import com.devops.ithelpdesk.entity.TicketPriority;
import com.devops.ithelpdesk.entity.TicketStatus;
import com.devops.ithelpdesk.entity.User;
import com.devops.ithelpdesk.exception.GlobalExceptionHandler;
import com.devops.ithelpdesk.service.AuthService;
import com.devops.ithelpdesk.service.TicketService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@ExtendWith(MockitoExtension.class)
class TicketControllerTest {

    private MockMvc mockMvc;

    @Mock
    private TicketService ticketService;

    @Mock
    private AuthService authService;

    @InjectMocks
    private TicketController ticketController;

    private final ObjectMapper objectMapper = new ObjectMapper();
    private User testUser;

    @BeforeEach
    void setUp() {
        mockMvc = MockMvcBuilders.standaloneSetup(ticketController)
                .setControllerAdvice(new GlobalExceptionHandler())
                .build();

        testUser = new User("John Doe", "john@company.com", "pass", "Eng", Role.ROLE_EMPLOYEE);
        testUser.setId(10L);
    }

    @Test
    void createTicket_Returns201CreatedForValidPayload() throws Exception {
        TicketRequest request = new TicketRequest("Printer Broken", "Printer tray jammed", TicketCategory.HARDWARE, TicketPriority.MEDIUM);

        TicketResponse response = new TicketResponse();
        response.setId(1L);
        response.setTicketCode("HD-1001");
        response.setTitle("Printer Broken");
        response.setStatus(TicketStatus.OPEN);

        when(authService.getCurrentAuthenticatedUser()).thenReturn(testUser);
        when(ticketService.createTicket(any(TicketRequest.class), eq(testUser))).thenReturn(response);

        mockMvc.perform(post("/api/tickets")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.ticketCode").value("HD-1001"))
                .andExpect(jsonPath("$.title").value("Printer Broken"));

        verify(ticketService, times(1)).createTicket(any(TicketRequest.class), eq(testUser));
    }

    @Test
    void createTicket_Returns400BadRequestWhenTitleIsTooShort() throws Exception {
        TicketRequest request = new TicketRequest("AB", "Printer tray jammed", TicketCategory.HARDWARE, TicketPriority.MEDIUM);

        mockMvc.perform(post("/api/tickets")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("Validation Error"));

        verify(ticketService, never()).createTicket(any(), any());
    }

    @Test
    void getTicketById_Returns200AndTicket() throws Exception {
        TicketResponse response = new TicketResponse();
        response.setId(5L);
        response.setTicketCode("HD-2005");
        response.setTitle("VPN issue");

        when(authService.getCurrentAuthenticatedUser()).thenReturn(testUser);
        when(ticketService.getTicketById(5L, testUser)).thenReturn(response);

        mockMvc.perform(get("/api/tickets/5"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.ticketCode").value("HD-2005"))
                .andExpect(jsonPath("$.title").value("VPN issue"));
    }

    @Test
    void updateStatus_Returns200ForValidPayload() throws Exception {
        StatusUpdateRequest request = new StatusUpdateRequest(TicketStatus.IN_PROGRESS, null);

        TicketResponse response = new TicketResponse();
        response.setId(5L);
        response.setStatus(TicketStatus.IN_PROGRESS);

        when(authService.getCurrentAuthenticatedUser()).thenReturn(testUser);
        when(ticketService.updateTicketStatus(eq(5L), any(StatusUpdateRequest.class), eq(testUser))).thenReturn(response);

        mockMvc.perform(put("/api/tickets/5/status")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"));
    }

    @Test
    void assignTicket_Returns200ForValidPayload() throws Exception {
        AssignTicketRequest request = new AssignTicketRequest(2L);

        TicketResponse response = new TicketResponse();
        response.setId(5L);
        response.setStatus(TicketStatus.IN_PROGRESS);

        when(authService.getCurrentAuthenticatedUser()).thenReturn(testUser);
        when(ticketService.assignTicket(eq(5L), any(AssignTicketRequest.class), eq(testUser))).thenReturn(response);

        mockMvc.perform(put("/api/tickets/5/assign")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(request)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("IN_PROGRESS"));
    }
}
