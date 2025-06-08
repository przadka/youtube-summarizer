import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from summarize_yt.pipeline import downloader
import tempfile
import subprocess

def test_extract_video_metadata_success():
    fake_json = '{"id": "abc123", "title": "Test Video", "duration": 123, "channel": "Test Channel", "uploader": "Uploader", "webpage_url": "http://yt"}'
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(stdout=fake_json, returncode=0)
        meta = downloader.extract_video_metadata("http://yt")
        assert meta["id"] == "abc123"
        assert meta["title"] == "Test Video"
        assert meta["duration"] == 123
        assert meta["channel"] == "Test Channel"

def test_extract_video_metadata_failure():
    with patch('subprocess.run', side_effect=Exception("fail")):
        with pytest.raises(Exception):
            downloader.extract_video_metadata("badurl")

def test_download_audio_file_not_found():
    # Patch extract_video_metadata to return a fake id
    with patch('summarize_yt.pipeline.downloader.extract_video_metadata') as mock_meta:
        mock_meta.return_value = {"id": "notfound"}
        with patch('subprocess.run'):
            with tempfile.TemporaryDirectory() as tmpdir:
                with pytest.raises(FileNotFoundError):
                    downloader.download_audio("http://yt", Path(tmpdir))

# Test success path
@patch('summarize_yt.pipeline.downloader.subprocess.run')
def test_downloader_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
    # Provide minimal video_metadata for filename
    video_metadata = {'id': 'testid'}
    with patch('pathlib.Path.exists', return_value=True):
        audio_file, temp_dir, meta = downloader.download_audio('video_url', output_dir=Path('/tmp'), video_metadata=video_metadata)
        assert meta['id'] == 'testid'

# Test stderr handling
@patch('summarize_yt.pipeline.downloader.subprocess.run')
def test_downloader_stderr(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', stderr=b'yt-dlp error')
    video_metadata = {'id': 'testid'}
    with pytest.raises(RuntimeError):
        downloader.download_audio('video_url', output_dir=Path('/tmp'), video_metadata=video_metadata)

# Test FileNotFoundError
@patch('summarize_yt.pipeline.downloader.subprocess.run')
def test_downloader_file_not_found(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
    video_metadata = {'id': 'testid'}
    with patch('pathlib.Path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            downloader.download_audio('video_url', output_dir=Path('/tmp'), video_metadata=video_metadata)

# Test JSON parsing error
@patch('summarize_yt.pipeline.downloader.subprocess.run')
def test_downloader_json_error(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout='not json', stderr='')
    with pytest.raises(RuntimeError, match='Failed to parse yt-dlp JSON output.'):
        downloader.extract_video_metadata('video_url') 