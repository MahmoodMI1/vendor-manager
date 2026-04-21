import os
import json
import msal
from src.config_manager import load_config

SCOPES = ["Mail.Send"]
TOKEN_CACHE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tokens", "token_cache.json")


def _get_cache() -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    if os.path.exists(TOKEN_CACHE_PATH):
        with open(TOKEN_CACHE_PATH, "r") as f:
            cache.deserialize(f.read())
    return cache


def _save_cache(cache: msal.SerializableTokenCache) -> None:
    os.makedirs(os.path.dirname(TOKEN_CACHE_PATH), exist_ok=True)
    with open(TOKEN_CACHE_PATH, "w") as f:
        f.write(cache.serialize())


def get_headers(config_path: str = None) -> dict:
    config = load_config(config_path) if config_path else load_config()
    client_id = config["client_id"]
    tenant_id = config["tenant_id"]
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    cache = _get_cache()
    app = msal.PublicClientApplication(client_id, authority=authority, token_cache=cache)

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            _save_cache(cache)
            return {"Authorization": f"Bearer {result['access_token']}"}

    result = app.acquire_token_interactive(scopes=SCOPES)
    if "access_token" in result:
        _save_cache(cache)
        return {"Authorization": f"Bearer {result['access_token']}"}

    raise Exception(f"Authentication failed: {result.get('error_description', 'Unknown error')}")


def get_credentials(config_path: str = None) -> dict:
    """Gmail fallback."""
    config = load_config(config_path) if config_path else load_config()
    return {
        "email": config["sender_email"],
        "app_password": config["app_password"],
    }