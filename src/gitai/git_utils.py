import subprocess


def get_staged_diff(limit=2000):
    """Return the staged diff text (truncated if very long)."""
    try:
        diff = subprocess.check_output(['git', 'diff', '--cached'], text=True)
        if not diff.strip():
            return None

        if len(diff) > limit:
            diff = diff[:limit] + "\n... (truncated)"

        stat = subprocess.check_output(['git', 'diff', '--stat', '--cached'], text=True)
        return f"Files changed summary:\n{stat}\n\nDiff:\n{diff}"
    except subprocess.CalledProcessError:
        raise RuntimeError("Not a Git repository or error getting diff.")


def commit_changes(message: str):
    """Commit staged changes with the given message."""
    subprocess.run(['git', 'commit', '-m', message])
