from flask import Blueprint, request, jsonify, Flask
from Models.saldo_model import Saldo
from Utils.auth import token_required
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
saldo_bp = Blueprint('saldo', __name__)

@saldo_bp.route('/saldo_atual/<int:fk_id_conta>', methods=['GET'])
@token_required
def obter_saldo_atual(fk_id_usuario, fk_id_conta):
    saldo = Saldo.buscar_por_usuario_e_conta(fk_id_usuario, fk_id_conta)

    if saldo:
        return jsonify(saldo.to_dict()), 200
    return jsonify({'erro': 'Saldo não encontrado para esta conta'}), 404


