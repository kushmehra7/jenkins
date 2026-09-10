# 🚀 Jenkins Dockerized CI/CD: High-Performance, Zero-Cost Alternative to GitHub Actions

A production-ready, containerized Jenkins CI/CD environment with **persistent mount volumes**, **isolated Docker agent execution**, and a declarative **Ruff linting & Pytest pipeline**.

This repository implements the **Zero-Cost Hybrid Architecture**:
- **GitHub** is used purely for free cloud Git storage and team collaboration.
- **Jenkins** runs locally (or on your private server/VPS) to execute all CI/CD jobs on-demand via the web UI.
- **$0.00 per-minute runner charges:** GitHub Actions workflows are completely bypassed, eliminating cloud CI runner billing while giving you unlimited, ultra-fast builds with local caching.

---

## 🏗️ Architecture Overview

```
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                       DEVELOPER WORKFLOW                                │
 │                                                                         │
 │  1. Write Code (Python / App)                                           │
 │  2. git push origin <branch> (Free storage on GitHub)                   │
 └────────────────────────────┬────────────────────────────────────────────┘
                              │
                              ▼
 ┌─────────────────────────────────────────────────────────────────────────┐
 │                      GITHUB (Cloud Storage)                             │
 │                                                                         │
 │  • Repository: git@github.com:kushmehra7/jenkins.git                    │
 │  • Storage & PR Collaboration (Zero GitHub Actions runners used)        │
 └────────────────────────────▲────────────────────────────────────────────┘
                              │
                              │ 4. Outbound Pull (git fetch/clone)
                              │    (No public IP or webhooks required!)
                              │
 ┌────────────────────────────┴────────────────────────────────────────────┐
 │                  JENKINS DOCKER STACK (Local / VPS)                     │
 │                                                                         │
 │  ┌───────────────────────────────────────────────────────────────────┐  │
 │  │ 3. Developer clicks "Build with Parameters" in Jenkins UI         │  │
 │  │    (Selects branch: main, staging, or feature/xyz)                │  │
 │  └───────────────────────────────┬───────────────────────────────────┘  │
 │                                  │                                      │
 │  ┌───────────────────────────────▼───────────────────────────────────┐  │
 │  │ Jenkins Controller (Port 8080)                                    │  │
 │  │ • Persistent Volume: jenkins_data (/var/jenkins_home)             │  │
 │  │ • Pre-baked plugins: git, workflow-aggregator, docker-workflow    │  │
 │  │ • Docker Socket: /var/run/docker.sock                             │  │
 │  └───────────────────────────────┬───────────────────────────────────┘  │
 │                                  │                                      │
 │  ┌───────────────────────────────▼───────────────────────────────────┐  │
 │  │ Ephemeral Docker Agent (python:3.11-slim)                         │  │
 │  │  Stage 1: Checkout specified branch                               │  │
 │  │  Stage 2: Ruff Lint (ruff check .)                                │  │
 │  │  Stage 3: Ruff Format Check (ruff format --check .)               │  │
 │  │  Stage 4: Unit Tests (pytest -v tests/)                           │  │
 │  └───────────────────────────────────────────────────────────────────┘  │
 └─────────────────────────────────────────────────────────────────────────┘
```

---

## 🌟 Why This Replaces GitHub Actions

| Feature | GitHub Actions Cloud Runners | Self-Hosted Jenkins in Docker |
| :--- | :--- | :--- |
| **Billing Model** | Per-minute billing ($0.008/min+ per runner) | **$0.00** (Unlimited builds, flat hardware cost) |
| **WIP Commit Waste** | Auto-triggers on every push, draining minutes | **Intentional execution** via web UI or scheduled SCM |
| **Dependency Caching**| Downloads Python & pip dependencies every run | Persistent local Docker & pip cache (seconds vs minutes)|
| **Network Security** | Requires public webhooks and inbound exposure | **Outbound only** (runs behind NAT/firewall without tunnels) |
| **Data Privacy** | Code executes on shared third-party VMs | Runs inside your private Docker environment |

---

## 📁 Repository Structure

```
.
├── .env.example              # Configurable ports and environment variables
├── .gitignore                # Excludes Python caches, Jenkins runtime, and secrets
├── docker-compose.yml        # Multi-container/volume definition with docker socket binding
├── Jenkinsfile               # Declarative, parameterized CI pipeline script
├── pyproject.toml            # Code quality rules: Ruff linter, formatter & Pytest
├── jenkins/
│   ├── Dockerfile            # Jenkins LTS controller with Docker CLI pre-installed
│   └── plugins.txt           # Pre-installed plugin manifest (git, pipeline, docker)
├── src/
│   ├── __init__.py
│   └── app.py                # Sample Python application logic
└── tests/
    ├── __init__.py
    └── test_app.py           # Unit tests validating application functions
```

---

