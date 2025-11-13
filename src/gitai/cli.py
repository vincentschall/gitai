import click
from .core import run_commit_flow
from .config import save_token, delete_token, load_token


@click.group()
def main():
    """GitAI – Generate smart Git commit messages with AI."""
    pass


@main.command()
def commit():
    """Generate an AI-powered commit message and commit the changes."""
    run_commit_flow()


@main.group()
def config():
    """Manage your GitAI configuration."""
    pass


@config.command("set")
@click.option("--token", prompt=True, hide_input=True, confirmation_prompt=True, help="Your Hugging Face API token")
def set_token(token):
    """Save your Hugging Face API token securely."""
    save_token(token)


@config.command("show")
def show_token():
    """Show the currently stored token (truncated)."""
    token = load_token()
    if token:
        click.echo(f"Current token: {token[:6]}...{token[-4:]}")
    else:
        click.echo("No token set.")


@config.command("delete")
def delete_config():
    """Delete the stored Hugging Face token."""
    delete_token()
