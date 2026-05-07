# Orbit — Product Brief
### NVIDIA ISV Intelligence Platform

**Version 1.0 — May 2026**
**Live:** https://orbit-isv-platform-474576936406.us-central1.run.app

---

## The Problem Orbit Solves

Developer Relations at scale is a people problem disguised as a technology problem.

A DevRel manager working with ISV partners spends the majority of their time on the same pre-work, over and over: discovering what a company builds, understanding their tech stack, figuring out which NVIDIA products are relevant to their use case, and then manually constructing a custom integration path. Before a single line of code gets written or a single partnership meeting is scheduled, hours of research and synthesis have already been consumed.

This is not sustainable at NVIDIA's pace. The DGX Cloud ecosystem is growing faster than any DevRel team can manually onboard. The answer is not more headcount — it is intelligence infrastructure.

Orbit is that infrastructure.

---

## What Orbit Is

Orbit is an agentic ISV intelligence platform that automates the intake, profiling, and adoption strategy generation for every ISV partner entering the NVIDIA DGX Cloud ecosystem.

It is not a chatbot. It is not a documentation portal. It is a working DevRel system — one that learns who an ISV is, what they need, and how they learn, then uses NVIDIA NIM to generate a fully personalized DGX Cloud adoption pathway before a DevRel manager ever gets on a call.

When a DevRel manager sits down with an ISV partner, they should not be starting from zero. They should be starting from seven.

Orbit makes that possible.

---

## How Orbit Makes DevRel More Effective

### Before Orbit
A DevRel manager preparing for an ISV conversation manually:
- Researches the company website and product documentation
- Identifies which NVIDIA products might be relevant
- Drafts a custom integration recommendation
- Prepares a workshop outline, technical brief, or exec-facing deck
- Follows up with resource links addressing the ISV's concerns
- Takes notes on team size, technical depth, and learning preferences
- Builds a tools reference guide for the ISV's specific stack

This process takes hours per ISV and does not scale.

### After Orbit
The ISV enters Orbit independently before any meeting. By the time the DevRel manager sees them, Orbit has already:

- Verified their identity and matched them against the NVIDIA ISV registry
- Pre-filled their company profile using Nemotron inference from partner data
- Collected their problem statement, tech stack, tool preferences, and adoption concerns
- Generated three context-aware DGX Cloud integration recommendations with exact NIM microservices named
- Produced a tailored deliverable matched to how their team learns:
  - A **Workshop Guide** for teams that learn through facilitated sessions
  - A **Jupyter Notebook** for engineers who learn by doing
  - A **Hackathon Brief** for teams that learn through structured challenges
  - An **Executive Adoption Brief** for C-suite stakeholders who need business rationale, ROI framing, and a recommended next steps plan
- Addressed each adoption concern with a specific NVIDIA resource and documentation link
- Inferred their learning style from how they ranked their format preferences
- Provided a browsable reference of every relevant NVIDIA product and OSS tool with Nemotron-generated descriptions and Ask Orbit integration
- Stored all generated documents in a persistent library for download, preview, and future reference

The DevRel manager arrives with a complete ISV profile, a generated adoption strategy, addressed concerns, and a document ready to share. The conversation starts at a completely different level.

Orbit does not replace the DevRel manager. It eliminates the busywork so the DevRel manager can do the work that only a human can do.

---

## Version 1.0 — What I Built

### Identity & Security
- Strict email domain validation against company website (no consumer email domains)
- OTP verification flow with session-based authentication
- Role-based access: ISV Team view and Admin / DevRel Manager view
- NVIDIA ISV partner registry with tier recognition (Inception, Elite)

### Intelligent Intake
- 8-step conversational adoption strategy flow
- ISV registry lookup with Nemotron pre-fill — company profile populated from NVIDIA partner data before the user types a word
- Current tech stack selection with 16 preset technologies plus free-entry
- Adoption concern capture with 8 preset blockers and free-text input
- Drag-to-rank learning format selection (Workshop, Jupyter Notebook, Internal Hackathon)
- Returning user detection — skips identity steps and goes straight to strategy on repeat visits

### Multi-Model NIM Architecture
- `nvidia/llama-3.3-nemotron-super-49b-v1` — ISV recommendations, concern responses, Orbit chat, workshop, hackathon, and executive brief generation
- `meta/llama-3.1-8b-instruct` — Learning style inference from format ranking patterns
- `mistralai/mistral-small-4-119b-2603` — Jupyter Notebook code generation

### Output Generation — 4 Deliverable Types
Orbit generates a different primary deliverable based on team context and learning format preference:

