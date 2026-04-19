import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def format_email(vendor_name: str, visit_date: str, sender_name: str, sender_email: str, recipient_email: str) -> dict:
    subject = f"Reminder: Vendor Visit Tomorrow — {vendor_name}"
    body = (
        f"Hi {vendor_name},\n\n"
        f"This is a reminder that your visit is scheduled for tomorrow, {visit_date}.\n\n"
        f"Please don't hesitate to reach out if you have any questions.\n\n"
        f"Best regards,\n"
        f"{sender_name}"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    return {
        "subject": subject,
        "body": body,
        "recipient": recipient_email,
        "mime_message": msg,
    }


def send_email(mime_message: MIMEText, sender_email: str, app_password: str) -> dict:
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(mime_message)
        server.quit()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}