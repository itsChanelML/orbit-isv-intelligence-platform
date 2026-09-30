from flask import Blueprint, render_template, session, redirect, url_for, request
from urllib.parse import urlparse
from routes.auth import login_required

intake_bp = Blueprint('intake', __name__)


def get_intake():
    return session.get('intake', {})


def save_intake(data):
    intake = get_intake()
    intake.update(data)
    session['intake'] = intake


def extract_domain(value):
    value = value.strip().lower()
    if '@' in value:
        return value.split('@')[-1]
    if not value.startswith('http'):
        value = 'https://' + value
    parsed = urlparse(value)
    domain = parsed.netloc.replace('www.', '')
    return domain


def domains_match(email, website):
    return extract_domain(email) == extract_domain(website)


# ── Step 0: Identity ──
@intake_bp.route('/intake')
@login_required
def index():
    session['intake'] = {}
    return redirect(url_for('intake.step0'))


@intake_bp.route('/intake/step/0')
@login_required
def step0():
    return render_template('intake.html', step=0, intake=get_intake(), error=None)


@intake_bp.route('/intake/step/0', methods=['POST'])
@login_required
def step0_post():
    name = request.form.get('contact_name', '').strip()
    email = request.form.get('contact_email', '').strip()
    website = request.form.get('company_website', '').strip()

    if not name or not email or not website:
        return render_template('intake.html', step=0,
            intake={'contact_name': name, 'contact_email': email, 'company_website': website},
            error='Please fill in all fields.')

    if not domains_match(email, website):
        email_domain = extract_domain(email)
        website_domain = extract_domain(website)
        return render_template('intake.html', step=0,
            intake={'contact_name': name, 'contact_email': email, 'company_website': website},
            error=f'Your email domain (@{email_domain}) must match your company website ({website_domain}). Please use your work email.')

    # Generate OTP
    from services.registry_service import generate_otp
    otp = generate_otp()
    session['otp'] = otp

    # Registry lookup -- direct JSON read, no NIM call (instant)
    domain = extract_domain(email)
    try:
        from services.registry_service import lookup_isv
        profile = lookup_isv(domain)
        if profile:
            prefill = {
                'found_in_registry': True,
                'welcome_message': f"Welcome, {name}. We found {profile['company_name']} in the NVIDIA ISV registry.",
                'company_name': profile['company_name'],
                'description': profile['description'],
                'tagline': profile['tagline'],
                'problem_statement': profile.get('problem_statement', ''),
                'contact_role': profile.get('contact_role', ''),
                'recommended_products': profile.get('nvidia_products_recommended', []),
                'nvidia_products': profile.get('nvidia_products_all', []),
                'tier': profile.get('tier', 'Inception')
            }
        else:
            prefill = None
    except Exception:
        prefill = None

    save_intake({
        'contact_name': name,
        'contact_email': email,
        'company_website': website,
        'company_name': prefill.get('company_name', '') if prefill else '',
        'company_description': prefill.get('description', '') if prefill else '',
        'tagline': prefill.get('tagline', '') if prefill else '',
        'problem_statement': prefill.get('problem_statement', '') if prefill else '',
        'contact_role': prefill.get('contact_role', '') if prefill else '',
        'nvidia_products': prefill.get('nvidia_products', []) if prefill else [],
        'welcome_message': prefill.get('welcome_message', '') if prefill else '',
        'tier': prefill.get('tier', '') if prefill else '',
        'found_in_registry': bool(prefill),
    })

    return redirect(url_for('intake.step0c'))


# ── Step 0c: OTP Verification ──
@intake_bp.route('/intake/step/0c')
@login_required
def step0c():
    intake = get_intake()
    if not intake.get('contact_email'):
        return redirect(url_for('intake.step0'))
    otp = session.get('otp', '000000')
    return render_template('intake.html', step='0c', intake=intake, otp=otp, error=None)


@intake_bp.route('/intake/step/0c', methods=['POST'])
@login_required
def step0c_post():
    entered = request.form.get('otp_code', '').strip()
    real_otp = session.get('otp', '')

    if entered != real_otp:
        intake = get_intake()
        otp = session.get('otp', '000000')
        return render_template('intake.html', step='0c', intake=intake, otp=otp,
            error='Incorrect verification code. Please try again.')

    return redirect(url_for('intake.step0b'))


