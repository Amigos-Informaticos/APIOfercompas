from flask import Flask

from src.servicios.RutasMiembroOfercompas import rutas_miembro
from src.servicios.RutasOferta import rutas_oferta

app = Flask(__name__)

app.register_blueprint(rutas_miembro)
app.register_blueprint(rutas_oferta)

@app.route('/')
def hello_world():
    return 'Hola mundo!'


if __name__ == '__main__':
    print("Hola, Edson")
    app.run(debug=True)
