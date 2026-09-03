from datetime import datetime

from src.database.connection import get_connection


def get_latest_timestamp(source: str, symbol: str) -> datetime | None:
    query = """
        SELECT MAX(timestamp)
        FROM raw_market_data
        WHERE source = %s
          AND symbol = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (source, symbol))
            result = cursor.fetchone()

    return result[0]