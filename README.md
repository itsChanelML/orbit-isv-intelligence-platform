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

Orbit is an agentic ISV onboarding and adoption intelligence platform built on NVIDIA NIM and DGX Cloud. It automates the pre-work of ISV developer relations — learning who a software vendor is, what they build, and what they need — then uses multi-model NIM inference to generate a personalized DGX Cloud adoption strategy, deliverable, and concern responses in a single flow. It also powers a verified ISV community where partners share wins, ask questions, and surface integration patterns — with Orbit responding in real time.

| Role | Access Code |
|---|---|
| ISV Team | `ORBIT-ISV-2025` |
| Admin / DevRel Manager | `ORBIT-ADMIN-2025` |

---

## What This Demonstrates

| Role Requirement | Orbit Implementation |
|---|---|
| Evangelize DGX Cloud to ISV partners | Conversational intake surfaces NIM microservices and DGX Cloud integration patterns specific to each ISV |
| Develop go-to-market with strategic ISVs | ISV registry grounded in NVIDIA partner data, Nemotron pre-fills company profile automatically |
| Create assets for conferences and hackathons | Generates Workshop guides, Jupyter Notebooks, Hackathon briefs, and Executive Adoption Briefs as downloadable deliverables |
| Build developer adoption programs | Learning style inference routes each ISV to their preferred adoption format |
| Measure ISV adoption and engagement | Admin dashboard with drop-off analytics, format preferences, world map, community signals, and monthly DevRel report |
| Drive ISV integrations with the NVIDIA ecosystem | GCP Service Usage API detects new ISV tech stack additions and triggers Orbit chat alerts |
| Create sales and marketing assets with developers | Generates bespoke adoption assets at the speed of a template but with the specificity of a custom engagement |
| Build and scale developer communities | Verified ISV community board with Orbit AI replies, category filtering, reactions, and admin signal capture |

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      Orbit Platform                       │
│                Flask + Python + Gunicorn                  │
│                 Deployed on GCP Cloud Run                 │
└───────────────────────┬──────────────────────────────────┘
                        │
           ┌────────────┴────────────┐
           │                         │
┌──────────▼───────┐     ┌───────────▼──────────┐
│   NVIDIA NIM     │     │    Google Cloud       │
│  ────────────────│     │  ────────────────────-│
│  Nemotron 49B    │     │  Cloud Run            │
│  Llama 3.1 8B    │     │  Cloud Build          │
│  Mistral Small 4 │     │  Artifact Registry    │
│                  │     │  Service Usage API    │
└──────────────────┘     └──────────────────────┘
```

### Model Routing

| Model | Provider | Role in Orbit |
|---|---|---|
| `llama-3.3-nemotron-super-49b-v1` | NVIDIA NIM | ISV recommendations, concern responses, Orbit chat, workshop/hackathon/exec brief generation, community replies, tool descriptions |
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

### ISV Identity & Security
- Strict email domain validation against company website
- OTP authentication with session-based security
- Role-based access: ISV Team and Admin / DevRel Manager
- NVIDIA ISV partner registry with tier recognition (Inception, Elite)
- Returning user detection — skips identity steps on repeat visits

### Intelligent 8-Step Intake
- ISV registry lookup with Nemotron pre-fill from NVIDIA partner data
- Current tech stack selection (16 presets + free entry)
- Adoption concern capture (8 presets + custom)
- Drag-to-rank learning format selection

### Multi-Model NIM Output — 4 Deliverable Types
| Deliverable | Trigger | Format | Model |
|---|---|---|---|
| Workshop Guide | Workshop ranked #1 | `.md` | Nemotron-Super-49B |
| Jupyter Notebook | Notebook ranked #1 | `.ipynb` | Mistral Small 4 |
| Hackathon Brief | Hackathon ranked #1 | `.md` | Nemotron-Super-49B |
| Executive Adoption Brief | Exec-Facing Output selected | `.md` | Nemotron-Super-49B |

Executive briefs include: executive summary, business problem framing, strategic rationale, 3 business use cases with ROI signals, competitive advantage narrative, deployment acceleration story, risk mitigation, and a recommended next steps table.

### Developer Tools Library
- 3-tab browsable directory: NVIDIA Products (16), OSS Tools (30+), My Stack
- Nemotron-generated 2-3 sentence descriptions cached per tool
- NVIDIA product pairing suggestions for every OSS tool
- Ask Orbit button pre-populates chat with "How can I use [Tool] at [Company]?"

### ISV Community Board
- Persistent shared board visible to all verified ISV partners
- 5 categories: Wins & Milestones, Best Practices, Questions, Integration Patterns, Announcements
- Post, comment, react (👍 Helpful, 🔥 Fire, 💡 Insight)
- Orbit AI replies on demand — Nemotron responds with NVIDIA docs, video tutorials, and upcoming events
- Orbit tag identifies AI responses alongside human comments
- Admin signals: trending topics, unanswered questions (DevRel action items), most active companies, Orbit response rate

### Documents Library
- Persistent file-based document store per session
- Preview, download, and delete for all generated deliverables
- Supports Workshop, Notebook, Hackathon Brief, and Executive Adoption Brief
- JSON manifest with metadata (type, size, date, strategy ID)

### Persistent ISV Portal
- Orbit chat powered by Nemotron, grounded in ISV profile and outputs
- Tech stack sidebar with GCP Service Usage API auto-detection
- Adoption strategy history with short-title descriptions
- Profile page: ISV identity, NVIDIA tier, products, learning style, strategy history

### Admin DevRel Dashboard
- Session analytics: total sessions, completions, completion rate, drop-off by step
- Learning style and format preference distribution
- Community signals: trending topics, unanswered questions, most active ISVs
- World map of ISV locations (ipinfo.io + Leaflet.js)
- Monthly report auto-emailed via SendGrid

---

## NVIDIA Products Featured

| Product | Category | Usage in Orbit |
|---|---|---|
| DGX Cloud | Infrastructure | Primary infrastructure recommendation for all ISVs |
| NVIDIA NIM | Inference | Powers all three inference models in the platform |
| Nemotron-Super-49B | LLM | Recommendations, chat, workshop/hackathon/exec brief, community replies, tool descriptions |
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

Orbit is deployed on **GCP Cloud Run** — the same infrastructure layer that DGX Cloud runs on top of.

### Why GCP Cloud Run
The deployment architecture is itself a demonstration of the NVIDIA + Google Cloud partnership. The app lives on the same hyperscaler that DGX Cloud runs on, GCP Service Usage API detects ISV tech stacks, and every architectural decision mirrors what we'd recommend to ISV partners.

### Deployment Files

| File | Purpose |
|---|---|
| `Dockerfile` | python:3.11-slim, installs dependencies, runs gunicorn |
| `wsgi.py` | Gunicorn WSGI entry point |
| `.dockerignore` | Excludes `.env`, `venv/`, credentials, data files |
| `cloudbuild.yaml` | GCP Cloud Build CI/CD config |
| `deploy.sh` | One-command deployment (gitignored) |

### Deploy Your Own

```bash
git clone https://github.com/itsChanelML/orbit-isv-intelligence-platform.git
cd orbit-isv-intelligence-platform

gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com

gcloud run deploy orbit-isv-platform \
  --source . --region us-central1 --allow-unauthenticated \
  --memory 1Gi --timeout 300 \
  --set-env-vars="NVIDIA_API_KEY=...,SENDGRID_API_KEY=...,IPINFO_TOKEN=...,GCP_PROJECT_ID=..."
```

---

## Local Development

```bash
git clone https://github.com/itsChanelML/orbit-isv-intelligence-platform.git
cd orbit-isv-intelligence-platform
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Fill in your API keys
python app.py  # Visit http://127.0.0.1:5000
```

---

## Project Structure

```
orbit-isv-intelligence-platform/
├── app.py                              # Flask entry point — registers 7 blueprints
├── wsgi.py                             # Gunicorn WSGI entry point
├── config.py                           # Environment configuration
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── cloudbuild.yaml
├── .env.example
├── README.md
├── PRODUCT_BRIEF.md
├── data/
│   ├── isv_registry.json               # NVIDIA ISV partner database
│   ├── nvidia_products_catalog.json    # NVIDIA product catalog (16 products)
│   ├── oss_tools_catalog.json          # OSS developer tools catalog (30+ tools)
│   ├── tools_cache.json                # Nemotron tool description cache
│   ├── community.json                  # Shared persistent ISV community posts
│   └── analytics.json                  # Session and event tracking
├── routes/
│   ├── auth.py                         # Login, session, decorators
│   ├── intake.py                       # 8-step adoption strategy flow
│   ├── output.py                       # NIM generation, exec brief, downloads
│   ├── portal.py                       # ISV portal, GCP sync, Orbit chat, tools
│   ├── documents.py                    # Document library, preview, download
│   ├── community.py                    # ISV community board, reactions, Orbit replies
│   └── admin.py                        # Dashboard, analytics, community signals, email
├── services/
│   ├── nim_service.py                  # All NIM API calls (3 models, 10+ functions)
│   ├── registry_service.py             # ISV registry lookup, Nemotron prefill, OTP
│   ├── gcp_service.py                  # GCP Service Usage API integration
│   ├── analytics_service.py            # Event logging, monthly report generation
│   ├── email_service.py                # SendGrid delivery, monthly scheduling
│   ├── exec_brief_service.py           # Executive adoption brief generation
│   ├── document_store.py               # File-based document management
│   ├── tools_service.py                # Tools catalog, Nemotron descriptions, caching
│   └── community_service.py            # Community posts, reactions, Orbit AI replies
├── templates/
│   ├── base.html                       # Dark theme, orbiting blob animation
│   ├── login.html
│   ├── portal.html                     # ISV portal with Orbit chat
│   ├── intake.html                     # 8-step adoption strategy flow
│   ├── output.html                     # Recommendations + deliverable
│   ├── profile.html                    # ISV profile page
│   ├── tools.html                      # Developer tools library
│   ├── documents.html                  # Documents library
│   ├── document_view.html              # Single document preview
│   ├── community.html                  # ISV community board
│   ├── community_post.html             # Post detail + new post form
│   └── admin.html                      # DevRel intelligence dashboard
└── static/
    ├── css/
    │   ├── main.css                    # Design system (NVIDIA theme)
    │   ├── portal.css
    │   ├── intake.css
    │   ├── output.css
    │   ├── admin.css
    │   ├── profile.css
    │   ├── tools.css
    │   ├── documents.css
    │   └── community.css
    └── js/
        └── orbit.js
```

---

## Built By

**Chanel Power** — Senior ML Engineer, Technical Advisor | Founder, Mentor Me Collective


[![GitHub](https://img.shields.io/badge/GitHub-itsChanelML-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/itsChanelML)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Chanel%20Power-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://linkedin.com/in/powerc1)