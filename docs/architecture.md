# Arquitectura propuesta para Expense Tracker

## 1. Análisis del estado actual

El proyecto actual funciona, pero su lógica está concentrada en un único archivo principal. En el código actual se mezclan varias responsabilidades:

- Configuración de la base de datos
- Conexión y acceso a datos
- Validación de negocio
- Manejo de rutas HTTP
- Renderizado de vistas
- Lógica de respuesta JSON

Este enfoque es válido para un prototipo, pero dificulta:

- mantener el código a largo plazo
- agregar nuevas funcionalidades
- probar piezas de forma aislada
- escalar el proyecto si crece en complejidad

## 2. Objetivo de la reestructuración

Separar el sistema en módulos con responsabilidades claras, de forma que cada parte tenga un propósito específico y sea fácil de extender.

La idea principal es pasar de un diseño monolítico a una arquitectura modular, manteniendo el mismo comportamiento funcional, pero con mejor organización.

Además, se propone mejorar la experiencia visual del usuario incorporando un diseño más llamativo en la interfaz, con tres tarjetas destacadas que resuman información clave de forma rápida y atractiva.

## 3. Principios de diseño propuestos

### Separación de responsabilidades
Cada módulo debe encargarse de una sola capa del sistema:

- presentación: rutas y vistas
- negocio: reglas y validaciones
- datos: acceso y persistencia
- infraestructura: configuración de la aplicación y base de datos

### Bajo acoplamiento
Los módulos deben interactuar mediante contratos claros, no directamente con detalles internos de otros módulos.

### Alta cohesión
Todo lo relacionado con gastos debe agruparse de forma lógica en un mismo dominio.

### Escalabilidad gradual
La estructura debe permitir crecer desde un proyecto pequeño hacia una aplicación más robusta sin reescribir todo desde cero.

## 4. Propuesta de arquitectura modular

### 4.1 Estructura sugerida

```text
expense_tracker/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── schema.py
│   ├── models/
│   │   └── expense.py
│   ├── repositories/
│   │   └── expense_repository.py
│   ├── services/
│   │   └── expense_service.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── home.py
│   │   └── expenses.py
│   ├── schemas/
│   │   └── expense_schema.py
│   ├── templates/
│   │   └── index.html
│   ├── static/
│   │   ├── style.css
│   │   └── script.js
│   └── utils/
│       └── errors.py
├── docker/
│   └── nginx/             # opcional, si se desea un proxy o reverse proxy
├── tests/
├── docs/
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── docker-compose.yml    # opcional para entorno local más completo
└── README.md
```

## 5. Propuesta de experiencia visual

Para dar un aspecto más moderno y llamativo al producto, se sugiere estructurar la vista principal con tres tarjetas visuales principales:

1. Tarjeta de total gastado
   - muestra el monto acumulado de los gastos registrados
   - destaca el valor de forma visual

2. Tarjeta de gastos del mes
   - presenta una vista resumida de los movimientos recientes o del periodo actual
   - ayuda a identificar el consumo más relevante

3. Tarjeta de categorías o balance
   - muestra una referencia rápida de cómo se distribuyen los gastos
   - puede evolucionar hacia un resumen por categoría o tendencia

Estas tarjetas pueden ir acompañadas de un encabezado más limpio, iconografía, colores suaves y una distribución más moderna para que la interfaz se sienta más premium y atractiva.

## 6. Responsabilidades por módulo

### app/__init__.py
Encargado de crear la instancia de Flask, registrar blueprints y configurar la aplicación.

### app/config.py
Centraliza los valores de configuración como:

- ruta de la base de datos
- modo debug
- configuración de entorno

### app/database/
Contiene todo lo relacionado con SQLite:

- conexión a la base de datos
- inicialización del esquema
- helpers de acceso a datos

### app/models/
Define la representación del dominio del gasto.

Este módulo no debería manejar SQL directamente, sino representar la estructura de un gasto y sus atributos.

### app/repositories/
Encargado del acceso a datos.

Aquí se agrupan operaciones como:

- crear gasto
- listar gastos
- eliminar gasto
- calcular total

El objetivo es aislar la lógica SQL para que las rutas y los servicios no dependan directamente de la base de datos.

### app/services/
Contiene la lógica de negocio.

Aquí se deberían validar reglas como:

- el título no puede estar vacío
- el monto debe ser mayor que cero
- la categoría puede normalizarse o validarse
- la fecha debe tener un formato esperado

### app/routes/
Define los endpoints HTTP.

Se recomienda separar las rutas en archivos por dominio, por ejemplo:

- home.py para la vista principal
- expenses.py para operaciones relacionadas con gastos

Esto evita que todas las rutas vivan en un único archivo.

### app/schemas/
Define estructuras o validaciones de entrada/salida.

Es útil para normalizar datos que llegan desde el cliente y para preparar respuestas consistentes.

### app/utils/
Contiene utilidades transversales como:

- manejo de errores
- respuestas estándar
- helpers comunes

## 7. Flujo recomendado

Un flujo típico de una operación sería:

1. La ruta recibe la petición HTTP.
2. La ruta delega a un servicio.
3. El servicio aplica reglas de negocio.
4. El servicio invoca un repositorio.
5. El repositorio interactúa con la base de datos.
6. La respuesta se devuelve de forma consistente al cliente.

Esto mejora la claridad y permite reemplazar o probar cada capa de forma independiente.

## 8. Migración recomendada

La transición debe hacerse de forma incremental, no de golpe.

### Fase 1: documentación y organización
- identificar responsabilidades actuales
- crear estructura de carpetas propuesta
- mover la lógica de negocio a un documento de referencia

### Fase 2: separación de capas
- extraer la conexión a la base de datos
- encapsular consultas en un repositorio
- mover validaciones a un servicio

### Fase 3: modularización de rutas
- separar rutas por dominio
- registrar blueprints
- mantener la interfaz del usuario igual

### Fase 4: mejora de calidad
- agregar pruebas unitarias
- introducir manejo de errores más claro
- preparar la aplicación para crecer con nuevas funciones

## 9. Beneficios esperados

Con esta arquitectura se logra:

- mejor legibilidad del proyecto
- menor riesgo de errores al modificar una parte específica
- facilidad para agregar nuevas funcionalidades como filtros, categorías, reportes o autenticación
- mejor base para introducir pruebas automatizadas
- mayor mantenibilidad a largo plazo

## 10. Conclusión

El proyecto actual es un buen punto de partida, pero su estructura monolítica limita su crecimiento. La propuesta de arquitectura modular permite transformar el sistema en una base más limpia, organizada y escalable, sin perder la simplicidad inicial del proyecto.

Este documento sirve como base de diseño para la siguiente fase de implementación.
