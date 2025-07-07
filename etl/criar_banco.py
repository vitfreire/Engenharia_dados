import psycopg2
import os
from dotenv import load_dotenv


def criar_banco():
    load_dotenv()

    user = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=user,
            password=senha,
            host=host,
            port=port
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database}'")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f'CREATE DATABASE "{database}"')
            print(f"Banco de dados '{database}' criado com sucesso.")
        else:
            print(f"Banco de dados '{database}' já existe.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar banco: {e}")
