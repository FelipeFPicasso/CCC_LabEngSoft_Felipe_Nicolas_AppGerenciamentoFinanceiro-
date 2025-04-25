from flask import Blueprint, request, jsonify
import datetime
from Models.usuario_model import Usuario

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    data_nasc = dados.get('data_nasc')
    cpf = dados.get('cpf')

    if not (nome and email and senha and data_nasc and cpf):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    try:
        datetime.datetime.strptime(data_nasc, '%Y-%m-%d')
    except ValueError:
        return jsonify({'erro': 'data_nasc deve estar no formato YYYY-MM-DD'}), 400

    novo_usuario = Usuario(nome, email, senha, data_nasc, cpf)
    usuario_cadastrado = Usuario.adicionar(novo_usuario)

    if usuario_cadastrado:
        return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201
    else:
        return jsonify({'erro': 'Erro ao criar usuário'}), 500
