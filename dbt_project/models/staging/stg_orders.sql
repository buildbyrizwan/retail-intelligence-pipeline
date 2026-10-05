WITH source_data AS (
    SELECT
        event_id,
        customer_id,
        product_id,
        category,
        price::NUMERIC(10, 2) AS unit_price,
        quantity::INT AS quantity,
        (price * quantity)::NUMERIC(10, 2) AS total_amount,
        order_timestamp::TIMESTAMP WITH TIME ZONE AS order_timestamp,
        order_timestamp::DATE AS order_date,
        LOWER(TRIM(payment_method)) AS payment_method
    FROM raw.orders
)

SELECT * FROM source_data