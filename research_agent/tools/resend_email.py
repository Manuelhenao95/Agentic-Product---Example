"""ResendEmailTool — Renders and sends the intelligence report via Resend API."""

import os
from datetime import datetime, timezone

import resend
from jinja2 import Environment, FileSystemLoader


# Resolve template directory relative to this file
_TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "templates",
)


def send_report_email(report_json: str) -> dict:
    """Sends the curated intelligence report as an HTML email via Resend.

    Receives the structured report data as a JSON string, renders it into
    a professional HTML template, and delivers it to the configured
    recipient using the Resend email API.

    The report_json must be a valid JSON string with these keys:
    - tldr_bullets: list of 3 strings (The Big Picture)
    - top_signal: string (headline for the email subject)
    - tech_news: list of 3 objects with {title, url, score, tldr, deep_dive, analogy}
    - product_eng: list of 3 objects with {title, url, score, tldr, deep_dive, analogy}
    - agentic_ai: list of 3 objects with {title, url, score, tldr, deep_dive, analogy}

    Args:
        report_json: A JSON string containing the structured report data.

    Returns:
        dict: A dictionary with 'status', 'message_id', and delivery details.
    """
    import json

    try:
        report = json.loads(report_json)
    except json.JSONDecodeError as e:
        return {"status": "error", "error_message": f"Invalid JSON: {e}"}

    try:
        # Configure Resend
        api_key = os.getenv("RESEND_API_KEY")
        if not api_key:
            return {"status": "error", "error_message": "RESEND_API_KEY not set"}

        resend.api_key = api_key

        recipient = os.getenv("RECIPIENT_EMAIL", "henaoperez.manuel@gmail.com")
        today = datetime.now(timezone.utc).strftime("%B %d, %Y")
        top_signal = report.get("top_signal", "Daily Intelligence")

        # Render HTML template
        env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR))
        template = env.get_template("report.html")

        html_content = template.render(
            subject=f"☕ Intelligence Report | {today} | {top_signal}",
            date=today,
            top_signal=top_signal,
            tldr_bullets=report.get("tldr_bullets", []),
            tech_news=report.get("tech_news", []),
            product_eng=report.get("product_eng", []),
            agentic_ai=report.get("agentic_ai", []),
        )

        # Send via Resend
        params: resend.Emails.SendParams = {
            "from": "Research & Delivery Agent <onboarding@resend.dev>",
            "to": [recipient],
            "subject": f"☕ Intelligence Report | {today} | {top_signal}",
            "html": html_content,
        }

        email = resend.Emails.send(params)

        return {
            "status": "success",
            "message_id": email.get("id", "unknown"),
            "recipient": recipient,
            "subject": params["subject"],
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}
