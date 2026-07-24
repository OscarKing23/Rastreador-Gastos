# ============================================
# ETAPA 1: Builder - Instalación de dependencias
# ============================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Copiar solo requirements.txt primero para aprovechar la caché de capas de Docker
COPY requirements.txt .

# Instalar dependencias en un directorio aislado
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt \
    && pip install --no-cache-dir --prefix=/install gunicorn

# ============================================
# ETAPA 2: Production - Imagen final ligera
# ============================================
FROM python:3.12-slim AS production

# Metadatos de la imagen
LABEL maintainer="Oscar" \
      description="Expense Tracker - Flask Application" \
      version="1.0"

# Crear usuario no-root por seguridad
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --create-home appuser

WORKDIR /app

# Copiar dependencias instaladas desde la etapa builder
COPY --from=builder /install /usr/local

# Copiar el código fuente de la aplicación
COPY app/ ./app/
COPY templates/ ./templates/
COPY static/ ./static/
COPY config.py .
COPY app.py .
COPY wsgi.py .
COPY requirements.txt .

# Crear directorio para la base de datos y asignar permisos
RUN mkdir -p /app/data \
    && chown -R appuser:appgroup /app

# Variables de entorno
ENV FLASK_ENV=production \
    DATABASE_PATH=/tmp/expenses.db \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cambiar al usuario no-root
USER appuser

# Puerto expuesto
EXPOSE 5000

# Comando de ejecución con Gunicorn (servidor WSGI de producción)
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 2 wsgi:app"]
