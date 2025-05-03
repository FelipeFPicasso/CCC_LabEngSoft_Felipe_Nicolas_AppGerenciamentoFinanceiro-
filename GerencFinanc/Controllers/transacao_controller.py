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

    if Transacao.adicionar(nova_transacao):
        return jsonify({'mensagem': 'Transação criada com sucesso'}), 201
    else:
        return jsonify({'erro': 'Erro ao criar transação'}), 500
    
#GET: Todas as transacoes
@transacao_bp.route('/transacao', methods=['GET'])
@token_required
def listar_transacoes(id_usuario):
    try:
        transacoes = Transacao.listar_todas()
        return jsonify({'transações': [transacao.to_dict() for transacao in transacoes]}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar contas: {str(e)}'}), 500
    
#GET: Lista transacao por ID
@transacao_bp.route('/transacao/<int:id_transacao>', methods=['GET'])
@token_required
def listar_transacao_por_id(id_usuario, id_transacao):
    try:
        transacao = Transacao.buscar_por_id(id_transacao)
        if transacao:
            return jsonify({'transacao': transacao.to_dict()}), 200
        else:
            return jsonify({'erro': 'Transacao nao encontrada'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar conta: {str(e)}'}), 500
    
# GET: Listar transações do usuário pelo ID do usuário
@transacao_bp.route('/transacao/usuario/<int:id_usuario>', methods=['GET'])
def listar_transacoes_por_usuario(id_usuario):
    try:
        transacoes = Transacao.listar_por_usuario(id_usuario)
        if transacoes:
            return jsonify({'transacoes': [transacao.to_dict() for transacao in transacoes]}), 200
        else:
            return jsonify({'erro': f'Nenhuma transação encontrada {str(e)}'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar transações do usuário: {str(e)}'}), 500
    
#PUT: Atualizar informacoes de transacao
@token_required
@transacao_bp.route('/transacao/<int:id_transacao>', methods=['PUT'])
def atualizar_transacao(id_transacao):
    try:
        dados = request.get_json()

        if not Transacao.buscar_por_id(id_transacao):
            return jsonify({'erro': 'Transação não encontrada'})
        
        permitidos = {'descricao', 'valor', 'data', 'fk_id_tipo_transacao', 'fk_id_conta', 'fk_id_categoria_transacao'}

        campos = {
            key: value for key, value in dados.items()
            if key in permitidos
        }

        if not campos:
            return jsonify({'erro': 'Nenhum dado enviado para atualização'}), 400
        
        if Transacao.atualizar(id_transacao, campos):
            return jsonify({'mensagem': f'Transação {id_transacao} atualizada com sucesso!'}), 200
        else:
            return jsonify({'erro': 'Erro ao atualizar banco'})
    except Exception as e:
        return jsonify({'erro': 'Erro ao atualizar transação'}), 500
    
#DELETE: Deleta transacao por ID
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
    
