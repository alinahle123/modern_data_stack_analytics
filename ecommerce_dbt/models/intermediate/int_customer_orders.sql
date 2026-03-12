with orders as (

    select * 
    from {{ ref('stg_orders') }}

)

select

    customer_id,

    count(order_id) as total_orders,

    min(order_purchase_ts) as first_order_date,

    max(order_purchase_ts) as last_order_date

from orders

group by customer_id