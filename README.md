<!-- ORBIT WORDMARK -->
<div align="center">

```
 ██████╗ ██████╗ ██████╗ ██╗████████╗
██╔═══██╗██╔══██╗██╔══██╗██║╚══██╔══╝
██║   ██║██████╔╝██████╔╝██║   ██║   
██║   ██║██╔══██╗██╔══██╗██║   ██║   
╚██████╔╝██║  ██║██████╔╝██║   ██║   
 ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚═╝   ╚═╝  
```

### NVIDIA ISV Intelligence Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GCP%20Cloud%20Run-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://orbit-isv-platform-474576936406.us-central1.run.app)
[![NVIDIA NIM](https://img.shields.io/badge/Powered%20By-NVIDIA%20NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/nim)
[![DGX Cloud](https://img.shields.io/badge/Built%20For-DGX%20Cloud-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://www.nvidia.com/en-us/data-center/dgx-cloud/)

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2.0-499848?style=flat-square&logo=gunicorn&logoColor=white)](https://gunicorn.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![GCP Cloud Run](https://img.shields.io/badge/GCP-Cloud%20Run-4285F4?style=flat-square&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![SendGrid](https://img.shields.io/badge/SendGrid-Email%20Reports-1A82E2?style=flat-square&logo=sendgrid&logoColor=white)](https://sendgrid.com)
[![Leaflet](https://img.shields.io/badge/Leaflet-World%20Map-199900?style=flat-square&logo=leaflet&logoColor=white)](https://leafletjs.com)

</div>

---

> Built as a portfolio project for the **Senior Developer Relations Manager (DGX Cloud)** role at NVIDIA — JR2008417

Orbit is an agentic ISV onboarding and adoption intelligence platform built on NVIDIA NIM and DGX Cloud. It automates the pre-work of ISV developer relations — learning who a software vendor is, what they build, and what they need — then uses multi-model NIM inference to generate a personalized DGX Cloud adoption strategy, deliverable, and concern responses in a single flow.

| Role | Access Code |
|---|---|
| ISV Team | `ORBIT-ISV-2025` |
| Admin / DevRel Manager | `ORBIT-ADMIN-2025` |

---

## What This Demonstrates

This project directly maps to the responsibilities of the DGX Cloud DevRel role:

| Role Requirement | Orbit Implementation |
|---|---|
| Evangelize DGX Cloud to ISV partners | Conversational intake surfaces NIM microservices and DGX Cloud integration patterns specific to each ISV |
| Develop go-to-market with strategic ISVs | ISV registry grounded in NVIDIA partner data, Nemotron pre-fills company profile automatically |
| Create assets for conferences and hackathons | Generates Workshop guides, Jupyter Notebooks, and Hackathon briefs as downloadable deliverables |
| Build developer adoption programs | Learning style inference routes each ISV to their preferred adoption format |
| Measure ISV adoption and engagement | Admin dashboard with drop-off analytics, format preferences, world map, and monthly DevRel report |
| Drive ISV integrations with the NVIDIA ecosystem | GCP Service Usage API detects new ISV tech stack additions and triggers Orbit chat alerts |

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Orbit Platform                    │
│              Flask + Python + Gunicorn               │
│            Deployed on GCP Cloud Run                 │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼────────┐
│  NVIDIA NIM    │   │   Google Cloud  │
│  ─────────────-│   │  ──────────────-│
│  Nemotron 49B  │   │  Cloud Run      │
│  Llama 3.1 8B  │   │  Service Usage  │
│  Mistral       │   │  API (Stack     │
│  Small 4       │   │  Detection)     │
└────────────────┘   └─────────────────┘
```

### Model Routing

| Model | Provider | Role in Orbit |
|---|---|---|
| `llama-3.3-nemotron-super-49b-v1` | NVIDIA NIM | ISV recommendations, concern responses, Orbit chat, workshop/hackathon generation |
| `llama-3.1-8b-instruct` | Meta via NIM | Learning style inference from format ranking |
| `mistral-small-4-119b-2603` | Mistral via NIM | Jupyter Notebook code generation |

---

## Tech Stack

### Core
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=gunicorn&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=flat-square&logo=jinja&logoColor=white)

### AI & Inference
![NVIDIA](https://img.shields.io/badge/NVIDIA%20NIM-76B900?style=flat-square&logo=nvidia&logoColor=white)
![Nemotron](https://img.shields.io/badge/Nemotron%2049B-76B900?style=flat-square&logo=nvidia&logoColor=white)
![Llama](https://img.shields.io/badge/Llama%203.1%208B-0467DF?style=flat-square&logo=meta&logoColor=white)
![Mistral](https://img.shields.io/badge/Mistral%20Small%204-FF7000?style=flat-square)

### Cloud & Infrastructure
![GCP](https://img.shields.io/badge/Google%20Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud%20Run-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![Cloud Build](https://img.shields.io/badge/Cloud%20Build-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![Artifact Registry](https://img.shields.io/badge/Artifact%20Registry-4285F4?style=flat-square&logo=googlecloud&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

### APIs & Services
![SendGrid](https://img.shields.io/badge/SendGrid-1A82E2?style=flat-square&logo=sendgrid&logoColor=white)
![ipinfo](https://img.shields.io/badge/ipinfo.io-Geolocation-333333?style=flat-square)
![GCP Service Usage](https://img.shields.io/badge/GCP%20Service%20Usage%20API-Stack%20Detection-4285F4?style=flat-square&logo=googlecloud&logoColor=white)

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white)
![Google Fonts](https://img.shields.io/badge/Syne%20+%20DM%20Sans-4285F4?style=flat-square&logo=googlefonts&logoColor=white)

### Partner Integrations (Surfaced in Recommendations)
![Anthropic](https://img.shields.io/badge/Anthropic%20Claude%20API-CC785C?style=flat-square)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square)
![Unsloth](https://img.shields.io/badge/Unsloth-Fast%20Finetuning-FF4B4B?style=flat-square)

---

## Features

### ISV Onboarding Flow
- **Identity verification** with strict email domain matching against company website
- **OTP authentication** (demo mode with hint display)
- **ISV Registry lookup** — Nemotron pre-fills company profile from NVIDIA partner database
- **8-step conversational intake** collecting company info, tech stack, problem statement, tools, concerns, team context, and learning format preference
- **Drag-to-rank** learning format selection (Workshop, Jupyter Notebook, Hackathon)

### NIM-Powered Output Generation
- **3 context-aware DGX Cloud integration recommendations** with exact NIM microservice names, NVIDIA stack components, and partner tools
- **Learning style inference** from format ranking patterns
- **Primary deliverable generation** based on #1 ranked format
- **Adoption concern responses** with hyperlinked developers.nvidia.com resources

### Persistent ISV Portal
- **Tech stack sidebar** with GCP Service Usage API auto-detection and manual entry
- **Orbit chat** powered by Nemotron, grounded in ISV profile and generated outputs
- **Adoption strategy history** saved per session with short-title descriptions
- **Profile page** showing ISV identity, NVIDIA partner tier, products, and strategy history

### Admin DevRel Dashboard
- Active users, completion rates, drop-off by intake step
- Learning style distribution (inferred by Llama 3.1 8B)
- Format preference breakdown
- Trending topics from Orbit chat with suggested DevRel actions
- World map of ISV locations via IP geolocation (ipinfo.io + Leaflet.js)
- Monthly report auto-generated and emailed via SendGrid

---

## NVIDIA Products Featured

| Product | Category | Usage in Orbit |
|---|---|---|
| DGX Cloud | Infrastructure | Primary infrastructure recommendation for all ISVs |
| NVIDIA NIM | Inference | Powers all three inference models in the platform |
| Nemotron-Super-49B | LLM | Recommendations, chat, workshop/hackathon generation |
| Llama 3.1 8B (NIM) | LLM | Learning style classification |
| Mistral Small 4 (NIM) | LLM | Jupyter Notebook code generation |
| MONAI | Healthcare AI | Recommended for medical imaging ISVs |
| Clara | Healthcare AI | Recommended for clinical decision support ISVs |
| Clara Holoscan | Healthcare AI | Recommended for medical device ISVs |
| BioNeMo | Life Sciences | Recommended for drug discovery ISVs |
| NeMo Framework | LLM Training | Surfaced in fine-tuning recommendations |
| TensorRT-LLM | Inference Optimization | Surfaced in latency optimization recommendations |
| Riva | Speech AI | Recommended for voice and transcription ISVs |
| Triton Inference Server | Inference | Surfaced in multi-model serving recommendations |
| Merlin | Recommender Systems | Recommended for personalization ISVs |
| Metropolis | Computer Vision | Recommended for video analytics ISVs |
| Omniverse | Simulation | Recommended for digital twin ISVs |

---

## Deployment

Orbit is deployed on **GCP Cloud Run** — the same infrastructure layer that DGX Cloud runs on top of. The deployment architecture itself is a demonstration of the NVIDIA + Google Cloud partnership.

### Why GCP Cloud Run (not Vercel)
Vercel is a frontend platform built for Next.js. GCP Cloud Run keeps the architecture coherent: the app lives on the same hyperscaler that DGX Cloud runs on, GCP Service Usage API detects ISV tech stacks, and every architectural decision mirrors what we'd recommend to ISV partners.

### Deployment Files

| File | Purpose |
|---|---|
| `Dockerfile` | Containerizes the Flask app using python:3.11-slim, installs dependencies, runs gunicorn |
| `wsgi.py` | WSGI entry point for gunicorn — calls `create_app()` from `app.py` |
| `.dockerignore` | Excludes `.env`, `venv/`, GCP credentials, and data files from the container |
| `cloudbuild.yaml` | GCP Cloud Build config for automated CI/CD on push to main |
| `deploy.sh` | One-command deployment script (gitignored, contains env vars) |

### Deploy Your Own Instance

```bash
git clone https://github.com/itsChanelML/orbit-isv-intelligence-platform.git
cd orbit-isv-intelligence-platform

# Enable GCP APIs
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com

# Deploy
gcloud run deploy orbit-isv-platform \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars="NVIDIA_API_KEY=...,SENDGRID_API_KEY=...,IPINFO_TOKEN=...,GCP_PROJECT_ID=..."
```

---

## Local Development

```bash
git clone https://github.com/itsChanelML/orbit-isv-intelligence-platform.git
cd orbit-isv-intelligence-platform

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in your API keys

python app.py
# Visit http://127.0.0.1:5000
```

### Environment Variables

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ISV_ACCESS_CODE=ORBIT-ISV-2025
ADMIN_ACCESS_CODE=ORBIT-ADMIN-2025
NVIDIA_API_KEY=nvapi-...
GCP_SERVICE_ACCOUNT_KEY=path/to/service-account.json
GCP_PROJECT_ID=your-project-id
SENDGRID_API_KEY=SG....
ADMIN_EMAIL=your-email@domain.com
SENDGRID_FROM_EMAIL=your-verified-sender@domain.com
IPINFO_TOKEN=your-token
```

---

## Project Structure

```
orbit-isv-intelligence-platform/
├── app.py                           # Flask entry point
├── wsgi.py                          # Gunicorn WSGI entry point
├── config.py                        # Environment configuration
├── requirements.txt                 # Python dependencies (incl. gunicorn)
├── Dockerfile                       # Container definition for GCP Cloud Run
├── .dockerignore                    # Files excluded from Docker build
├── cloudbuild.yaml                  # GCP Cloud Build CI/CD config
├── .env.example                     # Environment variable template
├── PRODUCT_BRIEF.md                 # Full product brief (V1/V2/V3 roadmap)
├── README.md
├── data/
│   ├── isv_registry.json            # NVIDIA ISV partner database
│   ├── nvidia_products_catalog.json # Full NVIDIA product catalog (16 products)
│   └── analytics.json               # Session and event tracking
├── routes/
│   ├── auth.py                      # Login, session, decorators
│   ├── intake.py                    # 8-step adoption strategy flow
│   ├── output.py                    # NIM generation, downloads
│   ├── portal.py                    # ISV portal, GCP sync, Orbit chat
│   └── admin.py                     # Dashboard, reports, email
├── services/
│   ├── nim_service.py               # All NIM API calls (3 models)
│   ├── registry_service.py          # ISV registry lookup + Nemotron prefill
│   ├── gcp_service.py               # GCP Service Usage API integration
│   ├── analytics_service.py         # Event logging + monthly report generation
│   └── email_service.py             # SendGrid report delivery
├── templates/
│   ├── base.html                    # Dark theme, orbiting blob animation
│   ├── login.html                   # Access code entry
│   ├── portal.html                  # ISV portal with Orbit chat
│   ├── intake.html                  # 8-step adoption strategy flow
│   ├── output.html                  # Recommendations + deliverable
│   ├── profile.html                 # ISV profile page
│   └── admin.html                   # DevRel intelligence dashboard
└── static/
    ├── css/
    │   ├── main.css                 # Design system (NVIDIA theme, Syne + DM Sans)
    │   ├── portal.css               # Portal layout and Orbit chat panel
    │   ├── intake.css               # 8-step flow, concerns, stack presets
    │   ├── output.css               # Recommendations and deliverable preview
    │   ├── admin.css                # Dashboard panels and world map
    │   └── profile.css              # ISV profile page
    └── js/
        └── orbit.js                 # Mouse parallax, entrance animations
```

---

## Built By

**Chanel Power** — Senior ML Engineer, Startup Advisor | Founder, Mentor Me Collective

Portfolio project for NVIDIA Senior Developer Relations Manager 

[![GitHub](https://img.shields.io/badge/GitHub-itsChanelML-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/itsChanelML)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Chanel%20Power-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/powerc1)
[![NVIDIA GTC](https://img.shields.io/badge/NVIDIA%20GTC-2026%20Attendee-76B900?style=flat-square&logo=nvidia&logoColor=white)](https://www.nvidia.com/gtc/)