from flask import Flask, jsonify, request
import psycopg2
import redis
import json

app = Flask(__name__)

# Conexión a Redis
cache = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_db_connection():
    return psycopg2.connect(
        host='database',
        database='blogdb',
        user='bloguser',
        password='blogpass'
    )

@app.route('/api/posts', methods=['GET'])
def get_posts():
    # Intentar obtener desde caché
    cached = cache.get('posts')
    if cached:
        return jsonify({'source': 'cache', 'posts': json.loads(cached)})
    
    # Si no está en caché, consultar DB
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Crear tabla si no existe
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200),
            content TEXT
        )
    ''')
    conn.commit()
    
    cur.execute('SELECT id, title, content FROM posts')
    posts = [{'id': row[0], 'title': row[1], 'content': row[2]} for row in cur.fetchall()]
    
    cur.close()
    conn.close()
    
    # Guardar en caché por 60 segundos
    cache.setex('posts', 60, json.dumps(posts))
    
    return jsonify({'source': 'database', 'posts': posts})

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.json
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Crear tabla si no existe
    cur.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200),
            content TEXT
        )
    ''')
    
    cur.execute(
        'INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING id',
        (data['title'], data['content'])
    )
    post_id = cur.fetchone()[0]
    conn.commit()
    
    cur.close()
    conn.close()
    
    # Invalidar caché
    cache.delete('posts')
    
    return jsonify({'id': post_id, 'message': 'Post creado'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
