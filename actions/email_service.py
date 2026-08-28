import os
import smtplib
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME)


def build_confirmation_email(contributor_name: str, event_name: str, amount, contribution_date: str) -> str:
    return f"""
    Dear {contributor_name},<br/><br/>
    Thank you for registering for <b>{event_name}</b>.<br/><br/>
    <b>Contribution Details</b><br/>
    Amount: {amount}<br/>
    Date: {contribution_date}<br/><br/>
    We appreciate your support!<br/><br/>
    Regards,<br/>
    Contribution Tracker Team
    """


def send_confirmation_email(to_email: str, contributor_name: str, event_name: str, amount, contribution_date: str):
    subject = f"Registration / Contribution Confirmation - {event_name}"
    html_body = build_confirmation_email(contributor_name, event_name, amount, contribution_date)

    message = MIMEText(html_body, "html")
    message["Subject"] = subject
    message["From"] = SMTP_FROM_EMAIL
    message["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_FROM_EMAIL, [to_email], message.as_string())