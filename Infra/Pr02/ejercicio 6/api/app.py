from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/api/data')
def get_data():
    try:
        conn = psycopg2.connect(
            host='database',
            database='mydb',
            user='user',
            password='password'
        )
        cur = conn.cursor()
        cur.execute('SELECT 1 as test;')
        result = cur.fetchone()
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'ok',
            'message': 'Conexión exitosa a la base de datos',
            'result': result[0]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
