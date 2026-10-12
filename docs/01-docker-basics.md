# DevOps Lab — Experiment 1: Docker Basics & Container Lifecycle Management

## 1. Aim and Objectives
- **Aim**: To install, verify, and master basic Docker commands on Windows, demonstrating container lifecycle management (pull, run, inspect, execute, stop, and remove) for web applications and databases.
- **Objectives**:
  1. Understand containerization fundamentals and compare containers with traditional virtual machines.
  2. Install and verify Docker Desktop on a Windows workstation.
  3. Execute fundamental Docker commands (`pull`, `images`, `run`, `ps`, `stop`, `rm`, `logs`, `exec`, `inspect`).
  4. Deploy interactive and detached test containers (`nginx:alpine` and `alpine:latest`) and examine container networking and filesystem isolation.
  5. Record expected terminal inputs and outputs for the DevOps Lab record and viva voce.

---

## 2. Theoretical Overview

### Containers vs. Virtual Machines
| Parameter | Virtual Machines (VMs) | Docker Containers |
|---|---|---|
| **Architecture** | Runs on a Hypervisor (Type 1 or 2) | Shares host OS kernel; utilizes cgroups and namespaces |
| **Guest OS** | Full guest OS per VM (GBs in size) | No guest OS; contains only app and dependencies (MBs) |
| **Startup Time** | Minutes | Milliseconds to seconds |
| **Resource Usage** | Heavy (pre-allocated RAM/CPU) | Lightweight (dynamic allocation on demand) |
| **Portability** | Harder to migrate across environments | Highly portable; runs anywhere Docker Engine is present |

### Docker Architecture
Docker utilizes a client-server architecture:
- **Docker Client (`docker`)**: Command-line interface used by developers to issue instructions.
- **Docker Daemon (`dockerd`)**: Background service on the host that listens for Docker API requests and manages Docker objects (images, containers, networks, volumes).
- **Docker Registry**: Repository for storing and retrieving container images (Docker Hub by default).
- **Docker Images**: Read-only templates containing libraries, application binaries, and configuration.
- **Docker Containers**: Runnable, isolated instances of a Docker image with a thin read-write top layer.

---

## 3. Windows Installation and Verification Guide

### 3.1 Prerequisites
1. **Operating System**: Windows 10 (Build 19044+) or Windows 11 64-bit.
2. **Virtualization**: Hardware virtualization (Intel VT-x or AMD-V) enabled in BIOS/UEFI.
3. **WSL 2 (Recommended)**: Windows Subsystem for Linux 2.

### 3.2 Installation Steps

#### Method A: Using Windows Package Manager (`winget`) — Command Line
Open PowerShell as Administrator and run:
```powershell
# 1. Enable WSL and install Ubuntu distribution
wsl --install

# 2. Install Docker Desktop via winget
winget install Docker.DockerDesktop
```

