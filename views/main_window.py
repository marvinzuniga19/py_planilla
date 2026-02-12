import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import tkinter as tk
from datetime import datetime

from models.database import init_db
from models.employee import Employee
from controllers.payroll import Payroll
from utils.export import ExportUtils


class MainWindow(ttk.Window):
    def __init__(self, themename):
        super().__init__(themename=themename)
        self.title("Sistema de Nóminas")
        self.geometry("1100x700")
        
        init_db()
        self.current_employee = None
        
        self.create_widgets()
        self.refresh_employees()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.tab_employees = ttk.Frame(notebook)
        self.tab_payroll = ttk.Frame(notebook)
        self.tab_reports = ttk.Frame(notebook)
        
        notebook.add(self.tab_employees, text="  Empleados  ")
        notebook.add(self.tab_payroll, text="  Nómina  ")
        notebook.add(self.tab_reports, text="  Reportes  ")
        
        self.build_employees_tab()
        self.build_payroll_tab()
        self.build_reports_tab()

    def build_employees_tab(self):
        left_frame = ttk.Frame(self.tab_employees)
        left_frame.pack(side=LEFT, fill=BOTH, padx=10, pady=10)
        
        inner_form = ttk.LabelFrame(left_frame, text="Datos del Empleado")
        inner_form.pack(fill=X, pady=5, padx=5)
        
        inner_form = ttk.Frame(inner_form, padding=15)
        inner_form.pack(fill=X)
        
        ttk.Label(inner_form, text="Nombre:").grid(row=0, column=0, sticky=W, pady=5)
        self.entry_name = ttk.Entry(inner_form, width=30)
        self.entry_name.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(inner_form, text="DPI:").grid(row=1, column=0, sticky=W, pady=5)
        self.entry_dpi = ttk.Entry(inner_form, width=30)
        self.entry_dpi.grid(row=1, column=1, pady=5, padx=5)
        
        ttk.Label(inner_form, text="Cargo:").grid(row=2, column=0, sticky=W, pady=5)
        self.entry_position = ttk.Entry(inner_form, width=30)
        self.entry_position.grid(row=2, column=1, pady=5, padx=5)
        
        ttk.Label(inner_form, text="Salario Base:").grid(row=3, column=0, sticky=W, pady=5)
        self.entry_salary = ttk.Entry(inner_form, width=30)
        self.entry_salary.grid(row=3, column=1, pady=5, padx=5)
        
        ttk.Label(inner_form, text="Horas Extras:").grid(row=4, column=0, sticky=W, pady=5)
        self.entry_hours_extra = ttk.Entry(inner_form, width=30)
        self.entry_hours_extra.grid(row=4, column=1, pady=5, padx=5)
        
        ttk.Label(inner_form, text="Tarifa/Hora:").grid(row=5, column=0, sticky=W, pady=5)
        self.entry_hourly_rate = ttk.Entry(inner_form, width=30)
        self.entry_hourly_rate.grid(row=5, column=1, pady=5, padx=5)
        
        ttk.Label(inner_form, text="Tasa AFP %:").grid(row=6, column=0, sticky=W, pady=5)
        self.entry_afp = ttk.Entry(inner_form, width=30)
        self.entry_afp.insert(0, "6.25")
        self.entry_afp.grid(row=6, column=1, pady=5, padx=5)
        
        ttk.Label(inner_form, text="Tasa ISSS %:").grid(row=7, column=0, sticky=W, pady=5)
        self.entry_isss = ttk.Entry(inner_form, width=30)
        self.entry_isss.insert(0, "3.0")
        self.entry_isss.grid(row=7, column=1, pady=5, padx=5)
        
        btn_frame = ttk.Frame(inner_form)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=15)
        
        self.btn_save = ttk.Button(btn_frame, text="Guardar", command=self.save_employee, bootstyle="success")
        self.btn_save.pack(side=LEFT, padx=5)
        
        self.btn_new = ttk.Button(btn_frame, text="Nuevo", command=self.clear_form, bootstyle="secondary")
        self.btn_new.pack(side=LEFT, padx=5)
        
        self.btn_delete = ttk.Button(btn_frame, text="Eliminar", command=self.delete_employee, bootstyle="danger")
        self.btn_delete.pack(side=LEFT, padx=5)
        
        right_frame = ttk.Frame(self.tab_employees)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=10, pady=10)
        
        self.emp_table = Tableview(
            right_frame,
            coldata=[
                {"text": "ID", "anchor": "center", "width": 50},
                {"text": "Nombre", "anchor": "w", "width": 150},
                {"text": "DPI", "anchor": "center", "width": 120},
                {"text": "Cargo", "anchor": "w", "width": 120},
                {"text": "Salario", "anchor": "e", "width": 100},
            ],
            rowdata=[],
            bootstyle="primary",
            height=20,
            paginated=True,
            on_select=self.on_employee_select
        )
        self.emp_table.pack(fill=BOTH, expand=YES)

    def build_payroll_tab(self):
        control_frame = ttk.Frame(self.tab_payroll)
        control_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Mes:").pack(side=LEFT, padx=5)
        self.payroll_month = ttk.Combobox(control_frame, values=list(range(1, 13)), width=5, state="readonly")
        self.payroll_month.current(datetime.now().month - 1)
        self.payroll_month.pack(side=LEFT, padx=5)
        
        ttk.Label(control_frame, text="Año:").pack(side=LEFT, padx=5)
        current_year = datetime.now().year
        self.payroll_year = ttk.Combobox(control_frame, values=list(range(current_year - 5, current_year + 2)), width=8, state="readonly")
        self.payroll_year.set(current_year)
        self.payroll_year.pack(side=LEFT, padx=5)
        
        self.btn_calculate = ttk.Button(control_frame, text="Calcular Nómina", command=self.calculate_payroll, bootstyle="primary")
        self.btn_calculate.pack(side=LEFT, padx=15)
        
        table_frame = ttk.Frame(self.tab_payroll)
        table_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        self.payroll_table = Tableview(
            table_frame,
            coldata=[
                {"text": "Nombre", "anchor": "w", "width": 150},
                {"text": "Salario Base", "anchor": "e", "width": 100},
                {"text": "Horas Extras", "anchor": "e", "width": 100},
                {"text": "AFP", "anchor": "e", "width": 80},
                {"text": "ISSS", "anchor": "e", "width": 80},
                {"text": "Otros", "anchor": "e", "width": 80},
                {"text": "Salario Neto", "anchor": "e", "width": 100},
            ],
            rowdata=[],
            bootstyle="success",
            height=20,
            paginated=True
        )
        self.payroll_table.pack(fill=BOTH, expand=YES)

    def build_reports_tab(self):
        control_frame = ttk.Frame(self.tab_reports)
        control_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(control_frame, text="Mes:").pack(side=LEFT, padx=5)
        self.report_month = ttk.Combobox(control_frame, values=list(range(1, 13)), width=5, state="readonly")
        self.report_month.current(datetime.now().month - 1)
        self.report_month.pack(side=LEFT, padx=5)
        
        ttk.Label(control_frame, text="Año:").pack(side=LEFT, padx=5)
        current_year = datetime.now().year
        self.report_year = ttk.Combobox(control_frame, values=list(range(current_year - 5, current_year + 2)), width=8, state="readonly")
        self.report_year.set(current_year)
        self.report_year.pack(side=LEFT, padx=5)
        
        self.btn_load_report = ttk.Button(control_frame, text="Cargar Reporte", command=self.load_report, bootstyle="info")
        self.btn_load_report.pack(side=LEFT, padx=15)
        
        btn_export_frame = ttk.Frame(control_frame)
        btn_export_frame.pack(side=RIGHT, padx=10)
        
        self.btn_pdf = ttk.Button(btn_export_frame, text="Exportar PDF", command=self.export_pdf, bootstyle="danger")
        self.btn_pdf.pack(side=LEFT, padx=5)
        
        self.btn_excel = ttk.Button(btn_export_frame, text="Exportar Excel", command=self.export_excel, bootstyle="success")
        self.btn_excel.pack(side=LEFT, padx=5)
        
        report_frame = ttk.Frame(self.tab_reports)
        report_frame.pack(fill=BOTH, expand=YES, padx=10, pady=5)
        
        self.report_table = Tableview(
            report_frame,
            coldata=[
                {"text": "Nombre", "anchor": "w", "width": 120},
                {"text": "DPI", "anchor": "center", "width": 100},
                {"text": "Cargo", "anchor": "w", "width": 100},
                {"text": "Salario Base", "anchor": "e", "width": 90},
                {"text": "Horas Extras", "anchor": "e", "width": 90},
                {"text": "AFP", "anchor": "e", "width": 70},
                {"text": "ISSS", "anchor": "e", "width": 70},
                {"text": "Otros", "anchor": "e", "width": 70},
                {"text": "Salario Neto", "anchor": "e", "width": 90},
            ],
            rowdata=[],
            bootstyle="warning",
            height=20,
            paginated=True
        )
        self.report_table.pack(fill=BOTH, expand=YES)

    def refresh_employees(self):
        employees = Employee.get_all()
        self.emp_table.delete_rows()
        for emp in employees:
            self.emp_table.insert_row(values=(
                emp.id, emp.name, emp.dpi, emp.position, f"${emp.salary:.2f}"
            ))
        self.emp_table.load_table_data()

    def on_employee_select(self, event):
        selection = self.emp_table.get_selection()
        if selection:
            item = selection[0]
            emp_id = item.values[0]
            employee = Employee.get_by_id(emp_id)
            if employee:
                self.current_employee = employee
                self.entry_name.delete(0, END)
                self.entry_name.insert(0, employee.name)
                self.entry_dpi.delete(0, END)
                self.entry_dpi.insert(0, employee.dpi or "")
                self.entry_position.delete(0, END)
                self.entry_position.insert(0, employee.position or "")
                self.entry_salary.delete(0, END)
                self.entry_salary.insert(0, str(employee.salary))
                self.entry_hours_extra.delete(0, END)
                self.entry_hours_extra.insert(0, str(employee.hours_extra))
                self.entry_hourly_rate.delete(0, END)
                self.entry_hourly_rate.insert(0, str(employee.hourly_rate))
                self.entry_afp.delete(0, END)
                self.entry_afp.insert(0, str(employee.afp_rate))
                self.entry_isss.delete(0, END)
                self.entry_isss.insert(0, str(employee.isss_rate))

    def save_employee(self):
        try:
            employee = Employee(
                id=self.current_employee.id if self.current_employee else None,
                name=self.entry_name.get(),
                dpi=self.entry_dpi.get(),
                position=self.entry_position.get(),
                salary=float(self.entry_salary.get() or 0),
                hours_extra=float(self.entry_hours_extra.get() or 0),
                hourly_rate=float(self.entry_hourly_rate.get() or 0),
                afp_rate=float(self.entry_afp.get() or 6.25),
                isss_rate=float(self.entry_isss.get() or 3.0)
            )
            employee.save()
            self.clear_form()
            self.refresh_employees()
        except ValueError as e:
            ttk.MessageBox.show_error("Error", "Por favor ingrese valores numéricos válidos")

    def clear_form(self):
        self.current_employee = None
        self.entry_name.delete(0, END)
        self.entry_dpi.delete(0, END)
        self.entry_position.delete(0, END)
        self.entry_salary.delete(0, END)
        self.entry_hours_extra.delete(0, END)
        self.entry_hourly_rate.delete(0, END)
        self.entry_afp.delete(0, END)
        self.entry_afp.insert(0, "6.25")
        self.entry_isss.delete(0, END)
        self.entry_isss.insert(0, "3.0")

    def delete_employee(self):
        if self.current_employee:
            if ttk.MessageBox.yesno("Confirmar", f"¿Eliminar a {self.current_employee.name}?"):
                self.current_employee.delete()
                self.clear_form()
                self.refresh_employees()

    def calculate_payroll(self):
        month = int(self.payroll_month.get())
        year = int(self.payroll_year.get())
        
        employees = Employee.get_all()
        
        self.payroll_table.delete_rows()
        
        for emp in employees:
            payroll = Payroll.calculate(emp, month, year)
            payroll.save()
            
            self.payroll_table.insert_row(values=(
                emp.name,
                f"${payroll.base_salary:.2f}",
                f"${payroll.extra_hours_amount:.2f}",
                f"${payroll.total_afp:.2f}",
                f"${payroll.total_isss:.2f}",
                f"${payroll.other_discounts:.2f}",
                f"${payroll.net_salary:.2f}"
            ))
        self.payroll_table.load_table_data()

    def load_report(self):
        month = int(self.report_month.get())
        year = int(self.report_year.get())
        
        data = Payroll.get_all_by_month(month, year)
        
        self.report_table.delete_rows()
        
        for row in data:
            self.report_table.insert_row(values=(
                row['name'],
                row['dpi'],
                row['position'],
                f"${row['base_salary']:.2f}",
                f"${row['extra_hours_amount']:.2f}",
                f"${row['total_afp']:.2f}",
                f"${row['total_isss']:.2f}",
                f"${row['other_discounts']:.2f}",
                f"${row['net_salary']:.2f}"
            ))
        self.report_table.load_table_data()

    def export_pdf(self):
        month = int(self.report_month.get())
        year = int(self.report_year.get())
        data = Payroll.get_all_by_month(month, year)
        
        if not data:
            ttk.MessageBox.show_warning("Advertencia", "No hay datos para exportar")
            return
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=f"nomina_{month}_{year}.pdf"
        )
        
        if filename:
            try:
                ExportUtils.export_to_pdf(data, filename)
                ttk.MessageBox.show_info("Éxito", f"PDF exportado a:\n{filename}")
            except Exception as e:
                ttk.MessageBox.show_error("Error", f"Error al exportar: {str(e)}")

    def export_excel(self):
        month = int(self.report_month.get())
        year = int(self.report_year.get())
        data = Payroll.get_all_by_month(month, year)
        
        if not data:
            ttk.MessageBox.show_warning("Advertencia", "No hay datos para exportar")
            return
        
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile=f"nomina_{month}_{year}.xlsx"
        )
        
        if filename:
            try:
                ExportUtils.export_to_excel(data, filename)
                ttk.MessageBox.show_info("Éxito", f"Excel exportado a:\n{filename}")
            except Exception as e:
                ttk.MessageBox.show_error("Error", f"Error al exportar: {str(e)}")
