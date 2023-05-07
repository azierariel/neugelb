import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from shared.logger import logging
from shared.gcpWrapper import Storage, BigQuery
from shared.newsapi import is_valid_import
import pandas as pd
import json


def process_articles(content: str) -> pd.DataFrame:
    articles = json.loads(content).get("articles", [])
    df = pd.json_normalize(articles)

    if df.shape[0] == 0:
        raise Exception("No articles found")

    df.rename(
        columns={
            "source.id": "source_id",
            "source.name": "source_name",
            "urlToImage": "article_url_to_image",
            "publishedAt": "article_published_at",
            "content": "article_content",
            "author": "article_author",
            "title": "article_title",
            "description": "article_description",
            "url": "article_url"
        },
        inplace=True,
    )

    df = df[~df["source_id"].isnull()]
    df['article_published_at'] = pd.to_datetime(df['article_published_at'])

    return df


def import_articles():
    gcs = Storage()
    bigquery = BigQuery()
    blobs = gcs.list_articles_to_process()

    for blob in blobs:
        content = blob.download_as_string()
        if is_valid_import(content):
            try:
                df = process_articles(content)
                logging.info(f"Importing {len(df)} articles from {blob.name}")
                bigquery.import_articles(df)
                logging.info(f"Moving {blob.name} to archive")
                gcs.move_blob_to_archive(blob, 'articles')
            except Exception as e:
                logging.error(f"Error importing {blob.name}")
                logging.error(e, exc_info=True)
                continue

        else:
            logging.error(f"Not possible to parse {blob.name}")


if __name__ == "__main__":
    try:
        import_articles()
    except Exception as e:
        logging.error(e, exc_info=True)
        sys.exit(1)
