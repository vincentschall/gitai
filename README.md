# GitAI 

A lightweight CLI tool that automates Git commit messages using generative AI. Instead of typing `git commit -m "..."`, just run `gitai commit`—it analyzes your staged diff via Hugging Face's Inference API, suggests a concise, imperative-style message, and commits after confirmation.

Built for developers tired of bland commit logs. Inspired by prompt engineering experiments in a Generative AI course—evaluates AI's effectiveness for code summarization tasks.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)

## Features
- **AI-Powered Suggestions**: Generates commit messages from `git diff --cached` using Llama 3.1 8B via Cerebras (ultra-fast, free tier).
- **Structured Output**: Ensures clean, parseable messages under 72 characters in imperative mood (e.g., "Fix login validation edge case").
- **Confirmation Flow**: Preview and approve before committing—never commit a message you don't like.
- **Secure Token Storage**: Tokens saved locally in `~/.config/gitai/config.json` (or `%APPDATA%\gitai` on Windows), excluded from Git.
- **Zero Local Compute**: Cloud-based via Hugging Face's free inference providers—no GPU/RAM requirements.
- **Free & Fast**: Uses Cerebras provider with 1M free tokens/day—enough for hundreds of commits daily.

## Installation

### Option 1: Install with pipx (Recommended for Global Use)

**Best for:** Users who want `gitai` available system-wide without affecting other Python projects.

pipx installs Python CLI applications in isolated environments while making them globally accessible, preventing dependency conflicts.

```bash
# Install pipx if you don't have it
# macOS
brew install pipx
pipx ensurepath

# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install pipx
pipx ensurepath

# Linux (Fedora)
sudo dnf install pipx
pipx ensurepath

# Windows / Other systems
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Restart your terminal after ensurepath

# Install gitai
cd /path/to/gitai
pipx install .

# Now 'gitai' is available globally!
gitai --help
```

### Option 2: Install in a Virtual Environment (Recommended for Development)

**Best for:** Developers who want to modify gitai or keep it isolated per-project.

Python's built-in venv module creates lightweight virtual environments with isolated package dependencies.

```bash
# Navigate to the project directory
cd /path/to/gitai

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install gitai in editable mode
pip install -e .

# Now 'gitai' is available while the venv is activated
gitai --help

# To deactivate when done:
deactivate
```

**Note:** With a virtual environment, you'll see `(venv)` in your terminal prompt when activated. You must activate the environment each time you open a new terminal to use gitai.

Then run gitai directly: `python -m gitai.cli commit`

## Initial Setup

After installation, configure your Hugging Face token:

1. **Get a free Hugging Face token:**
   - Sign up at [huggingface.co](https://huggingface.co/join)
   - Create an access token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (read permission is sufficient)

2. **Store your token:**
   ```bash
   gitai config set
   ```
   Enter your token when prompted. It's stored securely in `~/.config/gitai/config.json` (or `%APPDATA%\gitai\config.json` on Windows).

## Usage 

### Generate Commit Messages

Ensure you're in a Git repository with staged changes (`git add .` first):

```bash
gitai commit
```

You'll see output like:
```bash
Suggested message: Fix login error handling with ValueError raise
Commit this message? (y/n): 
```

Press `y` to commit automatically, or `n` to retry if you don't like the result.

### Managing Your Token

```bash
gitai config set      # Add or update your token
gitai config show     # Display current token (truncated for security)
gitai config delete   # Remove stored token
```

## How It Works

1. **Extracts the diff**: Runs `git diff --cached` to get your staged changes
2. **Sends to AI**: Uses Hugging Face's Inference API with the Cerebras provider (1M free tokens/day)
3. **AI Model**: Llama 3.1 8B Instruct—small enough to be free, smart enough for quality commit messages
4. **Generates message**: Returns a concise, imperative-mood commit message (e.g., "Add user authentication")
5. **Commits**: After your confirmation, runs `git commit -m "message"`

## Why These Technologies?

- **Hugging Face Inference API**: Free tier with generous limits, no local GPU needed
- **Cerebras Provider**: Ultra-fast inference (20x faster than GPUs) with 1M free tokens/day
- **Llama 3.1 8B**: Perfect balance—small enough to be free, capable enough for code analysis
- **No OpenAI API costs**: Completely free solution for unlimited commits

## Troubleshooting

### "Command not found: gitai"

- **If using pipx**: Run `pipx ensurepath` and restart your terminal
- **If using venv**: Make sure the virtual environment is activated (`source venv/bin/activate`)

### "Missing Hugging Face token"

Run `gitai config set` to configure your token. You can also set it via environment variable:
```bash
export HF_API_TOKEN="your_token_here"
```

### "No staged changes found"

Make sure you've staged files with `git add` before running `gitai commit`.

## Requirements

- **Python**: 3.8+ (tested with 3.12.7)
- **Dependencies**: 
  - `huggingface_hub` - For API access
  - `click` - For CLI interface (installed automatically)
- **Git**: Must be in a Git repository
- **Internet**: Required for API calls

## Project Structure

```
gitai/
├── src/gitai/
│       ├── __init__.py
│       ├── cli.py          # CLI commands and interface
│       ├── core.py         # Core system
│       ├── git_utils.py    # Git integrations
│       ├── api.py          # Hugging Face API integration
│       └── config.py       # Token management
├── pyproject.toml      # Package configuration
├── tests/
│   ├── __init__.py
├── README.md
├── LICENSE
└──.gitignore
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Hugging Face for their free Inference API and Cerebras provider
- Meta AI for the Llama 3.1 model
- Course: *Decoding Generative AI (Genres and Generativities)*, Fall 2025 at University of Basel
- Built using Python and open-source tools

## Contributing

Contributions welcome! Feel free to:
- Report bugs via GitHub Issues
- Suggest new features
- Submit pull requests

---

**Version 1.0.0** | Updated November 2025