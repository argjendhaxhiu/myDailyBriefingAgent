"""
CONCEPT: Sending email via Resend.
Resend is an API-based email service -- you make an HTTP request
and they handle delivery. Much simpler than configuring SMTP.
"""

import os
import re
from datetime import date
import resend


def markdown_to_html(text: str) -> str:
    lines = text.split("\n")
    html_lines = []

    for line in lines:
        if line.startswith("### "):
            line = f"<h3>{line[4:]}</h3>"
        elif line.startswith("## "):
            line = f"<h2>{line[3:]}</h2>"
        elif line.startswith("# "):
            line = f"<h1>{line[2:]}</h1>"
        elif line.startswith("- "):
            line = f"<li>{line[2:]}</li>"
        elif line.strip() == "---":
            line = "<hr>"
        elif line.strip() == "":
            line = "<br>"
        else:
            line = f"<p>{line}</p>"

        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"\[(.+?)\]\((https?://[^\)]+)\)", r'<a href="\2">\1</a>', line)
        html_lines.append(line)

    body = "\n".join(html_lines)
    return f"""
    <html><body style="font-family: Arial, sans-serif; max-width: 700px; margin: auto; padding: 20px; color: #222;">
    {body}
    </body></html>
    """


def send_briefing(briefing: str):
    resend.api_key = os.environ["RESEND_API_KEY"]

    today = date.today().strftime("%B %d, %Y")

    resend.Emails.send({
        "from": "Daily Briefing <onboarding@resend.dev>",
        "to": os.environ["EMAIL_RECIPIENT"],
        "subject": f"Your Daily Briefing - {today}",
        "html": markdown_to_html(briefing),
        "text": briefing,
    })

    print(f"Email sent to {os.environ['EMAIL_RECIPIENT']}")
