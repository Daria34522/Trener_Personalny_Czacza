import sqlite3

class DBHandler:
    def __init__(self, db_path="db.sqlite"):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path)

    # ----------------------------------------------------------------------
    # UserHandler
    def get_all_users(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username FROM users")
            return cursor.fetchall()

    def get_a_user(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_a_userid(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            return result[0] if result else None


    def add_user(self, username):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, created_at) VALUES (?, DATE('now'))", (username,))
            conn.commit()
            return cursor.lastrowid

    def delete_user(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            conn.commit()

    #----------------------------------------------------------------------
    # MusicHandler
    def get_random_song(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT song_id, title, artist, audio_file FROM music ORDER BY RANDOM() LIMIT 1")
            return cursor.fetchone()

    def get_chosen_song(self, music_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT song_id, title, artist, audio_file FROM music WHERE song_id = ?", (music_id,))
            return cursor.fetchone()

    def get_all_songs(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, artist, audio_file FROM music")
            return cursor.fetchall()

    #----------------------------------------------------------------------
    # TrainingPlanHandler
    def add_training_plan(self, user_id, training_date, goal, duration_seconds):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO training_plan (user_id, date, goal, duration_seconds)
                VALUES (?, ?, ?, ?)""", (user_id, training_date, goal, duration_seconds))
            conn.commit()
            return cursor.lastrowid

    def get_training_plan_from_date(self, user_id, date):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT goal, duration_seconds FROM training_plan
            WHERE user_id = ? AND "date" = ?""", (user_id,date))
            return cursor.fetchall()

    def get_training_plans(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT "date", goal, duration_seconds FROM training_plan 
                WHERE user_id = ? AND "date" > DATE('now') ORDER BY date ASC""", (user_id,))
            return cursor.fetchall()

    #------------------------------------------------------------------------------------
    # StatisticsHandler

    def add_statistics(self, user_id, training_date, repetitions, duration_seconds, comment, recording_file, tempo, step_accuracy, posture):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO statistics (user_id, date, repetitions, duration_seconds, comment, recording_file, tempo, step_accuracy, posture)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (user_id, training_date, repetitions, duration_seconds, comment, recording_file, tempo, step_accuracy, posture))
            conn.commit()
            return cursor.lastrowid

    def get_statistics_between_dates(self, user_id, date_from, date_to):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM statistics WHERE user_id = ? AND "date" BETWEEN ? AND ? ORDER BY s.date ASC""", (user_id, date_from, date_to))
            return cursor.fetchall()

    def get_statistics_from_date(self, user_id, date):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM statistics WHERE user_id = ? AND "date" = ?""", (user_id, date))
            return cursor.fetchall()

    def get_exercise_duration(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT SUM(duration_seconds) FROM statistics WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if result[0] is None:
                return 0
            return result[0]

    def get_statistics(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM statistics WHERE user_id = ? ORDER BY "date" ASC""", (user_id,))
            return cursor.fetchall()