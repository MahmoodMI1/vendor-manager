import pytest
from unittest.mock import patch, MagicMock
from src.email_sender import format_email, send_email


def test_format_email_subject():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        recipient_email="contact@acme.com",
    )
    assert email["subject"] == "Reminder: Vendor Visit Tomorrow — Acme Corp"


def test_format_email_body_contains_vendor_name():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        recipient_email="contact@acme.com",
    )
    assert "Acme Corp" in email["body"]


def test_format_email_body_contains_date():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        recipient_email="contact@acme.com",
    )
    assert "2026-04-16" in email["body"]


def test_format_email_body_contains_sender_name():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        recipient_email="contact@acme.com",
    )
    assert "John Doe" in email["body"]


def test_format_email_recipient():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        recipient_email="contact@acme.com",
    )
    assert email["recipient"] == "contact@acme.com"


def test_format_email_graph_payload_structure():
    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        recipient_email="contact@acme.com",
    )
    payload = email["graph_payload"]
    assert "message" in payload
    assert "subject" in payload["message"]
    assert "body" in payload["message"]
    assert "toRecipients" in payload["message"]
    assert payload["message"]["body"]["contentType"] == "Text"
    assert len(payload["message"]["toRecipients"]) == 1
    assert payload["message"]["toRecipients"][0]["emailAddress"]["address"] == "contact@acme.com"


@patch("src.email_sender.requests.post")
def test_send_email_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 202
    mock_post.return_value = mock_response

    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        recipient_email="contact@acme.com",
    )
    result = send_email(email["graph_payload"], headers={"Authorization": "Bearer fake"})
    assert result["success"] is True


@patch("src.email_sender.requests.post")
def test_send_email_failure(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_post.return_value = mock_response

    email = format_email(
        vendor_name="Acme Corp",
        visit_date="2026-04-16",
        sender_name="John Doe",
        recipient_email="contact@acme.com",
    )
    result = send_email(email["graph_payload"], headers={"Authorization": "Bearer fake"})
    assert result["success"] is False
    assert result["status_code"] == 401