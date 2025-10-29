# Menagerie - FastAPI REST Service
A small **Pet Menagerie REST API** built with **FastAPI**, **Pydantic**, and **SQLAlchemy**.

---

## Prerequisites

* Python 3.9+
* Git

---

## Clone Repository

```bash
git clone https://github.com/ridhima-khandelwal028/menagerie.git
cd menagerie
```

---

## Create and Activate Virtual Environment

### Windows

```bash
python -m venv env
env\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv env
source env/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup with Alembic

### Initialize Alembic

```bash
alembic init alembic
```

### Create Migration Script

```bash
alembic revision --autogenerate -m "Initial migration"
```

### Apply Migrations

```bash
alembic upgrade head
```
---

## Run Application

## Run App

```bash
uvicorn app.main:app --reload
```

---

## API Docs

Once running, access interactive API documentation at:

* Swagger UI: [http://127.0.0.1:8000/docs]
* ReDoc: [http://127.0.0.1:8000/redoc]

---
