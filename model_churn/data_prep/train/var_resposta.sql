DROP TABLE IF EXISTS tb_abt_churn;
CREATE TABLE tb_abt_churn AS
SELECT
    t2.*,
    t1.flag_venda
    
FROM (
    SELECT 
        t1.dt_ref,
        t1.seller_id,
        MAX(COALESCE(t2.venda, 0)) AS flag_venda
    FROM 
        tb_book_sellers AS t1
    LEFT JOIN (
        SELECT 
            strftime('%Y%m', t1.order_approved_at) AS dt_venda,
            t2.seller_id,
            1 AS venda
        FROM 
            tb_orders AS t1
        LEFT JOIN 
            tb_order_items AS t2 ON t1.order_id = t2.order_id
        WHERE 
            t1.order_approved_at IS NOT NULL
            AND t2.seller_id IS NOT NULL
            AND t1.order_status = 'delivered'
        GROUP BY 
            strftime('%Y%m', t1.order_approved_at), t2.seller_id
    ) AS t2 ON t1.seller_id = t2.seller_id
            AND t2.dt_venda BETWEEN strftime('%Y%m', t1.dt_ref) AND strftime('%Y%m', DATE(t1.dt_ref, '+2 MONTHS'))
    GROUP BY 
        t1.dt_ref, t1.seller_id
    ORDER BY 
        t1.dt_ref
) AS t1
LEFT JOIN 
    tb_book_sellers AS t2 ON t1.seller_id = t2.seller_id AND t1.dt_ref = t2.dt_ref;
