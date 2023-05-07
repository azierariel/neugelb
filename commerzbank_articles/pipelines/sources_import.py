import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from shared.logger import logging
from shared.gcpWrapper import Storage, BigQuery
from shared.newsapi import is_valid_import
import pandas as pd
import json


def process_sources(content: str) -> pd.DataFrame:
    sources = json.loads(content).get("sources", [])
    df = pd.json_normalize(sources)

    if df.shape[0] == 0:
        raise Exception("No articles found")

    df.rename(
        columns={
            "id": "source_id",
            "name": "source_name",
            "description": "source_description",
            "url": "source_url",
            "category": "source_category",
            "language": "source_language",
            "country": "source_country"
        },
        inplace=True,
    )
    return df


def import_sources():
    gcs = Storage()
    bigquery = BigQuery()
    blobs = gcs.list_sources_to_process()

    for blob in blobs:
        content = blob.download_as_string()
        if is_valid_import(content):
            try:
                df = process_sources(content)
                logging.info(f"Importing {len(df)} sources from {blob.name}")
                bigquery.import_sources(df)
                logging.info(f"Moving {blob.name} to archive")
                gcs.move_blob_to_archive(blob, 'sources')
            except Exception as e:
                logging.error(f"Error importing {blob.name}")
                logging.error(e, exc_info=True)
                continue

        else:
            logging.error(f"Not possible to parse {blob.name}")


if __name__ == "__main__":
    try:
        import_sources()
    except Exception as e:
        logging.error(e, exc_info=True)
        sys.exit(1)
