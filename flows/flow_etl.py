from prefect import flow, task
from etl.scrapping import main as executar_extracao
from etl.criar_banco import criar_banco
import subprocess
from pathlib import Path
import os


@task
def criar_banco_task():
    criar_banco()


@task
def extrair_dados_task():
    executar_extracao()


@task
def rodar_dbt_task():
    dbt_dir = Path(__file__).resolve().parent.parent / "dbt_project"
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = str(Path.home() / ".dbt")

    subprocess.run(["dbt", "run"], cwd=str(dbt_dir), env=env, check=True)
    print("Transformações DBT executadas com sucesso.")


@flow(name="pipeline_etl_servidores")
def pipeline_etl():
    criar_banco_task()
    extrair_dados_task()
    rodar_dbt_task()


if __name__ == "__main__":
    pipeline_etl()
