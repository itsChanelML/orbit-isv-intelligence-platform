# Orbit — Product Brief 2
### NVIDIA ISV Intelligence Platform

**Version 1.1 — May 2026**
**Live:** https://orbit-isv-platform-474576936406.us-central1.run.app

---

## The Problem Orbit Solves

Developer Relations at scale is a people problem disguised as a technology problem.

A DevRel manager working with ISV partners spends the majority of their time on the same pre-work, over and over: discovering what a company builds, understanding their tech stack, figuring out which NVIDIA products are relevant to their use case, constructing a custom integration path, and then trying to build a community of practice among partners who never talk to each other.

That last part is the hardest. ISV partners operating in the same vertical — healthcare AI, fintech, logistics — are solving the same problems in isolation. A healthcare ISV that figured out how to get sub-100ms inference with TensorRT-LLM on DGX Cloud could save three other healthcare ISVs weeks of work. But without a structured place to share that insight, it never travels.

Orbit solves both problems: it automates the individual ISV onboarding workflow AND it creates the infrastructure for ISV partners to share intelligence with each other.

---

## What Orbit Is

Orbit is an agentic ISV intelligence platform with three interconnected layers:

**Layer 1 — Onboarding Intelligence**
Automates the pre-work of ISV developer relations. Learns who an ISV is, what they need, and how they learn, then uses NVIDIA NIM to generate a fully personalized DGX Cloud adoption pathway.

**Layer 2 — Knowledge Infrastructure**
A browsable library of every NVIDIA product and OSS developer tool, with Nemotron-generated descriptions, NVIDIA product pairings, and Ask Orbit integration. Every ISV has instant access to the full ecosystem reference.

**Layer 3 — Community Intelligence**
A verified ISV community board where partners share wins, ask questions, post integration patterns, and surface best practices. Orbit participates in real time, surfacing NVIDIA docs, video tutorials, and upcoming events on demand.

---

## How Orbit Makes DevRel More Effective

### Before Orbit
A DevRel manager manually:
- Researches each ISV company before every meeting
- Identifies which NVIDIA products are relevant to their use case
- Drafts custom integration recommendations per ISV
- Prepares workshop outlines, technical briefs, or exec-facing decks
- Follows up with resource links for each concern
- Monitors partner channels for questions and friction signals
- Tries to connect ISVs with similar challenges to each other

This process takes hours per ISV, doesn't scale, and produces no institutional knowledge.

### After Orbit
The ISV enters Orbit independently. Before any meeting, Orbit has:
- Verified their identity against the NVIDIA ISV registry
- Pre-filled their company profile using Nemotron from partner data
- Collected their problem statement, stack, tool preferences, and concerns
- Generated three context-aware DGX Cloud integration recommendations
- Produced a tailored deliverable matched to their team's learning style
- Addressed every adoption concern with a NVIDIA resource link
- Inferred their learning style from format ranking behavior
- Stored all deliverables in a persistent documents library
- Connected them to a community of verified peers solving similar problems

The DevRel manager arrives with everything done. The conversation starts at a completely different level.

---

## Version 1.1 — Full Feature Set

### Identity & Security
- Strict email domain validation (email domain must match company website)
- OTP verification with session authentication
- Role-based access: ISV Team and Admin / DevRel Manager
- NVIDIA ISV partner registry with Inception and Elite tier recognition
- Returning user detection — skips identity steps on repeat visits

### Intelligent 8-Step Intake
- ISV registry lookup with Nemotron pre-fill from NVIDIA partner data
- Current tech stack selection (16 preset technologies + free entry)
- Adoption concern capture (8 preset blockers + custom)
- Drag-to-rank learning format selection (Workshop, Notebook, Hackathon)

### Multi-Model NIM Architecture
Three NVIDIA NIM models with workload-specific routing:

| Model | Role |
|---|---|
| `nvidia/llama-3.3-nemotron-super-49b-v1` | ISV recommendations, concern responses, Orbit chat, workshop/hackathon/exec brief generation, community AI replies, tool descriptions |
| `meta/llama-3.1-8b-instruct` | Learning style inference from format ranking patterns |
| `mistralai/mistral-small-4-119b-2603` | Jupyter Notebook code generation |

### Four Deliverable Types
Orbit generates a different primary deliverable based on team context and learning format:

