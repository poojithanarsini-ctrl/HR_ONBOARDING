import sqlite3
from pathlib import Path

# Find the main project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Store the database inside the data folder
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "hr_onboarding.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create the database tables if they do not exist."""
    with get_connection() as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'employee'
                    CHECK (role IN ('employee', 'hr_admin')),
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS onboarding_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                description TEXT DEFAULT '',
                is_active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS employee_task_progress (
                user_id INTEGER NOT NULL,
                task_id INTEGER NOT NULL,
                is_completed INTEGER NOT NULL DEFAULT 0
                    CHECK (is_completed IN (0, 1)),
                completed_at TEXT,
                PRIMARY KEY (user_id, task_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (task_id) REFERENCES onboarding_tasks(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL UNIQUE,
                category TEXT DEFAULT 'General',
                status TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN (
                        'pending', 'approved', 'inactive', 'failed'
                    )),
                uploaded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS chat_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL,
                role TEXT NOT NULL
                    CHECK (role IN ('user', 'assistant')),
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES chat_sessions(id)
                    ON DELETE CASCADE
            );
        """)


def seed_onboarding_tasks():
    """Add initial onboarding tasks without creating duplicates."""
    tasks = [
        (
            "Read the employee handbook",
            "Understand the main company policies."
        ),
        (
            "Review the code of conduct",
            "Learn expected workplace behavior."
        ),
        (
            "Understand attendance and working hours",
            "Review the approved attendance policy."
        ),
        (
            "Review the leave application procedure",
            "Learn how to submit a leave request."
        ),
        (
            "Read IT security guidelines",
            "Understand safe use of company systems."
        ),
        (
            "Find the HR support contact",
            "Identify where to ask HR questions."
        ),
    ]

    with get_connection() as connection:
        connection.executemany(
            """
            INSERT OR IGNORE INTO onboarding_tasks
                (title, description)
            VALUES (?, ?)
            """,
            tasks
        )


def get_onboarding_tasks():
    """Return all active onboarding tasks."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, description
            FROM onboarding_tasks
            WHERE is_active = 1
            ORDER BY id
            """
        ).fetchall()

    return [dict(row) for row in rows]


def set_task_progress(user_id, task_id, completed):
    """Save task progress for a specific employee."""
    with get_connection() as connection:
        # Confirm that the employee exists
        user = connection.execute(
            "SELECT id FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()

        if user is None:
            raise ValueError(
                "Employee account not found. Please log in again."
            )

        # Confirm that the task exists and is active
        task = connection.execute(
            """
            SELECT id FROM onboarding_tasks
            WHERE id = ? AND is_active = 1
            """,
            (task_id,)
        ).fetchone()

        if task is None:
            raise ValueError(
                "Onboarding task not found. Please refresh the page."
            )

        # Insert progress or update the existing record
        connection.execute(
            """
            INSERT INTO employee_task_progress
                (user_id, task_id, is_completed, completed_at)
            VALUES (?, ?, ?, CASE
                WHEN ? = 1 THEN CURRENT_TIMESTAMP
                ELSE NULL
            END)
            ON CONFLICT(user_id, task_id)
            DO UPDATE SET
                is_completed = excluded.is_completed,
                completed_at = CASE
                    WHEN excluded.is_completed = 1
                    THEN CURRENT_TIMESTAMP
                    ELSE NULL
                END
            """,
            (
                user_id,
                task_id,
                int(completed),
                int(completed)
            )
        )


def get_employee_progress(user_id):
    """Return tasks and their completion status for one employee."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                t.id,
                t.title,
                t.description,
                COALESCE(p.is_completed, 0) AS is_completed
            FROM onboarding_tasks AS t
            LEFT JOIN employee_task_progress AS p
                ON p.task_id = t.id AND p.user_id = ?
            WHERE t.is_active = 1
            ORDER BY t.id
            """,
            (user_id,)
        ).fetchall()

    return [dict(row) for row in rows]


def get_database_path():
    """Return the location of the database file."""
    return str(DB_PATH)


if __name__ == "__main__":
    initialize_database()
    seed_onboarding_tasks()

    print("Database initialized successfully!")
    print(f"Database location: {get_database_path()}")
    print(f"Onboarding tasks added: {len(get_onboarding_tasks())}")