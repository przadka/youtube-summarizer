import click

@click.command()
@click.argument("youtube_url")
@click.option("--model", "-m", default="gpt-3.5-turbo", help="LLM model to use")
@click.option("--output", "-o", type=click.Path(), help="Output file path")
@click.option("--keep-files", is_flag=True, help="Keep downloaded audio files")
@click.option("--format", type=click.Choice(["markdown", "json", "text"]), default="markdown")
def summarize_video(youtube_url, model, output, keep_files, format):
    """Download, transcribe, and summarize a YouTube video."""
    # Pipeline steps will be implemented here
    pass

if __name__ == "__main__":
    summarize_video() 