**Workshop Guide (.md)** — Facilitated session agenda with structured exercises, discussion prompts, and DGX Cloud integration checkpoints. For teams that learn through guided sessions.

**Jupyter Notebook (.ipynb)** — Runnable step-by-step technical lab with code cells and integration patterns specific to the ISV's stack. Generated by Mistral Small 4.

**Hackathon Brief (.md)** — Structured internal challenge with problem framing, success criteria, NVIDIA stack requirements, and judging criteria. For teams that learn through doing.

**Executive Adoption Brief (.md)** — Business-focused strategy document for C-suite audiences. Includes:
- Executive summary (outcome-first, no jargon)
- Business problem framing
- Strategic rationale for NVIDIA DGX Cloud
- 3 business use cases with ROI signals and NVIDIA product attribution
- Competitive advantage narrative
- Deployment acceleration story
- Risk mitigation responses
- Recommended next steps table with owner and timeline
- Closing statement

### Adoption Concerns — Nemotron Responses
Each concern receives a Nemotron-generated response with a hyperlinked developers.nvidia.com resource. Preset concerns cover team ML experience, migration complexity, cost uncertainty, latency requirements, data privacy, vendor lock-in, integration timeline, and team buy-in.

### Developer Tools Library
A three-tab browsable directory inside the ISV portal:

**NVIDIA Products (16)** — Full product catalog with Nemotron-generated descriptions, documentation links, and Ask Orbit integration.

**OSS Tools (30+)** — Open source tools organized by category: LLM Orchestration & Agents, Model Hub & Fine-Tuning, Inference & Serving, Vector Databases & RAG, MLOps & Experiment Tracking, Training Frameworks, Computer Vision, Speech & Audio. Each tool shows GitHub stars, language, NVIDIA compatibility, and which NVIDIA product it pairs with.

**My Stack** — The ISV's specific tools from intake and GCP detection, enriched with descriptions and Ask Orbit prompts.

All descriptions generated by Nemotron and cached in `data/tools_cache.json` — each tool description is generated once and served instantly on every subsequent load.

The Ask Orbit button on every tool card pre-populates the Orbit chat with "How can I use [Tool] at [Company]?" — turning the tools library into an interactive consultation layer.

### ISV Community Board
A verified community for the NVIDIA ISV ecosystem. Every post is tied to a domain-validated ISV identity.

**Five categories:**
- 🏆 Wins & Milestones — Share something you shipped on DGX Cloud
- 💡 Best Practices — Patterns and approaches that worked
- ❓ Questions — Stuck on something? Ask the community
- 🔧 Integration Patterns — How I connected X to NIM
- 📢 Announcements — From the NVIDIA DevRel team

**Orbit AI participation:**
Any post can trigger an Orbit response on demand. Nemotron reads the post and replies with:
- A direct, technical answer
- Relevant developers.nvidia.com documentation links
- On-demand video tutorial links (NVIDIA DLI)
- Upcoming event suggestions (GTC, DLI workshops, office hours)

Orbit's response appears as a tagged comment (`◈ Orbit · Nemotron`) alongside human comments. Orbit does not respond automatically — it responds when triggered, so human conversation is never displaced.

