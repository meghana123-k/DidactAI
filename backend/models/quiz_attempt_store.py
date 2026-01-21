import os
import json
import uuid
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")  # postgres://user:pass@host:port/dbname


def get_conn():
    return psycopg2.connect(DB_URL)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id UUID PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            mode TEXT,
            source TEXT,
            concepts JSONB,
            answers JSONB,
            evaluation JSONB
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def save_quiz_attempt(meta: dict, answers: dict, evaluation: dict) -> str:
    attempt_id = str(uuid.uuid4())

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO quiz_attempts
        (id, mode, source, concepts, answers, evaluation)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        attempt_id,
        meta.get("mode"),
        meta.get("source"),
        Json(meta.get("concepts", [])),
        Json(answers),
        Json(evaluation)
    ))

    conn.commit()
    cur.close()
    conn.close()

    return attempt_id


def get_attempt(attempt_id: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, created_at, mode, source, concepts, answers, evaluation
        FROM quiz_attempts
        WHERE id = %s
    """, (attempt_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "attempt_id": row[0],
        "created_at": row[1],
        "mode": row[2],
        "source": row[3],
        "concepts": row[4],
        "answers": row[5],
        "evaluation": row[6],
    }
