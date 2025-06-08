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

Advanced options:
```bash
# Use different model and temperature
python main.py -m "gpt-4" -t 0.7 "https://www.youtube.com/watch?v=VIDEO_ID"

# Different language and audio format
python main.py -l "es" --audio-format "mp3" "https://www.youtube.com/watch?v=VIDEO_ID"

# Custom prompt template
python main.py --prompt-path "custom_prompt.md" "https://www.youtube.com/watch?v=VIDEO_ID"

# Save to file and keep intermediate files
python main.py -o summary.txt --keep-files "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Configuration

### API Keys
Set your LLM API key:
```bash
export OPENAI_API_KEY="your-key-here"
# or for other providers, see LiteLLM documentation
```

### Environment Variables
Customize defaults via environment variables:
```bash
export SUMMARIZE_YT_MODEL="gpt-4"
export SUMMARIZE_YT_TEMPERATURE="0.7"
export SUMMARIZE_YT_LANGUAGE="es"
export SUMMARIZE_YT_AUDIO_FORMAT="mp3"
export SUMMARIZE_YT_PROMPT_PATH="custom_prompt.md"
```

### CLI Options
- `-m, --model`: LLM model (default: gpt-4.1-mini)
- `-t, --temperature`: LLM temperature 0.0-1.0 (default: 0.3)
- `-l, --language`: Audio language code (default: en)
- `--audio-format`: Audio format (default: wav)
- `--prompt-path`: Custom prompt template path
- `-o, --output`: Output file path
- `--keep-files`: Keep downloaded audio files

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