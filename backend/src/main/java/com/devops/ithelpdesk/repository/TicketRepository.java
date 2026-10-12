package com.devops.ithelpdesk.repository;

import com.devops.ithelpdesk.entity.Ticket;
import com.devops.ithelpdesk.entity.TicketCategory;
import com.devops.ithelpdesk.entity.TicketPriority;
import com.devops.ithelpdesk.entity.TicketStatus;
import com.devops.ithelpdesk.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface TicketRepository extends JpaRepository<Ticket, Long> {

    Optional<Ticket> findByTicketCode(String ticketCode);

    List<Ticket> findByCreatedByOrderByCreatedAtDesc(User createdBy);

    List<Ticket> findAllByOrderByCreatedAtDesc();

    long countByStatus(TicketStatus status);

    long countByCreatedBy(User user);

    long countByCreatedByAndStatus(User user, TicketStatus status);

    @Query("SELECT t FROM Ticket t WHERE " +
           "(:status IS NULL OR t.status = :status) AND " +
           "(:priority IS NULL OR t.priority = :priority) AND " +
           "(:category IS NULL OR t.category = :category) AND " +
           "(:search IS NULL OR LOWER(t.title) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(t.ticketCode) LIKE LOWER(CONCAT('%', :search, '%'))) AND " +
           "(:userId IS NULL OR t.createdBy.id = :userId) " +
           "ORDER BY t.createdAt DESC")
    List<Ticket> searchTickets(
            @Param("status") TicketStatus status,
            @Param("priority") TicketPriority priority,
            @Param("category") TicketCategory category,
            @Param("search") String search,
            @Param("userId") Long userId
    );
}
