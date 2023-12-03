import sqlite3
from datetime import datetime


class DataBase:
    _instance = None

    def __new__(cls, database_name):
        if cls._instance is None:
            cls._instance = super(DataBase, cls).__new__(cls)
            cls._instance.database_name = database_name
            cls._instance._connection = cls._instance.connect()
        return cls._instance

    def connect(self):
        return sqlite3.connect(self.database_name)

    def create_tables(self):
        cursor = self._connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS repositories (
                id INTEGER PRIMARY KEY,
                name TEXT,
                vcs_type TEXT,
                created_at DATETIME,
                repo_path TEXT
            )
        ''')
        self._connection.commit()
        cursor.close()

    def insert_repository(self, name, vcs_type, repo):
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO repositories (name, vcs_type, created_at, repo_path) VALUES (?, ?, ?, ?)",
                       (name, vcs_type, datetime.now(), repo))
        self._connection.commit()
        cursor.close()

    def fetch_active_repositories(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT name, vcs_type, repo_path FROM repositories")
        repositories = cursor.fetchall()
        cursor.close()
        return repositories

    def remove_repository(self, name):
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM repositories WHERE name=?", (name,))
        self._connection.commit()
        cursor.close()