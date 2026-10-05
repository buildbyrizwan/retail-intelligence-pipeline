-- Create distinct logical namespaces
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Raw orders landing table
CREATE TABLE IF NOT EXISTS raw.orders (
    event_id VARCHAR(64) PRIMARY KEY,
    customer_id VARCHAR(64) NOT NULL,
    product_id VARCHAR(64) NOT NULL,
    category VARCHAR(64) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    quantity INT NOT NULL,
    order_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    payment_method VARCHAR(32),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_raw_orders_timestamp ON raw.orders(order_timestamp);
CREATE INDEX IF NOT EXISTS idx_raw_orders_customer ON raw.orders(customer_id);