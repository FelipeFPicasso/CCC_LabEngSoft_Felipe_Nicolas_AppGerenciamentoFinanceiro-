# relatorio_controller.py
from flask import Blueprint, jsonify, Flask
from Utils.auth import token_required
from Models.relatorio_model import RelatorioTransacao
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
relatorio_transacao_bp = Blueprint('relatorio_transacao_bp', __name__)

@relatorio_transacao_bp.route('/relatorio_transacao/transacao/<int:fk_id_transacao>', methods=['GET'])
@token_required
def get_relatorio_transacao(usuario_id, fk_id_transacao):
    try:
        relatorio = RelatorioTransacao.buscar_por_fk_id_transacao(fk_id_transacao)

        if relatorio:
            return jsonify(relatorio), 200
        else:
            return jsonify({"mensagem": "Relatório não encontrado para esse ID de transação"}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
