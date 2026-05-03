import json
import os
import markdown as md
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, Response
from routes.auth import login_required
from services.nim_service import (
    generate_recommendations,
    infer_learning_style,
    generate_workshop,
    generate_hackathon_brief,
    generate_notebook
)

output_bp = Blueprint('output', __name__)


@output_bp.route('/output/generate')
@login_required
def generate():
    intake = session.get('intake', {})
    if not intake or not intake.get('company_name'):
        return redirect(url_for('intake.index'))

    # Check if we already generated (avoid re-calling NIM on refresh)
    if session.get('output_ready'):
        return redirect(url_for('output.results'))

    return render_template('output.html', state='loading', intake=intake)


@output_bp.route('/output/run', methods=['POST'])
@login_required
def run():
    """Called by JS on the loading screen to trigger NIM generation."""
    intake = session.get('intake', {})
    if not intake:
        return jsonify({'error': 'No intake data'}), 400

    try:
        # Step 1: Generate recommendations with Nemotron
        recommendations = generate_recommendations(intake)
        session['recommendations'] = recommendations

        # Step 2: Infer learning style with Llama 3.1 8B
        ranking = intake.get('format_ranking', ['workshop', 'notebook', 'hackathon'])
        learning_style = infer_learning_style(ranking)
        session['learning_style'] = learning_style

        # Step 3: Generate primary deliverable based on top format
        primary_format = ranking[0] if ranking else 'workshop'
        deliverable_content = ''

        if primary_format == 'workshop':
            deliverable_content = generate_workshop(intake, recommendations)
        elif primary_format == 'hackathon':
            deliverable_content = generate_hackathon_brief(intake, recommendations)
        elif primary_format == 'notebook':
            deliverable_content = generate_notebook(intake, recommendations)

        # Write deliverable to file instead of session
        import os
        deliverable_path = os.path.join('data', f"deliverable_{session.get('session_id', 'tmp')}.txt")
        with open(deliverable_path, 'w') as f:
            f.write(deliverable_content)
        session['deliverable_path'] = deliverable_path
        session['deliverable_content'] = ''  # Don't store in cookie
        session['primary_format'] = primary_format
        session['output_ready'] = True

        # Auto-add selected tools to tech stack
        try:
            selected_tools = intake.get('selected_tools', [])
            current_stack = session.get('tech_stack', [])
            for tool in selected_tools:
                tool_name = tool.title()
                if tool_name not in current_stack:
                    current_stack.append(tool_name)
            session['tech_stack'] = current_stack
        except Exception:
            pass

        # Generate concern responses
        try:
            from services.nim_service import generate_concern_responses
            concerns = intake.get('adoption_concerns', [])
            concern_responses = generate_concern_responses(intake, concerns) if concerns else []
            session['concern_responses'] = concern_responses
        except Exception:
            session['concern_responses'] = []

        # Save adoption strategy to history
        try:
            from datetime import datetime, timezone
            strategies = session.get('adoption_strategies', [])
            strategies.append({
                'id': len(strategies) + 1,
                'company': intake.get('company_name', 'Unknown'),
                'date': datetime.now(timezone.utc).strftime('%m.%d.%y'),
                'primary_format': primary_format,
                'tools': intake.get('selected_tools', []),
            })
            session['adoption_strategies'] = strategies
        except Exception:
            pass

        # Log completed output
        try:
            from services.analytics_service import log_output_generated
            log_output_generated(
                session_id=session.get('session_id', 'unknown'),
                company_name=intake.get('company_name', 'Unknown'),
                format_ranking=ranking,
                learning_style=learning_style
            )
        except Exception:
            pass

        return jsonify({'status': 'ready'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@output_bp.route('/output/results')
@login_required
def results():
    if not session.get('output_ready'):
        return redirect(url_for('output.generate'))

    intake = session.get('intake', {})
    recommendations = session.get('recommendations', [])
    learning_style = session.get('learning_style', {})
    primary_format = session.get('primary_format', 'workshop')
    deliverable_path = session.get('deliverable_path', '')
    deliverable_content = ''
    if deliverable_path and os.path.exists(deliverable_path):
        with open(deliverable_path, 'r') as f:
            deliverable_content = f.read()

    # Convert markdown to HTML for preview
    deliverable_html = ''
    if primary_format in ['workshop', 'hackathon']:
        deliverable_html = md.markdown(deliverable_content, extensions=['fenced_code', 'tables'])

    # Parse notebook cells for preview
    notebook_cells = []
    if primary_format == 'notebook':
        try:
            nb = json.loads(deliverable_content)
            for cell in nb.get('cells', []):
                notebook_cells.append({
                    'type': cell.get('cell_type', 'code'),
                    'source': ''.join(cell.get('source', []))
                })
        except Exception:
            notebook_cells = []

    return render_template('output.html',
        state='results',
        intake=intake,
        recommendations=recommendations,
        learning_style=learning_style,
        primary_format=primary_format,
        deliverable_html=deliverable_html,
        notebook_cells=notebook_cells,
        concern_responses=session.get('concern_responses', []),
        role=session.get('role', 'isv')
    )


@output_bp.route('/output/download/<format_type>')
@login_required
def download(format_type):
    intake = session.get('intake', {})
    company = intake.get('company_name', 'ISV').replace(' ', '-').lower()
    deliverable_path = session.get('deliverable_path', '')
    content = ''
    if deliverable_path and os.path.exists(deliverable_path):
        with open(deliverable_path, 'r') as f:
            content = f.read()

    if format_type == 'md':
        return Response(
            content,
            mimetype='text/markdown',
            headers={'Content-Disposition': f'attachment; filename=orbit-{company}-deliverable.md'}
        )
    elif format_type == 'txt':
        plain = content.replace('#', '').replace('**', '').replace('*', '').replace('`', '')
        return Response(
            plain,
            mimetype='text/plain',
            headers={'Content-Disposition': f'attachment; filename=orbit-{company}-deliverable.txt'}
        )
    elif format_type == 'ipynb':
        return Response(
            content,
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename=orbit-{company}-notebook.ipynb'}
        )

    return redirect(url_for('output.results'))


@output_bp.route('/output/reset')
@login_required
def reset():
    for key in ['intake', 'recommendations', 'learning_style',
                'deliverable_path', 'deliverable_content', 'primary_format',
                'output_ready', 'concern_responses', 'tech_stack']:
        session.pop(key, None)
    return redirect(url_for('intake.index'))