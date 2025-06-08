from pathlib import Path
from typing import Dict
import litellm
from . import config

def load_prompt_template(prompt_path: str = None) -> str:
    if prompt_path is None:
        # Always resolve relative to the package root
        base_dir = Path(__file__).parent.parent.parent
        prompt_path = base_dir / "prompts" / "summarization.md"
    else:
        prompt_path = Path(prompt_path)
    return prompt_path.read_text(encoding="utf-8")

def summarize_transcript(
    transcript: str,
    model: str,
    video_metadata: Dict,
    quality_metrics: Dict,
    temperature: float = None,
    prompt_path: str = None
) -> str:
    prompt_template = load_prompt_template(prompt_path)
    
    # Format upload_date from YYYYMMDD to YYYY-MM-DD
    upload_date_raw = video_metadata.get("upload_date", "")
    upload_date = ""
    if upload_date_raw and len(upload_date_raw) == 8:
        y = upload_date_raw[config.DATE_YEAR_SLICE]
        m = upload_date_raw[config.DATE_MONTH_SLICE]
        d = upload_date_raw[config.DATE_DAY_SLICE]
        upload_date = f"{y}-{m}-{d}"
    
    system_msg = prompt_template.format(
        title=video_metadata.get("title", ""),
        duration_string=video_metadata.get("duration_string", ""),
        channel=video_metadata.get("channel", video_metadata.get("uploader", "")),
        webpage_url=video_metadata.get("webpage_url", ""),
        upload_date=upload_date,
        quality_bucket=quality_metrics.get("bucket", "UNSURE")
    )
    if temperature is None:
        temperature = config.DEFAULT_TEMPERATURE
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": transcript}
        ],
        temperature=temperature
    )
    return response["choices"][0]["message"]["content"] 