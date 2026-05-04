# Orbit — NVIDIA ISV Intelligence Platform

> Built as a portfolio project for the Senior Developer Relations Manager (DGX Cloud) role at NVIDIA.

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
│                  Flask + Python                      │
│                 Deployed on GCP                      │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐   ┌────────▼────────┐
│  NVIDIA NIM    │   │   Google Cloud  │
│  ─────────────-│   │  ──────────────-│
│  Nemotron 49B  │   │  Service Usage  │
│  Llama 3.1 8B  │   │  API (Stack     │
│  Mistral       │   │  Detection)     │
│  Small 4       │   │                 │
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

- **Google Cloud Platform** — GCP Service Usage API for tech stack detection, Cloud Run for deployment, Vertex AI in recommendations
- **Anthropic Claude API** — Surfaced in RAG and agentic pipeline recommendations
- **Vercel** — Surfaced in deployment recommendations for web-facing ISVs

---

## Setup

### Prerequisites
- Python 3.9+
- NVIDIA NIM API key (get one at [build.nvidia.com](https://build.nvidia.com))
- GCP service account JSON with Service Usage API access
- SendGrid account (free tier)
- ipinfo.io account (free tier)

### Installation

```bash
git clone https://github.com/itsChanelML/orbit-isv-intelligence-platform.git
cd orbit-isv-intelligence-platform

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Fill in your API keys in .env

python app.py
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

### Access

| Role | Code | Access |
|---|---|---|
| ISV Team | `ORBIT-ISV-2025` | Full onboarding flow, portal, Orbit chat |
| Admin / DevRel Manager | `ORBIT-ADMIN-2025` | ISV view + admin dashboard + report controls |

---

## Project Structure

```
orbit-isv-intelligence-platform/
├── app.py                          # Flask entry point
├── config.py                       # Environment configuration
├── requirements.txt
├── data/
│   ├── isv_registry.json           # NVIDIA ISV partner database
│   ├── nvidia_products_catalog.json # Full NVIDIA product catalog
│   └── analytics.json              # Session and event tracking
├── routes/
│   ├── auth.py                     # Login, session, decorators
│   ├── intake.py                   # 8-step adoption strategy flow
│   ├── output.py                   # NIM generation, downloads
│   ├── portal.py                   # ISV portal, GCP sync, chat
│   └── admin.py                    # Dashboard, reports, email
├── services/
│   ├── nim_service.py              # All NIM API calls (3 models)
│   ├── registry_service.py         # ISV registry lookup + prefill
│   ├── gcp_service.py              # GCP Service Usage API
│   ├── analytics_service.py        # Event logging + aggregation
│   └── email_service.py            # SendGrid report delivery
├── templates/
│   ├── base.html                   # Dark theme, orbiting blobs
│   ├── login.html                  # Access code entry
│   ├── portal.html                 # ISV portal with Orbit chat
│   ├── intake.html                 # 8-step adoption flow
│   ├── output.html                 # Recommendations + deliverable
│   ├── profile.html                # ISV profile page
│   └── admin.html                  # DevRel dashboard
└── static/
    ├── css/
    │   ├── main.css                # Design system (NVIDIA theme)
    │   ├── portal.css
    │   ├── intake.css
    │   ├── output.css
    │   ├── admin.css
    │   └── profile.css
    └── js/
        └── orbit.js                # Parallax, animations
```

---

## Built By

**Chanel Power** — Senior ML Engineer, Startup Advisor | Founder, Mentor Me Collective

Portfolio project for NVIDIA Senior Developer Relations Manager

[GitHub](https://github.com/itsChanelML) · [LinkedIn](https://linkedin.com/in/powerc1)