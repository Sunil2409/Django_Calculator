# 🧮 Django Calculator — Production-Grade

A full-stack Django web application with user authentication, calculation history, and a complete DevOps pipeline. Containerized with Docker, orchestrated with Kubernetes, and CI/CD automated via GitHub Actions.

**🔴 Live Demo:** [https://django-calculator-xxxx.onrender.com](https://django-calculator-xxxx.onrender.com) *(update after deploy)*

---

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
│              Render / Docker / Kubernetes                 │
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
- **35+ Unit & Integration Tests** — 99% code coverage enforced in CI

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
| Hosting        | Render (Web Service + PostgreSQL)    |
| Code Quality   | flake8, coverage                     |

---

## 🚀 Deploy to Render (Production)

### Option A: One-Click Blueprint Deploy

1. Fork this repository
2. Go to [https://render.com/deploy](https://render.com/deploy)
3. Connect your GitHub account and select this repo
4. Render reads `render.yaml` and auto-creates:
   - A **Web Service** (Django + Gunicorn)
   - A **PostgreSQL database** (free tier)
5. Click **Apply** — your app will be live in ~3 minutes

### Option B: Manual Setup (Step-by-Step)

#### Step 1 — Create a PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/) → **New** → **PostgreSQL**
2. Fill in:
   - **Name:** `calculator-db`
   - **Database:** `calculator_db`
   - **User:** `calculator_user`
   - **Plan:** Free
3. Click **Create Database**
4. Copy the **Internal Database URL** (you'll need it in Step 2)

#### Step 2 — Create a Web Service

1. Go to **New** → **Web Service** → Connect your GitHub repo
2. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `django-calculator` |
| **Root Directory** | `config` |
| **Runtime** | Python |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |
| **Plan** | Free |

3. Add **Environment Variables**:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | *(click "Generate" to create a random key)* |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `DATABASE_URL` | *(paste the Internal Database URL from Step 1)* |
| `PYTHON_VERSION` | `3.12.0` |

4. Click **Create Web Service** — Render will run `build.sh`, install deps, migrate the DB, and start Gunicorn.

#### Step 3 — Create a Superuser (Optional)

1. Go to your Web Service → **Shell** tab
2. Run:
   ```bash
   python manage.py createsuperuser
   ```

#### Step 4 — Verify

- Visit `https://your-app-name.onrender.com/` → Login page
- Visit `https://your-app-name.onrender.com/health/` → `{"status": "healthy"}`
- Visit `https://your-app-name.onrender.com/admin/` → Django admin

---

## 💻 Local Development

```bash
# Clone
git clone https://github.com/Sunil2409/Django_Calculator.git
cd Django_Calculator/config

# Virtual environment
python -m venv env && source env/bin/activate

# Install & run
pip install -r requirements.txt
cp .env.example .env          # Edit with your values
python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000/**

### Docker Compose (Local Multi-Container)

```bash
cd config
cp .env.example .env
docker compose up --build
```

Starts Django + PostgreSQL + Redis at **http://localhost:8000**

---

## 🧪 Running Tests

```bash
cd config
source ../env/bin/activate

# Run all 38 tests
python manage.py test calculator_app -v 2

# With coverage report
coverage run manage.py test calculator_app
coverage report    # 99% coverage
```

---

## 📁 Project Structure

```
Django_Calculator/
├── .github/workflows/ci.yml       # CI/CD: lint → test → docker build
├── render.yaml                     # Render Blueprint (one-click deploy)
├── calculator-deploy.yaml          # K8s Deployment (health probes + limits)
├── calculator-service.yaml         # K8s NodePort Service
├── config/                         # Django project root
│   ├── calculator_app/
│   │   ├── models.py               # CalculationHistory model
│   │   ├── operations.py           # Pure arithmetic + custom exceptions
│   │   ├── views.py                # Auth-protected views + logging
│   │   ├── tests.py                # 38 tests across 7 test classes
│   │   └── templates/
│   ├── config/settings.py          # Env-driven (decouple + dj-database-url)
│   ├── build.sh                    # Render build script
│   ├── Dockerfile                  # Multi-stage + Gunicorn + non-root user
│   ├── docker-compose.yml          # Django + PostgreSQL + Redis
│   ├── requirements.txt
│   └── .env.example                # Documented env vars
└── README.md
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `change-me-in-production` | Django secret key |
| `DEBUG` | `False` | Debug mode toggle |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated hostnames |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection string |
| `REDIS_URL` | *(empty — cache disabled)* | Redis connection string |
| `RENDER_EXTERNAL_HOSTNAME` | *(auto-set by Render)* | Render hostname |

## License

MIT