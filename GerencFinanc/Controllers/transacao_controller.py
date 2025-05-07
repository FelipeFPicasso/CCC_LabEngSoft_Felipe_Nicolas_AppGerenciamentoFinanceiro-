from flask import Blueprint, request, jsonify
from Models.transacao_model import Transacao
from Utils.auth import token_required
import datetime

transacao_bp = Blueprint('transacao', __name__)

# POST: Criar nova transação
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

    try:
        id_transacao = Transacao.adicionar(nova_transacao)
        if id_transacao:
            return jsonify({
                'mensagem': 'Transação criada com sucesso',
                'id_transacao': id_transacao
            }), 201
        else:
            return jsonify({'erro': 'Erro ao criar transação, verifique os dados enviados.'}), 500
    except Exception as e:
        return jsonify({'erro': f'Erro ao criar transação: {str(e)}'}), 500

# GET: Listar todas as transações
@transacao_bp.route('/transacao', methods=['GET'])
@token_required
def listar_transacoes(usuario_id):
    try:
        transacoes = Transacao.listar_todas()
        return jsonify({'transacoes': [transacao.to_dict() for transacao in transacoes]}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar transações: {str(e)}'}), 500

# GET: Listar transação por ID
@transacao_bp.route('/transacao/<int:id_transacao>', methods=['GET'])
@token_required
def listar_transacao_por_id(usuario_id, id_transacao):
    try:
        transacao = Transacao.buscar_por_id(id_transacao)
        if transacao:
            return jsonify({'transacao': transacao.to_dict()}), 200
        else:
            return jsonify({'erro': 'Transação não encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar transação: {str(e)}'}), 500

# GET: Listar transações do usuário autenticado
@transacao_bp.route('/transacao/usuario', methods=['GET'])
@token_required
def listar_transacoes_por_usuario(usuario_id):
    try:
        transacoes = Transacao.listar_por_usuario(usuario_id)
        if transacoes:
            return jsonify({'transacoes': [transacao.to_dict() for transacao in transacoes]}), 200
        else:
            return jsonify({'mensagem': 'Nenhuma transação encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar transações do usuário: {str(e)}'}), 500

# PUT: Atualizar transação
@transacao_bp.route('/transacao/<int:fk_id_transacao>', methods=['PUT'])
@token_required
def atualizar_transacao(usuario_id, fk_id_transacao):
    try:
        dados = request.get_json()

        if not Transacao.buscar_por_id(fk_id_transacao):
            return jsonify({'erro': 'Transação não encontrada'})

        permitidos = {'descricao', 'valor', 'data', 'fk_id_tipo_transacao', 'fk_id_conta', 'fk_id_categoria_transacao'}
        campos = {key: value for key, value in dados.items() if key in permitidos}

        if not campos:
            return jsonify({'erro': 'Nenhum dado enviado para atualização'}), 400

        if Transacao.atualizar(fk_id_transacao, campos):
            return jsonify({'mensagem': f'Transação {fk_id_transacao} atualizada com sucesso!'}), 200
        else:
            return jsonify({'erro': 'Erro ao atualizar no banco'})
    except Exception as e:
        return jsonify({'erro': 'Erro ao atualizar transação'}), 500

# DELETE: Deletar transação
@token_required
@transacao_bp.route('/transacao/<int:id_transacao>', methods=['DELETE'])
def deletar_transacao(id_transacao):
    try:
        if Transacao.deletar(id_transacao):
            return jsonify({'mensagem': f'Transação de id {id_transacao} excluída com sucesso!'})
        else:
            return jsonify({'mensagem': 'Erro ao atualizar banco'})
    except Exception as e:
        return jsonify('Erro ao deletar transação'), 500

