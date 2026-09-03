CREATE TABLE IF NOT EXISTS raw_market_data (
    id BIGSERIAL PRIMARY KEY,

    source VARCHAR(100) NOT NULL,
    symbol VARCHAR(50) NOT NULL,  -- eg BTC
    timestamp TIMESTAMPTZ NOT NULL, -- when the market event happened

    payload JSONB NOT NULL, -- stores json raw data

    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),  -- when we recieved the data

    UNIQUE (source, symbol, timestamp) -- a natural key so that the same market observation can't be inserted twice.
);