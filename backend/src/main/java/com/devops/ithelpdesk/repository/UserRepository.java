package com.devops.ithelpdesk.repository;

import com.devops.ithelpdesk.entity.Role;
import com.devops.ithelpdesk.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Collection;
import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    boolean existsByEmail(String email);
    List<User> findByRoleIn(Collection<Role> roles);
}
