WITH base AS (
    SELECT
        *,
      ROW_NUMBER() OVER (PARTITION BY cpf ORDER BY total_convertido DESC) AS linha
    FROM (
        SELECT
            nome,
            cpf,
            funcionario_id,
            descricao_orgao,
            codigo_orgao,
            numero_ordem,
            id,
            CAST(SPLIT_PART(REPLACE(REPLACE(total, '.', ''), ',', '.'), 'R$', 1) AS NUMERIC) AS total_convertido,
            CAST(ano AS INT) AS ano,
            CAST(mes AS INT) AS mes
        FROM {{ ref('servidores') }}
    ) sub
)

SELECT
    nome,
    cpf,
    funcionario_id,
    descricao_orgao,
    codigo_orgao,
    numero_ordem,
    id,
    total_convertido AS total,
    total_convertido * 0.1 AS horas_extras,
    ano,
    mes
FROM base
WHERE linha = 1
