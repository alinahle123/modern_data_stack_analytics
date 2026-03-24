{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'OLIST_SELLERS_DATASET') }}

),

cleaned AS (

    SELECT

        NULLIF(TRIM(seller_id), '') AS seller_id,

        /* keep zip as string to match geolocation */
        LPAD(CAST(seller_zip_code_prefix AS STRING), 5, '0') AS seller_zip_code_prefix

    FROM source

)

SELECT *
FROM cleaned
WHERE seller_id IS NOT NULL
  AND seller_zip_code_prefix IS NOT NULL