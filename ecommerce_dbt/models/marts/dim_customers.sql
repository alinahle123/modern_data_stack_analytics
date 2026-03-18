with customers as (

    select *
    from {{ ref('stg_customers') }}

)

select

    c.customer_id,
    c.customer_unique_id,
    c.customer_zip_code_prefix,
    c.customer_city,
    c.customer_state,

from customers c
