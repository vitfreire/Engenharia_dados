from flows.flow_etl import pipeline_etl

if __name__ == "__main__":
    deployment = pipeline_etl.deploy(
        name="pipeline_servidores_deploy",
        work_pool_name="default",  # Nome do Work Pool criado no Prefect Cloud
        entrypoint="flows/flow_etl.py:pipeline_etl",
        tags=["etl"]
    )
