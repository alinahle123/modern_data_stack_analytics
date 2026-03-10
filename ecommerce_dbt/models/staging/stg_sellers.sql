{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'OLIST_SELLERS_DATASET') }}

),

cleaned AS (

    SELECT

        TRIM(seller_id) AS seller_id,

        CAST(seller_zip_code_prefix AS NUMBER) AS seller_zip_code_prefix,

        LOWER(TRIM(seller_city)) AS seller_city,

        UPPER(TRIM(seller_state)) AS seller_state

    FROM source

)

SELECT * FROM cleaned