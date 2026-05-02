import json
import os
from datetime import datetime, timezone
from collections import Counter
from config import Config

ANALYTICS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'analytics.json')


def _load():
    """Load analytics data from file."""
    try:
        with open(ANALYTICS_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return _empty_store()


def _save(data):
    """Save analytics data to file."""
    os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def _empty_store():
    return {
        "sessions": [],
        "intake_events": [],
        "chat_events": [],
        "output_events": [],
        "format_selections": [],
        "learning_styles": [],
        "ip_locations": []
    }


def _now():
    return datetime.now(timezone.utc).isoformat()


# ── Event Logging ──

def log_session_start(session_id, ip_address=None, role='isv'):
    """Log a new session start."""
    data = _load()
    data["sessions"].append({
        "session_id": session_id,
        "role": role,
        "ip": ip_address,
        "started_at": _now(),
        "last_active": _now()
    })
    _save(data)

    # Log IP location
    if ip_address and ip_address not in ['127.0.0.1', '::1']:
        log_ip_location(ip_address)


def log_intake_step(session_id, step, completed=True):
    """Log intake step progression or drop-off."""
    data = _load()
    data["intake_events"].append({
        "session_id": session_id,
        "step": step,
        "completed": completed,
        "timestamp": _now()
    })
    _save(data)


def log_chat_message(session_id, message, company_name=None):
    """Log a chat message for trending topic analysis."""
    data = _load()
    data["chat_events"].append({
        "session_id": session_id,
        "message": message[:200],  # truncate for storage
        "company": company_name,
        "timestamp": _now()
    })
    _save(data)


def log_output_generated(session_id, company_name, format_ranking, learning_style):
    """Log completed output generation."""
    data = _load()

    primary_format = format_ranking[0] if format_ranking else 'workshop'

    data["output_events"].append({
        "session_id": session_id,
        "company": company_name,
        "primary_format": primary_format,
        "format_ranking": format_ranking,
        "timestamp": _now()
    })

    data["format_selections"].append({
        "session_id": session_id,
        "format": primary_format,
        "timestamp": _now()
    })

    if learning_style:
        data["learning_styles"].append({
            "session_id": session_id,
            "style_label": learning_style.get("style_label", "Unknown"),
            "primary_format": primary_format,
            "timestamp": _now()
        })

    _save(data)


def log_ip_location(ip_address):
    """Log IP for world map."""
    try:
        import ipinfo
        handler = ipinfo.getHandler(Config.IPINFO_TOKEN)
        details = handler.getDetails(ip_address)
        data = _load()

        # Check if IP already logged
        existing_ips = [e["ip"] for e in data["ip_locations"]]
        if ip_address not in existing_ips:
            data["ip_locations"].append({
                "ip": ip_address,
                "lat": float(details.latitude) if hasattr(details, 'latitude') and details.latitude else None,
                "lng": float(details.longitude) if hasattr(details, 'longitude') and details.longitude else None,
                "city": getattr(details, 'city', ''),
                "country": getattr(details, 'country_name', ''),
                "timestamp": _now()
            })
            _save(data)
    except Exception:
        pass


# ── Analytics Aggregation ──

def get_dashboard_stats():
    """Aggregate all stats for the admin dashboard."""
    data = _load()

    # Active sessions (last 24 hours)
    now = datetime.now(timezone.utc)
    sessions = data.get("sessions", [])
    total_sessions = len(sessions)
    isv_sessions = len([s for s in sessions if s.get("role") == "isv"])

    # Drop-off analysis
    intake_events = data.get("intake_events", [])
    step_completions = Counter()
    for event in intake_events:
        if event.get("completed"):
            step_completions[event["step"]] += 1

    drop_off = []
    for step in range(1, 7):
        completed = step_completions.get(step, 0)
        drop_off.append({
            "step": step,
            "label": _step_label(step),
            "completed": completed
        })

    # Format preference distribution
    format_selections = data.get("format_selections", [])
    format_counts = Counter([s["format"] for s in format_selections])
    total_formats = len(format_selections)

    format_distribution = []
    for fmt in ["notebook", "workshop", "hackathon"]:
        count = format_counts.get(fmt, 0)
        pct = round((count / total_formats * 100) if total_formats > 0 else 0)
        format_distribution.append({
            "format": fmt.title(),
            "count": count,
            "percentage": pct
        })

    # Learning style breakdown
    learning_styles = data.get("learning_styles", [])
    style_counts = Counter([s["style_label"] for s in learning_styles])
    style_breakdown = [{"style": k, "count": v} for k, v in style_counts.most_common(5)]

    # Trending topics from chat
    chat_events = data.get("chat_events", [])
    trending = _get_trending_topics(chat_events)

    # IP locations for world map
    ip_locations = [
        loc for loc in data.get("ip_locations", [])
        if loc.get("lat") and loc.get("lng")
    ]

    # Recent companies
    output_events = data.get("output_events", [])
    recent_companies = []
    seen = set()
    for event in reversed(output_events):
        company = event.get("company", "Unknown")
        if company not in seen:
            seen.add(company)
            recent_companies.append({
                "company": company,
                "format": event.get("primary_format", ""),
                "timestamp": event.get("timestamp", "")
            })
        if len(recent_companies) >= 5:
            break

    return {
        "total_sessions": total_sessions,
        "isv_sessions": isv_sessions,
        "completions": len(output_events),
        "completion_rate": round((len(output_events) / isv_sessions * 100) if isv_sessions > 0 else 0),
        "drop_off": drop_off,
        "format_distribution": format_distribution,
        "style_breakdown": style_breakdown,
        "trending_topics": trending,
        "ip_locations": ip_locations,
        "recent_companies": recent_companies
    }


def _step_label(step):
    labels = {
        1: "Company",
        2: "Problem",
        3: "Why NVIDIA",
        4: "Tools",
        5: "Team",
        6: "Learning Style"
    }
    return labels.get(step, f"Step {step}")


def _get_trending_topics(chat_events):
    """Extract trending topics from chat messages."""
    keywords = [
        "huggingface", "langchain", "unsloth", "nim", "dgx", "fine-tuning",
        "workshop", "notebook", "hackathon", "inference", "training", "gcp",
        "deployment", "kubernetes", "cuda", "tensorrt", "nemo", "riva",
        "embeddings", "rag", "agents", "multimodal"
    ]

    counts = Counter()
    for event in chat_events:
        msg = event.get("message", "").lower()
        for kw in keywords:
            if kw in msg:
                counts[kw] += 1

    trending = []
    for kw, count in counts.most_common(6):
        trending.append({
            "topic": kw.title(),
            "count": count,
            "suggestion": _topic_suggestion(kw)
        })

    return trending if trending else [
        {"topic": "No data yet", "count": 0, "suggestion": "Chat interactions will appear here"}
    ]


def _topic_suggestion(topic):
    suggestions = {
        "huggingface": "Consider creating a HuggingFace × DGX Cloud workshop",
        "langchain": "Consider publishing a LangChain NIM integration notebook",
        "unsloth": "Schedule a fine-tuning webinar with Unsloth team",
        "nim": "Create a NIM microservices overview lab",
        "dgx": "Build a DGX Cloud onboarding guide",
        "fine-tuning": "Publish a fine-tuning Jupyter notebook series",
        "workshop": "High workshop interest -- schedule a live session",
        "inference": "Create an inference optimization notebook",
        "gcp": "Develop a GCP + NVIDIA integration guide",
        "deployment": "Create a deployment checklist for ISVs",
        "rag": "Build a RAG with NIM embeddings notebook",
        "agents": "Develop an agentic AI workshop curriculum"
    }
    return suggestions.get(topic, f"Create content around {topic.title()}")


def generate_monthly_report():
    """Generate end-of-month markdown report."""
    stats = get_dashboard_stats()
    now = datetime.now(timezone.utc)

    lines = [
        f"# Orbit Monthly Report — {now.strftime('%B %Y')}",
        f"*Generated {now.strftime('%Y-%m-%d')} by Orbit ISV Intelligence Platform*",
        "",
        "## Summary",
        f"- Total sessions: {stats['total_sessions']}",
        f"- ISV sessions: {stats['isv_sessions']}",
        f"- Completed onboardings: {stats['completions']}",
        f"- Completion rate: {stats['completion_rate']}%",
        "",
        "## Format Preference",
    ]

    for fmt in stats["format_distribution"]:
        lines.append(f"- {fmt['format']}: {fmt['count']} selections ({fmt['percentage']}%)")

    lines += [
        "",
        "## Learning Style Breakdown",
    ]
    for style in stats["style_breakdown"]:
        lines.append(f"- {style['style']}: {style['count']} users")

    lines += [
        "",
        "## Intake Drop-off Analysis",
    ]
    for step in stats["drop_off"]:
        lines.append(f"- Step {step['step']} ({step['label']}): {step['completed']} completions")

    lines += [
        "",
        "## Trending Topics",
    ]
    for topic in stats["trending_topics"]:
        lines.append(f"- **{topic['topic']}** ({topic['count']} mentions): {topic['suggestion']}")

    lines += [
        "",
        "## Recent ISV Companies",
    ]
    for company in stats["recent_companies"]:
        lines.append(f"- {company['company']} — chose {company['format'].title()} format")

    lines += [
        "",
        "---",
        "*This report was auto-generated by Orbit. Share with your DevRel leadership team.*"
    ]

    return "\n".join(lines)