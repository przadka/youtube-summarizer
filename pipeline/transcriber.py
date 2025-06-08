import subprocess
import json
from pathlib import Path
from typing import Tuple

def transcribe_with_existing_script(audio_file: Path, language: str = "en") -> Tuple[str, dict]:
    """
    Call the 'transcribe' CLI tool on the given audio file.
    Returns (transcript_text, quality_metrics_dict).
    """
    audio_file = Path(audio_file)
    transcript_txt = audio_file.with_suffix(".txt")
    quality_json = audio_file.with_suffix(".quality.json")
    cmd = [
        "transcribe",
        str(audio_file),
        "--language", language,
        "--quality-json"
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Transcription failed: {e.stderr.decode() if e.stderr else e}")
    if not transcript_txt.exists():
        raise FileNotFoundError(f"Transcript file not found: {transcript_txt}")
    if not quality_json.exists():
        raise FileNotFoundError(f"Quality metrics file not found: {quality_json}")
    transcript = transcript_txt.read_text(encoding="utf-8")
    with open(quality_json, "r", encoding="utf-8") as f:
        quality = json.load(f)
    return transcript, quality 