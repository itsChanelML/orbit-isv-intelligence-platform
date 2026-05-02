from flask import Blueprint, render_template, session, redirect, url_for, Response
from routes.auth import admin_required
from services.analytics_service import get_dashboard_stats, generate_monthly_report

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@admin_required
def dashboard():
    stats = get_dashboard_stats()
    return render_template('admin.html', stats=stats)


@admin_bp.route('/admin/report/download/md')
@admin_required
def download_report_md():
    report = generate_monthly_report()
    return Response(
        report,
        mimetype='text/markdown',
        headers={'Content-Disposition': 'attachment; filename=orbit-monthly-report.md'}
    )


@admin_bp.route('/admin/report/download/pdf')
@admin_required
def download_report_pdf():
    """Generate PDF from markdown report."""
    try:
        import markdown as md
        import io

        report_md = generate_monthly_report()
        report_html = md.markdown(report_md, extensions=['tables', 'fenced_code'])

        # Wrap in styled HTML for PDF
        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #111; }}
  h1 {{ font-size: 1.8rem; border-bottom: 2px solid #76B900; padding-bottom: 0.5rem; }}
  h2 {{ font-size: 1.2rem; color: #333; margin-top: 1.5rem; }}
  li {{ margin: 0.3rem 0; }}
  strong {{ color: #000; }}
  hr {{ border: 1px solid #eee; margin: 2rem 0; }}
  p {{ color: #555; font-size: 0.85rem; }}
</style>
</head>
<body>{report_html}</body>
</html>"""

        # Try weasyprint if available, otherwise return HTML
        try:
            from weasyprint import HTML
            pdf_bytes = HTML(string=html).write_pdf()
            return Response(
                pdf_bytes,
                mimetype='application/pdf',
                headers={'Content-Disposition': 'attachment; filename=orbit-monthly-report.pdf'}
            )
        except ImportError:
            # Fallback: return as HTML download
            return Response(
                html,
                mimetype='text/html',
                headers={'Content-Disposition': 'attachment; filename=orbit-monthly-report.html'}
            )

    except Exception as e:
        return Response(
            f"Error generating report: {str(e)}",
            mimetype='text/plain'
        )