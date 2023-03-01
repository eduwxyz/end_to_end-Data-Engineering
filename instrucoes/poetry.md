# Poetry

Quando vamos iniciar um projeto, precisamos escolher alguma ferramenta que gerencie as nossas dependência, uma das ferramentas mais utilizadas atualmente é o [poetry](https://python-poetry.org/), e é ela que utilizaremos aqui.

# Iniciando o projeto

Para iniciar no projeto, primeiramente precisamos fazer o download do poetry, para isso, vamos executar no terminal.

```
curl -sSL https://install.python-poetry.org | python3 -
```

Após instalado, vamos finalmente iniciar o nosso projeto.

```
poetry new [nome_do_projeto]
```

Para instalar todos as bibliotecas presentes no seu pacote, basta escrever o comando.

```
poetry install
```

Neste projeto, vamos trabalhar com diversas bibliotecas diferentes, e sempre que precisarmos instalar uma nova, precisamos pedir ao poetry que adicione isso na nossa lista de dependências, para isto vamos digitar no terminal

```
poetry add nome_da_dependência
```

Para saber mais sobre o poetry, você pode pesquisar em sua própria documentação, ou nesse [artigo](https://medium.com/@eduardo.machado1/poetry-gerenciamento-de-depend%C3%AAncias-em-python-a5fdb8b0510c) que eu mesmo criei!
