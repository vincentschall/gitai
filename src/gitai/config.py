from __future__ import annotations

import json
import os
import textwrap
from pathlib import Path
from typing import Any


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


def get_default_config(preserve_token: bool = True) -> dict[str, Any]:
    """
    Get default configuration values.

    Args:
        preserve_token: If True, loads existing token. If False, excludes token.

    Returns:
        Dictionary with default config values
    """
    config = {
        "PROMPT": (
            "The following changes sent to you are the current changes to a codebase." # Context
            "You are a git commit message generator." # Role
            "Generate a single, clear commit message in imperative mood (e.g., 'Add feature' not 'Added feature')." # Action
            "Focus on WHAT changed, not HOW. "
            "Be as specific about the changes as possible within these limits."
            "Return ONLY the commit message, no explanations or quotes." # Format
            "Expect people reading the commits to know the codebase, as they are most likely developers" # Target
        ),
        "MODEL": "meta-llama/Llama-3.1-8B-Instruct",
        "PROVIDER": "auto",  # Can be "auto", "cerebras", etc.
        "MAX_TOKENS": 200,
        "TEMPERATURE": 0.6,
        "MAX_CHAR_LENGTH": 100
    }

    if preserve_token:
        token = load_token()
        if token:
            config["HF_API_TOKEN"] = token

    return config


def reset_config():
    """
    Reset the configuration to default values.
    The token will be preserved if it exists.
    """
    config_path = get_config_path()

    # Get defaults with preserved token
    data = get_default_config(preserve_token=True)

    # Write with pretty formatting for readability
    config_path.write_text(json.dumps(data, indent=2))

    try:
        os.chmod(config_path, 0o600)  # user read/write only
    except Exception:
        pass  # ignore on Windows

    print(f"Configuration reset to defaults at {config_path}")


def load_config() -> dict[str, Any]:
    """
    Load config, creating with defaults if it doesn't exist.
    This ensures config file always exists after first use.
    """
    config_path = get_config_path()

    if not config_path.exists():
        # First run - create with defaults (no token yet)
        default_config = get_default_config(preserve_token=False)
        config_path.write_text(json.dumps(default_config, indent=2))
        try:
            os.chmod(config_path, 0o600)
        except Exception:
            pass
        return default_config

    try:
        data = json.loads(config_path.read_text())
        return data
    except json.JSONDecodeError:
        # Corrupted config - recreate with defaults, preserve token if possible
        print("Config file corrupted, resetting to defaults...")
        default_config = get_default_config(preserve_token=True)
        config_path.write_text(json.dumps(default_config, indent=2))
        return default_config


def save_config(config: dict[str, Any]):
    """Save the entire config dictionary to disk."""
    config_path = get_config_path()
    config_path.write_text(json.dumps(config, indent=2))
    try:
        os.chmod(config_path, 0o600)  # user read/write only
    except Exception:
        pass  # ignore on Windows


def update_config(**kwargs):
    """
    Update specific config values without overwriting the whole file.

    Example:
        update_config(TEMPERATURE=0.7, MAX_TOKENS=150)
    """
    config = load_config()
    config.update(kwargs)
    save_config(config)


def get_config_value(key: str, default: Any = None) -> Any:
    """Get a specific config value with optional default."""
    config = load_config()
    return config.get(key, default)


def save_token(token: str):
    """Save the Hugging Face token securely to disk."""
    config = load_config()
    config["HF_API_TOKEN"] = token.strip()
    save_config(config)
    print(f"Token saved to {get_config_path()}")


def load_token() -> str | None:
    """Load token from config file or environment variable."""
    # Environment variable takes precedence
    env_token = os.getenv("HF_API_TOKEN")
    if env_token:
        return env_token

    # Try to load from config file
    config = load_config()
    return config.get("HF_API_TOKEN")


def delete_token():
    """Remove the stored token from config."""
    config = load_config()
    if "HF_API_TOKEN" in config:
        del config["HF_API_TOKEN"]
        save_config(config)
        print(f"Token deleted from {get_config_path()}")
    else:
        print("No token found in config")


def show_config():
    """Display current configuration (with token truncated)."""
    config = load_config()

    print(f"\nConfig location: {get_config_path()}")
    print("\nCurrent configuration:")
    print("─" * 50)

    for key, value in config.items():
        if key == "HF_API_TOKEN" and value:
            # Truncate token for security
            displayed_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
            print(f"  {key}: {displayed_value}")
        elif key == "PROMPT":
            wrapped = "\n      ".join(textwrap.wrap(value, width=60))
            print(f"  {key}: {wrapped}")
        else:
            print(f"  {key}: {value}")

    print("─" * 50 + "\n")