WITH products AS (

    SELECT *
    FROM {{ ref('stg_products') }}

)

SELECT

    product_id,

    product_category_name

    from products