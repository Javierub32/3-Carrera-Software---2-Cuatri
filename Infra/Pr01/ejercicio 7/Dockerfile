FROM python:3.9-slim

WORKDIR /app

# Copiar el archivo de configuración
COPY config.json .

# Copiar el código
COPY appp.py .

CMD ["python", "app.py"]