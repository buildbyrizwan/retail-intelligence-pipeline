

SELECT
    event_id AS order_id,
    customer_id,
    product_id,
    category,
    unit_price,
    quantity,
    total_amount,
    payment_method,
    order_timestamp,
    order_date
FROM "retail_warehouse"."public_staging"."stg_orders"