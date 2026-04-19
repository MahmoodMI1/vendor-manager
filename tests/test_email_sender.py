import pytest
from unittest.mock import patch, MagicMock
from src.email_sender import format_email, send_email


def test_format_email_subject():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
    )
    assert email["subject"] == "Reminder: Vendor Visit Tomorrow — Acme Corp"


def test_format_email_body_contains_vendor_name():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
    )
    assert "Acme Corp" in email["body"]


def test_format_email_body_contains_date():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
    )
    assert "2026-04-16" in email["body"]


def test_format_email_body_contains_sender_name():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
    )
    assert "John Doe" in email["body"]


def test_format_email_recipient():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
    )
    assert email["recipient"] == "contact@acme.com"


def test_format_email_mime_headers():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
    )
    msg = email["mime_message"]
    assert msg["Subject"] == "Reminder: Vendor Visit Tomorrow — Acme Corp"
    assert msg["From"] == "test@gmail.com"
    assert msg["To"] == "contact@acme.com"


@patch("src.email_sender.smtplib.SMTP")
def test_send_email_success(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value = mock_server

    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
    )
    result = send_email(email["mime_message"], "test@gmail.com", "fakepassword")
    assert result["success"] is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with("test@gmail.com", "fakepassword")
    mock_server.send_message.assert_called_once()
    mock_server.quit.assert_called_once()


@patch("src.email_sender.smtplib.SMTP")
def test_send_email_failure(mock_smtp):
    mock_smtp.side_effect = Exception("Connection failed")

    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        sender_email="test@gmail.com",
        recipient_email="contact@acme.com",
    )
    result = send_email(email["mime_message"], "test@gmail.com", "fakepassword")
    assert result["success"] is False
    assert "Connection failed" in result["error"]