"""
documents.py

Blueprint for the ISV documents library.
Handles document listing, preview, download, and deletion.
"""

from flask import Blueprint, render_template, session, redirect, url_for, Response, jsonify, request
from routes.auth import login_required
from services.document_store import (
    get_all_documents,
    get_document,
    get_document_content,
    get_document_stats,
    delete_document,
    get_download_filename,
    format_file_size,
    DOCUMENT_TYPES
)

documents_bp = Blueprint('documents', __name__)


def _get_session_id() -> str:
    """Get a stable session identifier."""
    if 'session_id' not in session:
        import uuid
        session['session_id'] = str(uuid.uuid4())[:12]
    return session['session_id']


@documents_bp.route('/portal/documents')
@login_required
def index():
    """Main documents library page."""
    session_id = _get_session_id()
    docs = get_all_documents(session_id)
    stats = get_document_stats(session_id)

    # Add formatted size to each doc
    for doc in docs:
        doc['size_formatted'] = format_file_size(doc.get('size_bytes', 0))

    return render_template('documents.html',
        docs=docs,
        stats=stats,
        doc_types=DOCUMENT_TYPES,
        role=session.get('role', 'isv'),
        stack_items=session.get('tech_stack', []),
        adoption_strategies=session.get('adoption_strategies', [])
    )


@documents_bp.route('/portal/documents/<doc_id>')
@login_required
def view_document(doc_id):
    """View a single document with preview."""
    session_id = _get_session_id()
    doc = get_document(session_id, doc_id)
    if not doc:
        return redirect(url_for('documents.index'))

    content = get_document_content(session_id, doc_id)
    doc['size_formatted'] = format_file_size(doc.get('size_bytes', 0))

    # Convert markdown to HTML for preview
    preview_html = ''
    if doc.get('type') in ['workshop', 'hackathon', 'exec_brief']:
        try:
            import markdown as md
            preview_html = md.markdown(content or '', extensions=['fenced_code', 'tables'])
        except Exception:
            preview_html = f"<pre>{content}</pre>"

    # Parse notebook cells for preview
    notebook_cells = []
    if doc.get('type') == 'notebook':
        try:
            import json
            nb = json.loads(content or '{}')
            for cell in nb.get('cells', [])[:5]:  # Preview first 5 cells
                notebook_cells.append({
                    'type': cell.get('cell_type', 'code'),
                    'source': ''.join(cell.get('source', []))
                })
        except Exception:
            pass

    return render_template('document_view.html',
        doc=doc,
        content=content,
        preview_html=preview_html,
        notebook_cells=notebook_cells,
        role=session.get('role', 'isv'),
        stack_items=session.get('tech_stack', []),
        adoption_strategies=session.get('adoption_strategies', [])
    )


@documents_bp.route('/portal/documents/<doc_id>/download')
@login_required
def download_document(doc_id):
    """Download a document file."""
    session_id = _get_session_id()
    doc = get_document(session_id, doc_id)
    if not doc:
        return redirect(url_for('documents.index'))

    content = get_document_content(session_id, doc_id)
    if not content:
        return redirect(url_for('documents.index'))

    filename = get_download_filename(doc)
    mimetype = doc.get('mimetype', 'text/plain')

    return Response(
        content,
        mimetype=mimetype,
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )


@documents_bp.route('/portal/documents/<doc_id>/delete', methods=['POST'])
@login_required
def delete_doc(doc_id):
    """Delete a document."""
    session_id = _get_session_id()
    delete_document(session_id, doc_id)
    return jsonify({'status': 'ok'})


@documents_bp.route('/portal/documents/api/list')
@login_required
def api_list():
    """API endpoint returning documents as JSON."""
    session_id = _get_session_id()
    docs = get_all_documents(session_id)
    for doc in docs:
        doc['size_formatted'] = format_file_size(doc.get('size_bytes', 0))
        doc.pop('file_path', None)  # Don't expose file paths
    return jsonify({'documents': docs, 'total': len(docs)})