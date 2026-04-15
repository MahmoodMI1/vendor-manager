import requests

GRAPH_SEND_URL = "https://graph.microsoft.com/v1.0/me/sendMail"


def format_email(vendor_name: str, visit_date: str, sender_name: str, recipient_email: str) -> dict:
    subject = f"Reminder: Vendor Visit Tomorrow — {vendor_name}"
    body = (
        f"Hi {vendor_name},\n\n"
        f"This is a reminder that your visit is scheduled for tomorrow, {visit_date}.\n\n"
        f"Please don't hesitate to reach out if you have any questions.\n\n"
        f"Best regards,\n"
        f"{sender_name}"
    )

    graph_payload = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body,
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient_email,
                    }
                }
            ],
        }
    }

    return {
        "subject": subject,
        "body": body,
        "recipient": recipient_email,
        "graph_payload": graph_payload,
    }


def send_email(graph_payload: dict, headers: dict) -> dict:
    try:
        response = requests.post(GRAPH_SEND_URL, json=graph_payload, headers=headers)
        if response.status_code == 202:
            return {"success": True, "status_code": 202}
        else:
            return {"success": False, "status_code": response.status_code, "error": response.text}
    except Exception as e:
        return {"success": False, "status_code": None, "error": str(e)}