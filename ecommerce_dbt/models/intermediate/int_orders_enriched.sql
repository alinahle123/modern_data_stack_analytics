WITH orders AS (

    SELECT *
    FROM {{ ref('stg_orders') }}

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

),

order_reviews AS (

    SELECT
        order_id,
        AVG(review_score) AS avg_review_score
    FROM {{ ref('stg_order_reviews') }}
    GROUP BY order_id

)

SELECT

    o.order_id,
    o.customer_id,
    o.order_status,
    o.order_purchase_ts,
    o.order_approved_ts,
    o.delivered_customer_ts,

    COALESCE(p.total_payment, 0) AS total_payment,
    COALESCE(oi.total_items, 0) AS total_items,
    r.avg_review_score,

    CASE
        WHEN o.order_status = 'delivered'
             AND o.order_approved_ts IS NOT NULL
             AND o.delivered_customer_ts IS NOT NULL
        THEN DATEDIFF('day', o.order_approved_ts, o.delivered_customer_ts)
        ELSE NULL
    END AS approval_to_delivery_days

FROM orders o

LEFT JOIN payments p
    ON o.order_id = p.order_id

LEFT JOIN order_items oi
    ON o.order_id = oi.order_id

LEFT JOIN order_reviews r
    ON o.order_id = r.order_id