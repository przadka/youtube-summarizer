# YouTube Summarizer

A CLI tool to download, transcribe, and summarize YouTube videos using LLMs.

## Features
- Download YouTube videos as audio (WAV)
- Extract video metadata
- Transcribe audio using an external script
- Summarize transcripts with LLMs
- Modular, testable pipeline

## Prerequisites

Before using this tool, you need:

1. **yt-dlp**: Install via `pip install yt-dlp` or your package manager
2. **transcribe CLI tool**: External transcription script (must be in PATH)
3. **LLM API access**: OpenAI, Anthropic, or other LiteLLM-supported provider

## Installation

```bash
git clone <repository-url>
cd summarize-yt
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

With options:
```bash
# Use different model
python main.py -m "gpt-4" "https://www.youtube.com/watch?v=VIDEO_ID"

# Save to file
python main.py -o summary.txt "https://www.youtube.com/watch?v=VIDEO_ID"

# Keep downloaded audio files
python main.py --keep-files "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Configuration

Set your LLM API key:
```bash
export OPENAI_API_KEY="your-key-here"
# or for other providers, see LiteLLM documentation
```

Supported models include any LiteLLM-compatible model (gpt-3.5-turbo, gpt-4, claude-3, etc.)

## Summary Output Format
The summarizer produces structured output with video metadata, an overall summary, memorable quotes (with timestamps), and a detailed summary. The format is defined in `prompts/summarization.md` and can be customized as needed.

Example output structure:
```
<summary>
  <video_metadata>...</video_metadata>
  <overall_summary>...</overall_summary>
  <memorable_quotes>...</memorable_quotes>
  <detailed_summary>...</detailed_summary>
</summary>
```

## Development

### Setup
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Running Tests
- Unit and integration tests are in the `tests/` directory.
- Run all tests:
  ```bash
  .venv/bin/pytest tests/
  ```
- Integration tests (require network, yt-dlp, and real YouTube access) are skipped by default. To run them:
  ```bash
  RUN_INTEGRATION_TESTS=1 .venv/bin/pytest tests/
  ```

### Linting
- Lint the codebase with [ruff](https://docs.astral.sh/ruff/):
  ```bash
  .venv/bin/ruff check pipeline tests main.py
  ```
- Ruff is configured in `pyproject.toml`.

### Good Practices
- All development and testing should be done in the `.venv` virtual environment.
- `.venv` and test caches are git-ignored. 