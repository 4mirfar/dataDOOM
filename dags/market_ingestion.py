from datetime import datetime

from airflow.sdk import dag, task

from src.ingestion.api_client import CoinGeckoClient
from src.ingestion.incremental import filter_new_records
from src.ingestion.loader import load_raw_market_data
from src.ingestion.validation import validate_records


COINS = ["bitcoin", "ethereum"]


@dag(
    dag_id="market_data_ingestion",
    start_date=datetime(2026, 9, 3),
    schedule="*/10 * * * *",
    catchup=False,
    tags=["data-doom", "market-data"],
)
def market_data_ingestion():

    @task
    def extract():
        client = CoinGeckoClient()

        records = client.get_market_data(COINS)

        return records

    @task
    def validate(records):
        valid_records, rejected_count = validate_records(records)

        print(
            f"Validation | valid={len(valid_records)} "
            f"| rejected={rejected_count}"
        )

        return valid_records

    @task
    def incremental_filter(records):
        new_records = filter_new_records(
            records=records,
            source="coingecko",
        )

        print(f"Incremental filtering | new={len(new_records)}")

        return new_records

    @task
    def load(records):
        inserted = load_raw_market_data(records)

        print(f"Loading | inserted={inserted}")

    records = extract()

    valid_records = validate(records)

    new_records = incremental_filter(valid_records)

    load(new_records)


market_data_ingestion()