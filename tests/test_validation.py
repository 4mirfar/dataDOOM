from src.ingestion.validation import validate_records


def test_valid_record_is_accepted():
    records = [
        {
            "symbol": "btc",
            "current_price": 100000.0,
            "last_updated": "2026-09-03T10:00:00Z",
        }
    ]

    valid_records, rejected_count = validate_records(records)

    assert len(valid_records) == 1
    assert rejected_count == 0


def test_invalid_price_is_rejected():
    records = [
        {
            "symbol": "btc",
            "current_price": -100,
            "last_updated": "2026-09-03T10:00:00Z",
        }
    ]

    valid_records, rejected_count = validate_records(records)

    assert len(valid_records) == 0
    assert rejected_count == 1


def test_duplicate_records_are_rejected():
    records = [
        {
            "symbol": "btc",
            "current_price": 100000,
            "last_updated": "2026-09-03T10:00:00Z",
        },
        {
            "symbol": "btc",
            "current_price": 100000,
            "last_updated": "2026-09-03T10:00:00Z",
        },
    ]

    valid_records, rejected_count = validate_records(records)

    assert len(valid_records) == 1
    assert rejected_count == 1