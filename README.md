# Sistema de Nóminas - Nicaragua

Aplicación de escritorio para la gestión de nómina de empleados con deducciones INATEC e INSS propias de Nicaragua.

## Características

- **Gestión de Empleados**: Agregar, editar, eliminar y listar empleados
- **Cálculo de Nómina**: Cálculo automático de salario neto con deducciones
- **Deducciones Configurables**: INATEC y INSS con tasas personalizadas por empleado
- **Horas Extras**: Registro y cálculo de horas extras con tarifa configurable
- **Reportes**: Dashboard con métricas totales por período
- **Exportación**: Exportar nóminas a PDF y Excel
- **Moneda**: Córdoba Nicaragüense (C$)

## Requisitos

- Python 3.10+
- SQLite (incluido en Python)

## Instalación

1. Crear entorno virtual:
```bash
python -m venv env
```

2. Activar entorno virtual:
```bash
# Linux/Mac
source env/bin/activate

# Windows
env\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecutar la aplicación:
```bash
python main.py
```

### Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| Ctrl+N | Nuevo empleado |
| Ctrl+S | Guardar empleado |
| Ctrl+F | Buscar empleado |
| Delete | Eliminar empleado |

## Estructura del Proyecto

```
python_planillas/
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
├── models/
│   ├── database.py       # Configuración de SQLite
│   └── employee.py       # Modelo de empleado
├── views/
│   └── main_window.py    # Interfaz gráfica
├── controllers/
│   └── payroll.py        # Lógica de nómina
└── utils/
    └── export.py         # Exportación PDF/Excel
```

## Base de Datos

El sistema utiliza SQLite. La base de datos se crea automáticamente al iniciar la aplicación en `database.db`.

### Tablas

**employees**: Empleados
- id, name, dpi, position, salary, hours_extra, hourly_rate, afp_rate (INATEC), isss_rate (INSS)

**payroll**: Nómina por período
- id, employee_id, month, year, base_salary, extra_hours_amount, total_afp, total_isss, other_discounts, net_salary

## Cálculo de Nómina

```
Salario Bruto = Salario Base + (Horas Extras × Tarifa/Hora)
Deducción INATEC = Salario Bruto × (Tasa INATEC / 100)
Deducción INSS = Salario Bruto × (Tasa INSS / 100)
Salario Neto = Salario Bruto - INATEC - INSS - Otros Descuentos
```

### Valores por Defecto

- **Tasa INATEC**: 6.25%
- **Tasa INSS**: 3.0%

Estos valores pueden ser configurados individualmente por cada empleado.

## Interfaz

La aplicación cuenta con tres pestañas:

1. **Empleados**: Gestión de empleados con formulario y tabla filtrable
2. **Nómina**: Cálculo mensual con vista de deducciones y salarios netos
3. **Reportes**: Vista de datos históricos por período con exportación

## Exportación

Los reportes exportados incluyen:
- Nombre del empleado
- DPI
- Cargo
- Salario base
- Horas extras (monto)
- Deducción INATEC
- Deducción INSS
- Otros descuentos
- Salario neto

Formatos disponibles: PDF y Excel

## Tecnologías

- **UI**: ttkbootstrap (tkinter moderno)
- **Base de datos**: SQLite
- **PDF**: reportlab
- **Excel**: openpyxl
- **Tema**: superhero (oscuro)

## Licencia

MIT License
