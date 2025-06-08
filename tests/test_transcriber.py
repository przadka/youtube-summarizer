import pytest
from unittest.mock import patch, MagicMock, mock_open
import pipeline.transcriber as transcriber
import subprocess
from pathlib import Path

# Example: test successful transcription
@patch('pipeline.transcriber.subprocess.run')
def test_transcribe_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
    audio_file = Path('audio.wav')
    with patch.object(Path, 'exists', return_value=True):
        with patch('pathlib.Path.read_text', return_value='transcript'):
            with patch('builtins.open', mock_open(read_data='{"bucket": "GOOD"}')):
                transcript, quality = transcriber.transcribe_with_existing_script(audio_file)
                assert transcript == 'transcript'
                assert quality['bucket'] == 'GOOD'

# Example: test subprocess failure
@patch('pipeline.transcriber.subprocess.run')
def test_transcribe_subprocess_error(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    audio_file = Path('audio.wav')
    with pytest.raises(RuntimeError):
        transcriber.transcribe_with_existing_script(audio_file)

# Example: test missing transcript file
@patch('pipeline.transcriber.subprocess.run')
def test_transcribe_missing_transcript(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')
    audio_file = Path('audio.wav')
    # Patch Path.exists to return False for the transcript file, True otherwise
    def exists_side_effect(self):
        if str(self).endswith('.txt'):
            return False
        return True
    with patch('pathlib.Path.exists', new=exists_side_effect):
        with pytest.raises(FileNotFoundError):
            transcriber.transcribe_with_existing_script(audio_file) 