import sqlite3
from datetime import datetime


class DBHandler:
    def __init__(self, db_path="db.sqlite"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    # ------------------------------------------
    # UserHandler
    def get_all_users(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT username, profile_photo FROM users
            """)
            return cursor.fetchall()

    def add_user(self, username, profile_photo=None):
        created_at = datetime.now().strftime("%Y-%m-%d")
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, profile_photo, created_at)
                VALUES (?, ?, ?)
            """, (username, profile_photo, created_at))
            conn.commit()

    def delete_user(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username))
            conn.commit()


def main():
    print("Welcome to DBHandler")


if __name__ == "__main__":
    main()
