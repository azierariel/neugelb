import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from shared.newsapi import is_valid_download

import json
from unittest.mock import MagicMock
from requests import Response

def load_sample(filename):
    with open(os.path.join(os.path.dirname(__file__), f'samples/{filename}')) as f:
        return f.read()

def mock_response(content, status_code=200):
    response = Response()
    response.status_code = status_code
    response.json = MagicMock(return_value=json.loads(content))
    return response


def test_detect_valid_download():
    valid_download = load_sample('valid_articles_request.json')
    valid_response = mock_response(valid_download)
    assert is_valid_download(valid_response) == True

def test_detect_invalid_download():
    invalid_download = load_sample('invalid_articles_request.json')
    invalid_response = mock_response(invalid_download)
    assert is_valid_download(invalid_response) == False
