

-- BASE: Considerando 6 meses a partir da data mais recente
-- Suposicao hoje é dia 2025-08-09


WITH base AS 
(
    SELECT
     ID_cliente,
     idade,
     julianday("2025-08-09") - julianday(MAX(data)) AS Recencia,
     COUNT(DISTINCT(data)) AS Frequencia,
     SUM(valor_venda) AS Valor,
     SUM(valor_venda) / COUNT(data) as Ticket_medio
   
     
FROM Vendas
WHERE data >= DATE("2025-08-09", "-6 months") AND data < DATE("2025-08-09")
GROUP BY ID_cliente
ORDER BY Recencia 
),

idade_base AS (
    SELECT
     ID_cliente, 
     julianday("2025-08-09") - julianday(MIN(data)) AS Idade_base
     FROM Vendas   
     GROUP BY 1
)

SELECT  DATE("2025-08-09") AS Dt_ref,
        A.*,
        B.Idade_base
FROM base A
LEFT JOIN idade_base B
ON A.ID_cliente = B.ID_cliente