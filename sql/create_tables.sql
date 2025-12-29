-- Orders table
CREATE TABLE IF NOT EXISTS raw_orders (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    order_date TIMESTAMP,
    promised_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    delivery_status TEXT,
    order_total NUMERIC,
    payment_method TEXT,
    delivery_partner_id BIGINT,
    store_id BIGINT
);

-- Marketing table
CREATE TABLE IF NOT EXISTS raw_marketing (
    campaign_id BIGINT,
    campaign_name TEXT,
    date DATE,
    target_audience TEXT,
    channel TEXT,
    impressions BIGINT,
    clicks BIGINT,
    conversions BIGINT,
    spend NUMERIC,
    revenue_generated NUMERIC,
    roas NUMERIC
);

-- Customer feedback table
CREATE TABLE IF NOT EXISTS raw_feedback (
    feedback_id BIGINT PRIMARY KEY,
    order_id BIGINT,
    customer_id BIGINT,
    rating INT,
    feedback_text TEXT,
    feedback_category TEXT,
    sentiment TEXT,
    feedback_date DATE
);
