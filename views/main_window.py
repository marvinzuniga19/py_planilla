import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from models.database import init_db
from models.employee import Employee
from controllers.payroll import Payroll
from utils.export import ExportUtils


class MainWindow(ttk.Window):
    def __init__(self, themename):
        super().__init__(themename=themename)
        self.title("💼 Sistema de Nóminas - Nicaragua")
        self.geometry("1200x750")
        
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
        left_frame = ttk.Frame(self.tab_employees, padding=10)
        left_frame.pack(side=LEFT, fill=BOTH)
        
        header_frame = ttk.Frame(left_frame)
        header_frame.pack(fill=X, pady=(0, 15))
        ttk.Label(header_frame, text="👤 Gestión de Empleados", font=("Segoe UI", 16, "bold")).pack(side=LEFT)
        
        inner_form = ttk.LabelFrame(left_frame, text="  Datos del Empleado  ")
        inner_form.pack(fill=X, pady=(0, 10), padx=5)
        
        style_config = {"font": ("Segoe UI", 10)}
        
        ttk.Label(inner_form, text="Nombre:", **style_config).grid(row=0, column=0, sticky=W, pady=8, padx=5)
        self.entry_name = ttk.Entry(inner_form, width=35, font=("Segoe UI", 10))
        self.entry_name.grid(row=0, column=1, pady=8, padx=5, sticky=EW)
        
        ttk.Label(inner_form, text="DPI:", **style_config).grid(row=1, column=0, sticky=W, pady=8, padx=5)
        self.entry_dpi = ttk.Entry(inner_form, width=35, font=("Segoe UI", 10))
        self.entry_dpi.grid(row=1, column=1, pady=8, padx=5, sticky=EW)
        
        ttk.Label(inner_form, text="Cargo:", **style_config).grid(row=2, column=0, sticky=W, pady=8, padx=5)
        self.entry_position = ttk.Entry(inner_form, width=35, font=("Segoe UI", 10))
        self.entry_position.grid(row=2, column=1, pady=8, padx=5, sticky=EW)
        
        sep1 = ttk.Separator(inner_form, orient="horizontal")
        sep1.grid(row=3, column=0, columnspan=2, sticky=EW, pady=10)
        
        ttk.Label(inner_form, text="💰 Salario Base:", **style_config).grid(row=4, column=0, sticky=W, pady=8, padx=5)
        self.entry_salary = ttk.Entry(inner_form, width=35, font=("Segoe UI", 10))
        self.entry_salary.grid(row=4, column=1, pady=8, padx=5, sticky=EW)
        
        ttk.Label(inner_form, text="⏰ Horas Extras:", **style_config).grid(row=5, column=0, sticky=W, pady=8, padx=5)
        self.entry_hours_extra = ttk.Entry(inner_form, width=35, font=("Segoe UI", 10))
        self.entry_hours_extra.grid(row=5, column=1, pady=8, padx=5, sticky=EW)
        
        ttk.Label(inner_form, text="💵 Tarifa/Hora:", **style_config).grid(row=6, column=0, sticky=W, pady=8, padx=5)
        self.entry_hourly_rate = ttk.Entry(inner_form, width=35, font=("Segoe UI", 10))
        self.entry_hourly_rate.grid(row=6, column=1, pady=8, padx=5, sticky=EW)
        
        sep2 = ttk.Separator(inner_form, orient="horizontal")
        sep2.grid(row=7, column=0, columnspan=2, sticky=EW, pady=10)
        
        ttk.Label(inner_form, text="📊 Tasa INATEC %:", **style_config).grid(row=8, column=0, sticky=W, pady=8, padx=5)
        self.entry_afp = ttk.Entry(inner_form, width=35, font=("Segoe UI", 10))
        self.entry_afp.insert(0, "6.25")
        self.entry_afp.grid(row=8, column=1, pady=8, padx=5, sticky=EW)
        
        ttk.Label(inner_form, text="🏥 Tasa INSS %:", **style_config).grid(row=9, column=0, sticky=W, pady=8, padx=5)
        self.entry_isss = ttk.Entry(inner_form, width=35, font=("Segoe UI", 10))
        self.entry_isss.insert(0, "3.0")
        self.entry_isss.grid(row=9, column=1, pady=8, padx=5, sticky=EW)
        
        inner_form.columnconfigure(1, weight=1)
        
        btn_frame = ttk.Frame(inner_form)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=20)
        
        self.btn_save = ttk.Button(btn_frame, text="  Guardar  ", command=self.save_employee, bootstyle="success", cursor="hand2")
        self.btn_save.pack(side=LEFT, padx=8, pady=5)
        
        self.btn_new = ttk.Button(btn_frame, text="  Nuevo  ", command=self.clear_form, bootstyle="info", cursor="hand2")
        self.btn_new.pack(side=LEFT, padx=8, pady=5)
        
        self.btn_delete = ttk.Button(btn_frame, text="  Eliminar  ", command=self.delete_employee, bootstyle="danger", cursor="hand2")
        self.btn_delete.pack(side=LEFT, padx=8, pady=5)
        
        right_frame = ttk.Frame(self.tab_employees, padding=10)
        right_frame.pack(side=RIGHT, fill=BOTH, expand=YES)
        
        header_frame = ttk.Frame(right_frame)
        header_frame.pack(fill=X, pady=(0, 15))
        ttk.Label(header_frame, text="📋 Lista de Empleados", font=("Segoe UI", 14, "bold")).pack(side=LEFT)
        
        table_container = ttk.Frame(right_frame)
        table_container.pack(fill=BOTH, expand=YES)
        
        self.emp_table = Tableview(
            table_container,
            coldata=[
                {"text": "ID", "anchor": "center", "width": 50},
                {"text": "Nombre", "anchor": "w", "width": 180},
                {"text": "DPI", "anchor": "center", "width": 140},
                {"text": "Cargo", "anchor": "w", "width": 140},
                {"text": "Salario", "anchor": "e", "width": 120},
            ],
            rowdata=[],
            bootstyle="primary",
            height=18,
            paginated=True,
            on_select=self.on_employee_select,
            stripecolor=("lightgray", "#2a2a2a")
        )
        self.emp_table.pack(fill=BOTH, expand=YES, pady=(0, 10))
        
        status_frame = ttk.Frame(right_frame)
        status_frame.pack(fill=X)
        self.lbl_employee_count = ttk.Label(status_frame, text="Total: 0 empleados", font=("Segoe UI", 9), foreground="gray")
        self.lbl_employee_count.pack(side=LEFT)

    def build_payroll_tab(self):
        header_frame = ttk.Frame(self.tab_payroll, padding=15)
        header_frame.pack(fill=X)
        ttk.Label(header_frame, text="⚙ Cálculo de Nómina", font=("Segoe UI", 14, "bold")).pack(side=LEFT)
        
        control_frame = ttk.LabelFrame(self.tab_payroll, text="  Período  ")
        control_frame.pack(fill=X, padx=15, pady=(0, 10))
        
        date_frame = ttk.Frame(control_frame)
        date_frame.pack(side=LEFT)
        
        ttk.Label(date_frame, text="📅 Mes:", font=("Segoe UI", 10)).pack(side=LEFT, padx=5)
        self.payroll_month = ttk.Combobox(date_frame, values=list(range(1, 13)), width=5, state="readonly", font=("Segoe UI", 10))
        self.payroll_month.current(datetime.now().month - 1)
        self.payroll_month.pack(side=LEFT, padx=5)
        
        ttk.Label(date_frame, text="Año:", font=("Segoe UI", 10)).pack(side=LEFT, padx=5)
        current_year = datetime.now().year
        self.payroll_year = ttk.Combobox(date_frame, values=list(range(current_year - 5, current_year + 2)), width=8, state="readonly", font=("Segoe UI", 10))
        self.payroll_year.set(current_year)
        self.payroll_year.pack(side=LEFT, padx=5)
        
        self.btn_calculate = ttk.Button(control_frame, text="  Calcular Nómina  ", command=self.calculate_payroll, bootstyle="primary", cursor="hand2")
        self.btn_calculate.pack(side=LEFT, padx=20)
        
        table_frame = ttk.Frame(self.tab_payroll, padding=(15, 0, 15, 15))
        table_frame.pack(fill=BOTH, expand=YES)
        
        self.payroll_table = Tableview(
            table_frame,
            coldata=[
                {"text": "Nombre", "anchor": "w", "width": 180},
                {"text": "Salario Base", "anchor": "e", "width": 110},
                {"text": "Horas Extras", "anchor": "e", "width": 110},
                {"text": "INATEC", "anchor": "e", "width": 90},
                {"text": "INSS", "anchor": "e", "width": 90},
                {"text": "Otros", "anchor": "e", "width": 90},
                {"text": "Salario Neto", "anchor": "e", "width": 120},
            ],
            rowdata=[],
            bootstyle="success",
            height=18,
            paginated=True,
            stripecolor=("lightgray", "#2a2a2a")
        )
        self.payroll_table.pack(fill=BOTH, expand=YES)
        
        self.lbl_payroll_totals = ttk.Label(table_frame, text="", font=("Segoe UI", 10, "bold"), foreground="gray")
        self.lbl_payroll_totals.pack(side=BOTTOM, pady=(10, 0))

    def build_reports_tab(self):
        header_frame = ttk.Frame(self.tab_reports, padding=15)
        header_frame.pack(fill=X)
        ttk.Label(header_frame, text="📊 Reportes de Nómina", font=("Segoe UI", 14, "bold")).pack(side=LEFT)
        
        control_frame = ttk.LabelFrame(self.tab_reports, text="  Filtrar por Período  ")
        control_frame.pack(fill=X, padx=15, pady=(0, 10))
        
        date_frame = ttk.Frame(control_frame)
        date_frame.pack(side=LEFT)
        
        ttk.Label(date_frame, text="📅 Mes:", font=("Segoe UI", 10)).pack(side=LEFT, padx=5)
        self.report_month = ttk.Combobox(date_frame, values=list(range(1, 13)), width=5, state="readonly", font=("Segoe UI", 10))
        self.report_month.current(datetime.now().month - 1)
        self.report_month.pack(side=LEFT, padx=5)
        
        ttk.Label(date_frame, text="Año:", font=("Segoe UI", 10)).pack(side=LEFT, padx=5)
        current_year = datetime.now().year
        self.report_year = ttk.Combobox(date_frame, values=list(range(current_year - 5, current_year + 2)), width=8, state="readonly", font=("Segoe UI", 10))
        self.report_year.set(current_year)
        self.report_year.pack(side=LEFT, padx=5)
        
        self.btn_load_report = ttk.Button(control_frame, text="  Cargar Reporte  ", command=self.load_report, bootstyle="info", cursor="hand2")
        self.btn_load_report.pack(side=LEFT, padx=20)
        
        btn_export_frame = ttk.Frame(control_frame)
        btn_export_frame.pack(side=RIGHT, padx=10)
        
        self.btn_pdf = ttk.Button(btn_export_frame, text="  PDF  ", command=self.export_pdf, bootstyle="danger", cursor="hand2")
        self.btn_pdf.pack(side=LEFT, padx=5)
        
        self.btn_excel = ttk.Button(btn_export_frame, text="  Excel  ", command=self.export_excel, bootstyle="success", cursor="hand2")
        self.btn_excel.pack(side=LEFT, padx=5)
        
        report_frame = ttk.Frame(self.tab_reports, padding=(15, 0, 15, 15))
        report_frame.pack(fill=BOTH, expand=YES)
        
        self.report_table = Tableview(
            report_frame,
            coldata=[
                {"text": "Nombre", "anchor": "w", "width": 150},
                {"text": "DPI", "anchor": "center", "width": 120},
                {"text": "Cargo", "anchor": "w", "width": 120},
                {"text": "Salario Base", "anchor": "e", "width": 100},
                {"text": "Horas Extras", "anchor": "e", "width": 100},
                {"text": "INATEC", "anchor": "e", "width": 80},
                {"text": "INSS", "anchor": "e", "width": 80},
                {"text": "Otros", "anchor": "e", "width": 80},
                {"text": "Salario Neto", "anchor": "e", "width": 100},
            ],
            rowdata=[],
            bootstyle="warning",
            height=16,
            paginated=True,
            stripecolor=("lightgray", "#2a2a2a")
        )
        self.report_table.pack(fill=BOTH, expand=YES)

    def refresh_employees(self):
        employees = Employee.get_all()
        self.emp_table.delete_rows()
        count = len(employees)
        for emp in employees:
            self.emp_table.insert_row(values=(
                emp.id, emp.name, emp.dpi, emp.position, f"C$ {emp.salary:,.2f}"
            ))
        self.emp_table.load_table_data()
        self.lbl_employee_count.config(text=f"Total: {count} empleado{'s' if count != 1 else ''}")

    def on_employee_select(self, event):
        selection = self.emp_table.view.selection()
        if selection:
            item_iid = selection[0]
            emp_id = self.emp_table.view.item(item_iid)["values"][0]
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
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")

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
            if messagebox.askyesno("Confirmar", f"¿Eliminar a {self.current_employee.name}?"):
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
                f"C$ {payroll.base_salary:,.2f}",
                f"C$ {payroll.extra_hours_amount:,.2f}",
                f"C$ {payroll.total_afp:,.2f}",
                f"C$ {payroll.total_isss:,.2f}",
                f"C$ {payroll.other_discounts:,.2f}",
                f"C$ {payroll.net_salary:,.2f}"
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
                f"C$ {row['base_salary']:,.2f}",
                f"C$ {row['extra_hours_amount']:,.2f}",
                f"C$ {row['total_afp']:,.2f}",
                f"C$ {row['total_isss']:,.2f}",
                f"C$ {row['other_discounts']:,.2f}",
                f"C$ {row['net_salary']:,.2f}"
            ))
        self.report_table.load_table_data()

    def export_pdf(self):
        month = int(self.report_month.get())
        year = int(self.report_year.get())
        data = Payroll.get_all_by_month(month, year)
        
        if not data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
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
                messagebox.showinfo("Éxito", f"PDF exportado a:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")

    def export_excel(self):
        month = int(self.report_month.get())
        year = int(self.report_year.get())
        data = Payroll.get_all_by_month(month, year)
        
        if not data:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
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
                messagebox.showinfo("Éxito", f"Excel exportado a:\n{filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")
