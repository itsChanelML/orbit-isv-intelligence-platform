import json
import os
import random
import string
from config import Config

# Absolute path fix for Cloud Run compatibility
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_FILE = os.path.join(BASE_DIR, 'data', 'isv_registry.json')
CATALOG_FILE = os.path.join(BASE_DIR, 'data', 'nvidia_products_catalog.json')

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


def prefill_from_registry(domain: str, contact_name: str):
    """
    Look up ISV registry and return pre-fill data directly without NIM call.
    Reads straight from JSON registry for instant population.
    """
    profile = lookup_isv(domain)
    if not profile:
        return None

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
        'tier': profile.get('tier', 'Inception')
    }