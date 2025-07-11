import click
import sys
from summarize_yt.pipeline import downloader, transcriber, summarizer, config
import re

@click.command()
@click.argument("input_path")
@click.option("--model", "-m", default=config.DEFAULT_MODEL, help="LLM model to use")
@click.option("--temperature", "-t", default=config.DEFAULT_TEMPERATURE, type=float, help="LLM temperature")
@click.option("--language", "-l", default=config.DEFAULT_LANGUAGE, help="Audio language")
@click.option("--audio-format", default=config.DEFAULT_AUDIO_FORMAT, help="Audio format (e.g., wav)")
@click.option("--prompt-path", default=config.DEFAULT_PROMPT_PATH, help="Prompt template path")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--keep-files", is_flag=True, help="Keep downloaded audio files")
def summarize_video(input_path, model, temperature, language, audio_format, prompt_path, output, keep_files):
    """Download (if needed), transcribe, and summarize a YouTube video or local file."""
    temp_dir = None
    audio_file = None
    video_metadata = None
    try:
        click.echo(config.PROGRESS_STEPS[0])
        # Detect if input_path is a URL or a file
        is_url = bool(re.match(r"^(https?://|www\.)", input_path, re.IGNORECASE))
        if is_url:
            audio_file, temp_dir, video_metadata = downloader.download_audio(input_path, language=language, audio_format=audio_format)
        else:
            audio_file, temp_dir, video_metadata = downloader.handle_local_file(input_path)

        click.echo(config.PROGRESS_STEPS[1])
        transcript, quality_metrics = transcriber.transcribe_with_existing_script(audio_file, language=language)

        click.echo(config.PROGRESS_STEPS[2])
        summary = summarizer.summarize_transcript(
            transcript,
            model,
            video_metadata,
            quality_metrics,
            temperature=temperature,
            prompt_path=prompt_path
        )

        click.echo(config.PROGRESS_STEPS[3])
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(summary)
            click.echo(f"Summary written to {output}")
        else:
            click.echo(summary)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    finally:
        if not keep_files and audio_file:
            # Remove audio, transcript, and quality files
            for ext in [config.EXT_WAV, config.EXT_TXT, config.EXT_QUALITY_JSON]:
                f = audio_file.with_suffix(ext)
                if f.exists():
                    f.unlink()
        if temp_dir:
            temp_dir.cleanup()

if __name__ == "__main__":
    summarize_video() 