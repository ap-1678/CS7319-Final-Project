<<<<<<< HEAD

# CS7319 Final Project – Unselected Microservices (User & Task)

## Overview
This project implements two independent **FastAPI microservices**:
1. **User-Service** – handles user profile creation, retrieval, and deletion.
2. **Task-Service** – manages task creation and deletion linked to users.

Each service runs as its **own process** with its own API routes, state, and data ownership.  
They communicate via HTTP/JSON (not internal imports), following an microservice architecture.

---

## Architecture Summary
| Component | Description | Port | Connector Type |
|------------|--------------|------|----------------|
| `User-Service` | Manages users (create/get/delete). Owns user data and validation logic. | 8001 | REST/JSON |
| `Task-Service` | Manages tasks (create/delete). Owns task data. References user ID from User-Service. | 8002 | REST/JSON |

**Microservice evidence:**
- Independent processes (`uvicorn` servers on different ports).  
- Own data stores (in-memory `DB` dicts).  
- HTTP communication boundaries (no cross-imports).  
- Per-service health checks and OpenAPI documentation.  
- Independent scaling, isolation, and fault tolerance.

---

## Setup & Installation

# Clone the repo
git clone https://github.com/ap-1678/CS7319-Final-Project.git
cd CS7319-Final-Project

# Create a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

---

## Access URLs

Once both services are running locally, open these links in your browser:

| Service | Swagger UI | Base URL |
|----------|-------------|-----------|
| **User-Service** | [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs) | http://127.0.0.1:8001 |
| **Task-Service** | [http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs) | http://127.0.0.1:8002 |








=======
CS7319 Group 7
Layered Architecture (using Python/Flask):
Presentation (routes) → Service (rules) → Repository (DB I/O) → Database (SQLite via SQLAlchemy)

taskmgr_layered/
├─ app.py
├─ db.py
├─ models/
│  └─ user.py
├─ repositories/
│  └─ user_repository.py
├─ services/
│  └─ user_service.py
└─ presentation/
   └─ auth_routes.py

1. Start app: python app.py
2. Visit http://127.0.0.1:5000/ for the page.
3. Sign Up (creates a profile and auto-logs in).

Layered Architecture (Flask) app with a real Task Manager that appears after login,
supports main tasks and sub-tasks, and computes overall progress from sub-tasks.

4. After login/sign-up, users are sent to /app (a simple Task Manager UI).
Tasks: title, description, due date, notes.
Sub-tasks: title, description, priority, due date, done/undone.
Progress: if a task has sub-tasks, progress = done / total (as a %).
If no sub-tasks, progress is 0%.
>>>>>>> Selected/src-WithSearch
