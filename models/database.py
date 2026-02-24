import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "database.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dpi TEXT,
            position TEXT,
            salary REAL DEFAULT 0,
            hours_extra REAL DEFAULT 0,
            hourly_rate REAL DEFAULT 0,
            afp_rate REAL DEFAULT 2.0,
            isss_rate REAL DEFAULT 7.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payroll (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            base_salary REAL,
            extra_hours_amount REAL,
            total_afp REAL,
            total_isss REAL,
            other_discounts REAL DEFAULT 0,
            net_salary REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            UNIQUE(employee_id, month, year)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Base de datos creada en: {DB_PATH}")
