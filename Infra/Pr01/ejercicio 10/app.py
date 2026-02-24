from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World v1.0'

@app.route('/external')
def external():
    resp = requests.get('https://api.github.com')
    return f'GitHub API Status: {resp.status_code}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)