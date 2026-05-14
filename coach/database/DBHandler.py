import sqlite3
import datetime


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
            cursor.execute("SELECT user_id, username, profile_photo FROM users")
            return cursor.fetchall()

    def add_user(self, username, profile_photo=None):
        created_at = datetime.now().strftime("%Y-%m-%d")
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, profile_photo, created_at) VALUES (?, ?, ?)", (username, profile_photo, created_at))
            conn.commit()

    def delete_user(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id))
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

    def get_all_song(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT song_id, title, artist, audio_file FROM music")
            return cursor.fetchall()

    #----------------------------------------------------------------------
    # TrainingPlanHandler
    def add_training_plan(self, user_id, training_date, goal, duration_minutes):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO training_plan (user_id, date, goal, duration_minutes)
                VALUES (?, ?, ?, ?)""", (user_id, training_date, goal, duration_minutes))
            conn.commit()

    def get_training_plans(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT training_plan_id, date, goal, duration_minutes
                FROM training_plan WHERE user_id = ?
                ORDER BY date DESC""", (user_id,))
            return cursor.fetchall()

    #------------------------------------------------------------------------------------
    # StatisticsHandler
    def add_exercise_quality(self, tempo, step_accuracy, posture):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO exercise_quality (tempo, step_accuracy, posture)
                VALUES (?, ?, ?)""", (tempo, step_accuracy, posture))
            conn.commit()
            return cursor.lastrowid

    def add_statistics(self, user_id, quality_id, training_date, repetitions, duration_minutes, comment, recording_filename):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO statistics (
            user_id, quality_id, date, repetitions, duration_minutes, comment, recording_filename
            ) VALUES (?, ?, ?, ?, ?, ?, ?)""", (
            user_id, quality_id, training_date, repetitions, duration_minutes, comment, recording_filename
            ))
            conn.commit()
            return cursor.lastrowid

    def get_statistics(self, user_id):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT 
            s.statistics_id, s.date, s.repetitions, s.duration_minutes, s.comment, s.recording_filename,
            q.tempo, q.step_accuracy, q.posture FROM statistics s
            LEFT JOIN exercise_quality q ON s.quality_id = q.exercise_quality_id
            WHERE s.user_id = ? ORDER BY s.date DESC
            """, (user_id,))
            return cursor.fetchall()
def main():
    print("Welcome to DBHandler")


if __name__ == "__main__":
    main()
