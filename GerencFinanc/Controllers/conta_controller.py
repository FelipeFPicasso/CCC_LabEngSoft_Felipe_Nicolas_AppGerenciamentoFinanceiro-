from flask import Blueprint, request, jsonify
from Models.conta_model import Conta
from Utils.auth import token_required  # Vamos criar isso já já

conta_bp = Blueprint('conta', __name__)

@conta_bp.route('/conta', methods=['POST'])
@token_required
def criar_conta():
    #return jsonify({'SUCCESS': 'CRIADO COM SUCESSO'}), 200

    dados = request.get_json()
    nome_banco = dados.get('nome_banco')
    saldo_inicial = dados.get('saldo_inicial')
    fk_id_usuario = dados.get('fk_id_usuario')
    fk_id_cartao = dados.get('fk_id_cartao')

    if not (nome_banco and saldo_inicial):
        return jsonify({'erro': 'nome_banco e saldo_inicial são obrigatórios'}), 400

    nova_conta = Conta(nome_banco, saldo_inicial, fk_id_usuario, fk_id_cartao)
    conta_criada = Conta.adicionar(nova_conta)

    if conta_criada:
        return jsonify({'mensagem': 'Conta criada com sucesso', 'conta': conta_criada.to_dict()}), 201
    else:
        return jsonify({'erro': 'Erro ao criar conta'}), 500
