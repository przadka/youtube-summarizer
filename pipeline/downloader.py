import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Optional
import json

def download_audio(url: str, output_dir: Path = None, video_metadata: Optional[Dict] = None) -> tuple[Path, Optional[tempfile.TemporaryDirectory], Dict]:
    """
    Download YouTube video as WAV audio using yt-dlp.
    Returns (audio_file_path, temp_dir_object or None, video_metadata dict).
    If video_metadata is provided, uses its 'id' for the output filename.
    """
    if output_dir is None:
        temp_dir = tempfile.TemporaryDirectory()
        output_dir = Path(temp_dir.name)
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        temp_dir = None

    if video_metadata is None:
        video_metadata = extract_video_metadata(url)
    video_id = video_metadata.get("id")
    output_template = output_dir / f"{video_id}.%(ext)s"
    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", "wav",
        "--output", str(output_template),
        url
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"yt-dlp failed: {e.stderr.decode() if e.stderr else e}")

    audio_file = output_dir / f"{video_id}.wav"
    if not audio_file.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    return audio_file, temp_dir, video_metadata

def extract_video_metadata(url: str) -> Dict:
    """
    Extract video metadata (title, duration, channel, id, etc.) using yt-dlp.
    """
    cmd = [
        "yt-dlp",
        "--dump-json",
        url
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        info = json.loads(result.stdout)
        return {
            "id": info.get("id"),
            "title": info.get("title"),
            "duration": info.get("duration"),
            "channel": info.get("channel"),
            "uploader": info.get("uploader"),
            "webpage_url": info.get("webpage_url"),
        }
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"yt-dlp metadata extraction failed: {e.stderr if e.stderr else e}")
    except json.JSONDecodeError:
        raise RuntimeError("Failed to parse yt-dlp JSON output.") 