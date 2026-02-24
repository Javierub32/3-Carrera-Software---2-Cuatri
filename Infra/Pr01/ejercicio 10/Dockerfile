FROM python:3.9-slim

WORKDIR /app

# Copiamos SOLO el fichero de dependencias primero
COPY requirements.txt .

# Como requirements.txt casi nunca cambia, Docker usará la caché de esta capa y se saltará la instalacion
RUN pip install -r requirements.txt

# AHORA copiamos el código fuente, que es lo que más cambia
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]