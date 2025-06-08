from pathlib import Path
from typing import Dict
import litellm

def load_prompt_template() -> str:
    prompt_path = Path(__file__).parent.parent / "prompts/summarization.md"
    return prompt_path.read_text(encoding="utf-8")

def summarize_transcript(transcript: str, model: str, video_metadata: Dict, quality_metrics: Dict) -> str:
    prompt_template = load_prompt_template()
    
    # Format upload_date from YYYYMMDD to YYYY-MM-DD
    upload_date_raw = video_metadata.get("upload_date", "")
    upload_date = ""
    if upload_date_raw and len(upload_date_raw) == 8:
        upload_date = f"{upload_date_raw[:4]}-{upload_date_raw[4:6]}-{upload_date_raw[6:8]}"
    
    system_msg = prompt_template.format(
        title=video_metadata.get("title", ""),
        duration_string=video_metadata.get("duration_string", ""),
        channel=video_metadata.get("channel", video_metadata.get("uploader", "")),
        webpage_url=video_metadata.get("webpage_url", ""),
        upload_date=upload_date,
        quality_bucket=quality_metrics.get("bucket", "UNSURE")
    )
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": transcript}
        ],
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"] 