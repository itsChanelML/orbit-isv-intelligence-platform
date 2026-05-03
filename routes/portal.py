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
    adoption_strategies = session.get('adoption_strategies', [])
    return render_template('portal.html', role=role, stack_items=stack_items, adoption_strategies=adoption_strategies)

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

@portal_bp.route('/portal/stack/gcp-status', methods=['GET'])
@login_required
def gcp_status():
    try:
        from services.gcp_service import get_connection_status, get_current_stack_from_gcp
        status = get_connection_status()
        if status['connected']:
            stack, error = get_current_stack_from_gcp()
            if stack:
                # Merge GCP stack into session stack
                current = session.get('tech_stack', [])
                for item in stack:
                    if item not in current:
                        current.append(item)
                session['tech_stack'] = current
            status['gcp_stack'] = stack or []
        return jsonify(status)
    except Exception as e:
        return jsonify({'connected': False, 'message': str(e)})


@portal_bp.route('/portal/stack/gcp-alerts', methods=['GET'])
@login_required
def gcp_alerts():
    try:
        from services.gcp_service import get_pending_alerts
        alerts = get_pending_alerts()
        return jsonify({'alerts': alerts})
    except Exception as e:
        return jsonify({'alerts': []})


@portal_bp.route('/portal/stack/gcp-sync', methods=['POST'])
@login_required
def gcp_sync():
    try:
        from services.gcp_service import check_for_new_services, get_current_stack_from_gcp
        new_services, error = check_for_new_services(
            session_id=session.get('session_id')
        )
        stack, _ = get_current_stack_from_gcp()
        if stack:
            current = session.get('tech_stack', [])
            for item in stack:
                if item not in current:
                    current.append(item)
            session['tech_stack'] = current
        return jsonify({
            'status': 'ok',
            'new_services': new_services,
            'stack': session.get('tech_stack', []),
            'error': error
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
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