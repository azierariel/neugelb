# Data Pipeline Architecture Documentation

This documentation provides an overview of the data pipeline architecture and format for the project. The pipeline is divided into two steps, namely download and import. In the download step, articles and sources are extracted from the newsapi and stored as raw data in cloud storage. In the import step, the raw data is transformed and pushed into the DW bigquery.

## Pipeline Architecture Overview

The pipeline architecture consists of the following steps:

1. Download - Articles and sources are downloaded from the newsapi and stored as raw data in cloud storage.
2. Import - Raw data is validated, transformed and pushed into the DW bigquery.

## Download Steps
### Articles

The download step for articles involves downloading articles from the newsapi using the '`commerzbank`' keyword in the query. Tasks are generated for the last 30 days (max possible to be retrieved by the api) using the class created ad-hoc (see '`shared/taskManager.py`'). The _dates from_ and _dates to_ can be set up using the environment variables '`FROM_DATE`' and '`TO_DATE`', if a specific job needs to be ran.

#### Validations

- The task will be processed only if it does not already exist in any of the working buckets (download and archive).
- Once the requests were performed, a check on the status code is done, and if the '`result`' key is '`ok`' in the response body.

### Sources

The download step for sources involves downloading sources from a single endpoint without any other parameter, and they are extracted and stored into the download bucket.

#### Validations

- Once the requests were performed, a check on the status code is done, and if the '`result`' key is '`ok`' in the response body.

## Import Steps
### Articles

The import step for articles involves listing all the files available in the download bucket, processing them, and moving them to the archive bucket. Once the data is validated and transformed, the new entries are appended to the table in the DW.

#### Validations

- If the JSON is well-formatted (can be parsed).
- Check if the '`result`' key is '`ok`' in the response body.
- Volumetric check if the number of articles in the data is greater than `0`.
- If the source_id column is present in the data.

If the file does not check the validations, the error will be logged, skipped and continue with the next one.

#### Transformations

- All entries without a source id are filtered.
- Column names are improved for better understanding, using the same convention.
- Data types transformations (e.g. string to datetime).

### Sources

The import step for sources involves taking the sources from the download bucket, processing them, and moving them to the archive bucket. Once the data is validated and transformed, the destination table in the DW is recreated using the latest extracted sources.

#### Validations

- If the JSON is well-formatted (can be parsed).
- Check if the '`result`' key is '`ok`' in the response body.
- Volumetric check if the number of articles in the data is greater than 0.

If the file does not check the validations, the error will be logged, skipped and continue with the next one.

#### Transformations

- Column names are improved for better understanding, using the same convention.
