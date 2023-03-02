from datetime import datetime, timedelta
from textwrap import dedent
import os
from airflow.contrib.operators.file_to_gcs import FileToGoogleCloudStorageOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow import DAG
from airflow.operators.bash import BashOperator

url_sufix = "/yellow_tripdata_2022-{{ execution_date.strftime('%m') }}.parquet"
url_prefix = "https://d37ci6vzurychx.cloudfront.net/trip-data"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow")

url = url_prefix + url_sufix

with DAG(
    "ingest",

    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },

    description="A simple tutorial DAG",
    schedule=timedelta(days=30),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    t1 = BashOperator(
        task_id="wget",
        bash_command=f"curl -sSl {url} > {path_to_local_home}/output.parquet",
    )

    t2 = FileToGoogleCloudStorageOperator(
        task_id="LocalToGCS1",
        src=f"{path_to_local_home}/output.parquet",
        dst="data/dataset_tempe.parquet",
        bucket="dtc_data_lake_allspark-377318",
    )


    t3 = GCSToBigQueryOperator(
        task_id="GCS_to_BigQuery",
        bucket="dtc_data_lake_allspark-377318",
        source_objects=["data/dataset_tempe.parquet"],
        destination_project_dataset_table="allspark-377318:raw_data.trip_data",
        write_disposition="WRITE_TRUNCATE",
        source_format="PARQUET",
        allow_quoted_newlines=True,
        skip_leading_rows=1,
        schema_fields=[
            {"name": "VendorID", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tpep_pickup_datetime", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "tpep_dropoff_datetime", "type": "TIMESTAMP", "mode": "NULLABLE"},
        ],
    )

    t1 >> t2 >> t3
