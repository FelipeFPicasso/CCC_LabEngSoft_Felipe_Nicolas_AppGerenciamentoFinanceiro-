from flask import Blueprint, jsonify, Flask
from Database.conexao import conectar_financeiro
from flask_cors import CORS

from Utils.auth import token_required

app = Flask(__name__)
CORS(app)
dados_fixos_bp = Blueprint('dados_fixos', __name__)

@dados_fixos_bp.route('/tipos-transacao', methods=['GET'])
@token_required
def listar_tipos_transacao(usuario_id):  # <-- recebe o usuario_id do token_required
    try:
        conn = conectar_financeiro()
        cursor = conn.cursor()
        cursor.execute("SELECT id, tipo FROM tipo_transacao ORDER BY id;")
        tipos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{'id': t[0], 'nome': t[1]} for t in tipos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@dados_fixos_bp.route('/categorias-transacao', methods=['GET'])
@token_required
def listar_categorias_transacao(usuario_id):
    try:
        conn = conectar_financeiro()
        cursor = conn.cursor()
        cursor.execute("SELECT id, categoria FROM categoria_transacao ORDER BY id;")
        categorias = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify([{'id': c[0], 'nome': c[1]} for c in categorias]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
