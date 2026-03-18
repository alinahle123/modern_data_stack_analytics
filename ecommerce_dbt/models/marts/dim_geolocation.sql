WITH geolocation AS (

    SELECT *
    FROM {{ ref('stg_geolocation') }}

)


    SELECT

        zip_code_prefix,

        -- Average lat/lng because multiple entries exist per zip prefix
        AVG(latitude) AS latitude,
        AVG(longitude) AS longitude,

        -- City/state are usually consistent, MAX is safe after grouping
        MAX(city) AS city,
        MAX(state) AS state

    FROM geolocation
    GROUP BY zip_code_prefix

