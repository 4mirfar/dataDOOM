from src.ingestion.api_client import CoinGeckoClient
from src.ingestion.loader import load_raw_market_data


def run():
    client = CoinGeckoClient()

    records = client.get_market_data(
        ["bitcoin", "ethereum"]
    )

    print(f"Fetched {len(records)} records")

    inserted = load_raw_market_data(records)

    print(f"Inserted {inserted} new records")


if __name__ == "__main__":
    run()