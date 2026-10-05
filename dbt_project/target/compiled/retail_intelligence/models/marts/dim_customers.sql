

SELECT
    customer_id,
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS latest_order_date,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS lifetime_value,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM "retail_warehouse"."public_analytics"."fct_orders"
GROUP BY customer_id