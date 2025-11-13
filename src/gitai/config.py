from __future__ import annotations

import json
import os
from pathlib import Path

def get_config_path() -> Path:
    """Return the platform-appropriate path for storing GitAI config."""
    base_dir = (
        Path(os.getenv("APPDATA"))
        if os.name == "nt"
        else Path.home() / ".config"
    )
    config_dir = base_dir / "gitai"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.json"


def save_token(token: str):
    """Save the Hugging Face token securely to disk."""
    config_path = get_config_path()
    data = {"HF_API_TOKEN": token.strip()}

    # Write atomically and with restrictive permissions
    config_path.write_text(json.dumps(data))
    try:
        os.chmod(config_path, 0o600)  # user read/write only
    except Exception:
        pass  # ignore on Windows

    print(f"Token saved to {config_path}")


def load_token() -> str | None:
    """Load token from config file or environment variable."""
    env_token = os.getenv("HF_API_TOKEN")
    if env_token:
        return env_token

    config_path = get_config_path()
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text())
            return data.get("HF_API_TOKEN")
        except json.JSONDecodeError:
            return None
    return None


def delete_token():
    """Remove the stored token."""
    config_path = get_config_path()
    if config_path.exists():
        config_path.unlink()
        print(f"Token deleted ({config_path})")
