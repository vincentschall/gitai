import json
from huggingface_hub import InferenceClient
from .config import load_token


def generate_commit_message(diff_text: str) -> str:
    """
    Generate a commit message from git diff using FREE Hugging Face Inference API.

    This uses the hf-inference provider which is completely free (no credits deducted)
    with smaller, efficient models perfect for commit message generation.

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

    # Use hf-inference provider - completely FREE with no credit usage
    # Perfect for smaller, efficient models
    client = InferenceClient(api_key=token)

    # Prepare messages with a focused prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are a git commit message generator. Generate a single, clear commit message "
                "in imperative mood (e.g., 'Add feature' not 'Added feature'). "
                "Keep it under 72 characters. Focus on WHAT changed, not HOW. "
                "Return ONLY the commit message, no explanations or quotes."
            )
        },
        {
            "role": "user",
            "content": f"Git diff:\n\n{diff_text}\n\nCommit message:"
        }
    ]

    try:
        # Using a small, efficient model that's FREE on hf-inference
        # Options (in order of preference for free usage):
        # 1. microsoft/Phi-4 - Small, efficient, good at following instructions
        # 2. HuggingFaceH4/zephyr-7b-beta - Good balance of size and quality
        # 3. google/flan-t5-base - Very small and fast

        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",  # Will auto-route to cerebras
            messages=messages,
            max_tokens=100,  # Commit messages are short
            temperature=0.3,  # Lower temperature for more focused output
        )

        # Extract and clean the message
        message = response.choices[0].message.content.strip()

        # Remove quotes if the model added them
        if message.startswith('"') and message.endswith('"'):
            message = message[1:-1]
        if message.startswith("'") and message.endswith("'"):
            message = message[1:-1]

        # Ensure it's not too long (72 chars is conventional limit)
        if len(message) > 72:
            # Try to cut at a word boundary
            message = message[:69].rsplit(' ', 1)[0] + '...'

        return message

    except Exception as e:
        raise Exception(f"Failed to generate commit message: {e}")