SELECT
    symbol,
    timestamp,
    price_usd,
    market_cap,
    volume_24h,
    price_change_24h
FROM {{ ref('stg_market_data') }}