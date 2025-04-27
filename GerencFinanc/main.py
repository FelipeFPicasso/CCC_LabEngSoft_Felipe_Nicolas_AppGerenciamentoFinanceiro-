from flask import Flask
from Controllers.usuario_controller import usuario_bp
from Controllers.login_controller import login_bp
from Database.migrate import validar_estrutura_db
from flask_cors import CORS

app = Flask(__name__)

CORS(app)


# Registrar os blueprints sem prefixo
app.register_blueprint(usuario_bp)
app.register_blueprint(login_bp)

if __name__ == '__main__':
    validar_estrutura_db()
    app.run(debug=False, port=8000, host='localhost')
