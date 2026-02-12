from models.database import get_connection
from models.employee import Employee

class Payroll:
    def __init__(self, id=None, employee_id=None, month=None, year=None,
                 base_salary=0, extra_hours_amount=0, total_afp=0, 
                 total_isss=0, other_discounts=0, net_salary=0):
        self.id = id
        self.employee_id = employee_id
        self.month = month
        self.year = year
        self.base_salary = base_salary
        self.extra_hours_amount = extra_hours_amount
        self.total_afp = total_afp
        self.total_isss = total_isss
        self.other_discounts = other_discounts
        self.net_salary = net_salary

    @staticmethod
    def calculate(employee, month, year, other_discounts=0):
        extra_hours_amount = employee.hours_extra * employee.hourly_rate
        gross_salary = employee.salary + extra_hours_amount
        
        total_afp = gross_salary * (employee.afp_rate / 100)
        total_isss = gross_salary * (employee.isss_rate / 100)
        
        net_salary = gross_salary - total_afp - total_isss - other_discounts
        
        return Payroll(
            employee_id=employee.id,
            month=month,
            year=year,
            base_salary=employee.salary,
            extra_hours_amount=extra_hours_amount,
            total_afp=total_afp,
            total_isss=total_isss,
            other_discounts=other_discounts,
            net_salary=net_salary
        )

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO payroll 
            (employee_id, month, year, base_salary, extra_hours_amount, 
             total_afp, total_isss, other_discounts, net_salary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.employee_id, self.month, self.year, self.base_salary,
              self.extra_hours_amount, self.total_afp, self.total_isss,
              self.other_discounts, self.net_salary))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_employee(employee_id, month, year):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM payroll 
            WHERE employee_id=? AND month=? AND year=?
        """, (employee_id, month, year))
        row = cursor.fetchone()
        conn.close()
        return Payroll(**dict(row)) if row else None

    @staticmethod
    def get_all_by_month(month, year):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, e.name, e.dpi, e.position 
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            WHERE p.month=? AND p.year=?
            ORDER BY e.name
        """, (month, year))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
