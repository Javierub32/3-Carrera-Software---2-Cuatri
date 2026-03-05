from flask import Flask
import redis
import os

app = Flask(__name__)

# Conectar a Redis usando el nombre del servicio como hostname
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def hello():
    # Incrementar contador de visitas
    visits = redis_client.incr('visits')
    return f'''
        <h1>¡Hola desde Flask y Redis!</h1>
        <p>Esta página ha sido visitada {visits} veces.</p>
        <p>Recarga la página para incrementar el contador.</p>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
