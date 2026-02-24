from models.database import get_connection

class Employee:
    def __init__(self, id=None, name="", dpi="", position="", salary=0, 
                 hours_extra=0, hourly_rate=0, afp_rate=2.0, isss_rate=7.0):
        self.id = id
        self.name = name
        self.dpi = dpi
        self.position = position
        self.salary = salary
        self.hours_extra = hours_extra
        self.hourly_rate = hourly_rate
        self.afp_rate = afp_rate
        self.isss_rate = isss_rate

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id:
            cursor.execute("""
                UPDATE employees 
                SET name=?, dpi=?, position=?, salary=?, hours_extra=?, 
                    hourly_rate=?, afp_rate=?, isss_rate=?
                WHERE id=?
            """, (self.name, self.dpi, self.position, self.salary, 
                  self.hours_extra, self.hourly_rate, self.afp_rate, 
                  self.isss_rate, self.id))
        else:
            cursor.execute("""
                INSERT INTO employees (name, dpi, position, salary, hours_extra, 
                                       hourly_rate, afp_rate, isss_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.name, self.dpi, self.position, self.salary, 
                  self.hours_extra, self.hourly_rate, self.afp_rate, self.isss_rate))
            self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, dpi, position, salary, hours_extra, hourly_rate, afp_rate, isss_rate FROM employees ORDER BY name")
        rows = cursor.fetchall()
        conn.close()
        return [Employee(**dict(row)) for row in rows]

    @staticmethod
    def get_by_id(employee_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, dpi, position, salary, hours_extra, hourly_rate, afp_rate, isss_rate FROM employees WHERE id=?", (employee_id,))
        row = cursor.fetchone()
        conn.close()
        return Employee(**dict(row)) if row else None

    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employees WHERE id=?", (self.id,))
            conn.commit()
            conn.close()
