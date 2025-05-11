from flask import Flask
from Controllers.usuario_controller import usuario_bp
from Controllers.login_controller import login_bp
from Controllers.conta_controller import conta_bp
from Controllers.cartao_controller import cartao_bp# <--- Importar o blueprint da conta
from Database.migrate import validar_estrutura_db
from Controllers.limite_controller import limite_bp
from Controllers.transacao_controller import transacao_bp
from Controllers.saldo_controller import saldo_bp
from Controllers.relatorio_controller import relatorio_transacao_bp
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Registrar os blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(login_bp)
app.register_blueprint(conta_bp)  # <--- Registrar o blueprint da conta
app.register_blueprint(cartao_bp)
app.register_blueprint(limite_bp)
app.register_blueprint(transacao_bp)
app.register_blueprint(saldo_bp)
app.register_blueprint(relatorio_transacao_bp)

if __name__ == '__main__':
    validar_estrutura_db()
    app.run(debug=False, port=8000, host='localhost')
