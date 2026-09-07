SELECT
    id,
    source,
    symbol,
    timestamp,
    (payload->>'current_price')::numeric AS price_usd,
    (payload->>'market_cap')::numeric AS market_cap,
    (payload->>'total_volume')::numeric AS volume_24h,
    (payload->>'price_change_24h')::numeric AS price_change_24h,
    ingested_at
FROM {{ source('raw', 'raw_market_data') }}