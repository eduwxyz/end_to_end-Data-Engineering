# Configurando o Google Cloud

Como já foi mencionado, existem diversas nuvens que poderiamos utilizar nesse projeto, porém hoje utilizaremos o Google Cloud. Para isso, precisamos criar uma conta no Google Cloud, para isso, basta acessar o [site](https://cloud.google.com/) e criar uma conta.

A Google possui um plano gratuito de 300 dólares por 90 meses. É esse plano que iremos utilizar nesse projeto.

## Criando um projeto no Google Cloud

Após criar sua conta, você será redirecionado para a página inicial do Google Cloud. Nessa página, você verá uma lista de projetos, caso você não tenha nenhum projeto, você verá uma mensagem dizendo que você não possui nenhum projeto.

Para criar um projeto, basta clicar no botão `Criar projeto`.

Acesse a [documentação](https://developers.google.com/workspace/guides/create-project?hl=pt-br) do Google Cloud para mais informações sobre como criar um projeto.

## Criando sua conta de serviço

Agora que já temos um projeto, precisamos criar algumas contas de serviço, são elas que nos permitiram utilizar o airflow, terraform e dbt no nosso projeto. Precisamos dar permissão para essas contas de serviço acessarem os recursos do nosso projeto para criarmos tudo de forma automatizada.

Para saber como criar suas contas de serviço (service-account), acesse a [documentação](https://cloud.google.com/iam/docs/service-accounts-create#iam-service-accounts-create-console) do Google Cloud.

Você precisa criar 2 contas de serviço, uma para o terraform e airflow, e outra para o dbt. As permissões que precisamos pra cada uma são:

1. Terraform e Airflow: `Storage Admin` e `BigQuery Admin`
2. DBT: `BigQuery Admin`

## Gerando chaves de acesso

Após criar suas contas de serviço, precisamos gerar as chaves de acesso para que possamos utilizar essas contas de serviço no nosso projeto. Para gerar as chaves de acesso, acesse a [documentação](https://cloud.google.com/iam/docs/creating-managing-service-account-keys?hl=pt-br) do Google Cloud.

Agora que já temos as nossas contas de serviço, e chaves de cada conta, vamos dar continuidade ao nosso projeto.
