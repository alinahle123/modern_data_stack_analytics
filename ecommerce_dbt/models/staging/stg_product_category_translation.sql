{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'PRODUCT_CATEGORY_NAME_TRANSLATION') }}

),

cleaned AS (

    SELECT

        TRIM(product_category_name) AS product_category_name,

        TRIM(product_category_name_english) AS product_category_name_english

    FROM source

)

SELECT * FROM cleaned