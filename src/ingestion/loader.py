from psycopg.types.json import Json

from src.database.connection import get_connection

def load_raw_market_data(records: list[dict]) -> int:
    inserted_count = 0

    query = """
        INSERT INTO raw_market_data (
            source,
            symbol,
            timestamp,
            payload
        )
        VALUES (%s, %s, %s, %s) 
        ON CONFLICT (source, symbol, timestamp)
        DO NOTHING;
    """
    # Using parameterized queries with %s lets psycopg safely handle quoting, escaping, types, and SQL-injection protection.
    # One slightly confusing thing: %s doesn't mean the value has to be a string.
    # In psycopg parameterized SQL, it's the generic parameter placeholder.

    with get_connection() as conn:
        with conn.cursor() as cursor:
            for record in records:
                cursor.execute(
                    query,
                    (
                        "coingecko",
                        record["symbol"],
                        record["last_updated"],
                        Json(record),
                    ),
                )

                if cursor.rowcount == 1:
                    inserted_count += 1

        conn.commit()

    return inserted_count