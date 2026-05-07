"""
community_service.py

Shared persistent community board for the NVIDIA ISV ecosystem.
All posts, comments, and reactions are stored in data/community.json
and visible to every verified ISV partner regardless of session.

Post lifecycle:
  create_post() → add_comment() / add_reaction() / generate_orbit_reply()
  get_posts() → get_post() → delete_post()

Admin signals:
  get_trending_topics() → get_community_stats() → get_unanswered_questions()
"""

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Optional
from collections import Counter

COMMUNITY_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'community.json')

# ── Categories ───────────────────────────────────────────────────────────────

CATEGORIES = [
    {'id': 'wins', 'label': 'Wins & Milestones', 'icon': '🏆', 'description': 'Share something you shipped on DGX Cloud'},
    {'id': 'best_practices', 'label': 'Best Practices', 'icon': '💡', 'description': 'Patterns and approaches that worked'},
    {'id': 'questions', 'label': 'Questions', 'icon': '❓', 'description': 'Stuck on something? Ask the community'},
    {'id': 'integration', 'label': 'Integration Patterns', 'icon': '🔧', 'description': 'How I connected X to NIM'},
    {'id': 'announcements', 'label': 'Announcements', 'icon': '📢', 'description': 'From the NVIDIA DevRel team'},
]

CATEGORY_IDS = [c['id'] for c in CATEGORIES]

REACTION_TYPES = ['helpful', 'fire', 'insight']
REACTION_LABELS = {'helpful': '👍 Helpful', 'fire': '🔥 Fire', 'insight': '💡 Insight'}

# ── NVIDIA Resource Links ────────────────────────────────────────────────────

NVIDIA_RESOURCES = {
    'nim': {
        'docs': 'https://docs.nvidia.com/nim/',
        'video': 'https://www.youtube.com/watch?v=nim-getting-started',
        'label': 'NIM Documentation'
    },
    'dgx': {
        'docs': 'https://docs.nvidia.com/dgx-cloud/',
        'video': 'https://www.nvidia.com/en-us/training/',
        'label': 'DGX Cloud Docs'
    },
    'nemotron': {
        'docs': 'https://developer.nvidia.com/nemotron',
        'video': 'https://www.nvidia.com/en-us/training/',
        'label': 'Nemotron Resources'
    },
    'monai': {
        'docs': 'https://docs.monai.io/',
        'video': 'https://www.youtube.com/c/NVIDIA',
        'label': 'MONAI Documentation'
    },
    'tensorrt': {
        'docs': 'https://developer.nvidia.com/tensorrt',
        'video': 'https://www.nvidia.com/en-us/training/',
        'label': 'TensorRT Documentation'
    },
    'nemo': {
        'docs': 'https://docs.nvidia.com/nemo-framework/',
        'video': 'https://www.nvidia.com/en-us/training/',
        'label': 'NeMo Framework Docs'
    }
}

UPCOMING_EVENTS = [
    {'name': 'NVIDIA GTC 2027', 'date': 'March 2027', 'url': 'https://www.nvidia.com/gtc/'},
    {'name': 'NVIDIA DLI Workshop: NIM Deployment', 'date': 'Monthly', 'url': 'https://www.nvidia.com/en-us/training/'},
    {'name': 'ISV DevRel Office Hours', 'date': 'Weekly — Thursdays', 'url': 'https://developer.nvidia.com/'},
    {'name': 'NYC Tech Week AI Summit', 'date': 'June 2026', 'url': 'https://nyctechweek.xyz'},
]


# ── Storage ──────────────────────────────────────────────────────────────────

def _load_community() -> dict:
    """Load the full community data store."""
    try:
        with open(COMMUNITY_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'posts': [], 'meta': {'total_posts': 0, 'total_comments': 0}}


def _save_community(data: dict) -> None:
    """Save the community data store."""
    os.makedirs(os.path.dirname(COMMUNITY_FILE), exist_ok=True)
    with open(COMMUNITY_FILE, 'w') as f:
        json.dump(data, f, indent=2)


# ── Post Operations ──────────────────────────────────────────────────────────

