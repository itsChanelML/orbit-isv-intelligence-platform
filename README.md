# Orbit — NVIDIA ISV Intelligence Platform

> Built as a portfolio project for the Senior Developer Relations Manager (DGX Cloud) role at NVIDIA.

**Live Demo:** https://orbit-isv-platform-474576936406.us-central1.run.app

| Role | Access Code |
|---|---|
| ISV Team | `ORBIT-ISV-2025` |
| Admin / DevRel Manager | `ORBIT-ADMIN-2025` |

Orbit is an agentic ISV onboarding and adoption intelligence platform built on NVIDIA NIM and DGX Cloud. It automates the pre-work of ISV developer relations — learning who a software vendor is, what they build, and what they need — then uses multi-model NIM inference to generate a personalized DGX Cloud adoption strategy, deliverable, and concern responses in a single flow.

---

## What This Demonstrates

This project directly maps to the responsibilities of the DGX Cloud DevRel role:

| Role Requirement | Orbit Implementation |
|---|---|
| Evangelize DGX Cloud to ISV partners | Conversational intake that surfaces NIM microservices and DGX Cloud integration patterns specific to each ISV |
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

**Model routing:**
- `nvidia/llama-3.3-nemotron-super-49b-v1` — ISV recommendations, concern responses, Orbit chat, workshop generation
- `meta/llama-3.1-8b-instruct` — Learning style inference from format ranking
- `mistralai/mistral-small-4-119b-2603` — Jupyter Notebook code generation

---

## Features

### ISV Onboarding Flow
- **Identity verification** with strict email domain matching against company website
- **OTP authentication** (demo mode with hint display)
- **ISV Registry lookup** — Nemotron pre-fills company profile from NVIDIA partner database
- **8-step conversational intake** collecting company info, tech stack, problem statement, tools, concerns, team context, and learning format preference
- **Drag-to-rank** learning format selection (Workshop, Jupyter Notebook, Hackathon)

### NIM-Powered Output Generation
- **3 context-aware DGX Cloud integration recommendations** with exact NIM microservice names, NVIDIA stack components, and partner tools (GCP, Anthropic, Vercel)
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
- Trending topics from Orbit chat interactions with suggested DevRel actions
- World map of ISV locations via IP geolocation
- Monthly report auto-generated and emailed via SendGrid on the last day of each month

---

## NVIDIA Products Featured

| Product | Usage in Orbit |
|---|---|
| DGX Cloud | Primary infrastructure recommendation for all ISVs |
| NVIDIA NIM | Powers all three inference models in the platform |
| Nemotron-Super-49B | Recommendations, chat, workshop/hackathon generation |
| Llama 3.1 8B (NIM) | Learning style classification |
| Mistral Small 4 (NIM) | Jupyter Notebook code generation |
| MONAI | Recommended for healthcare/imaging ISVs |
| Clara | Recommended for medical device ISVs |
| BioNeMo | Recommended for life sciences ISVs |
| TensorRT-LLM | Surfaced in inference optimization recommendations |
| NeMo Framework | Surfaced in fine-tuning recommendations |

---

## Partner Integrations

- **Google Cloud Platform** — GCP Cloud Run for deployment, Service Usage API for stack detection, Vertex AI in recommendations
- **Anthropic Claude API** — Surfaced in RAG and agentic pipeline recommendations
- **Vercel** — Surfaced in deployment recommendations for web-facing ISVs
- **SendGrid** — Monthly DevRel report delivery via email
- **ipinfo.io** — IP geolocation for world map on admin dashboard

---

## Deployment

Orbit is deployed on **GCP Cloud Run** — the same infrastructure layer that DGX Cloud runs on top of. This means the deployment architecture itself is a live demonstration of the NVIDIA + Google Cloud partnership.

### Deployment Stack
- **Container:** Docker (python:3.11-slim)
- **WSGI Server:** Gunicorn (2 workers, 8 threads, 300s timeout)
- **Platform:** GCP Cloud Run (us-central1, 1Gi memory, 2 CPU)
- **CI/CD:** GCP Cloud Build (`cloudbuild.yaml`)
- **Registry:** GCP Artifact Registry

### Why GCP Cloud Run (not Vercel)
Vercel is a frontend deployment platform built for Next.js. Deploying here on GCP Cloud Run keeps the architecture story coherent: the app lives on the same hyperscaler layer that DGX Cloud runs on, GCP Service Usage API detects ISV tech stacks, and every architectural decision mirrors what we'd recommend to ISV partners.

### Deploy Your Own Instance

**Prerequisites:**
- gcloud CLI installed and authenticated
- GCP project with Cloud Run, Cloud Build, and Artifact Registry APIs enabled
- NVIDIA NIM API key
- SendGrid account (free tier)
- ipinfo.io account (free tier)

**Steps:**

