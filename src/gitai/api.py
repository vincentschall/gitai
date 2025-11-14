import json
from huggingface_hub import InferenceClient
from .config import load_token, load_config


def generate_commit_message(diff_text: str) -> str:
    """
    Generate a commit message from git diff using FREE Hugging Face Inference API.

    Args:
        diff_text: The git diff text to generate a commit message for

    Returns:
        The generated commit message string

    Raises:
        ValueError: If no token is configured
        Exception: If API call fails
    """
    token = load_token()
    if not token:
        raise ValueError(
            "Missing Hugging Face token. Set it via 'gitai config set' or HF_API_TOKEN env var."
        )

    config = load_config()

    client = InferenceClient(
        api_key=token,
        provider=config.get("PROVIDER"),
    )

    # Prepare messages with a focused prompt
    messages = [
        {
            "role": "system",
            "content": config.get("PROMPT")
        },
        {
            "role": "user",
            "content": f"Git diff:\n\n{diff_text}\n\nCommit message:"
        }
    ]

    try:

        response = client.chat.completions.create(
            model=config.get("MODEL"),
            messages=messages,
            max_tokens=config.get("MAX_TOKENS"),  # Commit messages are short
            temperature=config.get("TEMPERATURE"),  # Lower temperature for more focused output
        )

        # Extract and clean the message
        message = response.choices[0].message.content.strip()

        # Remove quotes if the model added them
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1]
        if message.startswith("'") and message.endswith("'"):
            message = message[1:-1]

        # Ensure it's not too long (72 chars is conventional limit)
        if len(message) > config.get("MAX_CHAR_LENGTH"):
            # Try to cut at a word boundary
            message = message[:69].rsplit(' ', 1)[0] + '...'

        return message

    except Exception as e:
        raise Exception(f"Failed to generate commit message: {e}")