**What this does for DevRel:**
- Questions with no replies appear as DevRel action items in the admin dashboard
- Wins become co-marketing signals (which ISVs shipped, what they built)
- Integration patterns become documentation signals (what's not in the docs)
- Trending topics become conference talk ideas, workshop topics, and roadmap signals

### Documents Library
Persistent document store for all generated deliverables per session:
- File-based storage with JSON manifest (`data/docs/{session_id}/`)
- In-browser preview for Workshop, Hackathon, and Exec Brief documents
- Jupyter Notebook preview shows first 5 cells
- Download in native format (`.md`, `.ipynb`, `.txt`)
- Delete individual documents
- Document metadata: type, label, size, date, strategy ID

### Persistent ISV Portal
- Orbit chat powered by Nemotron, grounded in ISV profile and generated outputs
- Tech stack sidebar with GCP Service Usage API auto-detection
- New technology alerts fire as Orbit chat conversation starters
- Adoption strategy history with short-title descriptions
- Profile page: identity, NVIDIA partner tier, products, learning style, strategy history

### Admin DevRel Dashboard
- Session analytics: total sessions, ISV sessions, completions, completion rate, drop-off by step
- Learning style and format preference distribution
- Community signals: trending topics, unanswered questions, most active ISV companies, Orbit response rate
- World map of ISV locations (ipinfo.io + Leaflet.js)
- Monthly DevRel report auto-emailed via SendGrid on the last day of each month

### Python Services Architecture (9 Modules)

| Service | Responsibility |
|---|---|
| `nim_service.py` | All NIM API calls — 3 models, 10+ generation functions |
| `registry_service.py` | ISV registry lookup, Nemotron prefill, OTP generation |
| `gcp_service.py` | GCP Service Usage API, stack detection |
| `analytics_service.py` | Event logging, drop-off tracking, monthly report |
| `email_service.py` | SendGrid delivery, monthly scheduling |
| `exec_brief_service.py` | Executive brief generation, markdown export |
| `document_store.py` | File-based document management |
| `tools_service.py` | Tools catalog, Nemotron descriptions, caching, Ask Orbit prompts |
| `community_service.py` | Community posts, reactions, comments, Orbit AI replies, admin signals |

### Deployment
- Docker (python:3.11-slim) + Gunicorn on GCP Cloud Run
- GCP Cloud Build CI/CD via `cloudbuild.yaml`
- GCP Artifact Registry for Docker images
- 7 Flask blueprints: auth, intake, output, portal, documents, community, admin

---

## Version 2.0 — What's Coming

### GitHub Integration
- Connect ISV GitHub repo to Orbit
- Auto-detect new libraries from `requirements.txt` or `package.json`
- Surface new tools as Orbit chat conversation starters

### Full User Authentication
- Replace access codes with OAuth via Google
- Persistent profiles stored in database
- Multi-user support per ISV organization

### Persistent Database
- Move from file-based to Firestore or BigQuery
- Documents and strategies persist across sessions and devices
- Shareable strategy URLs

### Community V2
- Upvote/downvote posts (Reddit-style ranking)
- Follow companies and topics
- DM between verified ISV partners
- Orbit-generated weekly digest email for community highlights

### Orbit Chat Memory
- Chat history persisted across sessions
- "Last time we discussed X" context awareness

---

## Version 3.0 — The Long-Term Vision

### Multi-ISV Admin Intelligence
- Pipeline view of all ISVs simultaneously
- Cohort analysis by stage and concern
- Automated outreach drafts generated by Nemotron

### Orbit for Other NVIDIA Verticals
- Omniverse DevRel Orbit
- Metropolis (Retail / Smart Cities) Orbit
- Clara (Healthcare) Orbit
- One platform, configurable per vertical

### Fully Agentic Operation
- Orbit monitors ISV GitHub, GCP projects, and community activity
- When signal threshold is met, Orbit drafts a DevRel outreach for review
- DevRel manager approves and sends
- Orbit handles research. The human handles relationship.

---

## Why This Is an Agentic Solution

Orbit learns, infers, and acts across three surfaces simultaneously:

**It learns** from structured intake (problem statement, stack, concerns, team context) and unstructured signals (chat messages, community posts, format ranking behavior).

**It infers** learning style from ranking patterns, relevant NVIDIA products from use case descriptions, adoption blockers from team context, and community sentiment from post categories and reaction patterns.

**It acts** by generating deliverables, addressing concerns, describing tools, replying to community posts, alerting on new technologies, and delivering monthly intelligence reports — without waiting for a human to tell it what to do.

The DevRel manager is not removed. They are elevated. Orbit handles intelligence work. The human handles relationship work. That division of labor is what makes enterprise developer relations scale.

---

## Built On the Partnership It Advocates

Every architectural decision in Orbit demonstrates the NVIDIA + Google Cloud partnership.

The application runs on **GCP Cloud Run**. Stack detection uses the **GCP Service Usage API**. Inference runs on **NVIDIA NIM**. Recommendations surface **Vertex AI**, **GCP BigQuery**, and **GCP Cloud Storage** alongside NVIDIA products.

Orbit does not just talk about the partnership. It is built on it.

---

*[GitHub](https://github.com/itsChanelML/orbit-isv-intelligence-platform) · [Live Demo](https://orbit-isv-platform-474576936406.us-central1.run.app)*