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
        oip.product_id,
        oe.customer_id,
        oe.order_purchase_ts,
        oip.price,
        oip.total_item_value
    FROM order_items_products oip
    LEFT JOIN orders_enriched oe
        ON oip.order_id = oe.order_id
    WHERE oe.order_status = 'delivered'
      AND oip.product_id IS NOT NULL
      AND oe.order_purchase_ts IS NOT NULL

)

SELECT
    product_id,
    EXTRACT(YEAR FROM order_purchase_ts) AS year,
    EXTRACT(MONTH FROM order_purchase_ts) AS month,
    AVG(price) AS average_price,
    COUNT(*) AS nb_times_sold,
    SUM(price) AS total_revenue,
    COUNT(DISTINCT customer_id) AS nb_unique_customers
FROM joined
GROUP BY
    product_id,
    EXTRACT(YEAR FROM order_purchase_ts),
    EXTRACT(MONTH FROM order_purchase_ts)