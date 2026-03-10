{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'OLIST_ORDER_REVIEWS_DATASET') }}

),

cleaned AS (

    SELECT

        TRIM(review_id) AS review_id,

        TRIM(order_id) AS order_id,

        CAST(review_score AS NUMBER(2,0)) AS review_score,

        TRIM(review_comment_title) AS review_comment_title,

        TRIM(review_comment_message) AS review_comment_message,

        CAST(review_creation_date AS TIMESTAMP) AS review_creation_date,

        CAST(review_answer_timestamp AS TIMESTAMP) AS review_answer_timestamp

    FROM source

)

SELECT * FROM cleaned