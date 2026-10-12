package com.devops.ithelpdesk.config;

import com.devops.ithelpdesk.entity.*;
import com.devops.ithelpdesk.repository.CommentRepository;
import com.devops.ithelpdesk.repository.TicketRepository;
import com.devops.ithelpdesk.repository.UserRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final TicketRepository ticketRepository;
    private final CommentRepository commentRepository;
    private final PasswordEncoder passwordEncoder;

    public DataInitializer(UserRepository userRepository,
                           TicketRepository ticketRepository,
                           CommentRepository commentRepository,
                           PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.ticketRepository = ticketRepository;
        this.commentRepository = commentRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        if (userRepository.count() > 0) {
            return; // Data already seeded
        }

        // 1. Create Users
        User admin = new User(
                "System Administrator",
                "admin@helpdesk.com",
                passwordEncoder.encode("Admin@123"),
                "IT Infrastructure",
                Role.ROLE_ADMIN
        );

        User supportAlex = new User(
                "Alex Vance",
                "support.alex@helpdesk.com",
                passwordEncoder.encode("Support@123"),
                "Technical Support",
                Role.ROLE_SUPPORT
        );

        User supportRachel = new User(
                "Rachel Green",
                "support.rachel@helpdesk.com",
                passwordEncoder.encode("Support@123"),
                "Network Operations",
                Role.ROLE_SUPPORT
        );

        User empJohn = new User(
                "John Doe",
                "john.doe@company.com",
                passwordEncoder.encode("Pass@123"),
                "Software Engineering",
                Role.ROLE_EMPLOYEE
        );

        User empSarah = new User(
                "Sarah Jenkins",
                "sarah.jenkins@company.com",
                passwordEncoder.encode("Pass@123"),
                "Human Resources",
                Role.ROLE_EMPLOYEE
        );

        User empMichael = new User(
                "Michael Chang",
                "michael.chang@company.com",
                passwordEncoder.encode("Pass@123"),
                "Finance & Accounting",
                Role.ROLE_EMPLOYEE
        );

        userRepository.save(admin);
        userRepository.save(supportAlex);
        userRepository.save(supportRachel);
        userRepository.save(empJohn);
        userRepository.save(empSarah);
        userRepository.save(empMichael);

        // 2. Create Sample Tickets
        Ticket t1 = new Ticket(
                "HD-1001",
                "VPN connection failing with TLS handshake error",
                "Unable to connect to internal corporate network from home office. Cisco AnyConnect client fails after entering 2FA OTP with TLS handshake timeout.",
                TicketCategory.NETWORK,
                TicketPriority.HIGH,
                empJohn
        );
        t1.setStatus(TicketStatus.IN_PROGRESS);
        t1.setAssignedTo(supportAlex);
        ticketRepository.save(t1);

        Comment c1_1 = new Comment(t1, empJohn, "I verified my home Wi-Fi is working fine. Other websites open without issues.", false);
        Comment c1_2 = new Comment(t1, supportAlex, "Looking into this. The VPN gateway certificates were rotated last night; updating your client profile should resolve it.", false);
        Comment c1_3 = new Comment(t1, supportAlex, "Internal: Checked Cisco ASA logs, user cert serial mismatch.", true);
        commentRepository.save(c1_1);
        commentRepository.save(c1_2);
        commentRepository.save(c1_3);

        Ticket t2 = new Ticket(
                "HD-1002",
                "Dual monitor display flickering on docking station",
                "Secondary Dell 27-inch monitor blinks black every few minutes when connected through the Thunderbolt dock.",
                TicketCategory.HARDWARE,
                TicketPriority.MEDIUM,
                empSarah
        );
        t2.setStatus(TicketStatus.OPEN);
        ticketRepository.save(t2);

        Comment c2_1 = new Comment(t2, empSarah, "Happens on both HDMI and DisplayPort cables. Tested with a colleague's dock and it worked.", false);
        commentRepository.save(c2_1);

        Ticket t3 = new Ticket(
                "HD-1003",
                "Request IAM developer access to AWS Staging cluster",
                "Need read-write access to dev and staging EKS namespaces for deploying the upcoming helpdesk microservices release.",
                TicketCategory.ACCESS_REQUEST,
                TicketPriority.LOW,
                empJohn
        );
        t3.setStatus(TicketStatus.RESOLVED);
        t3.setAssignedTo(supportAlex);
        t3.setResolutionNotes("Attached DeveloperRole to John Doe AWS SSO profile and synced kubectl config.");
        t3.setResolvedAt(LocalDateTime.now().minusHours(4));
        ticketRepository.save(t3);

        Comment c3_1 = new Comment(t3, supportAlex, "Permissions have been provisioned and tested. Let us know if you encounter any permission denials.", false);
        commentRepository.save(c3_1);

        Ticket t4 = new Ticket(
                "HD-1004",
                "Production build artifact deployment failure in Jenkins",
                "Pipeline job #428 is hanging on Docker image build step with error 'no space left on device' on worker node.",
                TicketCategory.SOFTWARE,
                TicketPriority.URGENT,
                empMichael
        );
        t4.setStatus(TicketStatus.IN_PROGRESS);
        t4.setAssignedTo(supportRachel);
        ticketRepository.save(t4);

        Comment c4_1 = new Comment(t4, supportRachel, "Pruning dangling Docker images on the Jenkins agent server to reclaim disk space.", false);
        commentRepository.save(c4_1);

        Ticket t5 = new Ticket(
                "HD-1005",
                "Email synchronization error in Outlook desktop client",
                "Emails are arriving on Outlook Web Access but desktop client displays 'Disconnected' status code 0x80040115.",
                TicketCategory.SOFTWARE,
                TicketPriority.MEDIUM,
                empSarah
        );
        t5.setStatus(TicketStatus.CLOSED);
        t5.setAssignedTo(supportAlex);
        t5.setResolutionNotes("Rebuilt Outlook OST cache and re-authenticated Microsoft 365 Exchange profile.");
        t5.setResolvedAt(LocalDateTime.now().minusDays(1));
        ticketRepository.save(t5);
    }
}
