<div align="center">

# 📝 Blog using FastAPI

### Async FastAPI Blog Platform with Authentication & Image Processing

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-asyncpg-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-1.18-DC143C?style=for-the-badge)

A full-stack blog application built with async Python, featuring JWT authentication, image processing, email system, and PostgreSQL — designed as a hands-on backend learning project.

[Live Demo](#) · [API Docs](#api-endpoints) · [Report Bug](https://github.com/wafissh/belajar-fastapi/issues)

</div>

---

## 📌 Overview

This project is a **backend learning journey** — built step-by-step while studying FastAPI, async programming, and production-ready backend patterns. Every line of code is written manually, without AI code generation tools.

> **Core Learning Goals:**
> - Asynchronous Python with FastAPI
> - Database design with SQLAlchemy ORM + Alembic migrations
> - JWT-based authentication & authorization
> - File upload & image processing
> - Email system (SMTP)
> - Docker containerization
> - Automated testing with pytest

---

## 🏗️ Architecture

Client (Browser / API Consumer)
         │
         ▼
┌─────────────────────────┐
│      FastAPI App        │
│  ┌───────────────────┐  │
│  │  Middleware       |  │  ← Security headers, CORS
│  │  Router Layer     │  │  ← /api/users, /api/posts
│  │  Auth Layer       │  │  ← JWT, OAuth2
│  │  Service Layer    │  │  ← Business logic
│  └───────────────────┘  │
│                         │
│  ┌───────────────────┐  │
│  │  SQLAlchemy ORM   │  │  ← Async models, relationships
│  │  Alembic          │  │  ← Schema migrations
│  └───────────────────┘  │
└────────────┬────────────┘
             │
    ┌────────┼────────┐
    ▼        ▼        ▼
 PostgreSQL  S3/     SMTP
 (Database)  Media   (Email) (1/4)


---

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication (access token)
- OAuth2 password flow (`/api/users/token`)
- Password hashing with **pwdlib** (Argon2/crypt)
- Password reset flow via email (forgot → email → reset)
- Role-based access control (owner-only edit/delete)

### 📝 Blog Posts
- Full CRUD operations (Create, Read, Update, Delete)
- Partial update support (PATCH) and full update (PUT)
- Pagination with `skip`/`limit` and `has_more` indicator
- Like/unlike toggle system

### 👤 User Management
- User registration with validation
- Profile picture upload (JPEG/PNG/GIF/WebP)
- Image processing (resize, EXIF transpose, optimization)
- Profile picture deletion
- Public vs private user data (schema separation)

### 📧 Email System
- Async email sending via `aiosmtplib`
- HTML email templates for password reset
- Background task processing (non-blocking)
- Use Email Mocking as a production tools

### 🛡️ Security
- Security headers middleware (X-Frame-Options, HSTS, nosniff)
- Password reset tokens stored as SHA-256 hashes
- Token expiration (configurable)
- Non-root Docker user

### 🏥 DevOps
- Multi-stage Dockerfile (builder → production)
- `.dockerignore` for optimized builds
- PostgreSQL via asyncpg (production-ready)
- Alembic migrations for schema versioning
- Health check endpoint (`/health`)

---

## 🧪 Testing

Tests use **pytest** with **httpx** for async HTTP testing, **moto** for S3 mocking, and transactional rollback for isolation.
bash

Run all testsuv run pytest

Run with verbose output
uv run pytest -v

Run specific test file
uv run pytest test/test_posts.p


### Test Coverage

| Module | Tests | What's Covered |
|--------|-------|----------------|
| `test_user.py` | 4 tests | Registration, duplicate email, validation, password reset email |
| `test_posts.py` | 7 tests | CRUD, authorization, pagination, validation |
| `conftest.py` | — | DB session setup, transaction rollback, auth helpers, S3 mock |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.14+
- PostgreSQL (or use Docker)
- [uv](https://docs.astral.sh/uv/) package manager

### 1. Clone & Setup
bash
git clone https://github.com/wafissh/belajar-fastapi.gitcd belajar-fastapi

Install dependencies
uv sync --all-groups


### 2. Configure Environment
bash
cp .env.example .env
Edit .env with your settings

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@localhost:5432/blog` |
| `SECRET_KEY` | JWT signing key (random hex string) | `openssl rand -hex 32` |

### 3. Run Database Migrations

bash
Apply migrationsuv run alembic upgrade head

### 4. Start the Server
bash
Development (with auto-reload)uv run fastapi dev

Production
uv run fastapi run

API docs available at: `http://localhost:8000/docs`

### 5. Docker (Alternative)

bash
docker build -t blog-api .
docker run -p 8080:8080 --env-file .env blog-api (2/4)


---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `POST` | `/api/users` | Register new user | ❌ |
| `POST` | `/api/users/token` | Login (get JWT) | ❌ |
| `POST` | `/api/users/forgot-password` | Request password reset | ❌ |
| `POST` | `/api/users/reset-password` | Reset password with token | ❌ |

### User Profile

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/users/me` | Get current user profile | ✅ |
| `GET` | `/api/users/{id}` | Get public user profile | ❌ |
| `PATCH` | `/api/users/{id}` | Update user (owner only) | ✅ |
| `DELETE` | `/api/users/{id}` | Delete user (owner only) | ✅ |
| `PATCH` | `/api/users/me/password` | Change password | ✅ |
| `PATCH` | `/api/users/{id}/picture` | Upload profile picture | ✅ |
| `DELETE` | `/api/users/{id}/picture` | Delete profile picture | ✅ |

### Blog Posts

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/api/posts` | Get all posts (paginated) | ❌ |
| `POST` | `/api/posts` | Create new post | ✅ |
| `GET` | `/api/posts/{id}` | Get single post | ❌ |
| `PATCH` | `/api/posts/{id}` | Update post (owner only) | ✅ |
| `PUT` | `/api/posts/{id}` | Full update post (owner only) | ✅ |
| `DELETE` | `/api/posts/{id}` | Delete post (owner only) | ✅ |
| `POST` | `/api/posts/{id}/likes` | Toggle like | ✅ |
| `GET` | `/api/posts/user/{id}` | Get user's posts | ❌ |

---

## 🗃️ Database Schema
┌──────────────┐     ┌──────────────┐     ┌────────────────────┐
│    users     │     │    posts     │     │  password_reset    │
├──────────────┤     ├──────────────┤     ├────────────────────┤
│ id (PK)      │──┐  │ id (PK)      │──┐  │ id (PK)            │
│ username     │  └─>│ user_id (FK) │  └─>│ user_id (FK)       │
│ email        │     │ title        │     │ token_hash         │
│ password_hash│     │ content      │     │ expires_at         │
│ image_file   │     │ date_posted  │     │ created_at         │
│              │     │ likes        │     └────────────────────┘
│              │     └──────────────┘
│              │     ┌──────────────┐
│              │────>│ post_likes   │
│              │     ├──────────────┤
└──────────────┘     │ id (PK)      │
                     │ user_id (FK) │
                     │ post_id (FK) │
                     └──────────────┘
---

## 📁 Project Structure
belajar-fastapi/
├── alembic/                 # Database migrations
│   ├── versions/            # Migration scripts
│   └── env.py               # Alembic configuration
├── routers/
│   ├── users.py             # User endpoints
│   └── posts.py             # Post endpoints
├── templates/               # Jinja2 HTML templates
├── static/                  # CSS, JS, images
├── test/
│   ├── conftest.py          # Test fixtures & setup
│   ├── test_user.py         # User endpoint tests
│   └── test_posts.py        # Post endpoint tests
├── models.py                # SQLAlchemy models
├── schemas.py               # Pydantic schemas
├── auth.py                  # JWT & password utilities
├── database.py              # Async engine & session
├── config.py                # Settings (env-based)
├── email_utils.py           # Async email sender
├── image_utils.py           # Image processing (Pillow)
├── main.py                  # FastAPI app entrypoint
├── alembic.ini              # Alembic config
├── Dockerfile               # Multi-stage Docker build
├── pyproject.toml           # Project metadata & deps
└── uv.lock                  # Locked dependencies (3/4)


---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI 0.138 (async) |
| **Language** | Python 3.14 |
| **ORM** | SQLAlchemy 2.0 (async) |
| **Database** | PostgreSQL (asyncpg) |
| **Migrations** | Alembic |
| **Auth** | JWT (PyJWT) + OAuth2 |
| **Password Hashing** | pwdlib (Argon2/crypt) |
| **Validation** | Pydantic v2 |
| **Email** | aiosmtplib (async SMTP) |
| **Image Processing** | Pillow |
| **File Storage** | Local / AWS S3 (boto3) |
| **Testing** | pytest + httpx + moto |
| **Containerization** | Docker (multi-stage) |
| **Package Manager** | uv |

---

## 📖 What I Learned

Building this project taught me the fundamentals of production-ready backend development:

1. **Async Python** — Why `async/await` matters for I/O-bound operations, and how FastAPI leverages it under the hood.

2. **Database Design** — Normalization, foreign keys, relationships, and why Alembic migrations beat `create_all()`.

3. **Authentication** — The difference between authentication (who are you?) and authorization (what can you do?), JWT lifecycle, and secure password storage.

4. **API Design** — RESTful conventions, proper HTTP status codes, pagination patterns, and schema separation (public vs private data).

5. **Testing** — Why transaction rollback > recreating DB for each test, how to mock external services (S3, SMTP), and the value of test fixtures.

6. **Docker** — Multi-stage builds, layer caching, non-root users, and why `.dockerignore` matters.

7. **Security** — Security headers, token hashing, CSRF awareness, and defense-in-depth principles.

---

## 📄 License

This project is for educational purposes.

---

<div align="center">

**Thanks For Reading**

*No AI code generation tools were used in the development of this project.*

</div>
