# Usa Python 3.9 como imagen base (la versión slim es más ligera)
FROM python:3.9-slim

# Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el requirements
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación (el archivo app.py)
COPY app.py .

# Indica el puerto que va a usar la aplicación
EXPOSE 5000

# Define el comando que se ejecutará al iniciar el contenedor
CMD ["python", "app.py"]