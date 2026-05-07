"""
community.py

Blueprint for the Orbit ISV Community board.
Handles post creation, viewing, reactions, comments, and Orbit AI replies.
"""

from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from routes.auth import login_required
from services.community_service import (
    create_post, get_posts, get_post, delete_post,
    add_reaction, add_comment, generate_orbit_reply,
    get_community_stats, get_unanswered_questions,
    CATEGORIES, REACTION_LABELS, seed_sample_posts
)

community_bp = Blueprint('community', __name__)


def _get_author_info() -> dict:
    """Extract author info from session."""
    intake = session.get('intake', {})
    return {
        'name': intake.get('contact_name', 'ISV Member'),
        'company': intake.get('company_name', 'ISV Partner'),
        'domain': intake.get('company_website', 'unknown')
    }


@community_bp.route('/portal/community')
@login_required
def index():
    """Main community board."""
    # Seed sample posts if empty
    seed_sample_posts()

    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    posts = get_posts(
        category=category if category != 'all' else None,
        search=search or None
    )

    # Add category info to each post
    for post in posts:
        from services.community_service import get_category_info
        cat_info = get_category_info(post.get('category', ''))
        post['category_label'] = cat_info['label'] if cat_info else post.get('category', '')
        post['category_icon'] = cat_info['icon'] if cat_info else '📌'
        post['comment_count'] = len(post.get('comments', []))
        post['total_reactions'] = sum(post.get('reactions', {}).values())

    return render_template('community.html',
        posts=posts,
        categories=CATEGORIES,
        active_category=category,
        search=search,
        role=session.get('role', 'isv'),
        stack_items=session.get('tech_stack', []),
        adoption_strategies=session.get('adoption_strategies', [])
    )


@community_bp.route('/portal/community/post/<post_id>')
@login_required
def view_post(post_id):
    """View a single post with comments."""
    post = get_post(post_id)
    if not post:
        return redirect(url_for('community.index'))

    from services.community_service import get_category_info
    cat_info = get_category_info(post.get('category', ''))
    post['category_label'] = cat_info['label'] if cat_info else post.get('category', '')
    post['category_icon'] = cat_info['icon'] if cat_info else '📌'

    author = _get_author_info()

    return render_template('community_post.html',
        post=post,
        categories=CATEGORIES,
        reaction_labels=REACTION_LABELS,
        author=author,
        role=session.get('role', 'isv'),
        stack_items=session.get('tech_stack', []),
        adoption_strategies=session.get('adoption_strategies', [])
    )


@community_bp.route('/portal/community/new', methods=['GET'])
@login_required
def new_post():
    """New post form."""
    return render_template('community_post.html',
        post=None,
        categories=CATEGORIES,
        reaction_labels=REACTION_LABELS,
        author=_get_author_info(),
        role=session.get('role', 'isv'),
        stack_items=session.get('tech_stack', []),
        adoption_strategies=session.get('adoption_strategies', [])
    )


@community_bp.route('/portal/community/new', methods=['POST'])
@login_required
def create_post_route():
    """Handle new post creation."""
    author = _get_author_info()
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()
    category = request.form.get('category', 'questions')
    tags_raw = request.form.get('tags', '')
    tags = [t.strip() for t in tags_raw.split(',') if t.strip()]

    if not title or not body:
        return redirect(url_for('community.new_post'))

    post = create_post(
        title=title,
        body=body,
        category=category,
        author_name=author['name'],
        author_company=author['company'],
        author_domain=author['domain'],
        tags=tags
    )

    return redirect(url_for('community.view_post', post_id=post['id']))


@community_bp.route('/portal/community/post/<post_id>/comment', methods=['POST'])
@login_required
def comment_route(post_id):
    """Add a comment to a post."""
    author = _get_author_info()
    body = request.form.get('body', '').strip()

    if not body:
        return redirect(url_for('community.view_post', post_id=post_id))

    add_comment(
        post_id=post_id,
        body=body,
        author_name=author['name'],
        author_company=author['company'],
        is_orbit=False
    )

    return redirect(url_for('community.view_post', post_id=post_id))


@community_bp.route('/portal/community/post/<post_id>/react', methods=['POST'])
@login_required
def react_route(post_id):
    """Add or toggle a reaction on a post."""
    author = _get_author_info()
    reaction_type = request.json.get('type', 'helpful')
    updated = add_reaction(post_id, reaction_type, author['domain'])
    return jsonify({'status': 'ok', 'reactions': updated})


@community_bp.route('/portal/community/post/<post_id>/orbit-reply', methods=['POST'])
@login_required
def orbit_reply_route(post_id):
    """Generate and save an Orbit AI reply to a post."""
    post = get_post(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    if post.get('orbit_responded'):
        return jsonify({'error': 'Orbit has already responded to this post'}), 400

    intake = session.get('intake', {})
    reply_text = generate_orbit_reply(post, intake)

    comment = add_comment(
        post_id=post_id,
        body=reply_text,
        author_name='Orbit',
        author_company='NVIDIA ISV Intelligence Platform',
        is_orbit=True
    )

    return jsonify({'status': 'ok', 'comment': comment})


@community_bp.route('/portal/community/post/<post_id>/delete', methods=['POST'])
@login_required
def delete_post_route(post_id):
    """Delete a post (author or admin only)."""
    author = _get_author_info()
    post = get_post(post_id)

    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # Only allow deletion by post author or admin
    role = session.get('role', 'isv')
    if post.get('author_domain') != author['domain'] and role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    delete_post(post_id)
    return jsonify({'status': 'ok'})


@community_bp.route('/portal/community/api/stats')
@login_required
def api_stats():
    """API endpoint for community stats (used by admin dashboard)."""
    stats = get_community_stats()
    return jsonify(stats)