from src.config_manager import load_config


def get_credentials(config_path: str = None) -> dict:
    config = load_config(config_path) if config_path else load_config()
    return {
        "email": config["sender_email"],
        "app_password": config["app_password"],
    }