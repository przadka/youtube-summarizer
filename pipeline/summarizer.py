from pathlib import Path
from typing import Dict
import litellm
import re

def load_prompt_template() -> str:
    prompt_path = Path("prompts/summarization.md")
    return prompt_path.read_text(encoding="utf-8")

def summarize_transcript(transcript: str, model: str, video_metadata: Dict, quality_metrics: Dict) -> str:
    prompt_template = load_prompt_template()
    # Fill in metadata, but leave out transcript
    system_msg = prompt_template.format(
        title=video_metadata.get("title", ""),
        duration=video_metadata.get("duration", ""),
        channel=video_metadata.get("channel", video_metadata.get("uploader", "")),
        quality_bucket=quality_metrics.get("bucket", "UNSURE"),
        transcript=""
    )
    # Remove the Transcript: section and everything after
    system_msg = re.split(r"Transcript:\s*", system_msg)[0].strip()
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": transcript}
        ],
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"] 