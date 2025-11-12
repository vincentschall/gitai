# GitAI 🚀

A lightweight CLI tool that automates Git commit messages using generative AI. Instead of typing `git commit -m "..."`, just run `gitai commit`—it analyzes your staged diff via Hugging Face's Inference API (powered by CodeLlama), suggests a concise, imperative-style message, and commits after confirmation.

Built for developers tired of bland commit logs. Inspired by prompt engineering experiments in a Generative AI course—evaluates AI's effectiveness for code summarization tasks.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

## Features
- **AI-Powered Suggestions**: Generates commit messages from `git diff --cached` using a code-aware LLM (CodeLlama-7B).
- **Structured Output**: Prompts for JSON to ensure parseable, 72-char max messages (e.g., "Fix login validation edge case").
- **Confirmation Flow**: Preview and approve before committing.
- **Evaluation Mode**: Optional `--score` flag to rate suggestions against best practices (e.g., imperative verbs, no tickets).
- **Zero Local Compute**: Cloud-based via free Hugging Face tier—no GPU/RAM hassles.
- **Extensible**: Easy to swap models or add prompt chains.

## Installation
1. Clone the repo: ```git clone https://github.com/Noah-Klaholz/gitai```
2. Move into project folder: ```cd gitai```
3. install dependencies (python 3.8+ required): ```pip install -e .```
   - This uses 'pyproject.toml' for the install, alternatively you can use 'pip install -r requirements.txt'
4. Get a free Hugging Face token:
   - Sign up at [huggingface.co](https://huggingface.co/join).
   - Create an access token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) (read-only is fine).
   - Set it as an env var: `export HF_TOKEN="hf_your_token_here"`.

## Usage 
Ensure you're in a Git repo with staged changes (```git add .``` first).
Just write: gitai commit
You will see some output like this: 
Suggested message: Fix login error handling with ValueError raise
Commit this message? (y/n): 
Either confirm the message (automatically commiting) or refuse and retry if you do not like the result.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Hugging Face for free Inference API.
- Course: *Decoding Generative AI (Genres and Generativities)*, Fall 2025.
- Built with ❤️ using Python and open-source tools.

---
*Version 0.1.0 | Updated Nov 2025*