import os
import sys

# Leer variables de entorno
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Validar que existen
if not all([DB_HOST, DB_PORT, DB_USER, DB_PASSWORD]):
    print('ERROR: Faltan variables de entorno requeridas')
    print(f'DB_HOST: {DB_HOST}')
    print(f'DB_PORT: {DB_PORT}')
    print(f'DB_USER: {DB_USER}')
    print(f'DB_PASSWORD: {DB_PASSWORD}')
    sys.exit(1)

print('Configuración cargada correctamente:')
print(f'Conectando a {DB_USER}@{DB_HOST}:{DB_PORT}')
print('Aplicación iniciada exitosamente')

# Mantener el contenedor activo
import time
while True:
    time.sleep(60)