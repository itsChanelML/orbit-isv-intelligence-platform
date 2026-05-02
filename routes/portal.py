from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from routes.auth import login_required

portal_bp = Blueprint('portal', __name__)

# In-memory stack store (per session) - GCP integration adds to this in later step
def get_stack():
    return session.get('tech_stack', [])

def add_to_stack(name):
    stack = get_stack()
    if name not in stack:
        stack.append(name)
        session['tech_stack'] = stack

@portal_bp.route('/portal')
@login_required
def index():
    role = session.get('role', 'isv')
    stack_items = get_stack()
    return render_template('portal.html', role=role, stack_items=stack_items)

@portal_bp.route('/portal/stack/add', methods=['POST'])
@login_required
def add_stack():
    data = request.get_json()
    name = data.get('name', '').strip()
    if name:
        add_to_stack(name)
    return jsonify({'status': 'ok', 'stack': get_stack()})

@portal_bp.route('/portal/chat', methods=['POST'])
@login_required
def chat():
    # Placeholder - NIM integration wired in Step 6
    data = request.get_json()
    message = data.get('message', '')
    return jsonify({
        'response': f"I received your message: \"{message}\". NIM integration coming in the next build step — Orbit will be fully powered by Nemotron shortly."
    })

@portal_bp.route('/portal/documents')
@login_required
def documents():
    return render_template('portal.html',
        role=session.get('role', 'isv'),
        stack_items=get_stack()
    )

@portal_bp.route('/portal/profile')
@login_required
def profile():
    return render_template('portal.html',
        role=session.get('role', 'isv'),
        stack_items=get_stack()
    )

@portal_bp.route('/portal/stack')
@login_required
def stack():
    return render_template('portal.html',
        role=session.get('role', 'isv'),
        stack_items=get_stack()
    )