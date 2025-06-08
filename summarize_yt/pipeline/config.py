import os

# LLM Model
DEFAULT_MODEL = os.getenv("SUMMARIZE_YT_MODEL", "gpt-4o-mini")

# LLM Temperature
DEFAULT_TEMPERATURE = float(os.getenv("SUMMARIZE_YT_TEMPERATURE", "0.3"))

# Prompt template path
DEFAULT_PROMPT_PATH = os.getenv("SUMMARIZE_YT_PROMPT_PATH", None)

# Audio settings
DEFAULT_AUDIO_FORMAT = os.getenv("SUMMARIZE_YT_AUDIO_FORMAT", "wav")
DEFAULT_AUDIO_QUALITY = os.getenv("SUMMARIZE_YT_AUDIO_QUALITY", "bestaudio")

# Default language
DEFAULT_LANGUAGE = os.getenv("SUMMARIZE_YT_LANGUAGE", "en")

# File extensions
EXT_WAV = ".wav"
EXT_TXT = ".txt"
EXT_QUALITY_JSON = ".quality.json"

# Binary names
YTDLP_BIN = os.getenv("SUMMARIZE_YT_YTDLP_BIN", "yt-dlp")
TRANSCRIBE_BIN = os.getenv("SUMMARIZE_YT_TRANSCRIBE_BIN", "transcribe")

# Progress indicators
PROGRESS_STEPS = [
    "[1/4] Downloading audio and extracting metadata...",
    "[2/4] Transcribing audio...",
    "[3/4] Summarizing transcript with LLM...",
    "[4/4] Outputting summary..."
]

# Date parsing indices (for legacy code, but should use a parser)
DATE_YEAR_SLICE = slice(0, 4)
DATE_MONTH_SLICE = slice(4, 6)
DATE_DAY_SLICE = slice(6, 8) 