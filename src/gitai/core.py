import click
from .git_utils import get_staged_diff, commit_changes
from .api import generate_commit_message


def run_commit_flow(retry_text: str):
    """Main logic for 'gitai commit' """
    diff = get_staged_diff()
    if not diff:
        click.echo("No staged changes. Stage with 'git add' first.")
        return

    try:
        message = generate_commit_message(diff, retry_text)
    except Exception as e:
        click.echo(f"Error generating commit message: {e}")
        return

    click.echo(f"\nSuggested commit message:\n> {message}\n")

    choice = click.prompt(
        "Commit this message? [y]es / [n]o / [r]etry",
        type=click.Choice(['y', 'n', 'r'], case_sensitive=False)
    )

    if choice == 'y':
        commit_changes(message)
        click.echo("Committed!")
    elif choice == 'r':
        click.echo("Retrying...")
        run_commit_flow(message)
    elif choice == 'n':
        click.echo("Aborted...")

