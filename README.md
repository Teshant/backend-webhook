# Lyftr Backend Assignment

This repository contains a Dockerized FastAPI backend service built as part of the Lyftr backend assignment.

The service ingests webhook events, stores them in SQLite with idempotency guarantees, and exposes APIs for querying messages, statistics, health checks, and metrics.

---

## 🚀 How to Run

### Prerequisites
- Docker Desktop (Linux containers)
- Docker Compose v2+

### Steps

```bash
docker compose up -d --build
