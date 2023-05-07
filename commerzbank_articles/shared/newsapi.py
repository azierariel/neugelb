import os
import json
from requests import get, Response

API_KEY = os.environ.get("NEWS_API_KEY")

def request_articles(from_date:str, to_date:str, query: str) -> Response:
    url = f"https://newsapi.org/v2/everything?q={query}&from={from_date}&to={to_date}&sortBy=publishedAt&apiKey={API_KEY}"
    response = get(url)
    return response

def request_sources() -> Response:
    url = f"https://newsapi.org/v2/top-headlines/sources?apiKey={API_KEY}"
    response = get(url)
    return response

def is_valid_download(response: Response) -> bool:
    if response.status_code != 200:
        return False
    if response.json()['status'] != 'ok':
        return False
    return True

def is_valid_import(content: str) -> bool:
    try:
        response = json.loads(content)
        if response['status'] != 'ok':
            return False
        return True
    except:
        return False