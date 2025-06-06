from flask import Blueprint, request, jsonify, Flask
from Models.conta_model import Conta
from Utils.auth import token_required
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
conta_bp = Blueprint('conta', __name__)

@conta_bp.route('/conta', methods=['POST'])
@token_required
def criar_conta(usuario_id):
    dados = request.get_json()
    nome_banco = dados.get('nome_banco')
    saldo_inicial = dados.get('saldo_inicial')

    if not (nome_banco and saldo_inicial):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    nova_conta = Conta(nome_banco, saldo_inicial, usuario_id)
    conta_adicionada = Conta.adicionar(nova_conta)

    if conta_adicionada:
        return jsonify({'mensagem': 'Conta criada com sucesso', 'conta': conta_adicionada.to_dict()}), 201
    else:
        return jsonify({'erro': 'Erro ao criar conta'}), 500

@conta_bp.route('/conta', methods=['GET'])
def listar_contas():
    try:
        contas = Conta.listar_todas()
        return jsonify({'contas': [conta.to_dict() for conta in contas]}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar contas: {str(e)}'}), 500

@conta_bp.route('/conta/<int:id_conta>', methods=['GET'])
def listar_conta_por_id(id_conta):
    try:
        conta = Conta.buscar_por_id(id_conta)
        if conta:
            return jsonify({'conta': conta.to_dict()}), 200
        else:
            return jsonify({'erro': 'Conta não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar conta: {str(e)}'}), 500

@conta_bp.route('/contas/usuario', methods=['GET'])
@token_required
def listar_contas_usuario_token(usuario_id):
    try:
        contas = Conta.listar_por_usuario(usuario_id)
        if contas:
            return jsonify({'contas': [conta.to_dict() for conta in contas]}), 200
        else:
            return jsonify({'erro': 'Nenhuma conta encontrada para este usuário'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar contas do usuário: {str(e)}'}), 500

@conta_bp.route('/conta/<int:id_conta>', methods=['PUT'])
@token_required
def atualizar_conta(usuario_id, id_conta):
    dados = request.get_json()

    if not Conta.buscar_por_id(id_conta):
        return jsonify({'erro': 'Conta não encontrada'}), 404

    permitidos = {'nome_banco', 'saldo_inicial'}
    campos = {key: value for key, value in dados.items() if key in permitidos}

    if not campos:
        return jsonify({'erro': 'Nenhum dado enviado para atualização'}), 400

    if Conta.atualizar(id_conta, campos):
        return jsonify({'mensagem': f'Conta {id_conta} atualizada com sucesso'}), 200
    else:
        return jsonify({'erro': 'Erro ao atualizar conta'}), 500

@conta_bp.route('/conta/<int:id_conta>', methods=['DELETE'])
def deletar_conta_por_id(id_conta):
    try:
        if Conta.deletar_por_id(id_conta):
            return jsonify({'mensagem': f'Conta de id {id_conta} excluída com sucesso!'}), 200
        else:
            return jsonify({'erro': 'Conta não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar conta: {str(e)}'}), 500
