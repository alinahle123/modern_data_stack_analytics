with payments as (

    select * 
    from {{ ref('stg_order_payments') }}

)

select

    order_id,

    sum(payment_value) as total_payment,

    count(payment_sequential) as number_of_payments

from payments

group by order_id