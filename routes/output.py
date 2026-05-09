import os
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
        team_context = intake.get('team_context', '')

        # Check if exec-facing output was selected
        if team_context == 'exec_facing':
            from services.exec_brief_service import generate_exec_brief, brief_to_markdown
            exec_brief = generate_exec_brief(intake, recommendations)
            deliverable_content = brief_to_markdown(exec_brief)
            primary_format = 'exec_brief'
            session['exec_brief'] = exec_brief
        elif primary_format == 'workshop':
            deliverable_content = generate_workshop(intake, recommendations)
        elif primary_format == 'hackathon':
            deliverable_content = generate_hackathon_brief(intake, recommendations)
        elif primary_format == 'notebook':
            deliverable_content = generate_notebook(intake, recommendations)

        session['deliverable_content'] = deliverable_content
        session['primary_format'] = primary_format
        session['output_ready'] = True

        # Save to document store
        try:
            from services.document_store import save_document
            session_id = session.get('session_id', 'default')
            company = intake.get('company_name', 'ISV')
            strategies = session.get('adoption_strategies', [])
            strategy_id = len(strategies) + 1
            save_document(
                session_id=session_id,
                doc_type=primary_format,
                content=deliverable_content,
                company_name=company,
                strategy_id=strategy_id
            )
        except Exception:
            pass

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

        # Concern responses skipped during generation to reduce latency
        # They load async on the results page
        session['concern_responses'] = []

        # Save adoption strategy to history
        try:
            from datetime import datetime, timezone
            strategies = session.get('adoption_strategies', [])
            problem = intake.get('problem_statement', '')
            tools = intake.get('selected_tools', [])
            fmt = primary_format.title()
            tool_str = tools[0].title() if tools else 'DGX'
            words = problem.split()[:4]
            short_title = ' '.join(words) + f' {fmt}' if words else f'{tool_str} {fmt}'
            short_title = short_title[:35]

            strategies.append({
                'id': len(strategies) + 1,
                'company': intake.get('company_name', 'Unknown'),
                'date': datetime.now(timezone.utc).strftime('%m.%d.%y'),
                'primary_format': primary_format,
                'tools': intake.get('selected_tools', []),
                'short_title': short_title,
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
    deliverable_content = session.get('deliverable_content', '')

    # Convert markdown to HTML for preview
    deliverable_html = ''
    if primary_format in ['workshop', 'hackathon', 'exec_brief']:
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
        adoption_strategies=session.get('adoption_strategies', []),
        stack_items=session.get('tech_stack', []),
        role=session.get('role', 'isv')
    )


@output_bp.route('/output/concerns')
@login_required
def load_concerns():
    """
    Async endpoint called by JS on results page to generate concern responses.
    Runs after results page loads so it doesn't block the main generation.
    """
    intake = session.get('intake', {})
    concerns = intake.get('adoption_concerns', [])

    if not concerns:
        return jsonify({'concern_responses': []})

    try:
        from services.nim_service import generate_concern_responses
        concern_responses = generate_concern_responses(intake, concerns)
        session['concern_responses'] = concern_responses
        return jsonify({'concern_responses': concern_responses})
    except Exception as e:
        return jsonify({'concern_responses': [], 'error': str(e)})


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
                'deliverable_content', 'primary_format', 'output_ready',
                'concern_responses', 'adoption_strategies', 'tech_stack']:
        session.pop(key, None)
    return redirect(url_for('intake.index'))