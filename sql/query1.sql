SELECT 
    t2.seller_id AS id_vendedor,
    t3.idade_base AS idade_base_dia,
    1 + CAST(t3.idade_base / 30 as INT) as idade_base_mes,
    COUNT(DISTINCT strftime('%m',t1.order_approved_at)) AS qtd_ativacao,
    ROUND(CAST(COUNT(DISTINCT strftime('%m',t1.order_approved_at)) AS FLOAT) / MIN(1 + CAST(t3.idade_base / 30 AS INT), 6),2) AS prop_ativacao,
    CAST(JULIANDAY('2017-04-01') - JULIANDAY(MAX(t1.order_approved_at))AS INT) AS dias_sem_vender,
    ROUND(SUM(t2.price), 2) AS receita_total,
    ROUND(SUM(t2.price) / COUNT(DISTINCT t2.order_id), 2) AS ticket_medio,
    ROUND(SUM(t2.price) / MIN(1 + CAST(t3.idade_base / 30 AS INT), 6), 2) AS ticket_medio_mes,
    ROUND(SUM(t2.price) / COUNT(DISTINCT strftime('%m',t1.order_approved_at)), 2) AS ticket_medio_mes_ativo,
    ROUND(SUM(t2.price) / COUNT(t2.product_id), 2) AS ticket_medio_produto,
    COUNT(DISTINCT t2.order_id) AS qtd_venda,
    COUNT(t2.product_id) AS qtd_itens,
    COUNT(DISTINCT t2.product_id) AS qtd_item_distintos,
    COUNT(t2.product_id) / COUNT(DISTINCT t2.order_id) AS media_item_vendido
FROM tb_orders AS t1
LEFT JOIN tb_order_items AS t2 ON t1.order_id = t2.order_id
LEFT JOIN (
    SELECT 
        t2.seller_id,
        CAST(MAX(JULIANDAY('2017-04-01') - JULIANDAY(t1.order_approved_at)) AS INT) AS idade_base
    FROM tb_orders AS t1
    LEFT JOIN tb_order_items AS t2 ON t1.order_id = t2.order_id
    WHERE t1.order_approved_at < '2017-04-01'
      AND t1.order_status = 'delivered'
    GROUP BY t2.seller_id
) AS t3 ON t2.seller_id = t3.seller_id 
WHERE t1.order_approved_at BETWEEN '2016-10-01' AND '2017-04-01'
  AND t1.order_status = 'delivered'
GROUP BY t2.seller_id;
