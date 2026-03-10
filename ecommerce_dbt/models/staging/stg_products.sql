{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'OLIST_PRODUCTS_DATASET') }}

),

cleaned AS (

    SELECT

        TRIM(product_id) AS product_id,

        TRIM(product_category_name) AS product_category_name,

        CAST(product_name_lenght AS NUMBER) AS product_name_lenght,

        CAST(product_description_lenght AS NUMBER) AS product_description_lenght,

        CAST(product_photos_qty AS NUMBER) AS product_photos_qty,

        CAST(product_weight_g AS NUMBER) AS product_weight_g,

        CAST(product_length_cm AS NUMBER) AS product_length_cm,

        CAST(product_height_cm AS NUMBER) AS product_height_cm,

        CAST(product_width_cm AS NUMBER) AS product_width_cm

    FROM source

)

SELECT * FROM cleaned