## ⚙️ Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (Docker Engine 20.10+ / Docker Desktop)
- [Docker Compose](https://docs.docker.com/compose/) (v2.0+)
- [Git](https://git-scm.com/)

---

## 🚀 Quick Start Guide

### Step 1: Clone the Repository & Configure Environment

```bash
git clone git@github.com:kushmehra7/jenkins.git
cd jenkins

# Copy the environment file template
cp .env.example .env
```

### Step 2: Launch the Jenkins Container

```bash
docker compose up -d --build
```

Verify that the container is healthy:
```bash
docker compose ps
```

### Step 3: Retrieve the Initial Admin Password

Jenkins generates a one-time administrator password upon first initialization:

```bash
docker exec jenkins-controller cat /var/jenkins_home/secrets/initialAdminPassword
```
*Copy the 32-character alphanumeric key output to your clipboard.*

---

## 🖥️ Jenkins Web UI Setup (One-Time)

1. Open your browser and navigate to: **`http://localhost:8080`**
2. Paste the **Administrator password** retrieved in Step 3 and click **Continue**.
3. On the *Customize Jenkins* page:
   - Click **Select plugins to install** or **Install suggested plugins**. Since our Docker image already bakes in `git`, `workflow-aggregator`, and `docker-workflow`, this completes almost instantly.
4. Create your **First Admin User** (or continue as `admin`) and set your Jenkins URL to `http://localhost:8080/`.

---

## 🔑 Configure GitHub Access (For Private Repos)

If your repository is private, grant Jenkins read access to pull the code:

1. In GitHub, go to **Settings** → **Developer settings** → **Personal access tokens (classic)**.
2. Generate a token with the **`repo`** (Read) scope.
3. In Jenkins:
   - Navigate to **Manage Jenkins** → **Credentials** → **System** → **Global credentials (unrestricted)**.
   - Click **Add Credentials**:
     - **Kind**: *Username with password*
     - **Username**: Your GitHub username
     - **Password**: Your GitHub Personal Access Token (PAT)
     - **ID**: `github-credentials`
     - **Description**: `GitHub Access Token`
   - Click **Create**.

*(If your repo is public, you can skip this step entirely!)*

---

## 🛠️ Creating the CI Pipeline Job

1. In the Jenkins dashboard, click **New Item** on the left menu.
2. Enter an item name (e.g. `python-lint-ci`) and select **Pipeline**. Click **OK**.
3. Scroll down to the **Pipeline** section:
   - **Definition**: Select **Pipeline script from SCM**.
   - **SCM**: Select **Git**.
   - **Repository URL**: `https://github.com/kushmehra7/jenkins.git` (or your repository URL).
   - **Credentials**: Select `github-credentials` (or *None* if public).
   - **Branch Specifier**: `*/${BRANCH_NAME}` (or `*/main`).
   - **Script Path**: `Jenkinsfile`
4. Check the box **"This project is parameterized"**:
   - Add a **String Parameter**:
     - **Name**: `BRANCH_NAME`
     - **Default Value**: `main`
     - **Description**: `Git branch or tag to build and test`
5. Click **Save**.

---

## 🎯 Running Your First Build

1. Click **Build with Parameters** in the left sidebar of your job.
2. Select or enter the branch you want to test:
   - `BRANCH_NAME`: `main`
   - `CHECK_FORMAT`: `true`
   - `RUN_TESTS`: `true`
3. Click **Build**.
4. Click on the build number (e.g. `#1`) → **Console Output** to watch the stages live:
   - ✅ **Environment Info**: Python runtime verification.
   - ✅ **Install Dependencies**: Ruff and Pytest installed inside container agent.
   - ✅ **Lint & Static Analysis**: `ruff check .` validates code quality.
   - ✅ **Format Verification**: `ruff format --check .` validates formatting.
   - ✅ **Unit Tests**: `pytest -v tests/` executes tests.

---

## ⚡ Local Development with `uv` (Recommended)

This project uses [`uv`](https://github.com/astral-sh/uv) for ultra-fast Python virtual environments and package resolution.

### 1. Initialize Virtual Environment with `uv`

```bash
# Create an isolated virtual environment (.venv)
uv venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install the project and development dependencies in editable mode
uv pip install -e ".[dev]"
```

Alternatively, you can install from the compiled lockfile:
```bash
uv pip install -r requirements-dev.txt
```

### 2. Run Checks Locally using `uv run`

You can run Ruff and Pytest directly through `uv` without manually activating the virtualenv:

```bash
# Run Ruff linting
uv run ruff check .

# Run Ruff formatting check
uv run ruff format --check .

# Automatically fix formatting
uv run ruff format .

# Run unit tests
uv run pytest -v
```

*(If you prefer standard pip instead of uv, `python -m venv .venv` and `pip install -e ".[dev]"` work identically!)*

---

## 🔄 Optional: SCM Polling (Automated Without Webhooks)

If you ever want Jenkins to automatically detect changes on GitHub without manually clicking "Build":
1. Open your pipeline job → **Configure**.
2. Under **Build Triggers**, check **Poll SCM**.
3. Set the schedule:
   ```cron
   H/15 * * * *
   ```
   *(Checks GitHub every 15 minutes for new commits. If no commits were pushed, no build is run. Zero inbound ports, zero ngrok tunnels, zero webhook costs!)*

---

## 📦 Data Persistence & Maintenance

- **Data Volume**: All pipeline definitions, plugins, secrets, and build logs are stored inside the Docker volume `jenkins_data`.
- **Stopping Jenkins**:
  ```bash
  docker compose down
  ```
- **Restarting Jenkins** (all data is preserved):
  ```bash
  docker compose up -d
  ```
- **Backing up Jenkins Data**:
  ```bash
  docker run --rm -v jenkins_data:/volume -v $(pwd):/backup alpine tar -czf /backup/jenkins_backup.tar.gz -C /volume .
  ```

---

## 🛡️ License

MIT License. Feel free to use and adapt this setup for your organization's CI/CD infrastructure!
