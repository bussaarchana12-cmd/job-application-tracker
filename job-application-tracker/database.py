"""
database.py
DatabaseManager class handling all persistent SQLite operations.
Demonstrates:
- Clean Separation of Concerns (Data layer independent of CLI/UI)
- Safe Parameterized Queries to eliminate SQL Injection
- Dynamic Schema Migration (Automatic priority column insertion if legacy DB exists)
- Context Management and Exception Handling
"""

import os
import sqlite3
from typing import Any, Dict, List, Optional
from models import ApplicationStatus, JobApplication, Priority


class DatabaseManager:
    """
    Manages SQLite database connections, schema migrations, and CRUD transactions.
    """

    DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    DEFAULT_DB_PATH = os.path.join(DEFAULT_DB_DIR, "jobs.db")

    def __init__(self, db_path: Optional[str] = None):
        """
        Initializes the DatabaseManager with a custom path or default 'data/jobs.db'.
        """
        self._db_path = db_path or self.DEFAULT_DB_PATH
        self._ensure_directory()
        self.init_db()

    @property
    def db_path(self) -> str:
        return self._db_path

    def _ensure_directory(self) -> None:
        """Ensures the directory containing the SQLite database file exists."""
        db_dir = os.path.dirname(self._db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """
        Creates and returns a connection configured with Row factory
        and foreign key constraints enabled.
        """
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        """
        Creates tables if they do not exist and applies schema migrations.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Primary Applications Table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company TEXT NOT NULL,
                    role TEXT NOT NULL,
                    location TEXT DEFAULT 'Remote',
                    application_date TEXT NOT NULL,
                    job_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority TEXT NOT NULL DEFAULT 'Medium',
                    salary_or_stipend TEXT DEFAULT 'Not Disclosed',
                    job_description TEXT DEFAULT '',
                    link TEXT DEFAULT '',
                    notes TEXT DEFAULT '',
                    interview_date TEXT DEFAULT 'None',
                    interview_rounds INTEGER DEFAULT 0,
                    interview_notes TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # Auto-migration: Check if 'priority' column exists (for backwards compatibility)
            cursor.execute("PRAGMA table_info(applications);")
            columns = [row["name"] for row in cursor.fetchall()]
            if "priority" not in columns:
                cursor.execute(
                    "ALTER TABLE applications ADD COLUMN priority TEXT NOT NULL DEFAULT 'Medium';"
                )

            # Indexes for high performance searches and sorting
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_company ON applications(company);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_status ON applications(status);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_priority ON applications(priority);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_app_date ON applications(application_date);")
            conn.commit()

    def add_application(self, app: JobApplication) -> int:
        """
        Inserts a new JobApplication record into the database using parameterized queries.
        Returns the newly created ID.
        """
        sql = """
            INSERT INTO applications (
                company, role, location, application_date, job_type, status, priority,
                salary_or_stipend, job_description, link, notes, interview_date,
                interview_rounds, interview_notes, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    app.company,
                    app.role,
                    app.location,
                    app.application_date,
                    app.job_type,
                    app.status,
                    app.priority,
                    app.salary_or_stipend,
                    app.job_description,
                    app.link,
                    app.notes,
                    app.interview_date,
                    app.interview_rounds,
                    app.interview_notes,
                    app.created_at,
                    app.updated_at,
                ),
            )
            conn.commit()
            new_id = cursor.lastrowid
            app.id = new_id
            return new_id

    def get_application_by_id(self, app_id: int) -> Optional[JobApplication]:
        """
        Fetches an individual application by its unique integer ID.
        """
        sql = "SELECT * FROM applications WHERE id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (app_id,))
            row = cursor.fetchone()
            if row:
                return JobApplication.from_row(row)
        return None

    def get_all_applications(
        self, sort_by: str = "id", order: str = "ASC"
    ) -> List[JobApplication]:
        """
        Retrieves all job applications with customizable sorting:
        - 'priority': Sorts by High -> Medium -> Low (or reverse)
        - 'company': Alphabetical company name
        - 'date': Application date
        - 'status': Application status
        - 'id': Application ID
        """
        order_dir = "DESC" if order.upper() == "DESC" else "ASC"

        if sort_by == "priority":
            # High (1) -> Medium (2) -> Low (3)
            sql = f"""
                SELECT * FROM applications
                ORDER BY CASE priority
                    WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                    ELSE 4
                END {order_dir}, id DESC
            """
        elif sort_by in ("date", "application_date"):
            sql = f"SELECT * FROM applications ORDER BY application_date {order_dir}, id DESC"
        elif sort_by == "company":
            sql = f"SELECT * FROM applications ORDER BY company COLLATE NOCASE {order_dir}, id DESC"
        elif sort_by == "role":
            sql = f"SELECT * FROM applications ORDER BY role COLLATE NOCASE {order_dir}, id DESC"
        elif sort_by == "status":
            sql = f"SELECT * FROM applications ORDER BY status {order_dir}, id DESC"
        else:
            sql = f"SELECT * FROM applications ORDER BY id {order_dir}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [JobApplication.from_row(row) for row in rows]

    def search_applications(
        self, query: str, search_field: str = "company"
    ) -> List[JobApplication]:
        """
        Searches job applications by company, role, status, or across all major fields.
        Uses LIKE with % wildcard and parameterized query.
        """
        search_pattern = f"%{query.strip()}%"
        field = search_field.lower().strip()

        if field == "company":
            sql = "SELECT * FROM applications WHERE company LIKE ? ORDER BY id DESC"
            params = (search_pattern,)
        elif field == "role":
            sql = "SELECT * FROM applications WHERE role LIKE ? ORDER BY id DESC"
            params = (search_pattern,)
        elif field == "status":
            sql = "SELECT * FROM applications WHERE status LIKE ? ORDER BY id DESC"
            params = (search_pattern,)
        elif field == "priority":
            sql = "SELECT * FROM applications WHERE priority LIKE ? ORDER BY id DESC"
            params = (search_pattern,)
        else:  # All fields
            sql = """
                SELECT * FROM applications
                WHERE company LIKE ? OR role LIKE ? OR location LIKE ? OR notes LIKE ? OR status LIKE ?
                ORDER BY id DESC
            """
            params = (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return [JobApplication.from_row(row) for row in rows]

    def update_application(self, app_id: int, updates: Dict[str, Any]) -> bool:
        """
        Updates specific columns of an application record safely using parameterized SQL.
        """
        if not updates:
            return False

        allowed_fields = {
            "company",
            "role",
            "location",
            "application_date",
            "job_type",
            "status",
            "priority",
            "salary_or_stipend",
            "job_description",
            "link",
            "notes",
            "interview_date",
            "interview_rounds",
            "interview_notes",
        }

        clean_updates = {k: v for k, v in updates.items() if k in allowed_fields}
        if not clean_updates:
            return False

        # Set updated_at timestamp automatically
        set_clauses = [f"{col} = ?" for col in clean_updates.keys()]
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        sql = f"UPDATE applications SET {', '.join(set_clauses)} WHERE id = ?"
        params = list(clean_updates.values()) + [app_id]

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount > 0

    def delete_application(self, app_id: int) -> bool:
        """
        Permanently deletes an application by ID.
        """
        sql = "DELETE FROM applications WHERE id = ?"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (app_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_statistics(self) -> Dict[str, Any]:
        """
        Aggregates application data for the dashboard.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Total count
            cursor.execute("SELECT COUNT(*) AS total FROM applications")
            total = cursor.fetchone()["total"]

            # Status breakdown
            cursor.execute(
                """
                SELECT status, COUNT(*) AS count
                FROM applications
                GROUP BY status
                """
            )
            status_counts = {row["status"]: row["count"] for row in cursor.fetchall()}

            # Priority breakdown (High, Medium, Low)
            cursor.execute(
                """
                SELECT priority, COUNT(*) AS count
                FROM applications
                GROUP BY priority
                """
            )
            priority_counts = {row["priority"]: row["count"] for row in cursor.fetchall()}

            # Job Type breakdown
            cursor.execute(
                """
                SELECT job_type, COUNT(*) AS count
                FROM applications
                GROUP BY job_type
                """
            )
            job_type_counts = {row["job_type"]: row["count"] for row in cursor.fetchall()}

            # Specific status tallies
            applied = status_counts.get(ApplicationStatus.APPLIED.value, 0)
            interviewing = status_counts.get(ApplicationStatus.INTERVIEW_SCHEDULED.value, 0)
            selected = status_counts.get(ApplicationStatus.SELECTED.value, 0)
            rejected = status_counts.get(ApplicationStatus.REJECTED.value, 0)
            pending = status_counts.get(ApplicationStatus.PENDING.value, 0)

            # Calculation of metrics
            success_rate = (selected / total * 100.0) if total > 0 else 0.0
            interview_rate = ((interviewing + selected) / total * 100.0) if total > 0 else 0.0

            return {
                "total": total,
                "applied": applied,
                "interviewing": interviewing,
                "selected": selected,
                "rejected": rejected,
                "pending": pending,
                "status_breakdown": status_counts,
                "priority_breakdown": {
                    Priority.HIGH.value: priority_counts.get(Priority.HIGH.value, 0),
                    Priority.MEDIUM.value: priority_counts.get(Priority.MEDIUM.value, 0),
                    Priority.LOW.value: priority_counts.get(Priority.LOW.value, 0),
                },
                "job_type_breakdown": job_type_counts,
                "success_rate": round(success_rate, 1),
                "interview_rate": round(interview_rate, 1),
            }
