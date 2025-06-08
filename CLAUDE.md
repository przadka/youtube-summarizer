# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Testing
- Run unit tests: `.venv/bin/pytest tests/`
- Run integration tests (requires network): `RUN_INTEGRATION_TESTS=1 .venv/bin/pytest tests/`
- Run single test: `.venv/bin/pytest tests/test_downloader.py::test_function_name`

### Linting
- Check code style: `.venv/bin/ruff check pipeline tests main.py`

## Architecture

This is a modular YouTube video processing pipeline with three main stages:

1. **Downloader** (`pipeline/downloader.py`): Downloads YouTube audio via yt-dlp and extracts metadata
2. **Transcriber** (`pipeline/transcriber.py`): Calls external `transcribe` CLI tool to convert audio to text
3. **Summarizer** (`pipeline/summarizer.py`): Uses LiteLLM to summarize transcripts with configurable models

The main CLI (`main.py`) orchestrates these stages sequentially, with cleanup handling for temporary files.

### Key Dependencies
- **yt-dlp**: YouTube downloading (external binary required)
- **transcribe**: Audio transcription (external CLI tool required)  
- **LiteLLM**: LLM interface supporting multiple providers
- **Click**: CLI framework

### Configuration System
All configuration is centralized in `pipeline/config.py` with environment variable support:
- Default values can be overridden via `SUMMARIZE_YT_*` environment variables
- CLI options in `main.py` expose key parameters (model, temperature, language, etc.)
- No hardcoded magic numbers - all constants are named and configurable

### Prompt System
The summarization prompt template is in `prompts/summarization.md` and uses format strings for video metadata injection. The system splits this into system/user messages for the LLM. Template path is configurable via `--prompt-path` or `SUMMARIZE_YT_PROMPT_PATH`.

### Testing Strategy
- Unit tests mock external dependencies (yt-dlp, transcribe CLI)
- Integration tests require actual network access and external tools
- Quality metrics from transcription are passed through to summarization
- Tests verify configuration system works correctly