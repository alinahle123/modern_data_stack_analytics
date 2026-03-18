WITH order_items_products AS (

    SELECT *
    FROM {{ ref('int_order_items_products') }}

),

orders_enriched AS (

    SELECT *
    FROM {{ ref('int_orders_enriched') }}

),

joined AS (

    SELECT
        oip.seller_id,
        oip.order_id,
        oe.customer_id,
        oe.order_purchase_ts,
        oip.price,
        oip.total_item_value
    FROM order_items_products oip
    LEFT JOIN orders_enriched oe
        ON oip.order_id = oe.order_id
    WHERE oe.order_status = 'delivered'
      AND oip.seller_id IS NOT NULL
      AND oe.order_purchase_ts IS NOT NULL

)

SELECT
    seller_id,
    EXTRACT(YEAR FROM order_purchase_ts) AS year,
    EXTRACT(MONTH FROM order_purchase_ts) AS month,
    COUNT(*) AS units_sold,
    SUM(price) AS revenue_per_month,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT order_id) AS unique_orders
FROM joined
GROUP BY
    seller_id,
    EXTRACT(YEAR FROM order_purchase_ts),
    EXTRACT(MONTH FROM order_purchase_ts)