import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from shared.taskManager import TaskManager
from shared.logger import logging
from shared.newsapi import request_articles, is_valid_download
from shared.gcpWrapper import Storage


def download_articles():
    tm = TaskManager()
    gcs = Storage()
    tasks = tm.generate_tasks()

    for task in tasks:
        if gcs.check_if_exists(task.blob_name):
            logging.info(
                f"Skipping articles from {task.from_date} to {task.to_date}, already downloaded"
            )
            continue

        logging.info(
            f"Downloading articles from {task.from_date} to {task.to_date}"
        )
        articles = request_articles(task.from_date, task.to_date, "Commerzbank")
        
        if is_valid_download(articles):
            logging.info(
                f"Saving articles from {task.from_date} to {task.to_date}"
            )
            gcs.upload_articles(task.blob_name, articles.text)
        else:
            logging.error("Not valid articles request")
            logging.error(articles.text)


if __name__ == "__main__":
    try:
        download_articles()
    except Exception as e:
        logging.error(e, exc_info=True)
        sys.exit(1)
