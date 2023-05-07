import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from shared.newsapi import is_valid_import
from pipelines.articles_import import process_articles
from pipelines.sources_import import process_sources


def load_sample(filename):
    with open(os.path.join(os.path.dirname(__file__), f"samples/{filename}")) as f:
        return f.read()


def test_detect_valid_import():
    valid_download = load_sample("valid_articles_request.json")
    assert is_valid_import(valid_download) == True


def test_detect_invalid_import():
    invalid_download = load_sample("invalid_articles_request.json")
    assert is_valid_import(invalid_download) == False


def test_process_articles():
    valid_download = load_sample("valid_articles_request.json")
    df = process_articles(valid_download)
    assert df[df["source_id"].isnull()].shape[0] == 0
    for col in df.columns:
        assert col in [
            "source_id",
            "source_name",
            "article_author",
            "article_title",
            "article_description",
            "article_url",
            "article_url_to_image",
            "article_published_at",
            "article_content",
        ]


def test_process_sources():
    valid_download = load_sample("valid_sources_request.json")
    df = process_sources(valid_download)
    for col in df.columns:
        assert col in [
            "source_id",
            "source_name",
            "source_description",
            "source_url",
            "source_category",
            "source_language",
            "source_country",
        ]
