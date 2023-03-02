# Dags

Agora que seu airflow está configurado, vamos criar a dag que irá executar o nosso pipeline.

Ao executar o comando `docker-compose up` o airflow já cria uma pasta chamada `dags` dentro do diretório `airflow` que é o local onde devemos colocar nossas dags.

## Entendendo o que precisamos fazer

Para começar a criar nossa dag, vamos criar um arquivo chamado `ingest_data.py` dentro da pasta `dags`.

Antes de começamos a codar, vamos entender o que precisamos fazer nesse arquivo. Precisamos fazer essas execuções na nossa pipeline:

1. Baixar os dados do site;
2. Fazer o upload dos dados para o GCS
3. Fazer o upload dos dados para o Bigquery

Agora que entendemos o que precisamos fazer, vamos começar a codar.

## Construindo nossa dag

Vamos começar importando as bibliotecas que vamos utilizar:

```python
from datetime import datetime, timedelta
import os
from airflow.contrib.operators.file_to_gcs import FileToGoogleCloudStorageOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from airflow import DAG
from airflow.operators.bash import BashOperator
```

A primeira coisa que precisamos fazer é configurar os paramêtros, para isso vamos criar o seguinte código:

```python
with DAG(
    "ingest", # Nome da dag

    default_args={
        "depends_on_past": False,
        "email": ["airflow@example.com"], # Email que irá receber as notificações
        "email_on_failure": False, # Se quer receber notificação quando a dag falhar
        "email_on_retry": False, # Se quer receber notificação quando a dag for reexecutada
        "retries": 1, # Quantas vezes a dag irá ser reexecutada
        "retry_delay": timedelta(minutes=5), # Tempo entre as reexecuções
    },

    description="Essa dag é responsável por extrair e carregar dados no bigquery", # Descrição da dag
    schedule=timedelta(days=30), # Frequência de execução da dag
    start_date=datetime(2021, 1, 1), # Data de início da dag
    catchup=False, # Se quer executar as tarefas que não foram executadas
    tags=["etl"], # Tags que podem ser utilizadas para filtrar as dags
) as dag:
```

Agora que já temos a dag configurada, vamos criar a nossa primeira tarefa. Essa tarefa será responsável por baixar os dados do site.

```python

    url_sufix = "/yellow_tripdata_2022-{{ execution_date.strftime('%m') }}.parquet" # Sufixo da url que será baixada
    url_prefix = "https://d37ci6vzurychx.cloudfront.net/trip-data" # Prefixo da url que será baixada
    path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow") # Caminho para o diretório onde será salvo o arquivo baixado

    t1 = BashOperator(
        task_id="wget",
        bash_command=f"curl -sSl {url} > {path_to_local_home}/output.parquet",
    )
```

Iremos baixar os dados 2022, para isso vamos utilizar o `execution_date` que é uma variável que o airflow disponibiliza para nós. Essa variável é a data que a dag está sendo executada. Porém como o execution_date retorna o dia atual de execução (2023), queremos extrair apenas o mês para fazer a concatenação com a url.

Agora que já temos a task que faz o download dos dados, vamos criar a tarefa que irá fazer o upload do arquivo para o GCS.

```python
    t2 = FileToGoogleCloudStorageOperator(
        task_id="upload_to_gcs",
        bucket="bucket_name", # Nome do bucket
        src=f"{path_to_local_home}/output.parquet", # Caminho do arquivo que será enviado
        dst="output.parquet", # Nome do arquivo que será enviado
    )
```

Agora que já temos a task que faz o upload do arquivo para o GCS, vamos criar a tarefa que irá fazer o upload do arquivo para o Bigquery.

```python
    t3 = GCSToBigQueryOperator(
        task_id="upload_to_bigquery",
        bucket="bucket_name", # Nome do bucket
        source_objects=["output.parquet"], # Nome do arquivo que será enviado
        destination_project_dataset_table="dataset.table", # Nome do dataset e tabela que será criada
        source_format="PARQUET", # Formato do arquivo que será enviado
        skip_leading_rows=1, # Quantas linhas serão ignoradas
        write_disposition="WRITE_TRUNCATE", # Se quer sobrescrever os dados
        allow_quoted_newlines=True, # Se quer permitir quebra de linha
        schema_fields=[
            {"name": "VendorID", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "tpep_pickup_datetime", "type": "TIMESTAMP", "mode": "NULLABLE"},
            {"name": "tpep_dropoff_datetime", "type": "TIMESTAMP", "mode": "NULLABLE"},
        ],
    )

```

Agora que já temos todas as tasks criadas, vamos definir a ordem de execução das tasks.

```python
    t1 >> t2 >> t3
```

Agora que criamos nossa dag, e definimos a ordem de execução das tasks, vamos executar a dag.

Para isso:

1. acesse o airflow em `http://localhost:8080/` e clique em `DAGs`.
2. Clique em `enable` na dag `ingest`.
3. Clique em `Trigger DAG` e selecione a data que você quer executar a dag.
4. Clique em `Trigger`.
5. Aguarde a execução da dag.

E depois de alguns segundos você conseguirá ver se sua dag foi executada com sucesso. Se você seguiu todo esse tutorial passo a passo, você já deve ter um dataset no bigquery com os dados do site. Abaixo estarão as imagens de como ficou o resultado final.

![airflow-execution](/imagens/airflow-exec.png)

Como deveria ficar o gcs:

![gcs](/imagens/gcs.png)

Como deveria ficar no bigquery:

![bigquery](/imagens/bigquery.png)

## Atenção

Foi ensinado aqui a baixar e fazer o carregamento dos dados da categoria `yellow` do site. Para fazer o carregamento dos dados da categoria `green` é necessário duplicar algumas partes, deixo como exercício para quem deseja fazer. De qualquer forma, o código final está no repositório.
