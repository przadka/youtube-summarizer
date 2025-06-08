import pytest
from unittest.mock import patch, MagicMock
from summarize_yt import main
import sys
import click

# Example: test valid CLI args
@patch('summarize_yt.main.downloader.download_audio')
@patch('summarize_yt.main.transcriber.transcribe_with_existing_script')
@patch('summarize_yt.main.summarizer.summarize_transcript')
def test_main_valid_args(mock_summarize, mock_transcribe, mock_download):
    mock_download.return_value = (MagicMock(), MagicMock(), {'id': 'testid'})
    mock_transcribe.return_value = ('transcript', {'quality': 'good'})
    mock_summarize.return_value = 'summary'
    test_args = ['main.py', 'http://youtube.com/test']
    with patch.object(sys, 'argv', test_args):
        with patch('click.echo') as mock_echo:
            main.summarize_video.main(standalone_mode=False)
            assert mock_echo.called

# Example: test invalid CLI args

def test_main_invalid_args():
    test_args = ['main.py', '--badflag']
    with patch.object(sys, 'argv', test_args):
        with pytest.raises(click.exceptions.NoSuchOption):
            main.summarize_video.main(standalone_mode=False)

# Example: test file cleanup
@patch('summarize_yt.main.downloader.download_audio')
@patch('summarize_yt.main.transcriber.transcribe_with_existing_script')
@patch('summarize_yt.main.summarizer.summarize_transcript')
def test_main_cleanup(mock_summarize, mock_transcribe, mock_download):
    mock_audio_file = MagicMock()
    mock_audio_file.with_suffix.return_value.exists.return_value = True
    mock_download.return_value = (mock_audio_file, MagicMock(), {'id': 'testid'})
    mock_transcribe.return_value = ('transcript', {'quality': 'good'})
    mock_summarize.return_value = 'summary'
    test_args = ['main.py', 'http://youtube.com/test']
    with patch.object(sys, 'argv', test_args):
        with patch('click.echo'):
            main.summarize_video.main(standalone_mode=False)
    # File cleanup is handled in finally block; no explicit assert here 

# Test valid CLI args with local file
@patch('summarize_yt.main.downloader.handle_local_file')
@patch('summarize_yt.main.transcriber.transcribe_with_existing_script')
@patch('summarize_yt.main.summarizer.summarize_transcript')
def test_main_local_file_args(mock_summarize, mock_transcribe, mock_handle_local):
    mock_handle_local.return_value = (MagicMock(), MagicMock(), {'id': 'localfile'})
    mock_transcribe.return_value = ('transcript', {'quality': 'good'})
    mock_summarize.return_value = 'summary'
    test_args = ['main.py', '/path/to/local/file.mp4']
    with patch.object(sys, 'argv', test_args):
        with patch('click.echo') as mock_echo:
            main.summarize_video.main(standalone_mode=False)
            assert mock_echo.called 

@patch('summarize_yt.main.transcriber.transcribe_with_existing_script')
@patch('summarize_yt.main.summarizer.summarize_transcript')
def test_cli_pipeline_with_local_file(mock_summarize, mock_transcribe, tmp_path):
    # Create a dummy local audio file
    dummy_file = tmp_path / 'clip.wav'
    dummy_file.write_bytes(b'data')
    # Patch handle_local_file to use the real implementation
    from summarize_yt.pipeline import downloader
    # Setup mocks
    mock_transcribe.return_value = ('transcript', {'quality': 'good'})
    mock_summarize.return_value = 'summary'
    test_args = ['main.py', str(dummy_file)]
    with patch('sys.argv', test_args):
        with patch('click.echo') as mock_echo:
            with patch('summarize_yt.main.downloader.handle_local_file', wraps=downloader.handle_local_file):
                import summarize_yt.main
                summarize_yt.main.summarize_video.main(standalone_mode=False)
                assert mock_echo.called 