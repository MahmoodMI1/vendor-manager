import logging
import os
from datetime import date, timedelta

from src.config_manager import load_config
from src.auth import get_credentials
from src.excel_reader import read_schedule, read_directory, get_visits_for_date, lookup_vendor_email
from src.email_sender import format_email, send_email

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "log.txt")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)


def run():
    logging.info("Running vendor reminder check...")

    try:
        config = load_config()
    except FileNotFoundError:
        logging.error("config.json not found. Run setup_wizard first.")
        return

    try:
        credentials = get_credentials()
    except Exception as e:
        logging.error(f"Failed to load credentials: {e}")
        return

    tomorrow = date.today() + timedelta(days=1)
    logging.info(f"Tomorrow is {tomorrow}")

    try:
        schedule = read_schedule(config["visit_schedule_path"])
    except FileNotFoundError:
        logging.error(f"Visit schedule not found: {config['visit_schedule_path']}")
        return

    try:
        directory = read_directory(config["vendor_directory_path"])
    except FileNotFoundError:
        logging.error(f"Vendor directory not found: {config['vendor_directory_path']}")
        return

    visits = get_visits_for_date(schedule, tomorrow)

    if not visits:
        logging.info("No visits found for tomorrow.")
        return

    logging.info(f"Found {len(visits)} visit(s) tomorrow")

    for visit in visits:
        vendor_name = visit["vendor_name"]
        email_address = lookup_vendor_email(vendor_name, directory)

        if not email_address:
            logging.warning(f'Vendor "{vendor_name}" not found in directory')
            continue

        email = format_email(
            vendor_name=vendor_name,
            visit_date=str(tomorrow),
            sender_name=config["sender_name"],
            sender_email=credentials["email"],
            recipient_email=email_address,
        )

        result = send_email(
            mime_message=email["mime_message"],
            sender_email=credentials["email"],
            app_password=credentials["app_password"],
        )

        if result["success"]:
            logging.info(f"EMAIL SENT — {vendor_name} ({email_address})")
        else:
            logging.error(f"FAILED — {vendor_name} ({email_address}): {result['error']}")

    logging.info("Done.")


if __name__ == "__main__":
    run()