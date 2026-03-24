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

standardized AS (

    SELECT DISTINCT
        LPAD(CAST(geolocation_zip_code_prefix AS STRING), 5, '0') AS zip_code_prefix,
        CAST(geolocation_lat AS FLOAT) AS latitude,
        CAST(geolocation_lng AS FLOAT) AS longitude,

        /* Strong city normalization */
        CASE
            /* explicit correction for observed encoding issue */
            WHEN INITCAP(
                TRIM(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(
                            TRANSLATE(
                                LOWER(
                                    REPLACE(
                                        REPLACE(
                                            REPLACE(TRIM(geolocation_city), '%26apos%3b', ''''),
                                        '£', ''),
                                    '´', '''')
                                ),
                                'áàâãäéèêëíìîïóòôõöúùûüç',
                                'aaaaaeeeeiiiiooooouuuuc'
                            ),
                            '[''`()-/,]',
                            ' '
                        ),
                        '\\s+',
                        ' '
                    )
                )
            ) = 'Sao Paulo'
            THEN 'Sao Paulo'

            ELSE INITCAP(
                TRIM(
                    REGEXP_REPLACE(
                        REGEXP_REPLACE(
                            TRANSLATE(
                                LOWER(
                                    REPLACE(
                                        REPLACE(
                                            REPLACE(TRIM(geolocation_city), '%26apos%3b', ''''),
                                        '£', ''),
                                    '´', '''')
                                ),
                                'áàâãäéèêëíìîïóòôõöúùûüç',
                                'aaaaaeeeeiiiiooooouuuuc'
                            ),
                            '[''`()-/,]',
                            ' '
                        ),
                        '\\s+',
                        ' '
                    )
                )
            )
        END AS city,

        UPPER(NULLIF(TRIM(geolocation_state), '')) AS state

    FROM source

)

SELECT *
FROM standardized