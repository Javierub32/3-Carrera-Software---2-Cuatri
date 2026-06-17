import os
import configparser
from flask import Flask, render_template

app = Flask(__name__)

def load_config():
    config = configparser.ConfigParser()
    config_path = "/config/settings.ini"
    if os.path.exists(config_path):
        config.read(config_path)
        title  = config.get("app", "title",  fallback="App sin configurar")
        author = config.get("app", "author", fallback="Desconocido")
    else:
        title  = "App sin configurar"
        author = "Desconocido"
    return title, author

@app.route("/")
def index():
    title, author = load_config()
    env = os.environ.get("APP_ENV", "development")
    return render_template("index.html", title=title, author=author, env=env)

@app.route("/health")
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
