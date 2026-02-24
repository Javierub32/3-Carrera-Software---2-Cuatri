import os
import time

LOG_FILE = '/app/logs/application.log'

# Intentar crear directorio y archivo
try:
    os.makedirs('/app/logs', exist_ok=True)
    with open(LOG_FILE, 'w') as f:
        f.write('Aplicación iniciada\n')
    print(f'Log creado exitosamente en {LOG_FILE}')
except PermissionError as e:
    print(f'ERROR: No tengo permisos para escribir en {LOG_FILE}')
    print(f'Detalles: {e}')
    exit(1)

# Escribir logs periódicamente
counter = 0
while True:
    try:
        with open(LOG_FILE, 'a') as f:
            counter += 1
            f.write(f'Log entry #{counter} - {time.ctime()}\n')
        print(f'Log #{counter} escrito')
    except Exception as e:
        print(f'Error escribiendo log: {e}')
    time.sleep(5)