**Workshop Guide (.md)**
A facilitated session agenda with structured exercises, discussion prompts, and integration checkpoints tailored to the ISV's specific DGX Cloud use case.

**Jupyter Notebook (.ipynb)**
A runnable step-by-step technical lab with code cells, markdown explanations, and integration patterns specific to the ISV's stack and tools. Generated by Mistral Small 4 via NIM.

**Hackathon Brief (.md / .txt)**
A structured internal hackathon problem statement with challenge framing, success criteria, NVIDIA stack requirements, team structure, and judging criteria.

**Executive Adoption Brief (.md)**
A business-focused adoption strategy document generated when the ISV selects "Exec-Facing Output." Includes:
- Executive summary
- Business problem framing
- Strategic rationale for NVIDIA DGX Cloud
- 3 business use cases with ROI signals and NVIDIA product attribution
- Competitive advantage narrative
- Deployment acceleration story
- Risk mitigation responses
- Recommended next steps table with owner and timeline
- Closing statement

All four deliverables are downloadable and stored in the ISV's Documents Library.

### Adoption Concerns — Nemotron Responses
Each adoption concern selected during intake receives a specific Nemotron-generated response with a hyperlinked resource from developers.nvidia.com. Preset concerns include team ML experience gaps, migration complexity, cost uncertainty, latency requirements, data privacy, vendor lock-in, integration timeline, and team buy-in.

### Developer Tools Library
A browsable three-tab directory inside the ISV portal:

**NVIDIA Products tab** — all 16 NVIDIA products from the extensible catalog, each with a Nemotron-generated 2-3 sentence description and an Ask Orbit button that pre-populates the chat with "How can I use [Product] at [Company]?"

**OSS Tools tab** — 30+ open source developer tools organized by category (LLM Orchestration, Model Hub & Fine-Tuning, Inference & Serving, Vector Databases & RAG, MLOps, Training Frameworks, Computer Vision, Speech) with NVIDIA compatibility flags and product pairing suggestions (e.g. LangChain → NVIDIA NIM + RAG pipelines)

**My Stack tab** — the ISV's specific tools from intake and GCP detection, enriched with Nemotron descriptions and Ask Orbit prompts

All descriptions are generated by Nemotron and cached in `data/tools_cache.json` — NIM is called once per tool and cached forever, making subsequent loads instant.

### Documents Library
A persistent document store for all generated deliverables:
- File-based storage with JSON manifest per session (`data/docs/{session_id}/`)
- Preview rendered in-browser for Workshop, Hackathon, and Exec Brief documents
- Jupyter Notebook preview shows first 5 cells
- Download in native format (`.md`, `.ipynb`, `.txt`)
- Delete individual documents
- Document metadata: type, size, date, strategy ID

### Persistent ISV Portal
- Orbit chat powered by Nemotron, grounded in the ISV's intake profile and generated outputs
- Tech stack sidebar with GCP Service Usage API auto-detection (polls enabled GCP APIs)
- New technology alerts fire as Orbit chat conversation starters
- Adoption strategy history saved with short-title descriptions
- ISV profile page showing identity, NVIDIA partner tier, products, learning style, and strategy history

### Admin DevRel Dashboard
- Session analytics: total sessions, ISV sessions, completions, completion rate
- Intake drop-off analysis by step
- Learning format preference distribution
- Learning style profiles inferred by Llama 3.1 8B
- Trending topics from Orbit chat with suggested DevRel actions
- World map of ISV locations via IP geolocation (ipinfo.io + Leaflet.js)
- Monthly DevRel report auto-emailed via SendGrid on the last day of each month

### NVIDIA Products Catalog
- 16 NVIDIA products catalogued with descriptions, use cases, categories, and documentation URLs
- Products span: Infrastructure, Inference, Healthcare AI, Life Sciences, Speech AI, Computer Vision, Robotics, Simulation, LLM Training, Inference Optimization, Recommender Systems
- Catalog is extensible — new products are added to `nvidia_products_catalog.json` without touching application code

### Python Services Architecture
Orbit is built around 8 dedicated Python service modules:

| Service | Responsibility |
|---|---|
| `nim_service.py` | All NIM API calls across 3 models, 8+ generation functions |
| `registry_service.py` | ISV registry lookup, Nemotron prefill, OTP generation |
| `gcp_service.py` | GCP Service Usage API integration, stack detection |
| `analytics_service.py` | Event logging, drop-off tracking, monthly report generation |
| `email_service.py` | SendGrid delivery, monthly scheduling, HTML report formatting |
| `exec_brief_service.py` | Executive adoption brief generation, markdown export, stats |
| `document_store.py` | File-based document management: save, retrieve, delete, metadata |
| `tools_service.py` | Tools catalog loading, Nemotron description generation, caching, Ask Orbit prompt builder |

