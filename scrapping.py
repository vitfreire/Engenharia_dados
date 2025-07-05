import requests
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# Variáveis da conexão
user = "postgres"
senha = "post"
host = "localhost"
port = 5432
database = "transparencia"

# Testar conexão psycopg2
try:
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=senha,
        host=host,
        port=port
    )
    print("Conectou com sucesso!")
    conn.close()
except Exception as e:
    print(f"Erro: {e}")

# Criar engine sqlalchemy
engine = create_engine(f'postgresql://{user}:{senha}@{host}:{port}/{database}') 

# Configuração da API
url_base = "https://transparencia.al.gov.br/pessoal/json-servidores/"
headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

ano = 2023
mes = 7
limit = 50  
offset = 0

params = {
    "ano": ano,
    "mes": mes,
    "limit": limit,
    "offset": offset
}

print("Iniciando coleta de dados...")

response = requests.get(url_base, headers=headers, params=params)
response.raise_for_status()
dados = response.json()

rows = dados.get("rows", [])

print(f"Coletados {len(rows)} registros.")

if rows:
    df = pd.DataFrame(rows)
    # Salvar CSV localmente
    csv_path = "servidores_{}_{}.csv".format(ano, mes)
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Arquivo CSV salvo em: {csv_path}")

    print("Inserindo dados no banco...")
    df.to_sql('servidores', con=engine, if_exists='replace', index=False)
    print("Dados inseridos com sucesso!")
else:
    print("Nenhum dado coletado.")
