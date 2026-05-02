import uuid
from flask import Blueprint, render_template, request, session, redirect, url_for
from config import Config

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/', methods=['GET'])
@auth_bp.route('/login', methods=['GET'])
def login():
    if session.get('role') == 'admin':
        return redirect(url_for('admin.dashboard'))
    if session.get('role') == 'isv':
        return redirect(url_for('portal.index'))
    return render_template('login.html', error=None)


@auth_bp.route('/login', methods=['POST'])
def login_post():
    code = request.form.get('access_code', '').strip().upper()

    if code == Config.ADMIN_ACCESS_CODE.upper():
        session['role'] = 'admin'
        session['access_code'] = code
        session.permanent = True
        return redirect(url_for('admin.dashboard'))

    elif code == Config.ISV_ACCESS_CODE.upper():
        session['role'] = 'isv'
        session['access_code'] = code
        session.permanent = True
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        try:
            from services.analytics_service import log_session_start
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            log_session_start(session_id, ip, role='isv')
        except Exception:
            pass
        return redirect(url_for('portal.index'))

    else:
        return render_template('login.html', error='Invalid access code. Please try again.')


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# Helper decorators
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('role'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated