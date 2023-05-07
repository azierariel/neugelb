from google.cloud import bigquery

ARTICLES_TABLE_SCHEMA= [
    bigquery.SchemaField("article_author", "STRING"),
    bigquery.SchemaField("article_title", "STRING"),
    bigquery.SchemaField("article_url", "STRING"),
    bigquery.SchemaField("article_url_to_image", "STRING"),
    bigquery.SchemaField("article_description", "STRING"),
    bigquery.SchemaField("article_published_at", "DATETIME"),
    bigquery.SchemaField("article_content", "STRING"),
    bigquery.SchemaField("source_id", "STRING"),
    bigquery.SchemaField("source_name", "STRING"),
]

SOURCES_TABLE_SCHEMA = [
    bigquery.SchemaField("source_id", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("source_name", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("source_description", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("source_url", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("source_category", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("source_language", bigquery.enums.SqlTypeNames.STRING),
    bigquery.SchemaField("source_country", bigquery.enums.SqlTypeNames.STRING)
]
