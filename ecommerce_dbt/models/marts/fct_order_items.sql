select
    order_id,
    order_item_id,
    product_id,
    seller_id,
    price,
    freight_value,
    total_item_value
from {{ ref('int_order_items_products') }}