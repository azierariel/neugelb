FROM python:3.9


WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --upgrade

COPY commerzbank_articles .

RUN chmod +x /app/main.sh

ENTRYPOINT ["/app/main.sh"]