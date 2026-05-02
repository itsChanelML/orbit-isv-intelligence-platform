from flask import Blueprint, render_template, session, redirect, url_for, request
from routes.auth import login_required

intake_bp = Blueprint('intake', __name__)


def get_intake():
    return session.get('intake', {})


def save_intake(data):
    intake = get_intake()
    intake.update(data)
    session['intake'] = intake


@intake_bp.route('/intake')
@login_required
def index():
    session['intake_step'] = 1
    return redirect(url_for('intake.step', step=1))


@intake_bp.route('/intake/step/<int:step>')
@login_required
def step(step):
    if step < 1 or step > 6:
        return redirect(url_for('intake.index'))
    intake = get_intake()
    return render_template('intake.html', step=step, intake=intake)


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
    save_intake({
        'problem_statement': request.form.get('problem_statement', '').strip(),
    })
    return redirect(url_for('intake.step', step=3))


@intake_bp.route('/intake/step/3', methods=['POST'])
@login_required
def step3_post():
    save_intake({
        'why_nvidia': request.form.get('why_nvidia', '').strip(),
    })
    return redirect(url_for('intake.step', step=4))


@intake_bp.route('/intake/step/4', methods=['POST'])
@login_required
def step4_post():
    tools_raw = request.form.get('selected_tools', '')
    tools = [t.strip() for t in tools_raw.split(',') if t.strip()]
    if not tools or len(tools) > 2:
        return redirect(url_for('intake.step', step=4))
    save_intake({'selected_tools': tools})
    return redirect(url_for('intake.step', step=5))


@intake_bp.route('/intake/step/5', methods=['POST'])
@login_required
def step5_post():
    team_context = request.form.get('team_context', '').strip()
    team_size = request.form.get('team_size', '').strip()
    if not team_context:
        return redirect(url_for('intake.step', step=5))
    save_intake({
        'team_context': team_context,
        'team_size': team_size if team_size else None,
    })
    return redirect(url_for('intake.step', step=6))


@intake_bp.route('/intake/step/6', methods=['POST'])
@login_required
def step6_post():
    ranking_raw = request.form.get('format_ranking', 'workshop,notebook,hackathon')
    ranking = [r.strip() for r in ranking_raw.split(',') if r.strip()]
    save_intake({'format_ranking': ranking})
    # All intake complete - go to output generation
    return redirect(url_for('output.generate'))


# Back navigation
@intake_bp.route('/intake/step/<int:step>/back')
@login_required
def step_back(step):
    target = max(1, step - 1)
    return redirect(url_for('intake.step', step=target))