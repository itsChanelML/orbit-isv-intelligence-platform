"""
tools_service.py

Handles loading of NVIDIA products and OSS tools catalogs,
Nemotron-powered description generation with file-based caching,
and Ask Orbit prompt string construction.
"""

import json
import os
import hashlib
from typing import Optional
from datetime import datetime, timezone

# File paths
NVIDIA_CATALOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'nvidia_products_catalog.json')
OSS_CATALOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'oss_tools_catalog.json')
TOOLS_CACHE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'tools_cache.json')


# ── Catalog Loaders ──────────────────────────────────────────────────────────

def load_nvidia_products() -> list:
    """Load NVIDIA products from catalog JSON."""
    try:
        with open(NVIDIA_CATALOG_FILE, 'r') as f:
            data = json.load(f)
        return data.get('catalog', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_oss_tools() -> list:
    """Load OSS developer tools from catalog JSON."""
    try:
        with open(OSS_CATALOG_FILE, 'r') as f:
            data = json.load(f)
        return data.get('tools', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_oss_categories() -> list:
    """Get all OSS tool categories."""
    try:
        with open(OSS_CATALOG_FILE, 'r') as f:
            data = json.load(f)
        return data.get('categories', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_nvidia_categories() -> list:
    """Get all NVIDIA product categories."""
    try:
        with open(NVIDIA_CATALOG_FILE, 'r') as f:
            data = json.load(f)
        return data.get('categories', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def get_tools_by_category(category: str, source: str = 'oss') -> list:
    """
    Get tools filtered by category.
    source: 'oss' for OSS tools, 'nvidia' for NVIDIA products
    """
    if source == 'nvidia':
        tools = load_nvidia_products()
    else:
        tools = load_oss_tools()
    return [t for t in tools if t.get('category') == category]


def search_tools(query: str) -> dict:
    """
    Search across both NVIDIA and OSS catalogs.
    Returns dict with 'nvidia' and 'oss' results.
    """
    query_lower = query.lower()
    nvidia_results = [
        t for t in load_nvidia_products()
        if query_lower in t.get('name', '').lower()
        or query_lower in t.get('description', '').lower()
        or query_lower in t.get('category', '').lower()
    ]
    oss_results = [
        t for t in load_oss_tools()
        if query_lower in t.get('name', '').lower()
        or query_lower in t.get('category', '').lower()
    ]
    return {'nvidia': nvidia_results, 'oss': oss_results}


# ── Description Cache ────────────────────────────────────────────────────────

def _load_cache() -> dict:
    """Load the tools description cache."""
    try:
        with open(TOOLS_CACHE_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_cache(cache: dict) -> None:
    """Save the tools description cache."""
    os.makedirs(os.path.dirname(TOOLS_CACHE_FILE), exist_ok=True)
    with open(TOOLS_CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)


def _cache_key(tool_name: str, company_name: Optional[str] = None) -> str:
    """Generate a cache key for a tool description."""
    key = f"{tool_name.lower().replace(' ', '_')}"
    if company_name:
        key += f"_{company_name.lower().replace(' ', '_')}"
    return hashlib.md5(key.encode()).hexdigest()[:12]


def get_cached_description(tool_name: str) -> Optional[str]:
    """Get a cached description for a tool if it exists."""
    cache = _load_cache()
    key = _cache_key(tool_name)
    entry = cache.get(key)
    if entry:
        return entry.get('description')
    return None


def cache_description(tool_name: str, description: str) -> None:
    """Cache a generated description for a tool."""
    cache = _load_cache()
    key = _cache_key(tool_name)
    cache[key] = {
        'tool': tool_name,
        'description': description,
        'generated_at': datetime.now(timezone.utc).isoformat()
    }
    _save_cache(cache)


# ── Nemotron Description Generation ─────────────────────────────────────────

def generate_tool_description(tool_name: str, category: str, use_cases: Optional[list] = None) -> str:
    """
    Generate a 2-3 sentence description of a tool using Nemotron via NIM.
    Checks cache first -- only calls NIM if not cached.
    Returns description string.
    """
    # Check cache first
    cached = get_cached_description(tool_name)
    if cached:
        return cached

    # Build prompt
    use_case_context = ''
    if use_cases:
        use_case_context = f" It is commonly used for: {', '.join(use_cases)}."

    prompt = f"""You are a senior NVIDIA Developer Relations engineer writing a developer tools reference.

Write exactly 2-3 sentences describing the following developer tool. Be specific, technical, and practical.
Focus on what it does, why developers use it, and how it relates to AI/ML workloads on NVIDIA hardware.

Tool: {tool_name}
Category: {category}{use_case_context}

Requirements:
- Exactly 2-3 sentences
- No bullet points
- No headers
- Start with the tool name
- Mention NVIDIA GPU compatibility or DGX Cloud relevance where applicable
- Be direct and informative

Return only the description text, nothing else."""

    try:
        from services.nim_service import _call_nim
        from config import Config

        description = _call_nim(
            Config.MODEL_PRIMARY,
            [{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.4
        )
        description = description.strip()

        # Cache the result
        cache_description(tool_name, description)
        return description

    except Exception:
        # Fallback description
        fallback = f"{tool_name} is an open-source {category.lower()} tool widely used in AI and ML development. It integrates with NVIDIA GPU infrastructure including DGX Cloud for accelerated workloads."
        cache_description(tool_name, fallback)
        return fallback


def generate_descriptions_batch(tools: list, max_tools: int = 10) -> dict:
    """
    Generate descriptions for a batch of tools.
    Only generates for tools not already cached.
    Returns dict of tool_name -> description.

    max_tools limits NIM calls per request to avoid timeouts.
    """
    results = {}
    nim_calls = 0

    for tool in tools:
        name = tool.get('name', '')
        if not name:
            continue

        # Check cache first
        cached = get_cached_description(name)
        if cached:
            results[name] = cached
            continue

        # Generate via NIM (up to max_tools new generations)
        if nim_calls < max_tools:
            category = tool.get('category', 'Developer Tool')
            use_cases = tool.get('use_cases', [])
            description = generate_tool_description(name, category, use_cases)
            results[name] = description
            nim_calls += 1
        else:
            # Return placeholder for uncached tools beyond limit
            results[name] = f"{name} is a powerful {tool.get('category', 'developer')} tool. Click to generate a full description."

    return results


# ── Ask Orbit Prompt Builder ─────────────────────────────────────────────────

def build_ask_orbit_prompt(tool_name: str, company_name: Optional[str] = None) -> str:
    """
    Build the pre-populated Ask Orbit prompt for a tool.
    If company_name is provided, personalizes the prompt.
    """
    if company_name and company_name.strip():
        return f"How can I use {tool_name} at {company_name}?"
    return f"How can I use {tool_name} with NVIDIA DGX Cloud?"


def get_tool_nvidia_relevance(tool_name: str) -> Optional[str]:
    """
    Return the relevant NVIDIA product pairing for a given OSS tool.
    Used to surface "pairs well with" suggestions on tool cards.
    """
    pairings = {
        'LangChain': 'NVIDIA NIM + RAG pipelines',
        'LlamaIndex': 'NVIDIA NIM Embeddings',
        'HuggingFace Transformers': 'NeMo Framework + DGX Cloud',
        'Unsloth': 'DGX Cloud H100 fine-tuning',
        'PEFT': 'NeMo Framework',
        'Axolotl': 'DGX Cloud H100 clusters',
        'TRL': 'NeMo RLHF pipelines',
        'vLLM': 'TensorRT-LLM + DGX Cloud',
        'Ollama': 'NVIDIA NIM microservices',
        'llama.cpp': 'TensorRT-LLM optimization',
        'Chroma': 'NVIDIA NIM Embeddings',
        'Weaviate': 'NVIDIA NIM Embeddings',
        'Qdrant': 'NVIDIA NIM Embeddings',
        'FAISS': 'NVIDIA NIM + cuVS',
        'PyTorch': 'CUDA + DGX Cloud',
        'DeepSpeed': 'NeMo + DGX Cloud',
        'Megatron-LM': 'DGX Cloud + NeMo',
        'Ray': 'DGX Cloud distributed training',
        'Weights & Biases': 'NeMo experiment tracking',
        'MLflow': 'Vertex AI + DGX Cloud',
        'RAGAS': 'NVIDIA NIM evaluation',
        'Whisper': 'NVIDIA Riva',
        'OpenCV': 'NVIDIA Metropolis',
        'AutoGen': 'NVIDIA NIM multi-agent',
        'CrewAI': 'NVIDIA NIM agentic workflows',
    }
    return pairings.get(tool_name)


# ── Full Catalog Builder ─────────────────────────────────────────────────────

def get_full_tools_catalog(company_name: Optional[str] = None, isv_stack: Optional[list] = None) -> dict:
    """
    Build the complete tools catalog for the tools library page.
    Returns structured dict with nvidia_products, oss_tools, and isv_stack sections.
    Generates descriptions for uncached tools via Nemotron.
    """
    nvidia_products = load_nvidia_products()
    oss_tools = load_oss_tools()

    # Generate descriptions for all tools (cached or NIM)
    nvidia_descriptions = generate_descriptions_batch(nvidia_products, max_tools=5)
    oss_descriptions = generate_descriptions_batch(oss_tools, max_tools=5)

    # Build nvidia section with descriptions and Ask Orbit prompts
    nvidia_section = []
    for product in nvidia_products:
        name = product.get('name', '')
        nvidia_section.append({
            **product,
            'description': nvidia_descriptions.get(name, ''),
            'ask_orbit_prompt': build_ask_orbit_prompt(name, company_name),
            'in_isv_stack': name in (isv_stack or [])
        })

    # Build OSS section with descriptions, relevance, and Ask Orbit prompts
    oss_section = []
    for tool in oss_tools:
        name = tool.get('name', '')
        oss_section.append({
            **tool,
            'description': oss_descriptions.get(name, ''),
            'nvidia_relevance': get_tool_nvidia_relevance(name),
            'ask_orbit_prompt': build_ask_orbit_prompt(name, company_name),
            'in_isv_stack': name in (isv_stack or [])
        })

    # Build ISV stack section (tools they've added)
    isv_section = []
    if isv_stack:
        all_tools = {t['name']: t for t in nvidia_products + oss_tools}
        for tool_name in isv_stack:
            if tool_name in all_tools:
                tool = all_tools[tool_name]
                isv_section.append({
                    **tool,
                    'description': nvidia_descriptions.get(tool_name) or oss_descriptions.get(tool_name, ''),
                    'ask_orbit_prompt': build_ask_orbit_prompt(tool_name, company_name),
                    'in_isv_stack': True
                })
            else:
                # Custom tool not in catalog
                isv_section.append({
                    'name': tool_name,
                    'category': 'Custom Stack',
                    'description': f"{tool_name} is part of your current technology stack.",
                    'ask_orbit_prompt': build_ask_orbit_prompt(tool_name, company_name),
                    'in_isv_stack': True,
                    'nvidia_compatible': False
                })

    return {
        'nvidia_products': nvidia_section,
        'oss_tools': oss_section,
        'isv_stack': isv_section,
        'nvidia_categories': get_nvidia_categories(),
        'oss_categories': get_oss_categories(),
        'company_name': company_name or ''
    }