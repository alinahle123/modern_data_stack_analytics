{{ config(
    materialized='view'
) }}

WITH source AS (

    SELECT
        geolocation_zip_code_prefix,
        geolocation_lat,
        geolocation_lng,
        geolocation_city,
        geolocation_state

    FROM {{ source('raw', 'OLIST_GEOLOCATION_DATASET') }}

),

cleaned AS (

    SELECT
        CAST(geolocation_zip_code_prefix AS STRING) AS zip_code_prefix,
        CAST(geolocation_lat AS FLOAT) AS latitude,
        CAST(geolocation_lng AS FLOAT) AS longitude,
        INITCAP(TRIM(geolocation_city)) AS city,
        UPPER(TRIM(geolocation_state)) AS state

    FROM source

)

SELECT * FROM cleaned