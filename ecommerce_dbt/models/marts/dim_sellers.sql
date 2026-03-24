select
        seller_id,
        seller_zip_code_prefix
    from {{ ref('stg_sellers') }}