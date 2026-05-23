# 🧮 Django Calculator — Production-Grade Web Application

[![CI/CD Pipeline](https://github.com/Sunil2409/Django_Calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/Sunil2409/Django_Calculator/actions)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Django 6.0](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![Code Coverage](https://img.shields.io/badge/Coverage-99%25-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A production-grade Django web application featuring user authentication, persistent calculation history, and a full DevOps pipeline — deployed live on Render with PostgreSQL.

### 🔴 Live Demo: [django-calculator-1.onrender.com](https://django-calculator-1.onrender.com)

---

## 🏗️ System Architecture

```
                        ┌──────────────────────────────┐
                        │       GitHub Repository       │
                        └──────────────┬───────────────┘
                                       │ push / PR
                        ┌──────────────▼───────────────┐
                        │     GitHub Actions CI/CD      │
                        │                               │
                        │  ┌─────────┐  ┌───────────┐  │
                        │  │  Lint   │→ │  Test +   │  │
                        │  │ flake8  │  │  Coverage  │  │
                        │  └─────────┘  └─────┬─────┘  │
                        │                     │        │
                        │              ┌──────▼──────┐ │
                        │              │ Docker Build │ │
                        │              │ Smoke Test   │ │
                        │              └─────────────┘ │
                        └──────────────┬───────────────┘
                                       │ deploy
               ┌───────────────────────▼────────────────────────┐
               │                Render Platform                  │
               │                                                 │
               │  ┌──────────┐  ┌────────────┐  ┌────────────┐  │
               │  │  Django  │  │ PostgreSQL │  │   Redis    │  │
               │  │ Gunicorn │──│   (Prod)   │  │  (Cache)   │  │
               │  │  :8000   │  │            │  │            │  │
               │  └──────────┘  └────────────┘  └────────────┘  │
               └─────────────────────────────────────────────────┘
```

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **User Authentication** | Signup, login, logout with Django's built-in auth + session management |
| **Calculator Engine** | Add, subtract, multiply, divide with input validation and error handling |
| **Calculation History** | Per-user persistent history with timestamps (PostgreSQL-backed) |
| **Health Check API** | `/health/` endpoint for container orchestration and uptime monitoring |
| **Structured Logging** | Console + file logging with configurable levels per module |
| **99% Test Coverage** | 38 unit & integration tests enforced at 80%+ in CI |

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend** | Django 6.0, Python 3.12 | Web framework & business logic |
| **WSGI Server** | Gunicorn (multi-worker) | Production-grade HTTP server |
| **Database** | PostgreSQL 16 / SQLite | Persistent storage (prod / dev) |
| **Caching** | Redis 7 | Response & query caching |
| **Static Files** | WhiteNoise | Compressed static file serving |
| **Containerization** | Docker (multi-stage) | Reproducible builds, non-root user |
| **Orchestration** | Docker Compose, Kubernetes | Multi-container & cluster deployment |
| **CI/CD** | GitHub Actions | Automated lint, test, build pipeline |
| **Hosting** | Render | Live deployment with managed PostgreSQL |
| **Code Quality** | flake8, coverage | Linting & test coverage enforcement |

---

## 🚀 Quick Start

### Local Development (2 minutes)

```bash
git clone https://github.com/Sunil2409/Django_Calculator.git
cd Django_Calculator/config
python -m venv env && source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```
→ Open **http://127.0.0.1:8000**

### Docker Compose (PostgreSQL + Redis)

```bash
cd Django_Calculator/config
cp .env.example .env
docker compose up --build
```
→ Starts Django + PostgreSQL + Redis at **http://localhost:8000**

### Kubernetes

```bash
kubectl apply -f calculator-deploy.yaml
kubectl apply -f calculator-service.yaml
minikube service calculator-service
```

---

## 🧪 Testing & Code Quality

```bash
# Run all 38 tests
python manage.py test calculator_app -v 2

# Run with coverage (99% coverage)
coverage run manage.py test calculator_app
coverage report

# Lint
flake8 calculator_app/ --max-line-length=120 --exclude=migrations
```

| Metric | Value |
|--------|-------|
| Total Tests | 38 |
| Test Classes | 7 (Operations, Auth, Views, History, Health) |
| Code Coverage | **99%** |
| Lint Warnings | 0 |

---

## ☁️ Production Deployment (Render)

### One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Sunil2409/Django_Calculator)

### Manual Setup

1. **Create PostgreSQL** → Render Dashboard → New → PostgreSQL (Free)
2. **Create Web Service** → Connect GitHub repo with these settings:

| Setting | Value |
|---------|-------|
| **Build Command** | `cd config && ./build.sh` |
| **Start Command** | `cd config && python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |

3. **Environment Variables:**

| Key | Value |
|-----|-------|
| `SECRET_KEY` | *(Generate)* |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `DATABASE_URL` | *(PostgreSQL Internal URL)* |
| `PYTHON_VERSION` | `3.12.0` |

---

## 📁 Project Structure

```
Django_Calculator/
├── .github/
│   └── workflows/ci.yml           # CI/CD: lint → test → docker smoke test
├── render.yaml                     # Render Blueprint (one-click deploy)
├── calculator-deploy.yaml          # K8s: 3 replicas, health probes, resource limits
├── calculator-service.yaml         # K8s: NodePort service
│
├── config/                         # Django project root
│   ├── calculator_app/
│   │   ├── models.py               # CalculationHistory model (FK → User)
│   │   ├── operations.py           # Pure functions + custom exceptions + logging
│   │   ├── views.py                # @login_required views + DRY dispatch map
│   │   ├── tests.py                # 38 tests across 7 test classes
│   │   ├── admin.py                # Admin with list_display, filters, search
│   │   └── templates/
│   │
│   ├── config/
│   │   ├── settings.py             # Env-driven (decouple + dj-database-url)
│   │   ├── wsgi.py                 # Gunicorn entry point
│   │   └── urls.py
│   │
│   ├── build.sh                    # Render build: pip, collectstatic, migrate
│   ├── Dockerfile                  # Multi-stage, non-root user, HEALTHCHECK
│   ├── docker-compose.yml          # Django + PostgreSQL + Redis
│   ├── requirements.txt            # Pinned production dependencies
│   └── .env.example                # Documented environment variables
│
└── README.md
```

## 🔐 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `change-me-in-production` | Django cryptographic key |
| `DEBUG` | `False` | Debug mode (never `True` in prod) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated allowed hostnames |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection URI |
| `REDIS_URL` | *(empty)* | Redis cache URI (optional) |
| `RENDER_EXTERNAL_HOSTNAME` | *(auto-set)* | Render's assigned hostname |

## 🔒 Security Considerations

- ✅ Secret key externalized via environment variables (never committed)
- ✅ `DEBUG=False` enforced in production
- ✅ Non-root Docker user (`django:django`)
- ✅ CSRF protection on all forms
- ✅ `@login_required` on protected views
- ✅ Password validation (4 validators)
- ✅ WhiteNoise for secure static file serving

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

## 👤 Author

**Sunil Kumar E** — [GitHub](https://github.com/Sunil2409)