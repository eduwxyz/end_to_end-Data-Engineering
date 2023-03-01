#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""
from __future__ import annotations

# [START tutorial]
# [START import_module]
from datetime import datetime, timedelta
from textwrap import dedent

import os
from airflow.contrib.operators.file_to_gcs import FileToGoogleCloudStorageOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)


# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator

# [END import_module]


url_sufix = "/yellow_tripdata_2022-{{ execution_date.strftime('%m') }}.parquet"
url_prefix = "https://d37ci6vzurychx.cloudfront.net/trip-data"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow")


url = url_prefix + url_sufix


# dataset_file = "/yellow_tripdata_{{ macros.ds_add(2015-01-01) }}.parquet"
# dataset_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data"


# [START instantiate_dag]
with DAG(
    "ingest",
    # [START default_args]
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    },
    # [END default_args]
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
    # [END basic_task]

    # [START jinja_template]
    templated_command = dedent(
        """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
    {% endfor %}
    """
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
    # [END jinja_template]

    t1 >> t2 >> t3
# [END tutorial]
