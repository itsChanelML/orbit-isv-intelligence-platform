"""
exec_brief_service.py

Generates executive-facing DGX Cloud adoption briefs using Nemotron.
Designed for ISVs who selected "Exec-Facing Output" in their team context step.

The exec brief is structured as a business document, not a technical guide.
It covers:
- Executive summary
- Business problem and opportunity
- Why NVIDIA DGX Cloud (strategic rationale)
- Business use cases with ROI framing
- Competitive positioning
- Deployment acceleration narrative
- Risk mitigation
- Recommended next steps
"""

import json
from typing import Optional
from config import Config


def generate_exec_brief(intake: dict, recommendations: list) -> dict:
    """
    Generate a full executive adoption brief from intake data and NIM recommendations.

    Returns a structured dict with all sections of the brief.
    Also returns a markdown string for download.
    """
    company = intake.get('company_name', 'Your Company')
    tagline = intake.get('tagline', '')
    description = intake.get('company_description', '')
    problem = intake.get('problem_statement', '')
    why_nvidia = intake.get('why_nvidia', '')
    tools = intake.get('selected_tools', [])
    concerns = intake.get('adoption_concerns', [])
    stack = intake.get('current_stack', [])

    # Build recommendation context
    rec_context = ''
    if recommendations:
        rec_lines = []
        for i, rec in enumerate(recommendations[:3], 1):
            rec_lines.append(f"{i}. {rec.get('title', '')} — {rec.get('description', '')}")
        rec_context = '\n'.join(rec_lines)

    prompt = f"""You are a senior NVIDIA Solutions Architect writing an executive adoption brief for a C-suite audience.

COMPANY PROFILE:
- Company: {company}
- Tagline: {tagline}
- Description: {description}
- Core Problem: {problem}
- Why NVIDIA: {why_nvidia}
- Current Stack: {', '.join(stack) if stack else 'Not specified'}
- Tools: {', '.join(tools) if tools else 'Not specified'}
- Adoption Concerns: {', '.join(concerns) if concerns else 'None stated'}

TECHNICAL RECOMMENDATIONS GENERATED:
{rec_context}

Generate a complete executive adoption brief. Respond ONLY with a valid JSON object with these exact keys:

- "executive_summary": string (3-4 sentences, business-focused, no jargon, lead with the business outcome)
- "business_problem": string (2-3 sentences framing the problem as a business risk or missed opportunity)
- "strategic_rationale": string (3-4 sentences explaining why NVIDIA DGX Cloud is the strategic choice, not just technical)
- "business_use_cases": array of exactly 3 objects, each with:
    - "title": string (business outcome, not technical feature)
    - "description": string (2-3 sentences, business impact focused)
    - "roi_signal": string (1 sentence quantifying or qualifying the business value)
    - "nvidia_product": string (which NVIDIA product enables this)
- "competitive_advantage": string (2-3 sentences on how NVIDIA DGX Cloud accelerates their competitive position)
- "deployment_acceleration": string (2-3 sentences on how DGX Cloud reduces time-to-production vs alternatives)
- "risk_mitigation": array of 3 strings, each addressing one concern with a business-level response
- "next_steps": array of exactly 4 objects, each with:
    - "step": string (action item)
    - "owner": string (who owns this -- CTO, Engineering Lead, etc.)
    - "timeline": string (e.g. Week 1-2, Month 1, etc.)
- "closing_statement": string (2-3 sentences, visionary close about what this partnership enables)

Return only the JSON object, no preamble, no markdown fences."""

    try:
        from services.nim_service import _call_nim

        raw = _call_nim(
            Config.MODEL_PRIMARY,
            [{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.5
        )

        # Clean and parse
        clean = raw.strip()
        if clean.startswith("```"):
            clean = clean.split("```")[1]
            if clean.startswith("json"):
                clean = clean[4:]
        clean = clean.strip()
        if not clean.startswith("{"):
            start = clean.find("{")
            if start != -1:
                clean = clean[start:]
        end = clean.rfind("}")
        if end != -1:
            clean = clean[:end+1]

        brief_data = json.loads(clean)
        brief_data['company'] = company
        brief_data['generated'] = True
        return brief_data

    except Exception as e:
        # Structured fallback
        return _fallback_brief(company, description, problem, recommendations)


def _fallback_brief(company: str, description: str, problem: str, recommendations: list) -> dict:
    """Return a structured fallback brief if NIM call fails."""
    return {
        'company': company,
        'generated': False,
        'executive_summary': f"{company} is positioned to accelerate its AI infrastructure through NVIDIA DGX Cloud, enabling faster model deployment, reduced operational overhead, and competitive differentiation through GPU-accelerated computing. The recommended integration path leverages NVIDIA NIM microservices to minimize re-engineering while maximizing throughput.",
        'business_problem': f"The current infrastructure cannot support the scale and latency requirements of {company}'s AI workloads, creating operational risk and slowing time-to-market for new AI capabilities.",
        'strategic_rationale': "NVIDIA DGX Cloud provides the H100 compute, optimized software stack, and managed infrastructure required to run enterprise AI workloads without the capital expenditure of on-premise GPU clusters. The NVIDIA + Google Cloud partnership means {company} can deploy on the same hyperscaler infrastructure already in use.",
        'business_use_cases': [
            {
                'title': 'Accelerated Model Inference',
                'description': 'Deploy production AI models with sub-100ms latency using NVIDIA NIM microservices. Eliminate the engineering overhead of inference optimization.',
                'roi_signal': 'Reduce inference infrastructure costs by up to 40% while improving response times by 3x.',
                'nvidia_product': 'NVIDIA NIM'
            },
            {
                'title': 'Faster Model Development Cycles',
                'description': 'Run training and fine-tuning workloads on H100 clusters without provisioning delays. Compress model development timelines from weeks to days.',
                'roi_signal': 'Cut model development cycle time by 60% with on-demand DGX Cloud access.',
                'nvidia_product': 'DGX Cloud'
            },
            {
                'title': 'Scalable AI Platform',
                'description': 'Scale from prototype to production without re-architecting. DGX Cloud grows with your workload.',
                'roi_signal': 'Eliminate infrastructure migration costs when scaling from pilot to enterprise deployment.',
                'nvidia_product': 'DGX Cloud + NeMo'
            }
        ],
        'competitive_advantage': f"Companies that deploy on NVIDIA DGX Cloud gain access to the same infrastructure powering the world's most advanced AI systems. {company} can move faster than competitors still managing on-premise GPU infrastructure.",
        'deployment_acceleration': "NVIDIA NIM microservices reduce inference deployment from months to days by providing pre-optimized, containerized models ready for production. DGX Cloud eliminates the infrastructure provisioning bottleneck entirely.",
        'risk_mitigation': [
            "NVIDIA DGX Cloud provides enterprise SLAs, dedicated support, and a managed environment that eliminates infrastructure risk.",
            "NIM microservices are cloud-portable and avoid vendor lock-in -- deploy on GCP, AWS, or Azure without re-engineering.",
            "NVIDIA's DLI training programs and dedicated DevRel support ensure your team is fully enabled before go-live."
        ],
        'next_steps': [
            {'step': 'Schedule DGX Cloud technical discovery call', 'owner': 'CTO / Engineering Lead', 'timeline': 'Week 1'},
            {'step': 'Deploy NIM proof-of-concept on DGX Cloud trial', 'owner': 'Engineering Lead', 'timeline': 'Week 2-3'},
            {'step': 'Benchmark NIM inference against current stack', 'owner': 'ML Engineering', 'timeline': 'Month 1'},
            {'step': 'Present production deployment proposal to leadership', 'owner': 'CTO', 'timeline': 'Month 2'}
        ],
        'closing_statement': f"NVIDIA DGX Cloud gives {company} the infrastructure foundation to build, scale, and lead with AI -- not just adopt it. This is the platform that turns AI investment into competitive advantage."
    }


def brief_to_markdown(brief: dict) -> str:
    """
    Convert a structured exec brief dict to a clean markdown document
    suitable for download or sharing.
    """
    company = brief.get('company', 'Your Company')
    lines = []

    lines.append(f"# Executive Adoption Brief: NVIDIA DGX Cloud")
    lines.append(f"## {company}")
    lines.append(f"*Generated by Orbit — NVIDIA ISV Intelligence Platform*")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append(brief.get('executive_summary', ''))
    lines.append("")

    # Business Problem
    lines.append("## The Business Problem")
    lines.append(brief.get('business_problem', ''))
    lines.append("")

    # Strategic Rationale
    lines.append("## Why NVIDIA DGX Cloud")
    lines.append(brief.get('strategic_rationale', ''))
    lines.append("")

    # Business Use Cases
    lines.append("## Business Use Cases")
    lines.append("")
    for uc in brief.get('business_use_cases', []):
        lines.append(f"### {uc.get('title', '')}")
        lines.append(uc.get('description', ''))
        lines.append(f"**ROI Signal:** {uc.get('roi_signal', '')}")
        lines.append(f"**Powered by:** {uc.get('nvidia_product', '')}")
        lines.append("")

    # Competitive Advantage
    lines.append("## Competitive Advantage")
    lines.append(brief.get('competitive_advantage', ''))
    lines.append("")

    # Deployment Acceleration
    lines.append("## Deployment Acceleration")
    lines.append(brief.get('deployment_acceleration', ''))
    lines.append("")

    # Risk Mitigation
    lines.append("## Risk Mitigation")
    for risk in brief.get('risk_mitigation', []):
        lines.append(f"- {risk}")
    lines.append("")

    # Next Steps
    lines.append("## Recommended Next Steps")
    lines.append("")
    lines.append("| Step | Owner | Timeline |")
    lines.append("|---|---|---|")
    for step in brief.get('next_steps', []):
        lines.append(f"| {step.get('step', '')} | {step.get('owner', '')} | {step.get('timeline', '')} |")
    lines.append("")

    # Closing
    lines.append("---")
    lines.append("")
    lines.append("## Closing")
    lines.append(brief.get('closing_statement', ''))
    lines.append("")
    lines.append("---")
    lines.append("*Generated by Orbit — NVIDIA ISV Intelligence Platform*")
    lines.append("*Powered by Nemotron-Super-49B via NVIDIA NIM*")

    return '\n'.join(lines)


def get_brief_stats(brief: dict) -> dict:
    """Extract key stats from a brief for display in the UI."""
    use_cases = brief.get('business_use_cases', [])
    next_steps = brief.get('next_steps', [])
    return {
        'use_case_count': len(use_cases),
        'next_step_count': len(next_steps),
        'risk_count': len(brief.get('risk_mitigation', [])),
        'nvidia_products': list(set([uc.get('nvidia_product', '') for uc in use_cases if uc.get('nvidia_product')])),
    }