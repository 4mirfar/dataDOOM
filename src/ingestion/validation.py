from pydantic import ValidationError

from src.ingestion.schemas import MarketRecord


def validate_records(records: list[dict]) -> tuple[list[dict], int]:
    valid_records = []
    rejected_count = 0

    for record in records:
        try:
            MarketRecord.model_validate(record)
            valid_records.append(record)

        except ValidationError as error:
            rejected_count += 1
            print(f"Rejected record: {error}")

    return valid_records, rejected_count