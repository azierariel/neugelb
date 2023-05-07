import os
from .logger import logging
from datetime import datetime, timedelta

class NewsApiArticleTask:
    def __init__(self, from_date: str, to_date: str) -> None:
        self.from_date = from_date
        self.to_date = to_date
        self.blob_name = f"newsapi-articles-{self.from_date}-{self.to_date}.json"

class NewsApiSourceTask:
    def __init__(self) -> None:
        self.blob_name = f"newsapi-sources-{datetime.now().strftime('%Y-%m-%d')}.json"

class TaskManager:
    def __init__(self) -> None:
        self.from_date = os.environ.get(
            "FROM_DATE", (datetime.now() - timedelta(days=29)).strftime("%Y-%m-%d")
        )  # YYYY-MM-DD
        self.to_date = os.environ.get(
            "TO_DATE", datetime.now().strftime("%Y-%m-%d")
        )  # YYYY-MM-DD

    def _generate_dateslist(self, from_date: str, to_date: str) -> list:
        logging.info(f"Generating dates from {from_date} to {to_date}")
        dates = []
        date = datetime.strptime(from_date, "%Y-%m-%d")
        while date <= datetime.strptime(to_date, "%Y-%m-%d"):
            dates.append(date.strftime("%Y-%m-%d"))
            date += timedelta(days=1)
        return dates

    def _generate_tasks_from_date(self, dates: list):
        tasks = []
        for date in dates:
            current_date = datetime.strptime(date, "%Y-%m-%d")
            previous_date = current_date - timedelta(days=1)
            tasks.append(NewsApiArticleTask(previous_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d")))

        return tasks

    def generate_tasks(self) -> list:
        dates = self._generate_dateslist(self.from_date, self.to_date)
        return self._generate_tasks_from_date(dates)
