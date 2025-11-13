import subprocess
import sys
import json
import click
import requests  # For HF API; swap for ollama if local


@click.command()
@click.argument('action', default='commit')
def gitai(action):
    if action != 'commit':
        click.echo("Only 'commit' supported.")
        sys.exit(1)

    # Step 1: Get staged diff
    try:
        diff = subprocess.check_output(['git', 'diff', '--cached'], text=True)
        if not diff.strip():
            click.echo("No staged changes. Stage with 'git add' first.")
            sys.exit(1)
        # Truncate/format diff
        if len(diff) > 2000:
            diff = diff[:2000] + "\n... (truncated)"
        context = f"Files changed summary: {subprocess.check_output(['git', 'diff', '--stat', '--cached'], text=True)}"
        full_input = f"{context}\n\nDiff:\n{diff}"
    except subprocess.CalledProcessError:
        click.echo("Not a Git repo or error getting diff.")
        sys.exit(1)

    # Step 2: Generate message via AI (HF example; adapt for Ollama/MagAI)
    prompt = f"Summarize these Git changes into a concise commit message (under 72 chars, imperative, no tickets). Respond ONLY with JSON: {{'message': 'msg here'}}\n\n{full_input}"

    # In the generate section:
    API_URL = "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-Instruct-hf"
    headers = {"Authorization": "Bearer hf_YOUR_TOKEN_HERE"}  # From hf.co/settings/tokens
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,  # Bump for better JSON
            "temperature": 0.1,  # Low for consistent structure
            "return_full_text": False
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        ai_output = response.json()[0]['generated_text'].strip()
    else:
        ai_output = f"API error: {response.status_code} - {response.text[:100]}"
        # Fallback: Print and exit, or use a local stub
    # Step 3: Parse JSON
    try:
        parsed = json.loads(ai_output)
        message = parsed.get('message', ai_output.split('\n')[0].strip())  # Fallback to first line
    except json.JSONDecodeError:
        message = ai_output.split('\n')[0].strip()  # Extract best-effort

    # Step 4: Confirm & Commit
    click.echo(f"Suggested message: {message}")
    confirm = click.confirm("Commit with this message?")
    if confirm:
        subprocess.run(['git', 'commit', '-m', message])
        click.echo("Committed!")
    else:
        click.echo("Aborted.")


if __name__ == '__main__':
    gitai()