def create_post(
    title: str,
    body: str,
    category: str,
    author_name: str,
    author_company: str,
    author_domain: str,
    tags: Optional[list] = None
) -> dict:
    """
    Create a new community post.
    Returns the created post dict.
    """
    if category not in CATEGORY_IDS:
        category = 'questions'

    now = datetime.now(timezone.utc)
    post = {
        'id': str(uuid.uuid4())[:10],
        'title': title.strip(),
        'body': body.strip(),
        'category': category,
        'author_name': author_name,
        'author_company': author_company,
        'author_domain': author_domain,
        'tags': tags or [],
        'reactions': {'helpful': 0, 'fire': 0, 'insight': 0},
        'reaction_users': {'helpful': [], 'fire': [], 'insight': []},
        'comments': [],
        'orbit_responded': False,
        'created_at': now.isoformat(),
        'date': now.strftime('%m.%d.%y'),
        'time': now.strftime('%I:%M %p UTC'),
        'view_count': 0
    }

    data = _load_community()
    data['posts'].insert(0, post)
    data['meta']['total_posts'] = len(data['posts'])
    _save_community(data)
    return post


def get_posts(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> list:
    """
    Get posts with optional category filter and search.
    Returns list of posts sorted newest first.
    """
    data = _load_community()
    posts = data.get('posts', [])

    if category and category != 'all':
        posts = [p for p in posts if p.get('category') == category]

    if search:
        search_lower = search.lower()
        posts = [
            p for p in posts
            if search_lower in p.get('title', '').lower()
            or search_lower in p.get('body', '').lower()
            or any(search_lower in tag.lower() for tag in p.get('tags', []))
        ]

    return posts[offset:offset + limit]


def get_post(post_id: str) -> Optional[dict]:
    """Get a single post by ID. Increments view count."""
    data = _load_community()
    for i, post in enumerate(data['posts']):
        if post['id'] == post_id:
            data['posts'][i]['view_count'] = post.get('view_count', 0) + 1
            _save_community(data)
            return data['posts'][i]
    return None


def delete_post(post_id: str) -> bool:
    """Delete a post by ID."""
    data = _load_community()
    original_len = len(data['posts'])
    data['posts'] = [p for p in data['posts'] if p['id'] != post_id]
    if len(data['posts']) < original_len:
        data['meta']['total_posts'] = len(data['posts'])
        _save_community(data)
        return True
    return False


# ── Reactions ────────────────────────────────────────────────────────────────

def add_reaction(post_id: str, reaction_type: str, user_domain: str) -> Optional[dict]:
    """
    Add or toggle a reaction on a post.
    Each user (by domain) can only react once per type.
    Returns updated reaction counts.
    """
    if reaction_type not in REACTION_TYPES:
        return None

    data = _load_community()
    for post in data['posts']:
        if post['id'] == post_id:
            users = post['reaction_users'].get(reaction_type, [])
            if user_domain in users:
                # Toggle off
                users.remove(user_domain)
                post['reactions'][reaction_type] = max(0, post['reactions'].get(reaction_type, 0) - 1)
            else:
                # Add reaction
                users.append(user_domain)
                post['reactions'][reaction_type] = post['reactions'].get(reaction_type, 0) + 1
            post['reaction_users'][reaction_type] = users
            _save_community(data)
            return post['reactions']
    return None


# ── Comments ─────────────────────────────────────────────────────────────────

def add_comment(
    post_id: str,
    body: str,
    author_name: str,
    author_company: str,
    is_orbit: bool = False
) -> Optional[dict]:
    """
    Add a comment to a post.
    is_orbit=True marks it as an Orbit AI response.
    Returns the created comment.
    """
    now = datetime.now(timezone.utc)
    comment = {
        'id': str(uuid.uuid4())[:8],
        'body': body.strip(),
        'author_name': 'Orbit' if is_orbit else author_name,
        'author_company': 'NVIDIA ISV Intelligence Platform' if is_orbit else author_company,
        'is_orbit': is_orbit,
        'created_at': now.isoformat(),
        'date': now.strftime('%m.%d.%y'),
        'time': now.strftime('%I:%M %p UTC'),
    }

    data = _load_community()
    for post in data['posts']:
        if post['id'] == post_id:
            post['comments'].append(comment)
            if is_orbit:
                post['orbit_responded'] = True
            data['meta']['total_comments'] = sum(
                len(p.get('comments', [])) for p in data['posts']
            )
            _save_community(data)
            return comment
    return None


# ── Orbit AI Reply ───────────────────────────────────────────────────────────

def generate_orbit_reply(post: dict, intake: Optional[dict] = None) -> str:
    """
    Generate an Orbit AI reply to a community post using Nemotron.
    Surfaces NVIDIA docs, video tutorials, and upcoming events.
    Returns the reply text.
    """
    title = post.get('title', '')
    body = post.get('body', '')
    category = post.get('category', 'questions')
    tags = post.get('tags', [])
    company = post.get('author_company', 'your company')

    # Find relevant resources
    relevant_resources = []
    body_lower = (title + ' ' + body).lower()
    for key, resource in NVIDIA_RESOURCES.items():
        if key in body_lower or any(key in tag.lower() for tag in tags):
            relevant_resources.append(resource)

    if not relevant_resources:
        relevant_resources = [NVIDIA_RESOURCES['nim'], NVIDIA_RESOURCES['dgx']]

    resource_context = '\n'.join([
        f"- {r['label']}: {r['docs']}" for r in relevant_resources[:3]
    ])

    events_context = '\n'.join([
        f"- {e['name']} ({e['date']}): {e['url']}"
        for e in UPCOMING_EVENTS[:3]
    ])

    prompt = f"""You are Orbit, NVIDIA's ISV community intelligence layer powered by Nemotron.

A verified ISV partner has posted the following in the community:

CATEGORY: {category}
COMPANY: {company}
TITLE: {title}
POST: {body}
TAGS: {', '.join(tags) if tags else 'none'}

RELEVANT NVIDIA RESOURCES:
{resource_context}

UPCOMING EVENTS:
{events_context}

Write a helpful, specific community reply as Orbit. Requirements:
- Be direct and technical where appropriate
- Reference specific NVIDIA products, NIM microservices, or docs that are relevant
- Include 1-2 resource links from the provided list using markdown format
- If this is a question, answer it specifically
- If this is a win, celebrate it and add a relevant tip or next step
- If this is a best practice, validate it and add complementary context
- Mention 1 upcoming event if relevant
- Keep it to 3-5 sentences plus links
- End with an invitation for others to share their experience
- Do NOT use generic filler phrases like "Great question!" or "Thanks for sharing!"
- Tone: knowledgeable peer, not corporate bot

Return only the reply text, no preamble."""

    try:
        from services.nim_service import _call_nim
        from config import Config

        reply = _call_nim(
            Config.MODEL_PRIMARY,
            [{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.6
        )
        return reply.strip()

    except Exception:
        # Fallback reply
        return (
            f"Thanks for posting this, {company}. "
            f"For resources on this topic, check out the [NVIDIA NIM Documentation]({NVIDIA_RESOURCES['nim']['docs']}) "
            f"and [DGX Cloud Docs]({NVIDIA_RESOURCES['dgx']['docs']}). "
            f"Would love to hear from other ISVs who've tackled similar challenges — drop your experience below."
        )


# ── Admin Signals ─────────────────────────────────────────────────────────────

def get_community_stats() -> dict:
    """Get community statistics for the admin dashboard."""
    data = _load_community()
    posts = data.get('posts', [])

    if not posts:
        return {
            'total_posts': 0,
            'total_comments': 0,
            'total_reactions': 0,
            'by_category': {},
            'unanswered_count': 0,
            'orbit_response_rate': 0,
            'most_active_companies': [],
            'trending_topics': []
        }

    # Category breakdown
    by_category = Counter(p.get('category', 'questions') for p in posts)

    # Total reactions
    total_reactions = sum(
        sum(p.get('reactions', {}).values()) for p in posts
    )

    # Total comments
    total_comments = sum(len(p.get('comments', [])) for p in posts)

    # Unanswered questions
    unanswered = [
        p for p in posts
        if p.get('category') == 'questions' and len(p.get('comments', [])) == 0
    ]

    # Orbit response rate
    questions = [p for p in posts if p.get('category') == 'questions']
    orbit_responses = [p for p in questions if p.get('orbit_responded')]
    orbit_rate = round(len(orbit_responses) / len(questions) * 100) if questions else 0

    # Most active companies
    company_counts = Counter(p.get('author_company', '') for p in posts)
    most_active = [
        {'company': company, 'post_count': count}
        for company, count in company_counts.most_common(5)
        if company
    ]

    # Trending topics -- extract from tags and titles
    all_tags = []
    for post in posts:
        all_tags.extend(post.get('tags', []))
        # Extract capitalized words from titles as topics
        words = post.get('title', '').split()
        all_tags.extend([w for w in words if len(w) > 4 and w[0].isupper()])

    tag_counts = Counter(all_tags)
    trending = [
        {'topic': topic, 'count': count}
        for topic, count in tag_counts.most_common(8)
        if topic and len(topic) > 2
    ]

    return {
        'total_posts': len(posts),
        'total_comments': total_comments,
        'total_reactions': total_reactions,
        'by_category': dict(by_category),
        'unanswered_count': len(unanswered),
        'unanswered_posts': unanswered[:5],
        'orbit_response_rate': orbit_rate,
        'most_active_companies': most_active,
        'trending_topics': trending
    }


def get_trending_topics(limit: int = 5) -> list:
    """Get trending community topics for the admin dashboard."""
    stats = get_community_stats()
    return stats.get('trending_topics', [])[:limit]


def get_unanswered_questions() -> list:
    """Get unanswered community questions -- DevRel action items."""
    data = _load_community()
    posts = data.get('posts', [])
    return [
        p for p in posts
        if p.get('category') == 'questions' and len(p.get('comments', [])) == 0
    ]


def get_category_info(category_id: str) -> Optional[dict]:
    """Get display info for a category."""
    for cat in CATEGORIES:
        if cat['id'] == category_id:
            return cat
    return None


def seed_sample_posts() -> None:
    """
    Seed the community with sample posts for demo purposes.
    Only runs if community is empty.
    """
    data = _load_community()
    if data.get('posts'):
        return  # Already has posts

    sample_posts = [
        {
            'title': 'Achieved sub-100ms inference with NIM on DGX Cloud H100',
            'body': 'After two weeks of optimization, we finally got our medical imaging inference pipeline under 100ms using TensorRT-LLM on DGX Cloud. Key insight: batching requests in groups of 8 and using FP8 precision cut our latency by 40%. Happy to share our config if anyone is working on similar healthcare workloads.',
            'category': 'wins',
            'author_name': 'Sarah Chen',
            'author_company': 'Lumina Health AI',
            'author_domain': 'luminahealth.ai',
            'tags': ['NIM', 'TensorRT-LLM', 'Healthcare', 'Inference']
        },
        {
            'title': 'Best approach for integrating LangChain with NVIDIA NIM embeddings?',
            'body': 'We are building a RAG pipeline for clinical document retrieval and want to use nvidia/nv-embedqa-e5-v5 for embeddings. Has anyone integrated this with LangChain\'s vector store pipeline? Specifically wondering about the best way to handle the NIM auth headers inside LangChain\'s embedding class.',
            'category': 'questions',
            'author_name': 'Marcus Torres',
            'author_company': 'HealthBridge AI',
            'author_domain': 'healthbridge.ai',
            'tags': ['LangChain', 'NIM', 'RAG', 'Embeddings']
        },
        {
            'title': 'Pattern: Using GCP Service Usage API to auto-detect NIM-ready services',
            'body': 'Sharing a pattern we discovered -- when you enable Vertex AI in your GCP project, you can use the Service Usage API to detect this and automatically surface relevant NIM microservices to your team. We built a weekly cron job that checks for newly enabled GCP APIs and maps them to NVIDIA products. Saved us from manually tracking what our infra team was enabling.',
            'category': 'integration',
            'author_name': 'Priya Nair',
            'author_company': 'DataStream Analytics',
            'author_domain': 'datastreamanalytics.com',
            'tags': ['GCP', 'NIM', 'Automation', 'DGX Cloud']
        },
        {
            'title': 'NeMo fine-tuning on DGX Cloud — our workflow after 3 months',
            'body': 'We have been running fine-tuning workloads on DGX Cloud H100 clusters for three months. Here is what we learned: (1) Always use gradient checkpointing for models over 13B params. (2) NeMo\'s built-in checkpointing saved us twice when spot instances were reclaimed. (3) Start with LoRA rank 8 before going higher -- we saw diminishing returns past rank 16 for our dataset size. DM if you want our full config.',
            'category': 'best_practices',
            'author_name': 'James Wu',
            'author_company': 'Synthos AI',
            'author_domain': 'synthos.ai',
            'tags': ['NeMo', 'Fine-Tuning', 'DGX Cloud', 'H100']
        }
    ]

    for post_data in sample_posts:
        create_post(**post_data)