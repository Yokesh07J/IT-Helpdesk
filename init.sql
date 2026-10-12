-- IT Helpdesk and Ticket Management System
-- Database Initialization Script

CREATE DATABASE IF NOT EXISTS it_helpdesk_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE it_helpdesk_db;

-- Grants for application user
-- GRANT ALL PRIVILEGES ON it_helpdesk_db.* TO 'helpdesk_user'@'%' IDENTIFIED BY 'helpdesk_pass';
-- FLUSH PRIVILEGES;

-- Note: Spring Boot JPA Hibernate ddl-auto=update automatically verifies and provisions
-- the schema tables (users, tickets, comments) and DataInitializer seeds demo accounts on boot.
