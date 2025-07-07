import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv


def main():
    load_dotenv()

    user = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    ano = int(os.getenv("API_ANO", 2023))
    mes = int(os.getenv("API_MES", 7))
    limit = int(os.getenv("API_LIMIT", 200))
    offset = int(os.getenv("API_OFFSET", 0))

    user_esc = quote_plus(user)
    senha_esc = quote_plus(senha)
    conn_str = f"postgresql+psycopg2://{user_esc}:{senha_esc}@{host}:{port}/{database}"
    engine = create_engine(conn_str)

    url_base = "https://transparencia.al.gov.br/pessoal/json-servidores/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    params = {
        "ano": ano,
        "mes": mes,
        "limit": limit,
        "offset": offset
    }

    print("Iniciando coleta de dados...")

    try:
        response = requests.get(url_base, headers=headers, params=params)
        response.encoding = 'latin1'
        dados = response.json()

        rows = dados.get("rows", [])
        print(f"Coletados {len(rows)} registros.")

        if not rows:
            print("Nenhum dado coletado.")
            return

        df = pd.DataFrame(rows)

        csv_path = f"servidores_{ano}_{mes}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"Arquivo CSV salvo em: {csv_path}")

        for col in df.select_dtypes(include=['object']):
            df[col] = df[col].astype(str).apply(
                lambda x: x.encode('latin1').decode('utf-8', errors='ignore')
            )

        print("Inserindo dados no banco...")
        df.to_sql("servidores", con=engine, if_exists="replace", index=False)
        print("Dados inseridos com sucesso!")

    except Exception as e:
        print(f"Erro durante execução: {e}")
