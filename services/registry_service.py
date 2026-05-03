import json
import os
import random
import string
from config import Config

REGISTRY_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'isv_registry.json')
CATALOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'nvidia_products_catalog.json')


def _load_registry():
    try:
        with open(REGISTRY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _load_catalog():
    try:
        with open(CATALOG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"catalog": [], "categories": []}


def lookup_isv(domain):
    """
    Look up an ISV by domain in the registry.
    Returns the ISV profile dict or None if not found.
    """
    registry = _load_registry()
    domain = domain.lower().strip()
    return registry.get(domain)


def generate_otp():
    """Generate a 6-digit OTP for demo auth."""
    return ''.join(random.choices(string.digits, k=6))


def get_nvidia_products():
    """Get full NVIDIA product catalog."""
    catalog = _load_catalog()
    return catalog.get('catalog', [])


def get_products_by_category(category):
    """Get NVIDIA products filtered by category."""
    products = get_nvidia_products()
    return [p for p in products if p.get('category') == category]


def prefill_from_registry(domain, contact_name):
    """
    Given a domain, look up ISV registry and use Nemotron to generate
    a polished pre-fill for the intake form.
    Returns dict with pre-filled fields.
    """
    profile = lookup_isv(domain)

    if not profile:
        return None

    # Use Nemotron to generate a natural, polished version of the profile
    try:
        from services.nim_service import _call_nim
        from config import Config

        catalog = _load_catalog()
        nvidia_products = profile.get('nvidia_products_all', [])

        # Build product context from catalog
        product_details = []
        for item in catalog.get('catalog', []):
            if item['name'] in nvidia_products:
                product_details.append(f"- {item['name']}: {item['description']}")

        product_context = '\n'.join(product_details) if product_details else 'NVIDIA DGX Cloud, NIM microservices'

        prompt = f"""You are Orbit, NVIDIA's ISV intelligence platform. We found this ISV in our partner registry.

ISV REGISTRY DATA:
- Company: {profile['company_name']}
- Industry: {profile['industry']}
- Description: {profile['description']}
- Tagline: {profile['tagline']}
- NVIDIA Products: {', '.join(nvidia_products)}
- Tier: {profile.get('tier', 'Inception')}
- Contact: {contact_name}, {profile.get('contact_role', 'Engineer')}

NVIDIA PRODUCT CONTEXT:
{product_context}

Generate a natural, polished welcome message and confirm the company details. Keep it concise and warm.
Respond ONLY with a valid JSON object with these exact keys:
- "welcome_message": string (1 sentence welcoming them by name and company, mentioning their tier)
- "company_name": string (company name from registry)
- "description": string (polished version of their description, 1-2 sentences)
- "tagline": string (their tagline from registry)
- "problem_statement": string (their problem statement, polished)
- "recommended_products": array of strings (top 3 NVIDIA products for their use case from the catalog)
- "contact_role": string (their role from registry)

Return only the JSON object."""

        raw = _call_nim(
            Config.MODEL_PRIMARY,
            [{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.4
        )

        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        clean = clean.strip()

        result = json.loads(clean)
        result['found_in_registry'] = True
        result['nvidia_products'] = nvidia_products
        result['tier'] = profile.get('tier', 'Inception')
        return result

    except Exception as e:
        # Fallback to raw registry data if NIM call fails
        return {
            'found_in_registry': True,
            'welcome_message': f"Welcome, {contact_name}. We found {profile['company_name']} in the NVIDIA ISV registry.",
            'company_name': profile['company_name'],
            'description': profile['description'],
            'tagline': profile['tagline'],
            'problem_statement': profile.get('problem_statement', ''),
            'contact_role': profile.get('contact_role', ''),
            'recommended_products': profile.get('nvidia_products_recommended', []),
            'nvidia_products': profile.get('nvidia_products_all', []),
            'tier': profile.get('tier', 'Inception','NVIDIA Connect')
        }