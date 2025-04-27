from flask import Blueprint, request, jsonify
from Models.conta_model import Conta
from Utils.auth import token_required  # Importando o decorator de autenticação

conta_bp = Blueprint('conta', __name__)

@conta_bp.route('/conta', methods=['POST'])
@token_required  # Garantir que o usuário esteja autenticado
def criar_conta(usuario_id):
    dados = request.get_json()
    nome_banco = dados.get('nome_banco')
    saldo_inicial = dados.get('saldo_inicial')
    fk_id_cartao = dados.get('fk_id_cartao')

    # Verifica se os campos obrigatórios estão presentes
    if not (nome_banco and saldo_inicial and fk_id_cartao):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    # Cria a conta associando o usuario_id que veio do token
    nova_conta = Conta(nome_banco, saldo_inicial, fk_id_cartao, usuario_id)
    conta_adicionada = Conta.adicionar(nova_conta)

    if conta_adicionada:
        return jsonify({'mensagem': 'Conta criada com sucesso', 'conta': conta_adicionada.to_dict()}), 201
    else:
        return jsonify({'erro': 'Erro ao criar conta'}), 500
