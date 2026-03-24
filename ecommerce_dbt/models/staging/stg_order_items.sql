{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date,
        price,
        freight_value
    FROM {{ source('raw', 'OLIST_ORDER_ITEMS_DATASET') }}

),

cleaned AS (

    SELECT

        NULLIF(TRIM(order_id), '') AS order_id,
        order_item_id AS order_item_id,
        NULLIF(TRIM(product_id), '') AS product_id,
        NULLIF(TRIM(seller_id), '') AS seller_id,

        CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_date,

        CAST(price AS NUMBER(10,2)) AS price,
        CAST(freight_value AS NUMBER(10,2)) AS freight_value

    FROM source

)

SELECT * FROM cleaned