from pathlib import Path

from src.database.connection import get_connection


def initialize_database():
    schema_path = Path(__file__).parent / "schema.sql"
    schema = schema_path.read_text()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(schema)

        conn.commit()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")