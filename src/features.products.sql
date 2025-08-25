

-- BASE: Considerando 6 meses a partir da data mais recente
-- Suposicao hoje é dia 2025-08-09

SELECT
     DATE("2025-08-09") AS Dt_ref,
     ID_cliente,
     idade,
     SUM(CASE WHEN categoria_produto = 'Eletronicos' THEN valor_venda else 0 END) / SUM(valor_venda) as pct_Eletronicos,
     SUM(CASE WHEN categoria_produto = 'Roupas' THEN valor_venda else 0 END) / SUM(valor_venda) as pct_Roupas,
     SUM(CASE WHEN categoria_produto = 'Alimentos' THEN valor_venda else 0 END) / SUM(valor_venda) as pct_Alimentos,
     SUM(CASE WHEN categoria_produto = 'Brinquedos' THEN valor_venda else 0 END) / SUM(valor_venda) as pct_Brinquedos,
     SUM(CASE WHEN categoria_produto = 'Livros' THEN valor_venda else 0 END) / SUM(valor_venda) as pct_Livros

     
FROM Vendas
WHERE data >= DATE("2025-08-09", "-6 months") AND data < DATE("2025-08-09")
GROUP BY ID_cliente

