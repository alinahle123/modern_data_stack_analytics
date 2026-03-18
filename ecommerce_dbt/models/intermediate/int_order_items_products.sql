with order_items as (

    select * 
    from {{ ref('stg_order_items') }}

)

select

    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) as total_item_value

from order_items oi

