from flask import Blueprint, request, jsonify, Flask
from Models.saldo_total_model import SaldoTotal
from Utils.auth import token_required
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

saldo_total_bp = Blueprint('saldo_total', __name__)


@saldo_total_bp.route('/saldo_total/usuarios', methods=['GET'])
@token_required
def obter_saldo_total(fk_id_usuario):
    saldo_total = SaldoTotal.buscar_saldo_total_por_usuario(fk_id_usuario)

    if saldo_total is not None:
        return jsonify({'saldo_total': saldo_total}), 200
    return jsonify({'erro': 'Saldo total não encontrado'}), 404