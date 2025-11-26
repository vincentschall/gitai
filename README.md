# GitAI

A lightweight CLI tool that automates Git commit messages using generative AI. Instead of typing `git commit -m "..."`, just run `gitai commit`—it analyzes your staged diff via Hugging Face's Inference API, suggests a concise, imperative-style message, and commits after confirmation.

Built for developers tired of bland commit logs. Inspired by prompt engineering experiments in a Generative AI course—evaluates AI's effectiveness for code summarization tasks.

**NOTE:** This project was built and tested _mostly_ on macOS, so there is a good chance of finding bugs on Windows!

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

### Install in a Virtual Environment (Recommended for Development)

**Best for:** Developers who want to modify gitai or keep it isolated per-project.

Python's built-in venv module creates lightweight virtual environments with isolated package dependencies.

```bash
# Navigate to the project directory
cd /path/to/gitai

# Create a virtual environment
python3 -m venv gitai

# Activate the virtual environment
# On macOS/Linux:
source gitai/bin/activate

# On Windows:
venv\Scripts\activate

# Install gitai in editable mode
pip install -e .

# Now 'gitai' is available while the venv is activated
gitai --help

# To deactivate when done:
deactivate
```

**Note:** With a virtual environment, you'll see `(gitai)` in your terminal prompt when activated. You must activate the environment each time you open a new terminal to use gitai.

## Initial Setup

After installation, configure your Hugging Face token:

1. **Get a free Hugging Face token:**
   - Sign up at [huggingface.co](https://huggingface.co/join)
   - Create an access token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (read permission is sufficient, or choose fine-grained and allow only "Make calls to Inference Providers")

2. **Store your token:**
   ```bash
   gitai config token
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
Fix login error handling with ValueError raise
Commit this message? [y]es / [n]o / [r]etry (y, n, r): y
```

Press `y` then enter to commit automatically, or `r` to retry if you don't like the result. You can abort the process with `n`.

### Managing Your Configuration

```bash
gitai config default     # Reset config file to default values
gitai config delete      # Delete the stored Hugging Face token.
gitai config set-token   # Save your Hugging Face API token securely.
gitai config show        # Show the currently stored config.
gitai config show-token  # Show the currently stored token (truncated).
gitai config update      # Update configuration values using command-line options.
giati --help          # Show help page
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

Make sure the virtual environment is activated (`source venv/bin/activate`) and the project was initially installed with pip.

### "Missing Hugging Face token"

Run `gitai config set` to configure your token (recommended). You can also set it via environment variable:
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