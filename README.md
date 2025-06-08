# YouTube Summarizer

A CLI tool to download, transcribe, and summarize YouTube videos or local audio/video files using LLMs.

## Features
- Download YouTube videos as audio (WAV) or process local audio/video files
- Extract video metadata (YouTube) or generate basic metadata (local files)
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
pip install youtube-summarizer
```

Or from source:
```bash
git clone <repository-url>
cd youtube-summarizer
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
ytsumm "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# OR with a local file (audio or video)
ytsumm "/path/to/local/file.mp4"
```

Advanced options:
```bash
# Use different model and temperature
ytsumm -m "gpt-4o" -t 0.7 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Use Claude model
ytsumm -m "claude-3-5-sonnet-20240620" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Different language and audio format
ytsumm -l "es" --audio-format "mp3" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Custom prompt template
ytsumm --prompt-path "custom_prompt.md" "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Save to file and keep intermediate files
ytsumm -o summary.txt --keep-files "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
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
export SUMMARIZE_YT_MODEL="gpt-4o"
export SUMMARIZE_YT_TEMPERATURE="0.7"
export SUMMARIZE_YT_LANGUAGE="es"
export SUMMARIZE_YT_AUDIO_FORMAT="mp3"
export SUMMARIZE_YT_PROMPT_PATH="custom_prompt.md"
```

### CLI Options
- `-m, --model`: LLM model (default: gpt-4o-mini)
- `-t, --temperature`: LLM temperature 0.0-1.0 (default: 0.3)
- `-l, --language`: Audio language code (default: en)
- `--audio-format`: Audio format (default: wav)
- `--prompt-path`: Custom prompt template path
- `-o, --output`: Output file path
- `--keep-files`: Keep downloaded audio files
- `input_path`: YouTube URL or path to a local audio/video file

Supported models include any LiteLLM-compatible model:
- OpenAI: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-3.5-turbo`
- Anthropic: `claude-3-5-sonnet-20240620`, `claude-3-haiku-20240307`
- And many others via LiteLLM

## Example Output

```
<summary>
  <video_metadata>Title: Python Tutorial - Learn Python in 10 Minutes | Channel: TechCoder</video_metadata>
  <overall_summary>A beginner-friendly Python tutorial covering variables, loops, and functions with practical examples.</overall_summary>
</summary>
```


## Performance & Cost
- Typical processing time: ~2-3 minutes for a 30min video (depends on hardware and LLM API latency)
- LLM costs vary by provider and model (cost estimates will be added in future releases)

## Limitations
- For video platforms: YouTube URLs only (no support for other video platforms)
- Also supports local audio/video files (any format supported by the transcribe tool)
- Requires external `transcribe` CLI tool in PATH
- English transcription works best; other languages may be less accurate

## Contributing
PRs welcome. Run tests first:
```bash
pytest tests/
```
Report issues on GitHub.

## License
MIT License. See [LICENSE](LICENSE) for details.

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
  .venv/bin/ruff check summarize_yt tests
  ```
- Ruff is configured in `pyproject.toml`.

### Good Practices
- All development and testing should be done in the `.venv` virtual environment.
- `.venv` and test caches are git-ignored. 