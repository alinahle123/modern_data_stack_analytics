WITH orders AS (

    SELECT *
    FROM {{ ref('stg_orders') }}

),

customers AS (

    SELECT *
    FROM {{ ref('stg_customers') }}

),

payments AS (

    SELECT
        order_id,
        SUM(payment_value) AS total_payment
    FROM {{ ref('stg_order_payments') }}
    GROUP BY order_id

),

order_items AS (

    SELECT
        order_id,
        COUNT(*) AS total_items
    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id

)

SELECT

    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_ts,

    c.customer_city,
    c.customer_state,

    COALESCE(p.total_payment, 0) AS total_payment,
COALESCE(oi.total_items, 0) AS total_items,
FROM orders o

LEFT JOIN customers c
    ON o.customer_id = c.customer_id

LEFT JOIN payments p
    ON o.order_id = p.order_id

LEFT JOIN order_items oi
    ON o.order_id = oi.order_id