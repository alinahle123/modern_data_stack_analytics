{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'OLIST_ORDER_PAYMENTS_DATASET') }}

),

typed AS (

    SELECT
        NULLIF(TRIM(order_id), '') AS order_id,
        CAST(payment_sequential AS NUMBER(5,0)) AS payment_sequential,
        LOWER(TRIM(payment_type)) AS payment_type,
        CAST(payment_installments AS NUMBER(5,0)) AS payment_installments,
        CAST(payment_value AS NUMBER(10,2)) AS payment_value
    FROM source

),

cleaned AS (

    SELECT
        order_id,

        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY payment_sequential, payment_value DESC, payment_type
        ) AS payment_sequential,

        payment_type,

        CASE
            WHEN payment_type IN ('credit_card', 'debit_card')
                 AND payment_value > 0
                 AND payment_installments = 0
            THEN 1
            ELSE payment_installments
        END AS payment_installments,

        payment_value

    FROM typed

)

SELECT * 
FROM cleaned
