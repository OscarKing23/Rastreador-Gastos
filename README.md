# 💰 Expense Tracker - Fase 1: Refactorización y Código Limpio

Un sistema moderno de **Gestión de Gastos (Expense Tracker)** desarrollado con **Python (Flask)**, **SQLite** e interfaz web interactiva (**HTML/CSS/JS**).

Este proyecto forma parte de un proceso de reingeniería progresivo en 6 fases. En esta **Fase 1**, la aplicación ha sido transformada desde una arquitectura monolítica inicial hacia una **arquitectura modular escalable basada en Flask Blueprints, Capa de Servicios/Repositorio y Configuración Centralizada**.

---

## 🏛️ Comparativa de Arquitectura: Legada vs. Modular (Fase 1)

### 🔴 Arquitectura Previa (Legada)
Anteriormente, el sistema operaba bajo un archivo único monolítico (`app.py`):
- **Acoplamiento Directo**: Conexiones a SQLite, definición de tablas SQL y ejecuciones `conn.execute()` incrustadas directamente dentro de las rutas HTTP.
- **Mezcla de Responsabilidades**: Las reglas de validación de negocio, manejo de peticiones JSON y renderizado HTML convivían en un solo bloque.
- **Dificultad de Pruebas**: No existía la posibilidad de probar aisladamente la base de datos o la lógica de negocio sin levantar la aplicación completa.
- **Ausencia de Configuración**: Los nombres de base de datos y parámetros de depuración estaban fijos en el código.

### 🟢 Nueva Arquitectura Modular Implementada
En cumplimiento con los requerimientos de la **Fase 1**, la estructura ha sido rediseñada bajo principios de **Código Limpio (Clean Architecture / Layered Architecture)**:

```text
Expense-tracker/
├── app/
│   ├── __init__.py          # Application Factory (create_app) y registro de Blueprints
│   ├── database.py          # Gestión de conexiones SQLite e inicialización de esquemas
│   ├── models/
│   │   ├── __init__.py
│   │   └── expense.py       # Modelo de dominio (Expense Dataclass)
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── expense_repository.py # Data Access Object (DAO) para SQLite
│   ├── services/
│   │   ├── __init__.py
│   │   └── expense_service.py    # Capa de negocio y validación de datos
│   └── routes/
│       ├── __init__.py
│       ├── main_routes.py    # Blueprint 'main' para la interfaz web (/)
│       └── expense_routes.py # Blueprint 'expenses' para la API JSON (/expenses)
├── docs/                    # Documentación del proyecto e hitos
├── static/                  # Estilos CSS y cliente JavaScript
├── templates/               # Plantillas HTML (index.html)
├── config.py                # Centralización de variables de entorno y configuración
├── app.py                   # Punto de entrada principal (Entrypoint)
├── requirements.txt         # Dependencias del proyecto
└── README.md                # Documentación técnica general
```

---

## 🧩 Responsabilidad por Módulo

| Módulo / Archivo | Responsabilidad Principal |
| :--- | :--- |
| `config.py` | Centralización de entornos (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`), rutas de BD y claves secretas. |
| `app/__init__.py` | Implementación del patrón **Application Factory (`create_app()`)** y registro de Blueprints. |
| `app/database.py` | Manejo desacoplado de la conexión a la base de datos y creación del esquema inicial. |
| `app/models/expense.py` | Representación de la entidad de dominio `Expense` y conversión de/hacia diccionarios JSON / SQLite rows. |
| `app/repositories/expense_repository.py` | Aislamiento de consultas SQL (`INSERT`, `SELECT`, `DELETE`, `SUM`). |
| `app/services/expense_service.py` | Reglas de negocio (validación de títulos no vacíos, montos mayores a cero y formatos de respuesta HTTP). |
| `app/routes/main_routes.py` | **Flask Blueprint (`main`)** encargado de servir las vistas HTML principales. |
| `app/routes/expense_routes.py` | **Flask Blueprint (`expenses`)** encargado de los endpoints REST / JSON API. |
| `app.py` | Punto de entrada ligero que ejecuta el Application Factory. |

---

## ✨ Funcionalidades

- ➕ **Registro de Gastos**: Ingreso de título, monto, categoría y fecha.
- 📋 **Listado Interactivo**: Visualización limpia de registros en tabla.
- 🧮 **Cálculo Automático**: Suma en tiempo real del total acumulado.
- 🗑️ **Eliminación**: Eliminación instantánea de gastos mediante API.
- 🔍 **Filtrado Flexible**: Filtros por rango de fechas y categorías en el frontend.
- 💾 **Persistencia SQLite**: Almacenamiento seguro en `expenses.db`.

---

## 🚀 Guía de Instalación y Ejecución

### 1. Clonar el repositorio
```bash
git clone https://github.com/hansinivakula/Expense-tracker.git
cd Expense-tracker
```

### 2. Crear y activar un entorno virtual
```bash
python -m venv .venv
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1
# En Linux/macOS:
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación
```bash
python app.py
```

Accede desde tu navegador a `http://127.0.0.1:5000/`.

---

## 📄 Requerimientos Cumplidos - Fase 1
- [x] **Repositorio Modular**: Código reestructurado aplicando patrones de diseño (Factory, Repository, Service).
- [x] **Blueprints**: Uso de `main_bp` y `expenses_bp` para separar vistas y API.
- [x] **Segregación de Modelos**: Abstracción de entidades en `app/models/`.
- [x] **Configuración Centralizada**: Archivo `config.py` con variables de entorno.
- [x] **Documentación Técnica**: Comparación clara entre arquitectura legada y modular en `README.md`.