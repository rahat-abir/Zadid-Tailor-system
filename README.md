# Zadid Tailor System (in progress)

A full-stack management system for a tailoring shop, focused on digitising customer measurements, orders, and delivery tracking.

> Status: Early work-in-progress. Expect changes and incomplete features.

---

## Features (in progress)

- Customer management (name, phone, address, notes)
- Measurement records for different garment types (e.g. panjabi, shirt, pant, etc.)
- Order management (style details, fabric info, trial/delivery dates)
- Basic dashboard for recent customers and upcoming deliveries
- Search/filter over customers and orders
- Dockerised local development setup (backend, frontend, MySQL)

---

## Tech Stack

- **Backend:** Python (see `app/`)
- **Frontend:** TypeScript + React (see `frontend/`)
- **Database:** MySQL
- **DevOps:** Docker & Docker Compose

Languages by repo (from GitHub):

- Python
- TypeScript
- CSS
- JavaScript
- Dockerfile
- HTML

---

## Project Structure


```Stracture
├── app/                # Python backend application
├── frontend/           # TypeScript/React frontend app
├── Dockerfile          # Backend Docker image
├── docker-compose.yml  # Local dev stack (backend, frontend, MySQL)
├── requirements.txt    # Python dependencies
└── .gitignore
```
For framework-specific details, check inside app/ and frontend/ as they evolve.

Prerequisites

- Git
- Docker & Docker Compose

Clone the repository

Run with Docker
```
docker compose up --build
```

If you see an error like:

Bind for ```0.0.0.0:3307 failed: port is already allocated ```

Either stop the existing MySQL on that port, or change the mapped port in docker-compose.yml.

# Roadmap / Next Ideas
Some possible next steps for the project:
-Authentication & roles (admin vs. staff)
-More detailed dashboard metrics (monthly orders, pending deliveries)
-Multi-branch support for multiple tailor shops
-Deployment pipeline (build & push Docker images to a server)
