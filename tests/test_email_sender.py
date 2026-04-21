import pytest
from unittest.mock import patch, MagicMock
from src.email_sender import format_email, send_email, load_template
from email.mime.text import MIMEText


@pytest.fixture
def template_path(tmp_path):
    template = tmp_path / "test_template.txt"
    template.write_text(
        "Subject: Reminder: Vendor Visit Tomorrow — {vendor_name}\n\n"
        "Hi {vendor_name},\n\n"
        "This is a reminder that your visit is scheduled for tomorrow, {visit_date}.\n\n"
        "Best regards,\n"
        "{sender_name}"
    )
    return str(template)


def test_load_template(template_path):
    template = load_template(template_path)
    assert "subject" in template
    assert "body" in template
    assert "{vendor_name}" in template["subject"]


def test_load_template_missing():
    with pytest.raises(FileNotFoundError):
        load_template("nonexistent/template.txt")


def test_format_email_subject(template_path):
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
        template_path=template_path,
    )
    assert email["subject"] == "Reminder: Vendor Visit Tomorrow — Acme Corp"


def test_format_email_body_contains_vendor_name(template_path):
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
        template_path=template_path,
    )
    assert "Acme Corp" in email["body"]


def test_format_email_body_contains_date(template_path):
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
        template_path=template_path,
    )
    assert "2026-04-16" in email["body"]


def test_format_email_body_contains_sender_name(template_path):
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
        template_path=template_path,
    )
    assert "John Doe" in email["body"]


def test_format_email_recipient(template_path):
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
        template_path=template_path,
    )
    assert email["recipient"] == "contact@acme.com"


def test_format_email_mime_headers(template_path):
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
        template_path=template_path,
    )
    msg = email["mime_message"]
    assert msg["Subject"] == "Reminder: Vendor Visit Tomorrow — Acme Corp"
    assert msg["From"] == "test@gmail.com"
    assert msg["To"] == "contact@acme.com"


@patch("src.email_sender.smtplib.SMTP")
def test_send_email_success(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server

    msg = MIMEText("test")
    msg["Subject"] = "test"
    msg["From"] = "test@gmail.com"
    msg["To"] = "contact@acme.com"

    result = send_email(msg, "test@gmail.com", "fakepassword")
    assert result["success"] is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("test@gmail.com", "fakepassword")
    mock_server.send_message.assert_called_once()
    mock_server.quit.assert_called_once()


@patch("src.email_sender.smtplib.SMTP")
def test_send_email_failure(mock_smtp):
    mock_smtp.side_effect = Exception("Connection failed")

    msg = MIMEText("test")
    msg["Subject"] = "test"
    msg["From"] = "test@gmail.com"
    msg["To"] = "contact@acme.com"

    result = send_email(msg, "test@gmail.com", "fakepassword")
    assert result["success"] is False
    assert "Connection failed" in result["error"]