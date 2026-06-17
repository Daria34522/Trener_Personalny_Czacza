from __future__ import annotations

import sqlite3
import tempfile
import unittest
from datetime import date
from datetime import timedelta
from pathlib import Path

from coach.database.DBHandler import DBHandler

SCHEMA = """
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL
);

CREATE TABLE music (
    song_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    audio_file TEXT NOT NULL,
    bpm REAL NOT NULL
);

CREATE TABLE training_plan (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    goal TEXT NOT NULL,
    duration_seconds INTEGER NOT NULL
);

CREATE TABLE statistics (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    repetitions INTEGER NOT NULL,
    duration_seconds INTEGER NOT NULL,
    comment TEXT,
    recording_file TEXT,
    tempo REAL,
    step_accuracy REAL,
    posture REAL
);
"""


class TestDBHandler(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.db_path = Path(self.temp_dir.name) / "test.sqlite"
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA)
        self.db: DBHandler = DBHandler(str(self.db_path))
        self.addCleanup(self.temp_dir.cleanup)

    def test_add_get_and_delete_user(self):
        user_id = self.db.add_user("ania")

        self.assertEqual(self.db.get_a_userid("ania"), user_id)
        self.assertEqual(self.db.get_a_user(user_id), "ania")
        self.assertEqual(self.db.get_all_users(), [(user_id, "ania")])

        self.db.delete_user(user_id)

        self.assertIsNone(self.db.get_a_user(user_id))
        self.assertIsNone(self.db.get_a_userid("ania"))
        self.assertEqual(self.db.get_all_users(), [])

    def test_training_plans_return_only_future_dates(self):
        user_id = self.db.add_user("bartek")
        today = date.today()
        past_day = (today - timedelta(days=1)).isoformat()
        first_future = (today + timedelta(days=1)).isoformat()
        second_future = (today + timedelta(days=2)).isoformat()

        self.db.add_training_plan(user_id, second_future, "drill", 30)
        self.db.add_training_plan(user_id, past_day, "old", 10)
        self.db.add_training_plan(user_id, first_future, "warmup", 20)

        plans = self.db.get_training_plans(user_id)

        self.assertEqual(
            plans,
            [
                (first_future, "warmup", 20),
                (second_future, "drill", 30),
            ],
        )
        self.assertEqual(
            self.db.get_training_plan_from_date(user_id, first_future),
            [("warmup", 20)],
        )

    def test_statistics_and_songs_queries(self):
        user_id = self.db.add_user("celina")
        self.db.add_statistics(
            user_id,
            "2026-06-10",
            12,
            45,
            "dobry trening",
            "recording.mp3",
            120.0,
            0.9,
            0.8,
        )
        self.db.add_statistics(
            user_id,
            "2026-06-12",
            15,
            60,
            "drugi trening",
            "recording-2.mp3",
            122.0,
            0.95,
            0.85,
        )

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO music (title, artist, audio_file, bpm) VALUES (?, ?, ?, ?)",
                ("Song A", "Artist A", "song-a.mp3", 118.0),
            )

        self.assertEqual(self.db.get_exercise_duration(user_id), 105)
        self.assertEqual(
            self.db.get_statistics_between_dates(user_id, "2026-06-09", "2026-06-11"),
            [("2026-06-10", 45)],
        )
        self.assertEqual(
            self.db.get_statistics_from_date(user_id, "2026-06-12"),
            [(15, 60, "drugi trening", 122.0, 0.95, 0.85)],
        )
        self.assertEqual(self.db.get_random_song(), 1)
        self.assertEqual(self.db.get_chosen_song(1), "song-a.mp3")
        self.assertEqual(self.db.get_song_tempo(1), 118.0)
        self.assertEqual(self.db.get_songid("Song A"), 1)
        self.assertEqual(
            self.db.get_all_songs(), [("Song A", "Artist A", "song-a.mp3")]
        )
