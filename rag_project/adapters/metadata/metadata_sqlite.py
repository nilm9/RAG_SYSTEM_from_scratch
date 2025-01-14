import sqlite3
from typing import Dict


class MetadataSQLite:
    """
    Handles metadata storage and querying in SQLite.
    """
    def __init__(self, db_path: str = "metadata.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS metadata (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            source TEXT,
            ingestion_timestamp TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def insert_metadata(self, filename: str, source: str, ingestion_timestamp: str):
        query = """
        INSERT INTO metadata (filename, source, ingestion_timestamp)
        VALUES (?, ?, ?)
        """
        self.conn.execute(query, (filename, source, ingestion_timestamp))
        self.conn.commit()

    def fetch_metadata(self):
        query = "SELECT * FROM metadata"
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def close(self):
        self.conn.close()
