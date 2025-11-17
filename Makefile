# create BQ datasets
bq --location=EU mk --dataset $PROJECT_ID:olist_raw
bq --location=EU mk --dataset $PROJECT_ID:olist_dbt
bq --location=EU mk --dataset $PROJECT_ID:olist_snapshots
