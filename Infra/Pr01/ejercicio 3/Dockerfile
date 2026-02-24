# 1. Usa Python 3.9 como imagen base (la versión slim es más ligera)
FROM python:3.9-slim

# 2. Define el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el requirements
COPY requirements.txt .

# 4. Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia el resto del código de la aplicación (el archivo app.py)
COPY app.py .

# 6. Indica el puerto que va a usar la aplicación (opcional pero recomendado como documentación)
EXPOSE 5000

# 7. Define el comando que se ejecutará al iniciar el contenedor
CMD ["python", "app.py"]