#### Method B: Using Docker Desktop GUI Installer
1. Download **Docker Desktop for Windows** from the official site:
   [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Run `Docker Desktop Installer.exe`.
3. Ensure **"Use WSL 2 instead of Hyper-V (recommended)"** is checked during installation.
4. Restart your computer when prompted.
5. Launch Docker Desktop from the Start Menu and wait until the status indicator in the bottom-left turns green (**Engine running**).

### 3.3 Verification Commands
Run these commands in PowerShell or Command Prompt to verify the installation:

```powershell
# Check Docker CLI version
docker --version

# Check Docker Compose version
docker compose version

# Check Docker system information and daemon connectivity
docker info

# Run canonical test image
docker run hello-world
```

**Expected Verification Output**:
```text
Docker version 26.1.1, build 4cf500e
Docker Compose version v2.27.0
Client:
 Version:    26.1.1
 Context:    default
 Debug Mode: false

Server:
 Containers: 0
  Running: 0
  Paused: 0
  Stopped: 0
 Images: 0
 Server Version: 26.1.1
 Operating System: Docker Desktop
 Architecture: x86_64

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

---

## 4. Core Docker Commands: Syntax, Usage & Expected Results

### Command 1: `docker pull`
Downloads a container image from Docker Hub without starting a container.

- **Syntax**: `docker pull <image-name>:<tag>`
- **Lab Command**:
  ```powershell
  docker pull nginx:alpine
  ```
- **Expected Output**:
  ```text
  alpine: Pulling from library/nginx
  4abcf2066143: Pull complete
  774d6c66cf17: Pull complete
  90b4e207904a: Pull complete
  Digest: sha256:1f77d85347f6a73a6ab60e58c8ecb58fc94c0347ee9370
  Status: Downloaded newer image for nginx:alpine
  docker.io/library/nginx:alpine
  ```

---

### Command 2: `docker images`
Lists container images downloaded to the local host repository.

- **Syntax**: `docker images [OPTIONS] [REPOSITORY[:TAG]]`
- **Lab Command**:
  ```powershell
  docker images
  ```
- **Expected Output**:
  ```text
  REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
  nginx        alpine    91b4b0e71a3f   3 days ago     42.6MB
  hello-world  latest    d2c94e258dcb   12 months ago  13.3kB
  ```

---

### Command 3: `docker run`
Creates and starts a container from an image.

- **Key Flags**:
  - `-d`: Detached mode (runs in background).
  - `-p <host-port>:<container-port>`: Exposes and maps network ports.
  - `--name <name>`: Assigns a custom name to the container.
  - `-it`: Interactive mode with an allocated Pseudo-TTY.
  - `--rm`: Automatically removes the container when it exits.
  - `-e <KEY=VALUE>`: Passes environment variables.

- **Lab Command A (Detached Web Server)**:
  ```powershell
  docker run -d -p 8085:80 --name helpdesk-web-test nginx:alpine
  ```
- **Expected Output**:
  ```text
  a1b2c3d4e5f67890123456789abcdef0123456789abcdef0123456789abcdef0
  ```

- **Lab Command B (Interactive Lightweight Container)**:
  ```powershell
  docker run -it --rm alpine:latest sh
  ```
- **Inside Container Commands**:
  ```sh
  uname -a
  cat /etc/os-release
  exit
  ```
- **Expected Output**:
  ```text
  / # uname -a
  Linux 4c5b6a78 5.15.153.1-microsoft-standard-WSL2 #1 SMP Fri Mar 29 23:14:13 UTC 2024 x86_64 Linux
  / # cat /etc/os-release
  NAME="Alpine Linux"
  ID=alpine
  VERSION_ID=3.20.0
  PRETTY_NAME="Alpine Linux v3.20"
  / # exit
  ```

---

### Command 4: `docker ps`
Lists running containers. Add `-a` to show all containers (including stopped ones).

- **Syntax**: `docker ps` / `docker ps -a`
- **Lab Command**:
  ```powershell
  docker ps
  ```
- **Expected Output**:
  ```text
  CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                  NAMES
  a1b2c3d4e5f6   nginx:alpine   "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   0.0.0.0:8085->80/tcp   helpdesk-web-test
  ```

- **All Containers Command**:
  ```powershell
  docker ps -a
  ```
- **Expected Output**:
  ```text
  CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS                     PORTS                  NAMES
  a1b2c3d4e5f6   nginx:alpine   "/docker-entrypoint.…"   3 minutes ago   Up 3 minutes               0.0.0.0:8085->80/tcp   helpdesk-web-test
  f9e8d7c6b5a4   hello-world    "/hello"                 10 minutes ago  Exited (0) 10 minutes ago                         eager_curie
  ```

---

### Command 5: `docker logs`
Fetches stdout and stderr streams generated by a container.

- **Key Flags**:
  - `-f`: Follow log output live.
  - `--tail <N>`: Show only the last N lines.
  - `-t`: Add timestamps.

- **Lab Command**:
  ```powershell
  docker logs --tail 10 helpdesk-web-test
  ```
- **Expected Output**:
  ```text
  /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
  /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
  /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
  10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
  10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
  /docker-entrypoint.sh: Configuration complete; ready for start up
  2026/10/12 15:45:00 [notice] 1#1: using the "epoll" event method
  2026/10/12 15:45:00 [notice] 1#1: nginx/1.25.5
  2026/10/12 15:45:00 [notice] 1#1: OS: Linux 5.15.153.1-microsoft-standard-WSL2
  ```

---

### Command 6: `docker exec`
Executes an interactive or one-off command inside an already running container.

- **Syntax**: `docker exec [OPTIONS] <CONTAINER> <COMMAND>`
- **Lab Command A (Inspect Nginx inside running container)**:
  ```powershell
  docker exec helpdesk-web-test nginx -v
  ```
- **Expected Output**:
  ```text
  nginx version: nginx/1.25.5
  ```

- **Lab Command B (Interactive shell session inside container)**:
  ```powershell
  docker exec -it helpdesk-web-test sh
  ```
- **Inside Container Execution**:
  ```sh
  cat /usr/share/nginx/html/index.html
  exit
  ```
- **Expected Output**:
  ```html
  <!DOCTYPE html>
  <html>
  <head>
  <title>Welcome to nginx!</title>
  ...
  ```

---

### Command 7: `docker inspect`
Returns low-level configuration and runtime JSON metadata for a container or image.

- **Syntax**: `docker inspect <container-name|id>`
- **Lab Command A (Full Inspection)**:
  ```powershell
  docker inspect helpdesk-web-test
  ```

- **Lab Command B (Extract specific IP Address using Go templates)**:
  ```powershell
  docker inspect --format '{{ .NetworkSettings.IPAddress }}' helpdesk-web-test
  ```
- **Expected Output**:
  ```text
  172.17.0.2
  ```

- **Lab Command C (Extract mapped port binding)**:
  ```powershell
  docker inspect --format '{{ (index (index .NetworkSettings.Ports "80/tcp") 0).HostPort }}' helpdesk-web-test
  ```
- **Expected Output**:
  ```text
  8085
  ```

---

### Command 8: `docker stop`
Gracefully halts a running container by sending `SIGTERM`, followed by `SIGKILL` after a grace period.

- **Syntax**: `docker stop <container-name|id>`
- **Lab Command**:
  ```powershell
  docker stop helpdesk-web-test
  ```
- **Expected Output**:
  ```text
  helpdesk-web-test
  ```
- **Verification**:
  ```powershell
  docker ps
  # helpdesk-web-test no longer appears in running containers
  ```

---

### Command 9: `docker rm`
Removes one or more stopped containers from host disk storage.

- **Syntax**: `docker rm <container-name|id>`
- **Lab Command**:
  ```powershell
  docker rm helpdesk-web-test
  ```
- **Expected Output**:
  ```text
  helpdesk-web-test
  ```

- **Prune command to clean all stopped containers and dangling images**:
  ```powershell
  docker container prune -f
  ```

---

## 5. Lab Record Summary Sheet

### Experiment Title:
**Demonstration of Containerization Lifecycle using Docker on Windows**

### Student Execution Checklist:
| Step # | Task | Command Executed | Status | Verified By |
|---|---|---|---|---|
| 1 | Check Docker Daemon Status | `docker info` | Passed | Local CLI |
| 2 | Pull Lightweight Nginx Image | `docker pull nginx:alpine` | Passed | Docker Hub Registry |
| 3 | Query Local Image Cache | `docker images` | Passed | Local Image Store |
| 4 | Launch Port-Forwarded Service | `docker run -d -p 8085:80 --name helpdesk-web-test nginx:alpine` | Passed | Port 8085 listening |
| 5 | Verify Active Process | `docker ps` | Passed | Health Status `Up` |
| 6 | Read Container Standard Logs | `docker logs helpdesk-web-test` | Passed | Nginx startup logs |
| 7 | Shell Access into Container | `docker exec -it helpdesk-web-test sh` | Passed | Linux shell session |
| 8 | Query Low-Level Metadata | `docker inspect --format '{{.NetworkSettings.IPAddress}}' helpdesk-web-test` | Passed | Bridge IP returned |
| 9 | Graceful Process Termination | `docker stop helpdesk-web-test` | Passed | SIGTERM acknowledged |
| 10 | Garbage Collection & Cleanup | `docker rm helpdesk-web-test` | Passed | Container removed |

---

## 6. Viva Voce Questions & Answers (Docker Basics)

**Q1: What is the difference between an image and a container in Docker?**  
*Answer:* A Docker image is a static, read-only template built from a `Dockerfile` containing the application code, libraries, runtime, and filesystem layers. A Docker container is a dynamic, runnable, isolated instance of that image with a writable container layer added on top.

**Q2: What is the difference between `docker run` and `docker start`?**  
*Answer:* `docker run` creates a *new* container from an image and starts it. `docker start` resumes an *already existing, stopped* container without re-creating it from the base image.

**Q3: What does the `-p 8085:80` flag signify in `docker run`?**  
*Answer:* It binds host machine port `8085` to container internal port `80`. External traffic reaching `http://localhost:8085` is routed across Docker's bridge network into port `80` of the container.

**Q4: How does Docker achieve process isolation without a Hypervisor?**  
*Answer:* Docker uses Linux kernel primitives:
- **Namespaces**: Provide isolation for PIDs, network interfaces, mount points, and inter-process communication.
- **Control Groups (cgroups)**: Enforce hardware resource limits (CPU, RAM, I/O bandwidth).
- **Union Filesystems (UnionFS / OverlayFS)**: Layered filesystems combining image layers into a single cohesive filesystem.

**Q5: What is the purpose of `docker inspect`?**  
*Answer:* It outputs complete, low-level JSON metadata for containers or images, including network configurations, mounted volumes, IP addresses, environment variables, health status, and state information.

**Q6: What is the difference between `docker stop` and `docker kill`?**  
*Answer:* `docker stop` sends `SIGTERM`, allowing the application inside the container 10 seconds to save state, finish requests, and exit cleanly before sending `SIGKILL`. `docker kill` immediately sends `SIGKILL`, terminating the process instantly.
