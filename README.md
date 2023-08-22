# Projeto de Teste para Hilab

Teste para a posição de Desenvolvedor Python na Hilab - Ago 2023.

Há dois projetos, uma aplicação CRUD usando Flask + Docker, e um script python
de modelagem e processamento de dados.

## Descrição

Este repositório contém dois programas em diferentes pastas, cada um com um propósito específico, como parte de um teste no processo de seleção da Hilab. O primeiro programa consome uma API de notificações de síndrome gripal do governo e insere os dados em um banco de dados local. O segundo programa cria uma API CRUD utilizando a framework Flask. Abaixo estão as instruções para executar ambos os programas.

## Requisitos

- Python 3.11.4 ou superior
- PostgreSQL instalado e configurado
- Docker

## Notificações de Gripe no Paraná (Desafio de Modelagem e Processamento de Dados):

O programa "notificacoes_gripe.py" na pasta "notificacoes_sindrome_gripal" consome a API de notificações de síndrome gripal do governo e insere os dados em um banco de dados PostgreSQL local. Após clonar o repositório localmente, siga estas etapas para executar o programa:
1. Clone o repositório localmente no diretório de sua escolha:
    ```bash
    git clone https://github.com/ericmidt/teste-hilab.git
    ```

2. No diretório "notificacoes_sindrome_gripal", instale as dependências utilizando o seguinte comando:

    ```bash
    pip install -r requirements.txt
    ```

3. Defina suas environment variables usando os seguintes comandos no seu terminal:

    Linux / macOS (Bash or Terminal):
    ```bash
    export DB_NAME="your_db_name"
    export DB_USER="your_user"
    export DB_PASSWORD="your_password"
    export DB_HOST="localhost"
    export DB_PORT="your_port"
    ```
    Windows PowerShell:
    ```bash 
    $env:DB_NAME="your_db_name"
    $env:DB_USER="your_user"
    $env:DB_PASSWORD="your_password"
    $env:DB_HOST="localhost"
    $env:DB_PORT="your_port"
    ```

    Windows Command Prompt:
    ```bash
    set DB_NAME=your_db_name
    set DB_USER=your_user
    set DB_PASSWORD=your_password
    set DB_HOST=localhost
    set DB_PORT=your_port
    ```

    Exemplo:
    ```bash
    set DB_NAME=postgres
    set DB_USER=postgres
    set DB_PASSWORD=senha
    set DB_HOST=localhost
    set DB_PORT=5432
    ```

4. Execute o programa com o seguinte comando:

    ```bash
    python notificacoes_gripe.py
    ```

### Testes
Abra o programa pgAdmin4, e clique com o botão direito na seção "Tables" e clique em "Refresh".
Você deve ver uma nova tabela chamada "notificacoes_sindrome_gripal_parana". Clique com botão direito na seção
"Tables", clique em "Query Tool". Em seguida você pode realizar uma query para
verificar os dados que foram salvos, como por exemplo:
```sql
SELECT * FROM notificacoes_sindrome_gripal_parana
```

## Flask CRUD API (Desafio Aplicação CRUD + Docker):

A pasta "flask_crud_api" contém o código de uma API CRUD utilizando o framework Flask que salva e manipula dados em um banco de dados PostgreSQL local. O programa "flask_app.py" implementa operações de criação, leitura, atualização e exclusão de pacientes com sintomas de gripe. 

O código está disponível para análise, mas para executar o container recomendo puxar a imagem do container do [repositório no Docker Hub](https://hub.docker.com/r/ericmidt/flask_crud_api).

Para executar o container, siga estas etapas:
1. Certifique-se de ter o Docker instalado.

2. Execute o aplicativo Docker Desktop.

3. No diretório de sua escolha, puxe a imagem do container:
    ```bash
    docker pull ericmidt/flask_crud_api
    ```
    Caso haja algum problema ao executar o comando, entre na sua conta Docker Hub no terminal e tente novamente.

4. Execute o seguinte comando (não se esqueça de substituir as credenciais
com as suas próprias para acessar seu banco local PostgreSQL):
    ```bash
    docker run -e DB_NAME="mydb" -e DB_USER="myuser" -e DB_PASSWORD="mypassword" -e DB_HOST="host.docker.internal" -e DB_PORT="your_db_port" -p 5000:5000 ericmidt/flask_crud_api:latest
    ```
    Exemplo:
    ```bash
    docker run -e DB_NAME="postgres" -e DB_USER="postgres" -e DB_PASSWORD="12345" -e DB_HOST="host.docker.internal" -e DB_PORT="5432" -p 5000:5000 ericmidt/flask_crud_api:latest
    ```
    Geralmente a porta padrão do PostgreSQL é "5432".

    Você deve a seguinte mensagem no seu terminal:
    ```bash
    * Serving Flask app 'flask_app'
    * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5000
    * Running on http://172.17.0.2:5000
    Press CTRL+C to quit
    ```



## Contato:

- Email: erickarlschmidt@gmail.com
- GitHub: ericmidt.github.com
