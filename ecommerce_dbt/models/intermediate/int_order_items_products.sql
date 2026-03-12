with order_items as (

    select * 
    from {{ ref('stg_order_items') }}

),

products as (

    select * 
    from {{ ref('stg_products') }}

),

sellers as (

    select * 
    from {{ ref('stg_sellers') }}

),

category_translation as (

    select * 
    from {{ ref('stg_product_category_translation') }}

)

select

    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,

    p.product_category_name,
    ct.product_category_name_english,

    s.seller_city,
    s.seller_state,

    oi.price,
    oi.freight_value,

    (oi.price + oi.freight_value) as total_item_value

from order_items oi

left join products p
    on oi.product_id = p.product_id

left join category_translation ct
    on p.product_category_name = ct.product_category_name

left join sellers s
    on oi.seller_id = s.seller_id