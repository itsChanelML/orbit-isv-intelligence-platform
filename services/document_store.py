"""
document_store.py

Manages all generated documents for an ISV session.
Handles storage, retrieval, metadata, and download preparation
for workshops, notebooks, hackathon briefs, and exec briefs.

This is a file-based document store using JSON metadata + raw content files.
Each document is stored as:
  - data/docs/{session_id}/{doc_id}.txt  (raw content)
  - data/docs/{session_id}/manifest.json (metadata index)
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Optional


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'data', 'docs')

# ── Document Types ────────────────────────────────────────────────────────────

DOCUMENT_TYPES = {
    'workshop': {
        'label': 'Workshop Guide',
        'icon': '🎯',
        'extension': 'md',
        'mimetype': 'text/markdown',
        'description': 'Facilitated team session with structured exercises'
    },
    'notebook': {
        'label': 'Jupyter Notebook',
        'icon': '📓',
        'extension': 'ipynb',
        'mimetype': 'application/json',
        'description': 'Step-by-step technical lab for independent exploration'
    },
    'hackathon': {
        'label': 'Hackathon Brief',
        'icon': '⚡',
        'extension': 'md',
        'mimetype': 'text/markdown',
        'description': 'Internal hackathon challenge brief for your team'
    },
    'exec_brief': {
        'label': 'Executive Adoption Brief',
        'icon': '📊',
        'extension': 'md',
        'mimetype': 'text/markdown',
        'description': 'Business-focused adoption strategy for leadership'
    }
}


# ── Session Directory ─────────────────────────────────────────────────────────

def _session_dir(session_id: str) -> str:
    """Get or create the document directory for a session."""
    path = os.path.join(DOCS_DIR, session_id)
    os.makedirs(path, exist_ok=True)
    return path


def _manifest_path(session_id: str) -> str:
    return os.path.join(_session_dir(session_id), 'manifest.json')


def _content_path(session_id: str, doc_id: str, extension: str) -> str:
    return os.path.join(_session_dir(session_id), f"{doc_id}.{extension}")


# ── Manifest Operations ───────────────────────────────────────────────────────

def _load_manifest(session_id: str) -> list:
    """Load the document manifest for a session."""
    path = _manifest_path(session_id)
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def _save_manifest(session_id: str, manifest: list) -> None:
    """Save the document manifest for a session."""
    path = _manifest_path(session_id)
    with open(path, 'w') as f:
        json.dump(manifest, f, indent=2)


# ── Core Document Operations ──────────────────────────────────────────────────

def save_document(
    session_id: str,
    doc_type: str,
    content: str,
    company_name: str,
    title: Optional[str] = None,
    strategy_id: Optional[int] = None
) -> dict:
    """
    Save a generated document to the document store.

    Args:
        session_id: The Flask session ID
        doc_type: One of 'workshop', 'notebook', 'hackathon', 'exec_brief'
        content: The raw document content
        company_name: ISV company name for display
        title: Optional custom title for the document
        strategy_id: Links this document to an adoption strategy run

    Returns:
        Document metadata dict
    """
    doc_info = DOCUMENT_TYPES.get(doc_type, DOCUMENT_TYPES['workshop'])
    doc_id = str(uuid.uuid4())[:8]
    now = datetime.now(timezone.utc)

    # Save content to file
    content_file = _content_path(session_id, doc_id, doc_info['extension'])
    with open(content_file, 'w') as f:
        f.write(content)

    # Build metadata
    doc_meta = {
        'id': doc_id,
        'type': doc_type,
        'label': doc_info['label'],
        'icon': doc_info['icon'],
        'extension': doc_info['extension'],
        'mimetype': doc_info['mimetype'],
        'title': title or f"{doc_info['label']} — {company_name}",
        'company': company_name,
        'created_at': now.isoformat(),
        'date': now.strftime('%m.%d.%y'),
        'strategy_id': strategy_id,
        'file_path': content_file,
        'size_bytes': len(content.encode('utf-8'))
    }

    # Add to manifest
    manifest = _load_manifest(session_id)
    manifest.append(doc_meta)
    _save_manifest(session_id, manifest)

    return doc_meta


def get_document(session_id: str, doc_id: str) -> Optional[dict]:
    """Get document metadata by ID."""
    manifest = _load_manifest(session_id)
    for doc in manifest:
        if doc['id'] == doc_id:
            return doc
    return None


def get_document_content(session_id: str, doc_id: str) -> Optional[str]:
    """Get raw document content by ID."""
    doc = get_document(session_id, doc_id)
    if not doc:
        return None
    file_path = doc.get('file_path', '')
    if not file_path or not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as f:
        return f.read()


def get_all_documents(session_id: str) -> list:
    """Get all documents for a session, sorted newest first."""
    manifest = _load_manifest(session_id)
    return sorted(manifest, key=lambda d: d.get('created_at', ''), reverse=True)


def get_documents_by_type(session_id: str, doc_type: str) -> list:
    """Get all documents of a specific type for a session."""
    return [d for d in get_all_documents(session_id) if d['type'] == doc_type]


def delete_document(session_id: str, doc_id: str) -> bool:
    """Delete a document and its content file."""
    doc = get_document(session_id, doc_id)
    if not doc:
        return False

    # Delete content file
    file_path = doc.get('file_path', '')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)

    # Remove from manifest
    manifest = _load_manifest(session_id)
    manifest = [d for d in manifest if d['id'] != doc_id]
    _save_manifest(session_id, manifest)
    return True


def get_document_stats(session_id: str) -> dict:
    """Get summary statistics about a session's documents."""
    docs = get_all_documents(session_id)
    stats = {
        'total': len(docs),
        'by_type': {},
        'latest': docs[0] if docs else None
    }
    for doc_type in DOCUMENT_TYPES:
        count = len([d for d in docs if d['type'] == doc_type])
        if count > 0:
            stats['by_type'][doc_type] = count
    return stats


# ── Format Helpers ────────────────────────────────────────────────────────────

def format_file_size(size_bytes: int) -> str:
    """Format file size for display."""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes // 1024}KB"
    else:
        return f"{size_bytes // (1024 * 1024)}MB"


def get_download_filename(doc: dict) -> str:
    """Generate a clean download filename for a document."""
    company = doc.get('company', 'isv').lower().replace(' ', '-')
    doc_type = doc.get('type', 'document')
    date = doc.get('date', '').replace('.', '-')
    ext = doc.get('extension', 'md')
    return f"orbit-{company}-{doc_type}-{date}.{ext}"


def get_document_type_info(doc_type: str) -> dict:
    """Get display info for a document type."""
    return DOCUMENT_TYPES.get(doc_type, {
        'label': 'Document',
        'icon': '📄',
        'extension': 'md',
        'mimetype': 'text/markdown',
        'description': 'Generated document'
    })