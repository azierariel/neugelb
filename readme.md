
# Build docker image

    docker build . --tag newsapi-pipeline


# Run pipelines

    docker-compose up articles-download

    docker-compose up articles-import

    docker-compose up sources-download

    docker-compose up sources-import

# Run tests

    docker run --entrypoint pytest newsapi-pipeline -v

# Join Tables

    SELECT
        *
    FROM
        commerzbank_articles.newsapi_articles articles
        LEFT JOIN `commerzbank_articles.newsapi_sources` sources ON articles.source_id = sources.source_id;