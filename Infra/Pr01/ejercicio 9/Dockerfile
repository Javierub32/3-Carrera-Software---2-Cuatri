FROM python:3.9-slim

# Crear directorio como root
RUN mkdir -p /app/logs && chmod 755 /app/logs

WORKDIR /app

COPY writer_app.py .

# Cambiar a usuario no-root para seguridad
USER nobody

CMD ["python", "writer_app.py"]