import os
import json
import requests
from config import Config


def _call_nim(model, messages, max_tokens=1000, temperature=0.7):
    """Base NIM API call using OpenAI-compatible endpoint."""
    headers = {
        "Authorization": f"Bearer {Config.NVIDIA_API_KEY}",
        "Content-Type": "application/json"
    }
    if 'nemotron' in model:
        if not any(m.get('role') == 'system' for m in messages):
            messages = [{"role": "system", "content": "detailed thinking off"}] + messages

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }
    response = requests.post(
        f"{Config.NVIDIA_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=120
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def generate_recommendations(intake: dict) -> list:
    """
    Nemotron-super-49b: Generate 3 DGX Cloud integration recommendations
    based on full intake profile.
    Returns list of 3 dicts: {title, description, nvidia_stack, partner_tools, use_case}
    """
    tools = ', '.join(intake.get('selected_tools', []))
    team = intake.get('team_context', 'solo')
    team_size = intake.get('team_size', '')
    team_str = f"engineering team of {team_size}" if team == 'engineering_team' and team_size else team.replace('_', ' ')

    prompt = f"""You are Orbit, NVIDIA's ISV intelligence platform powered by DGX Cloud.

An ISV has completed onboarding. Based on their profile, generate exactly 3 specific, actionable DGX Cloud integration recommendations.

ISV PROFILE:
- Company: {intake.get('company_name')}
- Description: {intake.get('company_description')}
- Tagline: {intake.get('tagline')}
- Problem: {intake.get('problem_statement')}
- Why NVIDIA: {intake.get('why_nvidia')}
- Tools: {tools}
- Team: {team_str}

REQUIREMENTS FOR EACH RECOMMENDATION:
1. Must be specific to their use case and tools
2. Must name exact NVIDIA NIM microservices (e.g. nvidia/llama-3.1-8b-instruct, nvidia/nv-embedqa-e5-v5, etc.)
3. Must name relevant NVIDIA stack components (DGX Cloud, NIM, CUDA, TensorRT-LLM, NeMo, etc.)
4. Must weave in partner tools contextually (Google Cloud Platform, Anthropic Claude API, Vercel, etc.)
5. Must be realistic and technically grounded

Respond ONLY with a valid JSON array of exactly 3 objects. Each object must have these exact keys:
- "title": string (short, specific recommendation title)
- "description": string (2-3 sentences explaining what to build and why)
- "nvidia_stack": array of strings (exact NVIDIA components and NIM models to use)
- "partner_tools": array of strings (GCP services, Anthropic, deployment tools)
- "complexity": string (one of: "Starter", "Intermediate", "Advanced")

Return only the JSON array. No preamble, no markdown, no explanation."""

    raw = _call_nim(Config.MODEL_PRIMARY, [{"role": "user", "content": prompt}], max_tokens=1500)

    # Clean and parse JSON
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("```")[1]
        if clean.startswith("json"):
            clean = clean[4:]
    clean = clean.strip()

    try:
        return json.loads(clean)
    except Exception as e:
        print(f"[Orbit] JSON parse failed: {e}")
        print(f"[Orbit] Raw response preview: {raw[:300]}")
        return _fallback_recommendations(intake)


def infer_learning_style(format_ranking: list) -> dict:
    """
    Llama-3.1-8b: Infer learning style from format ranking.
    Returns {style_label, style_description, primary_format}
    """
    ranking_str = ' > '.join(format_ranking)

    prompt = f"""Based on how someone ranked their preferred learning formats, infer their learning style.

Ranking (most preferred first): {ranking_str}

Format definitions:
- workshop: Facilitated group learning with discussion and exercises
- notebook: Independent technical exploration and hands-on coding
- hackathon: Collaborative problem-solving under time pressure

Respond ONLY with a valid JSON object with these exact keys:
- "style_label": string (2-3 word label, e.g. "Collaborative Builder", "Independent Learner", "Competitive Executor")
- "style_description": string (1 sentence describing their learning preference)
- "primary_format": string (the first item in the ranking)

Return only the JSON object. No preamble."""

    raw = _call_nim(Config.MODEL_INTAKE, [{"role": "user", "content": prompt}], max_tokens=200, temperature=0.5)

    clean = raw.strip().strip("```json").strip("```").strip()
    try:
        return json.loads(clean)
    except Exception:
        return {
            "style_label": "Adaptive Learner",
            "style_description": "Prefers a flexible approach to learning new technologies.",
            "primary_format": format_ranking[0] if format_ranking else "workshop"
        }


def generate_workshop(intake: dict, recommendations: list) -> str:
    """
    Nemotron: Generate a workshop facilitator guide in markdown.
    """
    tools = ', '.join(intake.get('selected_tools', []))
    recs_summary = '\n'.join([f"- {r['title']}: {r['description']}" for r in recommendations])

    prompt = f"""You are Orbit, NVIDIA's ISV intelligence platform.

Generate a professional workshop facilitator guide for an ISV team learning to integrate DGX Cloud into their stack.

ISV PROFILE:
- Company: {intake.get('company_name')}
- Problem: {intake.get('problem_statement')}
- Tools: {tools}
- Team: {intake.get('team_context', '').replace('_', ' ')}

TOP RECOMMENDATIONS:
{recs_summary}

Create a complete workshop guide in Markdown format. Include:
1. Workshop title and overview
2. Prerequisites and setup
3. Learning objectives (3-5)
4. Agenda with timing (90-120 min total)
5. Exercise 1: Hands-on NIM setup
6. Exercise 2: Tool integration with DGX Cloud
7. Group discussion prompts
8. Next steps and resources

Be specific to their use case. Reference exact NVIDIA NIM endpoints and GCP services where relevant.
Return only the Markdown content."""

    return _call_nim(Config.MODEL_PRIMARY, [{"role": "user", "content": prompt}], max_tokens=2000)


def generate_hackathon_brief(intake: dict, recommendations: list) -> str:
    """
    Nemotron: Generate a hackathon brief in markdown.
    """
    tools = ', '.join(intake.get('selected_tools', []))
    top_rec = recommendations[0] if recommendations else {}

    prompt = f"""You are Orbit, NVIDIA's ISV intelligence platform.

Generate an internal hackathon brief for an ISV team to tackle their DGX Cloud integration challenge.

ISV PROFILE:
- Company: {intake.get('company_name')}
- Problem: {intake.get('problem_statement')}
- Tools: {tools}
- Top Recommendation: {top_rec.get('title', '')}: {top_rec.get('description', '')}

Create a hackathon brief in Markdown format. Include:
1. Hackathon title and theme
2. The challenge statement (specific to their use case)
3. Success criteria (what does winning look like?)
4. Technical constraints and stack requirements (NVIDIA NIM, DGX Cloud, GCP)
5. Team structure suggestions
6. Timeline (1-day or 2-day format with milestones)
7. Judging criteria
8. Resources and starter code hints

Make it energizing and technically specific. Return only the Markdown content."""

    return _call_nim(Config.MODEL_PRIMARY, [{"role": "user", "content": prompt}], max_tokens=1500)


def generate_notebook(intake: dict, recommendations: list) -> str:
    """
    Mistral-7b: Generate Jupyter notebook as JSON string.
    """
    tools = ', '.join(intake.get('selected_tools', []))
    top_rec = recommendations[0] if recommendations else {}
    nvidia_stack = ', '.join(top_rec.get('nvidia_stack', []))

    prompt = f"""You are a technical AI engineer creating a Jupyter notebook for an ISV team.

Create a practical Jupyter notebook for integrating DGX Cloud with their stack.

ISV PROFILE:
- Company: {intake.get('company_name')}
- Problem: {intake.get('problem_statement')}
- Tools: {tools}
- NVIDIA Stack: {nvidia_stack}
- Top Use Case: {top_rec.get('title', '')}

Generate a Jupyter notebook JSON (nbformat 4.4) with:
1. Title markdown cell
2. Overview and objectives markdown cell
3. Install dependencies code cell (pip installs for their tools + openai for NIM)
4. Setup and authentication code cell (NVIDIA_API_KEY, GCP setup)
5. Core integration code cell (actual working code using NIM endpoint)
6. Tool-specific integration cell ({tools})
7. Test and validate cell
8. Next steps markdown cell

Use real NVIDIA NIM API patterns:
- base_url = "https://integrate.api.nvidia.com/v1"
- Use openai Python client pointed at NIM

Return ONLY valid nbformat 4.4 JSON. No preamble."""

    raw = _call_nim(Config.MODEL_CODEGEN, [{"role": "user", "content": prompt}], max_tokens=1500, temperature=0.3)
    
    clean = raw.strip()
    if clean.startswith("```"):
        clean = clean.split("```")[1]
        if clean.startswith("json"):
            clean = clean[4:]
    clean = clean.strip()

    # Validate it's parseable JSON
    try:
        json.loads(clean)
        return clean
    except Exception:
        return _fallback_notebook(intake, top_rec)


def chat_with_orbit(message: str, intake: dict, history: list) -> str:
    """
    Nemotron: Orbit chat grounded in ISV profile and outputs.
    """
    context = f"""You are Orbit, an intelligent DGX Cloud adoption assistant for NVIDIA ISV partners.

You are helping: {intake.get('company_name', 'an ISV')}
Their problem: {intake.get('problem_statement', '')}
Their tools: {', '.join(intake.get('selected_tools', []))}
Their team: {intake.get('team_context', '').replace('_', ' ')}

You are knowledgeable about:
- NVIDIA DGX Cloud, NIM microservices, CUDA, TensorRT-LLM, NeMo
- Google Cloud Platform (GKE, Vertex AI, Cloud Run, BigQuery)
- Anthropic Claude API
- HuggingFace, LangChain, Unsloth
- Developer adoption, workshops, hackathons, technical education

Be concise, warm, and technically specific. Always tie answers back to their use case."""

    messages = [{"role": "system", "content": context}]
    for h in history[-6:]:  # Last 6 turns for context
        messages.append(h)
    messages.append({"role": "user", "content": message})

    return _call_nim(Config.MODEL_PRIMARY, messages, max_tokens=600)


# ── Fallbacks ──

def _fallback_recommendations(intake):
    tools = intake.get('selected_tools', ['HuggingFace'])
    return [
        {
            "title": f"DGX Cloud Inference Pipeline with NIM",
            "description": f"Deploy {tools[0]} models via NVIDIA NIM microservices on DGX Cloud for optimized GPU inference. Use TensorRT-LLM for up to 3x throughput improvement over standard deployment.",
            "nvidia_stack": ["NVIDIA NIM", "DGX Cloud", "TensorRT-LLM", "nvidia/llama-3.1-8b-instruct"],
            "partner_tools": ["Google Cloud Run", "GCP Vertex AI"],
            "complexity": "Starter"
        },
        {
            "title": "Fine-Tuning Pipeline on DGX Cloud",
            "description": "Run parameter-efficient fine-tuning using your proprietary data on DGX Cloud H100 clusters. Use NeMo framework for training orchestration with automatic checkpointing.",
            "nvidia_stack": ["DGX Cloud", "NeMo Framework", "CUDA", "H100 GPUs"],
            "partner_tools": ["Google Cloud Storage", "GCP BigQuery"],
            "complexity": "Intermediate"
        },
        {
            "title": "RAG Pipeline with NIM Embeddings",
            "description": "Build a retrieval-augmented generation pipeline using NVIDIA NIM embedding microservices and your vector store. Combine with LangChain for orchestration.",
            "nvidia_stack": ["NVIDIA NIM", "nvidia/nv-embedqa-e5-v5", "DGX Cloud"],
            "partner_tools": ["Anthropic Claude API", "Google Cloud Run", "Vercel"],
            "complexity": "Intermediate"
        }
    ]


def _fallback_notebook(intake, top_rec):
    import json as j
    nb = {
        "nbformat": 4,
        "nbformat_minor": 4,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [f"# DGX Cloud Integration: {intake.get('company_name', 'ISV')}\n\nGenerated by Orbit — NVIDIA ISV Intelligence Platform"]},
            {"cell_type": "code", "metadata": {}, "source": ["!pip install openai langchain huggingface_hub"], "outputs": [], "execution_count": None},
            {"cell_type": "code", "metadata": {}, "source": [
                "import os\nfrom openai import OpenAI\n\n",
                "client = OpenAI(\n",
                "    base_url='https://integrate.api.nvidia.com/v1',\n",
                "    api_key=os.environ.get('NVIDIA_API_KEY')\n",
                ")\n\n",
                "response = client.chat.completions.create(\n",
                "    model='nvidia/llama-3.3-nemotron-super-49b-v1',\n",
                "    messages=[{'role': 'user', 'content': 'Hello from DGX Cloud!'}],\n",
                "    max_tokens=100\n",
                ")\n",
                "print(response.choices[0].message.content)"
            ], "outputs": [], "execution_count": None}
        ]
    }
    return j.dumps(nb)