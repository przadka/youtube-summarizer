import os
import pytest
from summarize_yt.pipeline import downloader

pytestmark = pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"),
    reason="Set RUN_INTEGRATION_TESTS=1 to run integration tests (requires network and yt-dlp)"
)

def test_download_and_metadata_real():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example video
    audio_file, temp_dir, video_metadata = downloader.download_audio(url)
    assert audio_file.exists()
    meta = downloader.extract_video_metadata(url)
    assert meta["title"]
    assert meta["id"] 