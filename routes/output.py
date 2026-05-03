import json
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

        session['deliverable_content'] = deliverable_content
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
    deliverable_content = session.get('deliverable_content', '')

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
        role=session.get('role', 'isv')
    )


@output_bp.route('/output/download/<format_type>')
@login_required
def download(format_type):
    intake = session.get('intake', {})
    company = intake.get('company_name', 'ISV').replace(' ', '-').lower()
    content = session.get('deliverable_content', '')

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
                'deliverable_content', 'primary_format', 'output_ready']:
        session.pop(key, None)
    return redirect(url_for('intake.index'))