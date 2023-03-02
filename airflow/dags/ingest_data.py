from datetime import datetime, timedelta
import os
from airflow.contrib.operators.file_to_gcs import FileToGoogleCloudStorageOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow import DAG
from airflow.operators.bash import BashOperator


PATH_TO_LOCAL_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")

URL_SUFIX_YELLOW = "/yellow_tripdata_2022-{{ execution_date.strftime('%m') }}.parquet"
URL_SUFIX_GREEN = "/green_tripdata_2022-{{ execution_date.strftime('%m') }}.parquet"
URL_PREFIX = "https://d37ci6vzurychx.cloudfront.net/trip-data"

URL_YELLOW = URL_PREFIX + URL_SUFIX_YELLOW
URL_GREEN = URL_PREFIX + URL_SUFIX_GREEN

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
        task_id="wget_yellow_tripdata",
        bash_command=f"curl -sSl {URL_YELLOW} > {PATH_TO_LOCAL_HOME}/output-yellow.parquet",
    )
    
    t2 = BashOperator(
        task_id="wget_green_tripdata",
        bash_command=f"curl -sSl {URL_GREEN} > {PATH_TO_LOCAL_HOME}/output-green.parquet",
    )

    t3 = FileToGoogleCloudStorageOperator(
        task_id="LocalToGCS-yellow",
        src=f"{PATH_TO_LOCAL_HOME}/output-yellow.parquet",
        dst="data/raw_data_yellow.parquet",
        bucket="dtc_data_lake_allspark-377318",
    )
    
    t4 = FileToGoogleCloudStorageOperator(
        task_id="LocalToGCS-green",
        src=f"{PATH_TO_LOCAL_HOME}/output-green.parquet",
        dst="data/raw_data_green.parquet",
        bucket="dtc_data_lake_allspark-377318",
    )


    t5 = GCSToBigQueryOperator(
        task_id="GCS_to_BigQuery-yellow",
        bucket="dtc_data_lake_allspark-377318",
        source_objects=["data/raw_data_yellow.parquet"],
        destination_project_dataset_table="allspark-377318:raw_data.trips_yellow",
        write_disposition="WRITE_TRUNCATE",
        source_format="PARQUET",
        allow_quoted_newlines=True,
        skip_leading_rows=1,
    )
    
    
    t6 = GCSToBigQueryOperator(
        task_id="GCS_to_BigQuery-green",
        bucket="dtc_data_lake_allspark-377318",
        source_objects=["data/raw_data_green.parquet"],
        destination_project_dataset_table="allspark-377318:raw_data.trips_green",
        write_disposition="WRITE_TRUNCATE",
        source_format="PARQUET",
        allow_quoted_newlines=True,
        skip_leading_rows=1,
    )
    

    t1 >> t2 >> [t3, t4] >> t5 >> t6