### Deployment
- Containerized with Docker (python:3.11-slim), deployed on GCP Cloud Run
- Gunicorn WSGI server (2 workers, 8 threads, 300s timeout for NIM inference calls)
- GCP Cloud Build CI/CD pipeline via `cloudbuild.yaml`
- GCP Artifact Registry stores Docker images
- The deployment architecture itself demonstrates the NVIDIA + Google Cloud partnership

---

## Version 2.0 — What's Coming

### GitHub Integration
- Connect an ISV's GitHub repository to Orbit
- Auto-detect new libraries and dependencies added to `requirements.txt` or `package.json`
- Surface new tools as Orbit chat conversation starters without requiring manual GCP API polling
- Webhook-based detection for real-time stack updates

### Full User Authentication
- Replace access codes with proper account-based authentication
- OAuth via Google (ISV uses their work Google account — same domain validation)
- Persistent user profiles stored in database, not session
- Multi-user support within a single ISV organization

### Persistent Database
- Move from file-based and session-based storage to a proper database (Firestore or BigQuery)
- Documents, strategies, and profiles persist across sessions and devices
- Shareable strategy URLs for ISV teams to distribute internally

### Orbit Chat Memory
- Chat history persisted across sessions
- Orbit remembers previous conversations and references prior strategies
- "Last time we discussed X" context awareness

### NIM Model Selector
- Allow ISV to choose which NIM model powers their recommendations
- Surface model cards with benchmark data from the NVIDIA product catalog
- Show inference speed vs. quality tradeoffs per model

---

## Version 3.0 — The Long-Term Vision

### Multi-ISV Admin Intelligence
- DevRel manager dashboard showing all ISVs across the pipeline simultaneously
- Cohort analysis: which ISVs at the same stage have similar concerns
- Recommended DevRel actions generated by Nemotron based on aggregate signal
- Automated webinar topic suggestions when trending topics reach threshold

### Live Partner Ecosystem Directory
- Public-facing ISV directory showing NVIDIA-verified partners
- Filter by industry, NVIDIA products used, integration stage
- ISV self-service profile management
- Co-marketing asset generation directly from Orbit

### Orbit for Other NVIDIA Tech Stacks
- Orbit V1 is scoped to DGX Cloud DevRel
- V3 extends the same architecture to support any NVIDIA product vertical:
  - An Orbit instance for NVIDIA Omniverse partners
  - An Orbit instance for NVIDIA Metropolis (retail / smart cities)
  - An Orbit instance for NVIDIA Clara (healthcare)
- One platform, configurable per vertical, powered by the same NIM infrastructure

### Agentic Expansion
- Orbit evolves from intake + generation to fully agentic operation
- Orbit proactively monitors ISV GitHub repos, GCP projects, and chat activity
- When signal threshold is met, Orbit drafts a DevRel outreach email for review
- DevRel manager approves and sends — Orbit handles the research, the human handles the relationship

---

## Why This Is an Agentic Solution

Orbit is not a form that generates a PDF. It is an agent that learns, infers, and acts.

**It learns** who an ISV is from structured intake and unstructured signals — their problem statement, their stack, their concerns, how they ranked their learning formats.

**It infers** things that were never explicitly stated — their learning style from ranking behavior, which NVIDIA products are most relevant from their use case description, what concerns are likely to block adoption based on their team context, which deliverable format will be most effective for their audience.

**It acts** by generating recommendations, producing deliverables, addressing concerns, alerting on new technologies, delivering reports, describing tools, and building a document library — without waiting for a human to tell it what to do.

The DevRel manager is not removed from the process. They are elevated within it. Orbit handles the intelligence work. The DevRel manager handles the relationship work. That division of labor is what makes enterprise developer relations scale.

---

## Built On the Partnership It Advocates

Every architectural decision in Orbit is a demonstration of the NVIDIA + Google Cloud partnership that the DGX Cloud DevRel team evangelizes.

The application runs on **GCP Cloud Run** — the same hyperscaler layer that DGX Cloud runs on top of. The tech stack detection uses the **GCP Service Usage API**. The inference layer runs on **NVIDIA NIM** via `integrate.api.nvidia.com`. The ISV recommendations surface **Vertex AI**, **GCP BigQuery**, **GCP Cloud Run**, and **GCP Cloud Storage** as partner tools alongside NVIDIA products.

Orbit does not just talk about the partnership. It is built on it.

---

*[GitHub](https://github.com/itsChanelML/orbit-isv-intelligence-platform) · [Live Demo](https://orbit-isv-platform-474576936406.us-central1.run.app)*