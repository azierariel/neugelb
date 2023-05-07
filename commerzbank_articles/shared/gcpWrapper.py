import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from settings.tables_schemas import ARTICLES_TABLE_SCHEMA, SOURCES_TABLE_SCHEMA
from pandas import DataFrame
from google.cloud import storage
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.cloud.storage.blob import Blob


class BigQuery:
    def __init__(self):
        self.client = bigquery.Client.from_service_account_json(
            os.environ["SERVICE_ACCOUNT_FILE_PATH"]
        )
        self.dataset_id = "commerzbank_articles"
        self.articles_table_id = (
            f"{self.client.project}.{self.dataset_id}.newsapi_articles"
        )
        self.sources_table_id = (
            f"{self.client.project}.{self.dataset_id}.newsapi_sources"
        )

        self.articles_table_schema = ARTICLES_TABLE_SCHEMA
        self.sources_table_schema = SOURCES_TABLE_SCHEMA
        self.init_tables()

    def init_tables(self):
        # init dataset if not exist
        try:
            self.client.get_dataset(self.dataset_id)
        except NotFound:
            self.client.create_dataset("commerzbank_articles")

        # init articles table if not exist
        try:
            self.client.get_table(self.articles_table_id)
        except NotFound:
            table = bigquery.Table(
                self.articles_table_id, schema=self.articles_table_schema
            )
            table = self.client.create_table(table)

        # init sources table if not exist
        try:
            self.client.get_table(self.sources_table_id)
        except NotFound:
            table = bigquery.Table(
                self.sources_table_id, schema=self.sources_table_schema
            )
            table = self.client.create_table(table)

    def import_articles(self, data: DataFrame):
        """Append dataframe with articles to articles table"""

        job_config = bigquery.LoadJobConfig(
            schema=self.articles_table_schema,
            write_disposition="WRITE_APPEND",
        )

        job = self.client.load_table_from_dataframe(
            data, self.articles_table_id, job_config=job_config
        )
        return job.result()

    def import_sources(self, data: DataFrame):
        """Recreate sources table from dataframe"""

        job_config = bigquery.LoadJobConfig(
            schema=self.sources_table_schema,
            write_disposition="WRITE_TRUNCATE",
        )

        job = self.client.load_table_from_dataframe(
            data, self.sources_table_id, job_config=job_config
        )
        return job.result()

    def query(self, query: str) -> list:
        query_job = self.client.query(query)
        results = query_job.result()
        return results


class Storage:
    def __init__(self):
        self.client = storage.Client.from_service_account_json(
            os.environ["SERVICE_ACCOUNT_FILE_PATH"]
        )
        self.articles_download_bucket = storage.Bucket(
            self.client, os.environ["ARTICLES_DOWNLOAD_BUCKET_NAME"]
        )
        self.articles_archive_bucket = storage.Bucket(
            self.client, os.environ["ARTICLES_ARCHIVE_BUCKET_NAME"]
        )
        self.sources_download_bucket = storage.Bucket(
            self.client, os.environ["SOURCES_DOWNLOAD_BUCKET_NAME"]
        )
        self.sources_archive_bucket = storage.Bucket(
            self.client, os.environ["SOURCES_ARCHIVE_BUCKET_NAME"]
        )

    def upload_articles(self, blob_name: str, data: str):
        self.articles_download_bucket.blob(blob_name).upload_from_string(data)

    def upload_sources(self, blob_name: str, data: str):
        self.sources_download_bucket.blob(blob_name).upload_from_string(data)

    def list_articles_to_process(self):
        blobs = self.articles_download_bucket.list_blobs()
        return blobs

    def list_sources_to_process(self):
        blobs = self.sources_download_bucket.list_blobs()
        return blobs

    def move_blob_to_archive(self, blob: Blob, blob_type: str):
        if blob_type == "articles":
            self.articles_download_bucket.copy_blob(blob, self.articles_archive_bucket)
        elif blob_type == "sources":
            self.sources_download_bucket.copy_blob(blob, self.sources_archive_bucket)
        else:
            raise Exception("Invalid blob type")

        blob.delete()

    def check_if_exists(self, blob_name: str) -> bool:
        if self.articles_archive_bucket.blob(blob_name).exists():
            return True
        elif self.articles_download_bucket.blob(blob_name).exists():
            return True

        return False
