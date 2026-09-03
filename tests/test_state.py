from src.ingestion.state import get_latest_timestamp


def test_get_latest_timestamp():
    timestamp = get_latest_timestamp("coingecko", "btc")

    assert timestamp is not None