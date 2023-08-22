import requests
import psycopg2
from datetime import datetime, timedelta
import calendar

class NotificacoesProcessor:

    def __init__(self, db_params):
        # Credenciais para acessar a API
        self.url = "https://elasticsearch-saps.saude.gov.br/desc-esus-notifica-estado-pr/_search"
        self.username = "user-public-notificacoes"
        self.password = "Za4qNXdyQNSa9YaA"
        self.db_params = db_params
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    # Busca e processa os dados
    def fetch_and_processs_data(self,start_date, end_date):
        # Realiza a conexão ao banco de dados
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Cria uma tabela
        cursor.execute("""CREATE TABLE IF NOT EXISTS Notificacoes_sindrome_gripal_parana(
                                id VARCHAR(255),
                                timestamp TIMESTAMP,
                                sexo VARCHAR(255),
                                idade INTEGER,
                                cor VARCHAR(255),
                                sintomas VARCHAR(255),
                                dataInicioSintomas TIMESTAMP,
                                municipio VARCHAR(255),
                                estado VARCHAR(255),
                                dataPrimeiraDose TIMESTAMP,
                                dataSegundaDose TIMESTAMP,
                                dataNotificacao TIMESTAMP,
                                municipioNotificacao VARCHAR(255),
                                estadoNotificacao VARCHAR(255),
                                recebeuAntiviral VARCHAR(255),
                                profissionalSaude VARCHAR(255),
                                profissionalSeguranca VARCHAR(255)
                        );""")

        # Define a data de início para a busca dos dados e a data final. Não há registros antes de 01/11/2022
        start_date = datetime(2022, 11, 1)
        end_date = datetime.now()

        # Itera por cada ano e mês
        current_date = start_date
        while current_date <= end_date:
            # Calcula o último dia de cada mês
            last_day = calendar.monthrange(current_date.year, current_date.month)[1]

            # Define os parâmetros para a busca
            query_params = {
                "q": f"@timestamp:[{current_date.strftime('%Y-%m-%dT00:00:00.000Z')} TO {current_date.replace(day=last_day).strftime('%Y-%m-%dT23:59:59.999Z')}]",
                "size": 10000  # Quantidade de hits a serem buscados (10 mil é o máximo da API)
            }

            # Realiza um GET request para o URL da API
            response = self.session.get(self.url, params=query_params)

            if response.status_code == 200:
                data = response.json()
                # Hit é a denominação da API para uma entrada no banco, esse loop itera 
                # por cada um e busca informações específicas
                hits = data.get("hits", {}).get("hits", [])
                for hit in hits:
                    source = hit.get("_source", {})
                    keys_to_retrieve = ["id", "@timestamp", "sexo", "idade", "racaCor",
                                        "sintomas", "dataInicioSintomas",
                                        "municipio", "estado", "dataPrimeiraDose", "dataSegundaDose",
                                        "dataNotificacao", "municipioNotificacao", "estadoNotificacao",
                                        "recebeuAntiviral", "profissionalSaude", "profissionalSeguranca"]

                    selected_data = []
                    for key in keys_to_retrieve:
                        value = source.get(key)
                        if value is None:
                            # Insere um valor específico caso alguma data seja null
                            if key in ["@timestamp", "dataInicioSintomas", "dataPrimeiraDose", "dataSegundaDose", "dataNotificacao"]:
                                selected_data.append("1970-01-01 00:00:00")
                            # Insere N/A caso algum valor seja null
                            else:
                                selected_data.append("N/A")
                        else:
                            selected_data.append(value)

                    # Insere os dados no banco de dados local PostgreSQL
                    insert_query = "INSERT INTO Notificacoes_sindrome_gripal_parana VALUES (%s)" % ','.join(['%s'] * len(selected_data))
                    cursor.execute(insert_query, selected_data)

                conn.commit()
                print(f"Processed {len(hits)} hits for {current_date}")

            else:
                print(f"Error in request for {current_date}: {response.status_code}")

            # Move a busca para o próximo mês
            current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)

        # Encerra a conexão com o banco de dados
        cursor.close()
        conn.close()

        print("Data insertion complete.")

if __name__ == "__main__":

    # Credenciais para conexão com o banco de dados PostgreSQL
    db_params = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "12345",
        "host": "localhost",
        "port": "5432"
    }

    processor = NotificacoesProcessor(db_params)

    start_date = datetime(2022, 11, 1)
    end_date = datetime.now()

    processor.fetch_and_processs_data(start_date, end_date)