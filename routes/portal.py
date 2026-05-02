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
    from services.nim_service import chat_with_orbit
    data = request.get_json()
    message = data.get('message', '')
    history = data.get('history', [])
    intake = session.get('intake', {})

    if not message:
        return jsonify({'response': 'Please send a message.'})

    try:
        response = chat_with_orbit(message, intake, history)
        # Log chat for trending topics
        try:
            from services.analytics_service import log_chat_message
            log_chat_message(
                session_id=session.get('session_id', 'unknown'),
                message=message,
                company_name=intake.get('company_name')
            )
        except Exception:
            pass
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Orbit is unavailable right now. Error: {str(e)}'})

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