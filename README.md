# 🧩 MicroServices_Architecture
This project demonstrates two independent **FastAPI-based microservices** that can be run and tested locally:

1. **Search & Filter Service** — provides text-based task search, status filtering, and sorting.
2. **Task Completion Service** — manages task/subtask completion and reopening actions.

Each service runs independently and exposes its own `/health` endpoint.

---

## 🗂️ Project Structure
MicroServices_Architecture/
│
├── search_filter_service/
│ ├── init.py
│ └── main.py
│
├── taskcompletion_service/
│ ├── init.py
│ └── main.py
│
├── requirements.txt

---

---

## ⚙️ Requirements

- **Python 3.11 – 3.13 (recommended)**  
  Pydantic v2’s core (`pydantic-core`) currently does **not** support Python 3.14.  
  If you are on 3.14, you’ll need to create a 3.12 virtual environment (see below).

- Dependencies listed in `requirements.txt`:
  ```text
  fastapi==0.115.0
  uvicorn==0.32.0
  pydantic==2.9.0