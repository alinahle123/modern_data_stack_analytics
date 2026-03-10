{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'OLIST_ORDER_ITEMS_DATASET') }}

),

cleaned AS (

    SELECT

        TRIM(order_id)                AS order_id,
        order_item_id                 AS order_item_id,
        TRIM(product_id)              AS product_id,
        TRIM(seller_id)               AS seller_id,

        CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_date,

        CAST(price AS NUMBER(10,2))          AS price,
        CAST(freight_value AS NUMBER(10,2))  AS freight_value

    FROM source

)

SELECT * FROM cleaned