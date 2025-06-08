import click
from pathlib import Path
import tempfile
import sys
import pipeline.downloader as downloader
import pipeline.transcriber as transcriber
import pipeline.summarizer as summarizer

@click.command()
@click.argument("youtube_url")
@click.option("--model", "-m", default="gpt-3.5-turbo", help="LLM model to use")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--keep-files", is_flag=True, help="Keep downloaded audio files")
@click.option("--format", type=click.Choice(["markdown", "json", "text"]), default="markdown")
def summarize_video(youtube_url, model, output, keep_files, format):
    """Download, transcribe, and summarize a YouTube video."""
    temp_dir = None
    audio_file = None
    try:
        click.echo("[1/4] Downloading audio and extracting metadata...")
        audio_file, temp_dir = downloader.download_audio(youtube_url)
        video_metadata = downloader.extract_video_metadata(youtube_url)

        click.echo("[2/4] Transcribing audio...")
        transcript, quality_metrics = transcriber.transcribe_with_existing_script(audio_file)

        click.echo("[3/4] Summarizing transcript with LLM...")
        summary = summarizer.summarize_transcript(transcript, model, video_metadata, quality_metrics)

        click.echo("[4/4] Outputting summary...")
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
            for ext in [".wav", ".txt", ".quality.json"]:
                f = audio_file.with_suffix(ext)
                if f.exists():
                    f.unlink()
        if temp_dir:
            temp_dir.cleanup()

if __name__ == "__main__":
    summarize_video() 