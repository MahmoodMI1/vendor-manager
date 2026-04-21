import smtplib
import requests
import os
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GRAPH_SEND_URL = "https://graph.microsoft.com/v1.0/me/sendMail"
DEFAULT_TEMPLATE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates", "default.txt")


def load_template(path: str = DEFAULT_TEMPLATE) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Email template not found: {path}")
    with open(path, "r") as f:
        content = f.read()
    subject_line, body = content.split("\n\n", 1)
    subject = subject_line.replace("Subject: ", "").strip()
    return {"subject": subject, "body": body.strip()}


def format_email(vendor_name: str, visit_date: str, sender_name: str, sender_email: str, recipient_email: str, template_path: str = DEFAULT_TEMPLATE) -> dict:
    template = load_template(template_path)

    replacements = {
        "{vendor_name}": vendor_name,
        "{visit_date}": visit_date,
        "{sender_name}": sender_name,
        "{sender_email}": sender_email,
    }

    subject = template["subject"]
    body = template["body"]
    for key, value in replacements.items():
        subject = subject.replace(key, value)
        body = body.replace(key, value)

    # MIME message for Gmail
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # Graph API payload for Outlook
    graph_payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body,
            },
            "toRecipients": [
                {"emailAddress": {"address": recipient_email}}
            ],
        }
    }

    return {
        "subject": subject,
        "body": body,
        "recipient": recipient_email,
        "mime_message": msg,
        "graph_payload": graph_payload,
    }


def send_email_gmail(mime_message: MIMEText, sender_email: str, app_password: str) -> dict:
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(mime_message)
        server.quit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_email_outlook(graph_payload: dict, headers: dict) -> dict:
    try:
        response = requests.post(GRAPH_SEND_URL, json=graph_payload, headers=headers)
        if response.status_code == 202:
            return {"success": True}
        else:
            return {"success": False, "status_code": response.status_code, "error": response.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_email(mime_message: MIMEText, sender_email: str, app_password: str) -> dict:
    """Gmail send - kept as default for backward compatibility."""
    return send_email_gmail(mime_message, sender_email, app_password)