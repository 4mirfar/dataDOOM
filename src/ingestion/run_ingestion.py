from src.ingestion.api_client import CoinGeckoClient
from src.ingestion.incremental import filter_new_records
from src.ingestion.loader import load_raw_market_data
from src.ingestion.validation import validate_records


COINS = ["bitcoin", "ethereum"]


def run():
    client = CoinGeckoClient()

    records = client.get_market_data(COINS)

    print(f"Fetched {len(records)} records")

    valid_records, rejected_count = validate_records(records)

    print(f"Valid records: {len(valid_records)}")
    print(f"Rejected records: {rejected_count}")

    new_records = filter_new_records(
        records=valid_records,
        source="coingecko",
    )

    print(f"New records: {len(new_records)}")

    inserted = load_raw_market_data(new_records)

    print(f"Inserted {inserted} new records")


if __name__ == "__main__":
    run()