# ── Async NIM prefill endpoint ──
@intake_bp.route('/intake/prefill', methods=['POST'])
@login_required
def async_prefill():
    """
    Called by JS after step 0b loads.
    Runs Nemotron prefill in background and returns polished data.
    """
    intake = get_intake()
    domain = extract_domain(intake.get('contact_email', ''))
    name = intake.get('contact_name', '')

    try:
        from services.registry_service import prefill_from_registry
        from flask import jsonify
        prefill = prefill_from_registry(domain, name)
        if prefill:
            # Update session with polished data
            save_intake({
                'company_name': prefill.get('company_name', intake.get('company_name', '')),
                'company_description': prefill.get('description', ''),
                'tagline': prefill.get('tagline', ''),
                'problem_statement': prefill.get('problem_statement', ''),
                'contact_role': prefill.get('contact_role', intake.get('contact_role', '')),
                'welcome_message': prefill.get('welcome_message', ''),
            })
            return jsonify({'status': 'ok', 'prefill': prefill})
        return jsonify({'status': 'not_found'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


# ── Step 0b: Confirm company + role ──
@intake_bp.route('/intake/step/0b')
@login_required
def step0b():
    intake = get_intake()
    if not intake.get('contact_email'):
        return redirect(url_for('intake.step0'))
    return render_template('intake.html', step='0b', intake=intake)


@intake_bp.route('/intake/step/0b', methods=['POST'])
@login_required
def step0b_post():
    role = request.form.get('contact_role', '').strip()
    company_name = request.form.get('company_name', '').strip()
    save_intake({
        'contact_role': role,
        'company_name': company_name,
    })
    return redirect(url_for('intake.step', step=1))


# ── Steps 1-8 ──
@intake_bp.route('/intake/step/<int:step>')
@login_required
def step(step):
    if step < 1 or step > 8:
        return redirect(url_for('intake.index'))
    intake = get_intake()
    if not intake.get('contact_email'):
        return redirect(url_for('intake.step0'))
    return render_template('intake.html', step=step, intake=intake, error=None)


@intake_bp.route('/intake/step/1', methods=['POST'])
@login_required
def step1_post():
    save_intake({
        'company_name': request.form.get('company_name', '').strip(),
        'company_description': request.form.get('company_description', '').strip(),
        'tagline': request.form.get('tagline', '').strip(),
    })
    return redirect(url_for('intake.step', step=2))


@intake_bp.route('/intake/step/2', methods=['POST'])
@login_required
def step2_post():
    stack_raw = request.form.get('current_stack', '')
    stack_items = [s.strip() for s in stack_raw.split(',') if s.strip()]
    additional = request.form.get('additional_stack', '').strip()
    if additional:
        for item in additional.split(','):
            item = item.strip()
            if item and item not in stack_items:
                stack_items.append(item)

    current = session.get('tech_stack', [])
    for item in stack_items:
        if item not in current:
            current.append(item)
    session['tech_stack'] = current

    save_intake({'current_stack': stack_items})
    return redirect(url_for('intake.step', step=3))


@intake_bp.route('/intake/step/3', methods=['POST'])
@login_required
def step3_post():
    save_intake({
        'problem_statement': request.form.get('problem_statement', '').strip(),
    })
    return redirect(url_for('intake.step', step=4))


@intake_bp.route('/intake/step/4', methods=['POST'])
@login_required
def step4_post():
    save_intake({
        'why_nvidia': request.form.get('why_nvidia', '').strip(),
    })
    return redirect(url_for('intake.step', step=5))


@intake_bp.route('/intake/step/5', methods=['POST'])
@login_required
def step5_post():
    tools_raw = request.form.get('selected_tools', '')
    tools = [t.strip() for t in tools_raw.split(',') if t.strip()]
    if not tools or len(tools) > 2:
        return redirect(url_for('intake.step', step=5))
    save_intake({'selected_tools': tools})
    return redirect(url_for('intake.step', step=6))


@intake_bp.route('/intake/step/6', methods=['POST'])
@login_required
def step6_post():
    preset_concerns = request.form.getlist('preset_concerns')
    custom_concern = request.form.get('custom_concern', '').strip()
    all_concerns = preset_concerns.copy()
    if custom_concern:
        all_concerns.append(custom_concern)
    save_intake({'adoption_concerns': all_concerns})
    return redirect(url_for('intake.step', step=7))


@intake_bp.route('/intake/step/7', methods=['POST'])
@login_required
def step7_post():
    team_context = request.form.get('team_context', '').strip()
    team_size = request.form.get('team_size', '').strip()
    if not team_context:
        return redirect(url_for('intake.step', step=7))
    save_intake({
        'team_context': team_context,
        'team_size': team_size if team_size else None,
    })
    return redirect(url_for('intake.step', step=8))


@intake_bp.route('/intake/step/8', methods=['POST'])
@login_required
def step8_post():
    ranking_raw = request.form.get('format_ranking', 'workshop,notebook,hackathon')
    ranking = [r.strip() for r in ranking_raw.split(',') if r.strip()]
    save_intake({'format_ranking': ranking})
    return redirect(url_for('output.generate'))


# Back navigation
@intake_bp.route('/intake/step/<int:step>/back')
@login_required
def step_back(step):
    if step <= 1:
        return redirect(url_for('intake.step0b'))
    return redirect(url_for('intake.step', step=step - 1))


@intake_bp.route('/intake/step/0b/back')
@login_required
def step0b_back():
    return redirect(url_for('intake.step0c'))


@intake_bp.route('/intake/step/0c/back')
@login_required
def step0c_back():
    return redirect(url_for('intake.step0'))