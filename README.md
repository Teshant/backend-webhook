# Backend Webhook Service

This is a Dockerized FastAPI backend service.

It:
- Receives webhook events
- Verifies webhook signatures using HMAC
- Stores data in SQLite with idempotency
- Exposes APIs for messages, stats, health, and metrics

---

## 🚀 How to Run

### Requirements
- Docker Desktop
- Docker Compose

---

## ⚠️ REQUIRED CONFIGURATION (READ THIS)

Before running the service, you **MUST** create a `.env` file.

### `.env` file (REQUIRED)

Create a file named `.env` in the project root with **EXACTLY** these variables:

```env
WEBHOOK_SECRET=your_own_secret_value
DATABASE_URL=sqlite:////data/app.db

