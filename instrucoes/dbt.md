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
