from flask import Flask
import redis
import os

app = Flask(__name__)

# Leer configuración desde variables de entorno
redis_host = os.getenv('REDIS_HOST', 'redis')
app_name = os.getenv('APP_NAME', 'Mi Aplicación')
app_version = os.getenv('APP_VERSION', '1.0')

redis_client = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def hello():
    visits = redis_client.incr('visits')
    return f'''
        <h1>{app_name} v{app_version}</h1>
        <p>¡Hola desde Flask y Redis!</p>
        <p>Esta página ha sido visitada {visits} veces.</p>
        <p>Conectado a Redis en: {redis_host}</p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)