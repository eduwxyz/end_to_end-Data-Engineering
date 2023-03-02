# Dbt

# Sobre o dbt

dbt (data build tool) é uma ferramenta de transformação que fica no topo do nosso data warehouse. Com o dbt podemos fazer transformações de dados de forma estruturada e automatizada. O dbt fornece uma conta gratuita para desenvolvimento e testes.

# Setup

Existem 2 formas de configurar o dbt para o seu projeto:

1. Utilizando o dbt Cloud
2. Utilizando o dbt por via de linha de comando

Neste tutorial vamos utilizar o dbt por via de linha de comando.

## Instalação

Como vamos utilizar o dbt com o bigquery, vamos utilizar o dbt-bigquery. Para isso, dentro da raiz do projeto, execute o seguinte comando:

```bash
poetry add dbt-bigquery
```

## Configuração

Com o dbt-bigquery instalado, basta agora iniciarmos um projeto dbt, para isso, execute o seguinte comando:

```bash
dbt init [nome-do-projeto]
```

Ao executar o comando, você precisará informar o seu project_id, e fazer autenticar com o bigquery.

Após executar o comando, será criado uma pasta com o nome do projeto que você passou como parâmetro. Dentro dessa pasta, você irá encontrar os seguintes arquivos:

- `dbt_project.yml`: Arquivo de configuração do projeto
- `profiles.yml`: Arquivo de configuração do bigquery
- `README.md`: Arquivo de documentação do projeto
- `schema.yml`: Arquivo de configuração do schema do projeto
- `models`: Pasta onde ficam os arquivos de transformação
- `seed`: Pasta onde ficam os arquivos de seed
- `analysis`: Pasta onde ficam os arquivos de análise
- `macros`: Pasta onde ficam os arquivos de macros
- `snapshots`: Pasta onde ficam os arquivos de snapshots
- `tests`: Pasta onde ficam os arquivos de testes

Para entender um pouco mais sobre a estrutura do dbt, você pode acessar a documentação oficial do dbt [aqui](https://docs.getdbt.com/docs/building-a-dbt-project/building-models).

## Criando nossa transformação dbt

Apague tudo que foi criado automaticamente dentro da pasta `models` e crie uma nova pasta dentro de `models` com o nome `staging`. Dentro dessa pasta construiremos nosso primeiro modelo.

Crie agora um arquivo chamado `schema.yml` dentro da pasta `models/staging` e adicione o seguinte conteúdo:

```yml
version: 2

sources:
  - name: raw_data #nome do dataset no bigquery

    tables:
      - name: trips_yellow #nome da tabela no bigquery
```

Sempre para criar uma nova tabela no dbt, precisamos definir a origem desses dados. Nossos dados estão no dataset `raw_data` e as tabelas é a trips_yellow. Lembrando que isso foi definido nos arquivos terraform e na nossa dag do airflow, respectivamente.

Agora que já definimos a fonte do nosso modelo, vamos finalmente criar ele. Ainda dentro da pasta staging, crie um arquivo chamado `stg_yellow_data.sql` os seguintes conteúdos:

Para o dbt, primeiro precisamos definir o tipo de materialização do nosso modelo, para o nosso caso materializamos nossa tabela como uma view. Para isso, no nosso arquivo criado escreva:

```sql
{{ config(materialized='view') }}
```

Agora vamos de fato efetuar as transformações. As transformações que vamos fazer são:

1. Remover os dados onde o `vendorid` é nulo
2. Criar a nossa chave primária

Continuando nosso código, aplique o seguinte código:

```sql
with tripdata as
(
  select *,
    row_number() over(partition by vendorid, tpep_pickup_datetime) as rn
  from {{ source('raw_data','trips_yellow') }}
  where vendorid is not null )
```

E agora por fim vamos construir a nossa chave primária, para isso vou utilizar uma macro do próprio dbt, que é a `dbt_utils.surrogate_key`. Para isso, vamos adicionar o seguinte código:

```sql
select
    {{ dbt_utils.surrogate_key(['vendorid', 'tpep_pickup_datetime', 'rn']) }} as id,
    tpep_pickup_datetime as pickup_datetime,
    tpep_dropoff_datetime as dropoff_datetime,
from tripdata
```

Para o código funcionar, como estamos utilizando uma macro do dbt, precisamos importar o pacote `dbt_utils` no nosso projeto. Para isso, criar o arquivo `packages.yml` na raiz do projeto e adicionar o seguinte conteúdo:

```yml
packages:
  - package: dbt-labs/dbt_utils
    version: 0.8.0
```

E agora tudo está pronto para executarmos o nosso modelo, para isso, execute o seguinte comando:

```bash
dbt run
```

Se der tudo certo, você verá que o dbt criou uma view no bigquery com o nome `stg_yellow_data`. Para verificar, acesse o bigquery e verifique se a view foi criada.

![dbt view](/imagens/modelo.png)

Deixo como atividade, se você extraiu os dados tbm da tabela `trips_green`, crie um modelo para essa tabela também.

## Importante

O dbt é uma ferramenta muito poderosa, e com ela podemos fazer muitas coisas, como por exemplo, criar um modelo de dados de forma automatizada, criar testes automatizados, criar documentação automatizada, criar snapshots, entre outras coisas. Nesse repositório, não iremos abordar todas essas coisas, mas caso você queira aprender mais sobre o dbt, recomendo que você acesse a documentação oficial do dbt [aqui](https://docs.getdbt.com/docs/building-a-dbt-project/building-models).
