from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host='database',
        database=os.getenv('POSTGRES_DB', 'miapp'),
        user=os.getenv('POSTGRES_USER', 'usuario'),
        password=os.getenv('POSTGRES_PASSWORD', 'password')
    )
    return conn

@app.route('/api/status')
def status():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()[0]
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'ok',
            'message': 'Backend funcionando correctamente',
            'database': 'conectada',
            'db_version': db_version
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
