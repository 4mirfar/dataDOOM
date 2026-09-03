from datetime import datetime

from src.ingestion.state import get_latest_timestamp


def filter_new_records(
    records: list[dict],
    source: str,
) -> list[dict]:
    new_records = []

    for record in records:
        latest_timestamp = get_latest_timestamp(
            source=source,
            symbol=record["symbol"],
        )

        record_timestamp = datetime.fromisoformat(
            record["last_updated"].replace("Z", "+00:00")
        )

        if latest_timestamp is None or record_timestamp > latest_timestamp:
            new_records.append(record)

    return new_records