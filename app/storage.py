import sqlite3
from pathlib import Path



DB_PATH = Path("data/automation.db")


def initialise_database():
    DB_PATH.parent.mkdir(exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS processed_events (
                even_id TEXT PRIMARY KEY
            )
            """
        )


def is_event_processed(event_id: str) -> bool:
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            SELECT 1
            FROM processed_events
            WHERE even_id = ?
            """,
            (event_id,),
        )

        return cursor.fetchone() is not None


def mark_event_processed(event_id: str):
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            INSERT INTO processed_events (even_id)
            VALUES (?)
            """,
            (event_id,),
        )

