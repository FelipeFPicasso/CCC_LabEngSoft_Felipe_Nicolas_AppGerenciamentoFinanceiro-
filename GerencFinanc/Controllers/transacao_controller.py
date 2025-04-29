from flask import Blueprint, request, jsonify
from Models.transacao_model import Transacao
from Utils.auth import token_required  # já deve estar criado
import datetime

transacao_bp = Blueprint('transacao', __name__)

@transacao_bp.route('/transacao', methods=['POST'])
@token_required
def criar_transacao(usuario_id):
    dados = request.get_json()

    descricao = dados.get('descricao')
    valor = dados.get('valor')
    data = dados.get('data')
    fk_id_conta = dados.get('fk_id_conta')
    fk_id_categoria_transacao = dados.get('fk_id_categoria_transacao')
    fk_id_tipo_transacao = dados.get('fk_id_tipo_transacao')

    # Validação
    if not all([descricao, valor, data, fk_id_conta, fk_id_categoria_transacao, fk_id_tipo_transacao]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    try:
        data_formatada = datetime.datetime.strptime(data, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'erro': 'Data inválida. Use o formato YYYY-MM-DD'}), 400

    nova_transacao = Transacao(
        descricao,
        valor,
        data_formatada,
        usuario_id,
        fk_id_tipo_transacao,
        fk_id_conta,
        fk_id_categoria_transacao
    )

    sucesso = Transacao.adicionar(nova_transacao)
    if sucesso:
        return jsonify({'mensagem': 'Transação criada com sucesso'}), 201
    else:
        return jsonify({'erro': 'Erro ao criar transação'}), 500
