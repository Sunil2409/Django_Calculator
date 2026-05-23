# 🧮 Django Calculator — Production-Grade

A full-stack Django web application with user authentication, calculation history, and a complete DevOps pipeline. Containerized with Docker, orchestrated with Kubernetes, and CI/CD automated via GitHub Actions.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   GitHub Actions CI/CD                   │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Lint     │→ │  Test + Cov  │→ │  Docker Build +   │  │
│  │  (flake8) │  │  (PostgreSQL)│  │  Smoke Test       │  │
│  └──────────┘  └──────────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                Docker Compose / Kubernetes               │
│                                                          │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Django   │→ │  PostgreSQL  │  │  Redis (Cache)    │  │
│  │ Gunicorn │  │              │  │                   │  │
│  └──────────┘  └──────────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Features

- **User Authentication** — Signup, login, logout with Django's auth system
- **Calculator** — Add, subtract, multiply, divide with input validation
- **Calculation History** — Persisted per-user with timestamps
- **Health Check** — `/health/` endpoint for container orchestration probes
- **Structured Logging** — Console + file output with configurable levels
- **35+ Unit & Integration Tests** — 80%+ code coverage enforced in CI

## Tech Stack

| Layer          | Technology                           |
|----------------|--------------------------------------|
| Backend        | Django 6.0, Python 3.12              |
| WSGI Server    | Gunicorn (3 workers)                 |
| Database       | PostgreSQL 16 (prod) / SQLite (dev)  |
| Caching        | Redis 7                              |
| Static Files   | WhiteNoise                           |
| Containerization | Docker (multi-stage), Docker Compose |
| Orchestration  | Kubernetes (Deployment, Service, ReplicaSet) |
| CI/CD          | GitHub Actions                       |
| Code Quality   | flake8, coverage                     |

## Quick Start

### Local Development

```bash
cd config
python -m venv env && source env/bin/activate
pip install -r requirements.txt
cp .env.example .env          # Edit with your values
python manage.py migrate
python manage.py runserver
```

### Docker Compose (Recommended)

```bash
cd config
cp .env.example .env
docker compose up --build
```

Access at `http://localhost:8000`. The stack includes Django + PostgreSQL + Redis.

### Kubernetes

```bash
kubectl apply -f calculator-deploy.yaml
kubectl apply -f calculator-service.yaml
kubectl get pods
```

## Running Tests

```bash
cd config
python manage.py test calculator_app -v 2

# With coverage report
coverage run manage.py test calculator_app
coverage report
```

## Project Structure

```
calculator/
├── .github/workflows/ci.yml       # CI/CD pipeline
├── config/                         # Django project root
│   ├── calculator_app/
│   │   ├── models.py               # CalculationHistory model
│   │   ├── operations.py           # Pure arithmetic functions
│   │   ├── views.py                # Views with auth + logging
│   │   ├── tests.py                # 35+ tests
│   │   └── templates/
│   ├── config/settings.py          # Env-driven settings
│   ├── Dockerfile                  # Multi-stage + Gunicorn
│   ├── docker-compose.yml          # Django + PostgreSQL + Redis
│   └── .env.example                # Documented env vars
├── calculator-deploy.yaml          # K8s with health probes
└── calculator-service.yaml         # K8s NodePort service
```

## Environment Variables

| Variable        | Default                    | Description                |
|-----------------|----------------------------|----------------------------|
| `SECRET_KEY`    | `change-me-in-production`  | Django secret key          |
| `DEBUG`         | `False`                    | Debug mode toggle          |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1`      | Comma-separated hostnames  |
| `DATABASE_URL`  | `sqlite:///db.sqlite3`     | Database connection string |
| `REDIS_URL`     | *(empty — cache disabled)* | Redis connection string    |

## License

MIT