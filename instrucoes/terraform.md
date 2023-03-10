# Sobre o terraform

O Terraform é uma ferramenta de código aberto usada para criar e gerenciar recursos de infraestrutura de forma automatizada. Com o Terraform, você pode descrever sua infraestrutura como código, o que significa que suas configurações de infraestrutura são armazenadas em arquivos de texto que podem ser versionados, compartilhados e auditados.

Com o Terraform, você pode criar e gerenciar recursos em diversos provedores de nuvem (como AWS, Azure, Google Cloud Platform, entre outros), bem como em infraestrutura local (como servidores físicos ou virtuais). O Terraform suporta diversos tipos de recursos, como instâncias EC2, grupos de segurança, Buckets S3, máquinas virtuais, redes virtuais, etc.

Ao usar o Terraform, você define sua infraestrutura como código usando a sintaxe do HCL (HashiCorp Configuration Language). Esses arquivos de configuração descrevem todos os recursos necessários para a infraestrutura desejada, incluindo seus relacionamentos e dependências. Com essas informações, o Terraform cria um plano de execução que mostra quais recursos serão criados, modificados ou excluídos.

O Terraform é capaz de gerenciar recursos de forma segura e consistente, garantindo que todos os recursos sejam criados com as mesmas configurações e que a infraestrutura seja mantida em um estado previsível. Além disso, o Terraform permite que você compartilhe e reutilize módulos de infraestrutura, o que ajuda a acelerar o desenvolvimento e a manutenção da infraestrutura.

Em resumo, o Terraform é uma ferramenta poderosa para criar e gerenciar infraestrutura de forma automatizada, consistente e segura, ajudando a acelerar a entrega de serviços e aplicações.

# Instalação

Para fazer a instalação do terraform , acesse a própria [documentação](https://developer.hashicorp.com/terraform/downloads) e siga o passo a passo de acordo com seu sistema operacional.

# Configuração

Dentro do projeto que criamos na etapa anterior utilizando o poetry, vamos criar um arquivo chamado `main.tf` na raiz do projeto. Esse arquivo é responsável por conter todas as configurações do terraform.

`touch tf`

Como nós iremos transferir nossos para o gcs e posteriormente para o bigquery, precisamos de 2 `resources`, que é o que o terraform irá criar. No nosso caso, iremos criar um `resource` do tipo `google_storage_bucket` e outro do tipo `google_bigquery_dataset`.

Dentro do arquivo `main.tf` vamos adicionar o seguinte código:

```hcl
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {

  project = var.project
  region  = var.region
  zone    = var.zone
}


resource "google_storage_bucket" "data-lake-bucket" {
  name     = "${local.data_lake_bucket}_${var.project}" # Concatenating DL bucket & Project name for unique naming
  location = var.region

  # Optional, but recommended settings:
  storage_class               = var.storage_class
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.BQ_DATASET
  project    = var.project
  location   = var.region
}

```

Para entender mais a fundo sobre o que cada trecho desse código faz, acesse a [documentação](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started) do terraform.

# Variáveis

Para que o terraform possa criar o nosso dataset, precisamos passar algumas informações para ele. Essas informações são chamadas de variáveis e são definidas no arquivo `variables.tf`.

`touch variables.tf`

Dentro do arquivo `variables.tf` vamos adicionar o seguinte código:

```
variable "project" {}

variable "credentials_file" {}

variable "region" {
  default = "US"
}

variable "zone" {
  default = "US"
}


variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}



variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "raw_data" #nome do nosso dataset
}


locals {
  data_lake_bucket = "dtc_data_lake" #nome do nosso bucket
}

```

# Terraform init

Para que o terraform possa criar o nosso dataset e nosso bucket, precisamos inicializar o terraform. Para isso, vamos rodar o comando `terraform init` na raiz do nosso projeto.

```
terraform init
```

# Terraform plan

Agora vamos criar um plano de execução. Para isso, vamos rodar o comando `terraform plan`, passando o argumento -var="project=<project-id>" para que o terraform saiba qual projeto ele deve criar o dataset e o bucket.

```
terraform plan -var="project=allspark-377318"
```

# Terraform apply

Agora vamos aplicar o plano de execução. Para isso, vamos rodar o comando `terraform apply`, passando o argumento -var="project=<project-id>".

```
terraform apply -var="project=<project-id>"
```

# Configuração do terraform concluida

E é isso que precisamos de configuração do terraform neste projeto, se tudo ocorreu bem, no seu ambiente do bigquery você deve ver um dataset chamado `raw_data` e no gcs (google cloud storage) um bucket chamado `dtc_data_lake`.

Imagem do bucket no gcs

![bucket](/imagens/gcs-print.png)

Imagem do dataset no bigquery
![raw_data](/imagens/bigquery.png)
