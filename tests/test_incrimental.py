from datetime import datetime, timezone
from unittest.mock import patch

from src.ingestion.incremental import filter_new_records


def test_new_record_is_selected():
    records = [
        {
            "symbol": "btc",
            "current_price": 100000,
            "last_updated": "2026-09-03T10:00:00Z",
        }
    ]

    latest_timestamp = datetime(
        2026, 9, 3, 9, 0, 0, tzinfo=timezone.utc
    )

    with patch(
        "src.ingestion.incremental.get_latest_timestamp",
        return_value=latest_timestamp,
    ):
        result = filter_new_records(records, "coingecko")

    assert len(result) == 1


def test_existing_record_is_filtered_out():
    records = [
        {
            "symbol": "btc",
            "current_price": 100000,
            "last_updated": "2026-09-03T10:00:00Z",
        }
    ]

    latest_timestamp = datetime(
        2026, 9, 3, 10, 0, 0, tzinfo=timezone.utc
    )

    with patch(
        "src.ingestion.incremental.get_latest_timestamp",
        return_value=latest_timestamp,
    ):
        result = filter_new_records(records, "coingecko")

    assert len(result) == 0