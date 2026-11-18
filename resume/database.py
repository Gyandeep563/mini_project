
import sqlite3
from datetime import datetime

DB_NAME = "resumes.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resume_db (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            filename TEXT,
            job_role TEXT,
            pdf_data BLOB,
            analysis TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_resume(candidate_name, filename, job_role, pdf_data, analysis):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO resume_db
        (candidate_name, filename, job_role, pdf_data, analysis, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        candidate_name,
        filename,
        job_role,
        sqlite3.Binary(pdf_data),
        analysis,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_resumes():
    # conn = get_connection()
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resumes")
    resumes = cursor.fetchall()

    conn.close()
    return resumes


def get_resume(resume_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM resume_db WHERE id = ?
    """, (resume_id,))

    data = cursor.fetchone()
    conn.close()

    return data
