from pathlib import Path
from typing import Dict
import litellm

def load_prompt_template() -> str:
    prompt_path = Path("prompts/summarization.txt")
    return prompt_path.read_text(encoding="utf-8")

def summarize_transcript(transcript: str, model: str, video_metadata: Dict, quality_metrics: Dict) -> str:
    prompt_template = load_prompt_template()
    prompt = prompt_template.format(
        title=video_metadata.get("title", ""),
        duration=video_metadata.get("duration", ""),
        channel=video_metadata.get("channel", video_metadata.get("uploader", "")),
        quality_bucket=quality_metrics.get("bucket", "UNSURE"),
        transcript=transcript
    )
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"LLM summarization failed: {e}") 