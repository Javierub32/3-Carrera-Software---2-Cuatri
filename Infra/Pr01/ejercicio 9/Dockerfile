FROM python:3.9-slim

WORKDIR /app
COPY writer_app.py .

# Creamos un usuario no privilegiado 'appuser' y un grupo 'appuser'
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Creamos el directorio de logs y le damos permisos al usuario 'appuser'
RUN mkdir -p /app/logs && chown -R appuser:appuser /app

# Cambiamos al usuario 'appuser'
USER appuser

CMD ["python", "-u", "writer_app.py"]