# Terminando projeto

Se você chegou até aqui, parabéns! Você finalizou o projeto! Agora você pode utilizar esse projeto para adicionar no seu portifólio, ou então, utilizar para aprender mais sobre essas ferramentas. Se você encontrou alguma dificuldade no código fornecido, ou algo que mudou, pode entrar em contato comigo e eu atualizo ou melhoro assim que possível.

Como criarmos uma conta com plano gratuito e limitado na Google Cloud, precisamos encerrar os recursos que criamos para não sermos cobrados. Para isso, vamos utilizar o terraform para destruir os recursos que criamos.

## Encerrando recursos

1. Encerre os recursos da GCP executando o seguinte comando no diretório `terraform`:

```
terraform destroy
```

2. Pare e exclua conteineres, exclua volumes de dados, para isso execute o seguinte comando no diretório `airflow`:

```
docker-compose down --volumes --rmi all
```

3. O comando a seguir remove todos os contêineres interrompidos, todas as redes não usadas por pelo menos um contêiner, todas as imagens não utilizadas, todos os volumes e todo o cache de compilação pendente:

```
docker system prune -a --volumes
```

4. Apague sua conta na GCP, para isso, acesse o [console da GCP](https://console.cloud.google.com/), clique no seu nome no canto superior direito, e clique em `Sair`. Após isso, clique em `Excluir conta` e siga as instruções.
