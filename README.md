# CARE4ANIMALS V2

**CARE4ANIMALS: A Microlearning Platform for Empowering Farmers with Bite-Sized Animal Wellness Knowledge**

CARE4ANIMALS is a mobile-oriented microlearning platform designed to enhance livestock welfare by providing small-scale farmers with practical knowledge through concise, multimedia educational modules. The platform supports hybrid access via a mobile-friendly web app and offline SMS-based lessons.

## Core Goals
- Deliver bite-sized animal welfare modules through web and SMS
- Support multilingual learning in English, Luganda, and Swahili
- Improve farmer knowledge, practices, and livestock welfare outcomes
- Enable low-tech and low-connectivity access

## Tech Stack
- **Backend:** FastAPI, PostgreSQL, SQLAlchemy
- **Frontend:** React, Vite, TypeScript, PWA-ready
- **SMS/USSD:** RapidPro/Viamo via webhooks
- **Analytics:** Python (pandas, scipy), SPSS

## Monorepo Structure
```text
Care4AnimalsV2/
├── backend/
├── frontend/
├── docs/
├── sms-flows/
├── analytics/
├── docker-compose.yml
└── .env.example
```

## Initial API Routes
- `GET /health`
- `GET /api/v1/languages`
- `GET /api/v1/topics`
- `GET /api/v1/lessons`
- `GET /api/v1/lessons/{lesson_id}`
- `POST /api/v1/sms/webhook`
- `POST /api/v1/analytics/events`
