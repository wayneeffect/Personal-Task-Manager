# Resilient Task Manager (Full-Stack MVP)

A hardened, full-stack personal task management application engineered with strict input validation boundaries, centralized server-side error boundaries, automated transaction rollbacks, and infrastructure-as-code deployment profiles. 

Unlike standard local-only client applications, this platform features an active backend pipeline paired with persistent relational data layers to maintain a zero-loss state runtime environment.

---

## 🛠️ Architectural Blueprint & Methodology

The development life cycle of this application strictly adheres to production software completeness metrics:


```

[ MoSCoW Framework ] ──> Focuses scope on Core CRUD workflows, ignoring multi-user bloat.
[ Completeness List ] ──> Hardens inputs, isolates environments, and establishes telemetry.
[ Resilient Layer ]   ──> Wraps all API and DB interfaces in global exception handlers.

```

### 1. The MoSCoW Blueprint
*   **Must Have:** Asynchronous JSON REST API endpoints, automated relational SQLite compilation, deployment compatibility via Python WSGI (`gunicorn`), and persistent disk volume states.
*   **Should Have:** Unified client-side network error messaging, frontend state validation boundaries, and a responsive mobile-first UI interface.
*   **Could / Won't Have:** Multi-user authentication tables, OAuth2 login modules, or third-party web-hook pushes (deliberately omitted to minimize service footprint and maximize operational simplicity).

### 2. Software Completeness & Guardrails
*   **Data Integrity Protection:** Any anomalous operation targeting the storage block triggers an immediate database statement fallback (`db.session.rollback()`), preventing write collisions and engine freezes.
*   **Defensive Boundary Enforcement:** Strict payload filtering on both the client (max length attributes) and server-side strings blocks malicious scripts, overflow scripts, or malformed parameters.
*   **Proactive System Telemetry:** Includes a dedicated `/health` endpoint to allow cloud infrastructure managers to automatically verify database and application availability.

---

## 🏗️ System Architecture

*   **Backend Runtime:** Python 3 (Flask Micro-framework)
*   **Production WSGI Server:** Gunicorn
*   **Storage Tier:** SQLite (Isolated persistently via targeted block mount storage paths)
*   **Frontend Stack:** Semantic, responsive HTML5 / Utility-focused CSS3 / Native Asynchronous JavaScript (Vanilla ES6 Architecture)

---

## 🚀 Installation & Local Environment Spin-Up

To run the application locally for testing or feature iteration, execute the following commands in your terminal terminal:

```bash
# 1. Clone the repository structure
git clone [https://github.com/your-username/your-repository.git](https://github.com/your-username/your-repository.git)
cd your-repository

# 2. Create and engage an isolated virtual runtime environment
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Inject explicit dependencies
pip install -r requirements.txt

# 4. Fire up the local framework kernel
python3 app.py

```

The application will launch on `http://127.0.0.1:5000/`. A local development database file (`tasks.db`) will generate dynamically within your project directory.

---

## ☁️ Cloud Infrastructure Deployment (Render)

This project contains an active `render.yaml` infrastructure specification. Deploying to production requires zero manual platform UI adjustments:

1. Push this complete file directory structure to your **GitHub** account.
2. Access your **Render Dashboard**, choose **New +**, and click on **Blueprint**.
3. Select and authorize your task manager repository.
4. Render will parse the internal configurations, automatically mount a **1GB Persistent Disk Volume** at `/var/data/`, bind the SQLite database pipeline, run the gunicorn initialization sequence, and generate your live application URL.

*Note: Because Render mounts a persistent storage disk directly to the application container, your stored tasks will survive automatic server spin-downs, maintenance cycles, and system redeploys.*

```

```
