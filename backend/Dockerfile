# Multi-stage Dockerfile for IT Helpdesk Backend (Java 21 / Spring Boot 3.2.5)

# -------------------------------------------------------------
# Stage 1: Builder
# -------------------------------------------------------------
FROM maven:3.9.6-eclipse-temurin-21-alpine AS builder

WORKDIR /build

# Copy Maven descriptor and resolve dependencies to leverage Docker layer caching
COPY pom.xml .
RUN mvn dependency:resolve -B

# Copy application source code and compile production JAR
COPY src ./src
RUN mvn clean package -DskipTests

# -------------------------------------------------------------
# Stage 2: Minimal Production JRE Runtime
# -------------------------------------------------------------
FROM eclipse-temurin:21-jre-alpine

# Set metadata labels
LABEL maintainer="DevOps Team <devops@ithelpdesk.local>"
LABEL description="IT Helpdesk and Ticket Management System Backend Service"
LABEL version="1.0.0"

# Create dedicated non-root application group and user
RUN addgroup -S spring && adduser -S spring -G spring

WORKDIR /app

# Copy executable jar from builder stage and assign permissions
COPY --from=builder /build/target/*.jar app.jar
RUN chown -R spring:spring /app

# Switch to non-root user for principle of least privilege
USER spring:spring

# Expose application port (8088)
EXPOSE 8088

# Container healthcheck targeting Spring Boot Actuator endpoint
HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
  CMD wget -q -O /dev/null http://localhost:8088/actuator/health || exit 1

# Launch application
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
