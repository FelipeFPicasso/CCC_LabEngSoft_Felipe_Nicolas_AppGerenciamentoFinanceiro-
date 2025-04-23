from flask import Flask
from Controllers.usuario_controller import usuario_bp

app = Flask(__name__)

# Registrar o blueprint
app.register_blueprint(usuario_bp)

@app.route('/menu')
def hello():
    return 'Esse é um app de gerenciamento financeiro'

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='localhost')
