from flask import Flask

from src.servicios.RutasMiembroOfercompas import rutas_miembro

app = Flask(__name__)

app.register_blueprint(rutas_miembro)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
