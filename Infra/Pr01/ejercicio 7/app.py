import os

def main():
    print("Iniciando aplicación...")
    # La aplicación espera encontrar el archivo en una subcarpeta de datos
    ruta_config = 'data/config.json'
    
    if os.path.exists(ruta_config):
        with open(ruta_config, 'r') as f:
            print(f"Configuración leída: {f.read()}")
    else:
        raise FileNotFoundError(f"ERROR CRÍTICO: No se encuentra el archivo en {ruta_config}")

if __name__ == '__main__':
    main()
