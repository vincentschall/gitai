import click
from .core import run_commit_flow
from .config import save_token, delete_token, load_token, reset_config, update_config, show_config


@click.group()
def main():
    """GitAI – Generate smart Git commit messages with AI."""


@main.command()
def commit():
    """Generate an AI-powered commit message and commit the changes."""
    run_commit_flow("")


@main.group()
def config():
    """Manage your GitAI configuration."""
    pass

@config.command("show")
def view_config():
    """Show the currently stored config."""
    show_config()


@config.command("set-token")
@click.option("--token", prompt=True, hide_input=True, confirmation_prompt=True, help="Your Hugging Face API token")
def set_token(token):
    """Save your Hugging Face API token securely."""
    save_token(token)


@config.command("show-token")
def show_token():
    """Show the currently stored token (truncated)."""
    token = load_token()
    if token:
        click.echo(f"Current token: {token[:6]}...{token[-4:]}")
    else:
        click.echo("No token set.")


@config.command("delete")
def remove_token():
    """Delete the stored Hugging Face token."""
    delete_token()

@config.command("default")
def default_config():
    """Reset config file to default values"""
    reset_config()


@config.command("update")
@click.option("--temperature", type=float, help="Sampling temperature (0.0-1.0)")
@click.option("--max-tokens", type=int, help="Maximum tokens to generate")
@click.option("--max-length", type=int, help="Maximum character length for commit message")
@click.option("--model", type=str, help="Model name to use")
@click.option("--provider", type=click.Choice(['auto', 'cerebras', 'hf-inference']), help="Provider to use")
@click.option("--prompt", type=str, help="System prompt for commit generation")
def update_config_options(temperature, max_tokens, max_length, model, provider, prompt):
    """
    Update configuration values using command-line options.

    Usage:
        gitai config update --temperature 0.7 --max-tokens 150
        gitai config update --model "meta-llama/Llama-3.1-8B-Instruct"
    """
    updates = {}

    if temperature is not None:
        if not 0 <= temperature <= 1:
            click.secho("Temperature must be between 0.0 and 1.0", fg="red")
            return
        updates["TEMPERATURE"] = temperature

    if max_tokens is not None:
        if max_tokens <= 0:
            click.secho("Max tokens must be positive", fg="red")
            return
        updates["MAX_TOKENS"] = max_tokens

    if max_length is not None:
        if max_length <= 0:
            click.secho("Max length must be positive", fg="red")
            return
        updates["MAX_CHAR_LENGTH"] = max_length

    if model is not None:
        updates["MODEL"] = model

    if provider is not None:
        updates["PROVIDER"] = provider

    if prompt is not None:
        updates["PROMPT"] = prompt

    if not updates:
        click.secho("No values provided to update", fg="red")
        click.echo("Use --help to see available options")
        return

    update_config(**updates)
    click.secho(f"Updated {len(updates)} configuration value(s)", fg="green")

    # Show what was updated
    for key, value in updates.items():
        if key == "PROMPT":
            value_display = f"{value[:50]}..." if len(value) > 50 else value
        else:
            value_display = value
        click.echo(f"  {key}: {value_display}")