```bash
git clone https://github.com/itsChanelML/orbit-isv-intelligence-platform.git
cd orbit-isv-intelligence-platform

# Create deploy script
cat > deploy.sh << 'EOF'
#!/bin/bash
gcloud run deploy orbit-isv-platform \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars="SECRET_KEY=your-secret,ISV_ACCESS_CODE=ORBIT-ISV-2025,ADMIN_ACCESS_CODE=ORBIT-ADMIN-2025,NVIDIA_API_KEY=your-nim-key,SENDGRID_API_KEY=your-sg-key,ADMIN_EMAIL=your-email,SENDGRID_FROM_EMAIL=your-email,IPINFO_TOKEN=your-token,GCP_PROJECT_ID=your-project-id,DEBUG=False"
EOF

chmod +x deploy.sh
./deploy.sh
```

### Deployment Files

| File | Purpose |
|---|---|
| `Dockerfile` | Containerizes the Flask app using python:3.11-slim, installs dependencies, runs gunicorn |
| `wsgi.py` | WSGI entry point for gunicorn — calls `create_app()` from `app.py` |
| `.dockerignore` | Excludes `.env`, `venv/`, GCP credentials, and data files from the container |
| `cloudbuild.yaml` | GCP Cloud Build config for automated CI/CD on push to main |
| `deploy.sh` | One-command deployment script (gitignored, contains env vars) |

---

## Local Development

```bash
git clone https://github.com/itsChanelML/orbit-isv-intelligence-platform.git
cd orbit-isv-intelligence-platform

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in your API keys in .env

python app.py
# Visit http://127.0.0.1:5000
```

### Environment Variables

```bash
# Flask
SECRET_KEY=your-secret-key
DEBUG=True

# Access Codes (role-based auth)
ISV_ACCESS_CODE=ORBIT-ISV-2025
ADMIN_ACCESS_CODE=ORBIT-ADMIN-2025

# NVIDIA NIM
NVIDIA_API_KEY=nvapi-...

# GCP
GCP_SERVICE_ACCOUNT_KEY=path/to/service-account.json
GCP_PROJECT_ID=your-project-id

# SendGrid
SENDGRID_API_KEY=SG....
ADMIN_EMAIL=your-email@domain.com
SENDGRID_FROM_EMAIL=your-verified-sender@domain.com

# ipinfo
IPINFO_TOKEN=your-token
```

---

## Project Structure

```
orbit-isv-intelligence-platform/
├── app.py                          # Flask entry point
├── wsgi.py                         # Gunicorn WSGI entry point
├── config.py                       # Environment configuration
├── requirements.txt                # Python dependencies (incl. gunicorn)
├── Dockerfile                      # Container definition for GCP Cloud Run
├── .dockerignore                   # Files excluded from Docker build
├── cloudbuild.yaml                 # GCP Cloud Build CI/CD config
├── deploy.sh                       # One-command GCP deployment script
├── .env.example                    # Environment variable template
├── README.md
├── data/
│   ├── isv_registry.json           # NVIDIA ISV partner database
│   ├── nvidia_products_catalog.json # Full NVIDIA product catalog (16 products)
│   └── analytics.json              # Session and event tracking
├── routes/
│   ├── auth.py                     # Login, session, decorators
│   ├── intake.py                   # 8-step adoption strategy flow
│   ├── output.py                   # NIM generation, downloads
│   ├── portal.py                   # ISV portal, GCP sync, chat
│   └── admin.py                    # Dashboard, reports, email
├── services/
│   ├── nim_service.py              # All NIM API calls (3 models)
│   ├── registry_service.py         # ISV registry lookup + Nemotron prefill
│   ├── gcp_service.py              # GCP Service Usage API integration
│   ├── analytics_service.py        # Event logging + monthly report generation
│   └── email_service.py            # SendGrid report delivery
├── templates/
│   ├── base.html                   # Dark theme, orbiting blob animation
│   ├── login.html                  # Access code entry
│   ├── portal.html                 # ISV portal with Orbit chat
│   ├── intake.html                 # 8-step adoption strategy flow
│   ├── output.html                 # Recommendations + deliverable
│   ├── profile.html                # ISV profile page
│   └── admin.html                  # DevRel intelligence dashboard
└── static/
    ├── css/
    │   ├── main.css                # Design system (NVIDIA theme, Syne + DM Sans)
    │   ├── portal.css              # Portal layout and Orbit chat panel
    │   ├── intake.css              # 8-step flow, concerns, stack presets
    │   ├── output.css              # Recommendations and deliverable preview
    │   ├── admin.css               # Dashboard panels and world map
    │   └── profile.css             # ISV profile page
    └── js/
        └── orbit.js                # Mouse parallax, entrance animations
```

---

## Built By

**Chanel Power** — Senior ML Engineer, Startup Advisor | Founder, Mentor Me Collective

Portfolio project for NVIDIA Senior Developer Relations Manager 

[GitHub](https://github.com/itsChanelML) · [LinkedIn](https://linkedin.com/in/powerc1)