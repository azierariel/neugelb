NewsAPI Data Pipeline
======

This repository contains a data pipeline that collects data from NewsAPI and loads it into BigQuery. It includes scripts to download data and store it in GCP buckets, as well as scripts to transform it and import the data into BigQuery.

## Requirements

Before using this pipeline, ensure that you have the following software installed on your local computer:

- Docker and Docker Compose
- Git

Additionally, you will need a GCP service account with the following permissions:

- BigQuery: BigQuery Admin (roles/bigquery.admin)
- Cloud Storage: Storage Object Admin (roles/storage.objectAdmin)

## Setting up the Environment

### Creating the Service Account

To create a GCP service account, follow these steps:

1. Navigate to [IAM & Admin > Service Account](https://console.cloud.google.com/iam-admin/serviceaccounts) in your GCP console.
2. Click on the `CREATE SERVICE ACCOUNT` button.
3. Enter a name for your service account and grant it the BigQuery Admin and Storage Object Admin roles.
4. Create keys in JSON format. The key will automatically be downloaded to your computer.

![How to create a Service Account](https://storage.googleapis.com/gif-for-test/Peek%202023-05-08%2022-25.gif)

### Creating the Buckets

To create the required GCP buckets, follow these steps:

1. Navigate to [Cloud Storage > Buckets](https://console.cloud.google.com/storage/browser)  in your GCP console.
2. Click on `CREATE` to create a new bucket.
3. Create four buckets - one for each source (articles or sources) and one for downloads and archives for each source. Repeat the process for each bucket. For example, you could create the following buckets:
    - newsapi-articles
    - newsapi-articles-archive
    - newsapi-sources
    - newsapi-sources-archive

Note that bucket names must be unique across GCP, so you may need to choose different names than those listed above.

![How to create a bucket](https://storage.googleapis.com/gif-for-test/Peek%202023-05-08%2022-42.gif)

### Preparing the Local Files

To prepare your local files, follow these steps:

1. Clone this repository to your local machine using `git clone https://github.com/azierariel/neugelb`.
2. Copy the service account file (created previously) into the root folder of the repository.
3. Rename the service account file to `newsapi-sa.json`.
4. Update the environment variables in the `.env.prod` file (you can copy from `.env.sample`). Replace the sample values with the names of the buckets you created and your NewsAPI key.

```
SERVICE_ACCOUNT_FILE_PATH='/app/newsapi-sa.json'
ARTICLES_ARCHIVE_BUCKET_NAME='newsapi-articles-archive'
ARTICLES_DOWNLOAD_BUCKET_NAME='newsapi-articles'
SOURCES_DOWNLOAD_BUCKET_NAME='newsapi-sources'
SOURCES_ARCHIVE_BUCKET_NAME='newsapi-sources-archive'
NEWS_API_KEY="<newsapi key here>"
```

## Running the Data Pipeline

### Building the Docker Image

To build the Docker image, navigate to the root folder of the repository and run the following command:

    docker build . --tag newsapi-pipeline


## Running the Pipelines

To run the different steps of the pipeline, use the services defined in the docker-compose.yml file. Note that you must run the download step before the import step for each source.

    docker-compose up articles-download
    docker-compose up articles-import
    docker-compose up sources-download
    docker-compose up sources-import

## Run Tests

You can also run tests on the pipeline by running:

    docker run --entrypoint pytest newsapi-pipeline -v

## Join Tables

After running the pipelines, you will find a new dataset `commerzbank_articles` in your Data Warehouse (DW) with two new tables: `newsapi_articles` and `newsapi_sources`. To join these tables, you can use the following query:

    SELECT
        *
    FROM
        commerzbank_articles.newsapi_articles articles
        LEFT JOIN `commerzbank_articles.newsapi_sources` sources ON articles.source_id = sources.source_id;

This will select all the columns from both tables and joins them based on the `source_id` column. You can modify the query as needed to select specific columns or filter the results.