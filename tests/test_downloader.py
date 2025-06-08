import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pipeline.downloader as downloader
import tempfile

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
    with patch('pipeline.downloader.extract_video_metadata') as mock_meta:
        mock_meta.return_value = {"id": "notfound"}
        with patch('subprocess.run'):
            with tempfile.TemporaryDirectory() as tmpdir:
                with pytest.raises(FileNotFoundError):
                    downloader.download_audio("http://yt", Path(tmpdir)) 