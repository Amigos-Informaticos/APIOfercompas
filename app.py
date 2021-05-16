from flask import Flask

from src.servicios.RutasCodigoDescuento import rutas_codigo
from src.servicios.RutasMiembroOfercompas import rutas_miembro
from src.servicios.RutasOferta import rutas_oferta
from src.servicios.RutasPublicacion import rutas_publicacion

app = Flask(__name__)

app.register_blueprint(rutas_miembro)
app.register_blueprint(rutas_oferta)
app.register_blueprint(rutas_publicacion)
app.register_blueprint(rutas_codigo)


@app.route('/')
def hello_world():
    return 'Hola mundo!'


if __name__ == '__main__':
    app.run()
