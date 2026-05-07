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

## 📲 Africa's Talking + Multi-Channel Notifications Setup

Configure backend environment variables for production-safe notification delivery:

```bash
# Africa's Talking (sandbox by default)
AT_USERNAME=sandbox
AT_API_KEY=your_africas_talking_api_key
AT_SENDER_ID=
AT_WEBHOOK_TOKEN=strong-shared-secret
# Optional: comma-separated IPs or CIDRs (only checked when AT_WEBHOOK_TOKEN is unset)
AT_WEBHOOK_ALLOWED_IPS=
SMS_MAX_RETRIES=3
SMS_RETRY_BACKOFF_SECONDS=0.5

# Email (SMTP)
EMAIL_PROVIDER=smtp
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your_smtp_user
SMTP_PASSWORD=your_smtp_password
SMTP_USE_TLS=true
EMAIL_FROM=no-reply@care4animals.org
```

### SMS webhook endpoint

- Configure Africa's Talking inbound callback URL to: `POST /api/v1/sms/callback`
- Expected payload fields include: `from`, `to`, `text`, `date`, `id`, `linkId`
- If `AT_WEBHOOK_TOKEN` is configured, send it via `X-AT-Webhook-Token` header (recommended).
- If no shared secret is used, set `AT_WEBHOOK_ALLOWED_IPS` to Africa's Talking source IPs/CIDRs from their docs (less robust behind proxies unless you trust `X-Forwarded-For`).

### Notification APIs

- `POST /api/v1/notifications/send` sends a message by requested channels while respecting user preferences.
- `POST /api/v1/notifications/reminders` sends lesson/system reminders with SMS-first fallback: `sms -> email -> push`.

### User preferences

Users can opt channels in/out using these fields on `user_profiles`:
- `notify_sms`
- `notify_email`
- `notify_push`
- `email` and `push_token` must be set for corresponding channels.

---
## 🤝 Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting a pull request.

## 🌍 Research Context
This platform is a core component of research into **"Changing farmer behaviours towards good welfare for farm animals in Africa."** It delivers practical, culturally relevant knowledge to empower smallholder communities.

**License:** MIT  
**Lead Developer:** kmuwanga83
