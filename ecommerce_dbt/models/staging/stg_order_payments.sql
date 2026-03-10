{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'OLIST_ORDER_PAYMENTS_DATASET') }}

),

cleaned AS (

    SELECT

        TRIM(order_id) AS order_id,

        payment_sequential AS payment_sequential,

        LOWER(TRIM(payment_type)) AS payment_type,

        CAST(payment_installments AS NUMBER(5,0)) AS payment_installments,

        CAST(payment_value AS NUMBER(10,2)) AS payment_value

    FROM source

)

SELECT * FROM cleaned