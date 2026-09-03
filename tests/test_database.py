from src.database.connection import get_connection


def test_database_connection():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()

            assert result == (1,)