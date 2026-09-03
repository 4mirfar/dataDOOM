import logging

from pydantic import ValidationError

from src.ingestion.schemas import MarketRecord


logger = logging.getLogger(__name__)


def validate_records(records: list[dict]) -> tuple[list[dict], int]:
    valid_records = []
    rejected_count = 0
    seen_records = set()

    for record in records:
        try:
            validated = MarketRecord.model_validate(record)

            record_key = (
                validated.symbol,
                validated.last_updated,
            )

            if record_key in seen_records:
                logger.warning(
                    "Duplicate record in API response | symbol=%s | timestamp=%s",
                    validated.symbol,
                    validated.last_updated,
                )
                rejected_count += 1
                continue

            seen_records.add(record_key)
            valid_records.append(record)

        except ValidationError as error:
            rejected_count += 1

            logger.warning(
                "Record validation failed | error=%s",
                error,
            )

    return valid_records, rejected_count