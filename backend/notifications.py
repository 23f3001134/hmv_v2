import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape

import requests
from flask import current_app


def send_gchat_message(message, webhook_url=None, timeout=10):
    url = webhook_url or current_app.config.get("DEFAULT_GCHAT_WEBHOOK_URL", "")
    if not url:
        return False

    try:
        resp = requests.post(url, json={"text": message}, timeout=timeout)
        ok = 200 <= resp.status_code < 300
        if not ok:
            current_app.logger.warning("Google Chat webhook returned %s", resp.status_code)
        return ok
    except Exception:
        current_app.logger.exception("Google Chat webhook failed")
        return False


def send_email(to_email, subject, html_body, text_body=None, attachments=None):
    host = current_app.config.get("SMTP_HOST")
    username = current_app.config.get("SMTP_USERNAME")
    password = current_app.config.get("SMTP_PASSWORD")
    port = current_app.config.get("SMTP_PORT", 587)
    use_tls = current_app.config.get("SMTP_USE_TLS", True)
    from_email = current_app.config.get("SMTP_FROM_EMAIL")

    if not host or not to_email:
        current_app.logger.info("Email skipped (SMTP_HOST not configured or no recipient)")
        return False

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject

    if text_body:
        message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    for attachment in attachments or []:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment["content"])
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={attachment['filename']}"
        )
        message.attach(part)

    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            if use_tls:
                server.starttls()
            if username and password:
                server.login(username, password)
            server.send_message(message)
        return True
    except Exception:
        current_app.logger.exception("Failed to send email to %s", to_email)
        return False


def notify_user(email, subject, message, html_body=None, attachments=None):
    html = html_body or f"<p>{escape(message)}</p>"
    sent = send_email(email, subject, html, text_body=message, attachments=attachments)
    if sent:
        return True
    return send_gchat_message(f"{subject}\n{message}")
