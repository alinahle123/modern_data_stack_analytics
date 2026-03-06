{{ config(
    materialized='view'
) }}

WITH base AS (
    SELECT
        CUSTOMER_ID,
        CUSTOMER_UNIQUE_ID,
        CUSTOMER_ZIP_CODE_PREFIX,
        CUSTOMER_CITY,
        CUSTOMER_STATE
    FROM {{ source('raw', 'OLIST_CUSTOMERS_DATASET') }}
)

SELECT
    TRIM(CUSTOMER_ID) AS CUSTOMER_ID,
    TRIM(CUSTOMER_UNIQUE_ID) AS CUSTOMER_UNIQUE_ID,
    CAST(CUSTOMER_ZIP_CODE_PREFIX AS STRING) AS CUSTOMER_ZIP_CODE_PREFIX,  -- cast number to string for consistency
    INITCAP(TRIM(CUSTOMER_CITY)) AS CUSTOMER_CITY,                           -- capitalize first letter
    UPPER(TRIM(CUSTOMER_STATE)) AS CUSTOMER_STATE                            -- uppercase state codes
FROM base