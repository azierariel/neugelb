import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from shared.logger import logging
from shared.newsapi import request_sources, is_valid_download
from shared.taskManager import NewsApiSourceTask
from shared.gcpWrapper import Storage

def download_sources():
    logging.info("Downloading sources")
    gcs = Storage()
    task = NewsApiSourceTask()
    sources = request_sources()
    if is_valid_download(sources):
        logging.info("Writing sources to file")
        gcs.upload_sources(task.blob_name, sources.text)
    else:
        logging.error("Not valid sources request")
        logging.error(sources.text)
        raise Exception("Not valid sources request")

if __name__ == "__main__":
    try:
        download_sources()
    except Exception as e:
        logging.error(e, exc_info=True)
        sys.exit(1)