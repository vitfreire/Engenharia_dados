WITH base AS (
    SELECT
        nome,
        REPLACE(REPLACE(total, '.', ''), ',', '.')::numeric AS total_convertido
    FROM "transparencia"."public"."servidores"
)

SELECT
    nome,
    total_convertido,
    total_convertido * 0.1 AS horas_extras
FROM base