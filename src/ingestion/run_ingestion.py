import logging

from src.config.logging import setup_logging
from src.ingestion.api_client import CoinGeckoClient
from src.ingestion.incremental import filter_new_records
from src.ingestion.loader import load_raw_market_data
from src.ingestion.validation import validate_records


setup_logging()

logger = logging.getLogger(__name__)

COINS = ["bitcoin", "ethereum"]


def run():
    logger.info("Starting ingestion")

    client = CoinGeckoClient()

    records = client.get_market_data(COINS)

    logger.info("Fetched %d records", len(records))

    valid_records, rejected_count = validate_records(records)

    logger.info(
        "Validation complete | valid=%d | rejected=%d",
        len(valid_records),
        rejected_count,
    )

    new_records = filter_new_records(
        records=valid_records,
        source="coingecko",
    )

    logger.info("Incremental filtering | new=%d", len(new_records))

    inserted = load_raw_market_data(new_records)

    logger.info("Loading complete | inserted=%d", inserted)

    logger.info("Ingestion completed successfully")


if __name__ == "__main__":
    run()