{{ config(materialized='table') }}

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
FROM {{ ref('stg_orders') }}