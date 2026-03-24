{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'OLIST_PRODUCTS_DATASET') }}

),

typed AS (

    SELECT

        NULLIF(TRIM(product_id), '') AS product_id,

        NULLIF(TRIM(product_category_name), '') AS product_category_name,

        CAST(product_name_lenght AS NUMBER) AS product_name_lenght,
        CAST(product_description_lenght AS NUMBER) AS product_description_lenght,
        CAST(product_photos_qty AS NUMBER) AS product_photos_qty,
        CAST(product_weight_g AS NUMBER) AS product_weight_g,
        CAST(product_length_cm AS NUMBER) AS product_length_cm,
        CAST(product_height_cm AS NUMBER) AS product_height_cm,
        CAST(product_width_cm AS NUMBER) AS product_width_cm

    FROM source

),

cleaned AS (

    SELECT

        product_id,

        COALESCE(product_category_name, 'unknown') AS product_category_name,

        product_name_lenght,

        product_description_lenght,

        product_photos_qty,

        CASE
            WHEN product_weight_g <= 0 THEN NULL
            ELSE product_weight_g
        END AS product_weight_g,

        product_length_cm,

        product_height_cm,

        product_width_cm

    FROM typed

)

SELECT *
FROM cleaned
WHERE product_id IS NOT NULL