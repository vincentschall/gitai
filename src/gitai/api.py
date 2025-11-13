import requests
import json
from .config import load_token

def generate_commit_message(diff_text: str) -> str:
    token = load_token()
    if not token:
        raise ValueError(
            "Missing Hugging Face token. Set it via 'gitai config set' or HF_API_TOKEN env var."
        )

    api_url = "https://router.huggingface.co/hf-inference"
    headers = {"Authorization": f"Bearer {token}"}

    model = "meta-llama/CodeLlama-7b-Instruct-hf"

    payload = {
        "model": model,
        "inputs": (
            "Summarize these Git changes into a concise commit message (under 72 chars, "
            "imperative mood, no tickets). Respond ONLY with JSON: {'message': 'msg here'}\n\n"
            f"{diff_text[:2000]}"
        ),
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"API error: {response.status_code} - {response.text[:200]}")

    try:
        # HF router returns a list of outputs for some models
        data = response.json()
        if isinstance(data, list):
            output_text = data[0].get("generated_text", "").strip()
        else:
            output_text = data.get("generated_text", "").strip()

        parsed = json.loads(output_text)
        return parsed.get("message", output_text.split("\n")[0].strip())
    except Exception:
        return output_text.split("\n")[0].strip()
