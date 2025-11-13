import click
from .git_utils import get_staged_diff, commit_changes
from .api import generate_commit_message


def run_commit_flow():
    """Main logic for 'gitai commit'."""
    diff = get_staged_diff()
    if not diff:
        click.echo("No staged changes. Stage with 'git add' first.")
        return

    try:
        message = generate_commit_message(diff)
    except Exception as e:
        click.echo(f"Error generating commit message: {e}")
        return

    click.echo(f"\nSuggested commit message:\n> {message}\n")
    if click.confirm("Commit with this message?"):
        commit_changes(message)
        click.echo("✅ Committed!")
    else:
        click.echo("❌ Aborted.")
