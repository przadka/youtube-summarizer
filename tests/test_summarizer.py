import pytest
from unittest.mock import patch
from summarize_yt.pipeline import summarizer

# Example: test successful summarization
@patch('litellm.completion')
def test_summarize_success(mock_completion):
    mock_completion.return_value = {"choices": [{"message": {"content": "summary"}}]}
    result = summarizer.summarize_transcript('transcript', 'gpt-3.5-turbo', {'title': 'Test', 'duration_string': '', 'channel': '', 'webpage_url': '', 'upload_date': '', 'uploader': ''}, {'bucket': 'GOOD'})
    assert result == 'summary'

# Example: test LiteLLM API error
@patch('litellm.completion')
def test_summarize_litellm_error(mock_completion):
    mock_completion.side_effect = Exception('API error')
    with pytest.raises(Exception):
        summarizer.summarize_transcript('transcript', 'gpt-3.5-turbo', {'title': 'Test', 'duration_string': '', 'channel': '', 'webpage_url': '', 'upload_date': '', 'uploader': ''}, {'bucket': 'GOOD'})

# Example: test empty transcript
@patch('litellm.completion')
def test_summarize_empty_transcript(mock_completion):
    mock_completion.return_value = {"choices": [{"message": {"content": ""}}]}
    result = summarizer.summarize_transcript('', 'gpt-3.5-turbo', {'title': 'Test', 'duration_string': '', 'channel': '', 'webpage_url': '', 'upload_date': '', 'uploader': ''}, {'bucket': 'GOOD'})
    assert result == '' 