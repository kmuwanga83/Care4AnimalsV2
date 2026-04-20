# CARE4ANIMALS V2

**CARE4ANIMALS** is a multilingual microlearning platform designed to bridge the veterinary knowledge gap for smallholder farmers in Africa. By combining a modern web experience with a robust SMS fallback, the platform ensures that critical animal welfare education is accessible to everyone, regardless of connectivity or hardware.

---

## 🚀 What’s New in V2
* **Granular Analytics Pipeline:** Integrated tracking for farmer engagement and lesson interactions via the `/analytics/` endpoint.
* **Integrated SMS & Chat:** Fully optimized workflows for SMS-formatted lessons and in-app communication.
* **DevContainer Support:** Standardized development environment for consistent cross-platform onboarding.
* **Refined CMS-to-SMS Pipeline:** Improved logic for publishing multilingual content across Web and SMS channels.

---

## 🛠 Core Features
* **Multilingual Experience:** Bite-sized lessons available in English (**en**), Luganda (**lg**), and Swahili (**sw**).
* **Hybrid Delivery:** * **Smartphone:** React-based PWA for high-engagement learning.
    * **Feature Phone:** Plain-text SMS flows (`TOPICS`, `LESSON <code>`) for offline access.
* **Behavioral Analytics:** Real-time logging of interactions to measure educational impact and behavioral change.
* **Admin CMS:** Simplified API for authoring, translating, and publishing content.

---

## 🏗 System Architecture & Structure

The platform uses a decoupled FastAPI backend and React frontend, supported by a PostgreSQL database and SMS gateway integration.

```text
care4animals/
├── backend/                # FastAPI, SQLAlchemy models, & Analytics logic
├── frontend/               # React (Vite) + TypeScript PWA
├── analytics/              # Data processing & engagement assets
├── sms-flows/              # USSD logic and SMS response templates
├── docs/                   # Architecture diagrams and system documentation
├── scripts/                # Root helper scripts (bootstrap & automation)
└── .devcontainer/          # Dev environment configuration
```

For detailed technical documentation, see:
* **Setup Guide:** `docs/07_architecture_setup_guide.md`
* **SMS Webhook Flow:** `docs/architecture/sequence-sms-webhook.md`

---

## ⚡ Quick Start (Recommended)

### Prerequisites
* **Docker** + **Docker Compose**
* **Python 3** (to execute local seed scripts via bootstrap)

### One-Command Bootstrap
This command starts all services, seeds multilingual lessons, and publishes them automatically:
```bash
./start.sh
```

**Local Endpoints:**
* **Frontend:** [http://localhost:5173](http://localhost:5173)
* **Backend API:** [http://localhost:8000](http://localhost:8000)
* **API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔄 CMS → SMS → Analytics Workflow

1.  **Author & Publish:** Admins create topics and lesson drafts. Once published, lessons are exposed to public endpoints.
2.  **Multilingual Fetch:** The App UI or SMS gateway fetches content based on the user's selected language.
3.  **SMS Interaction:** Low-connectivity users interact via keywords (e.g., `LESSONS <topic>`) to receive plain-text content.
4.  **Data Capture:** Every view—whether via Web or SMS—is captured by the `/analytics/` endpoint to log `event_type` and `metadata_json` for research analysis.

---

## 🧪 Development Notes
* **Data Persistence:** In local Docker setups, the backend utilizes a persistent database volume. 
* **Environment Sync:** If you update `schemas.py` or `models.py`, ensure you run `docker compose restart backend` to refresh the Python process.
* **Line Endings:** We use `.gitattributes` to enforce **LF** line endings, ensuring consistency between Windows hosts and Linux containers.

---

## 🌍 Research Context
This platform is a core component of research into **"Changing farmer behaviours towards good welfare for farm animals in Africa."** It delivers practical, culturally relevant knowledge to empower smallholder communities.

**License:** MIT  
**Lead Developer:** kmuwanga83
```
