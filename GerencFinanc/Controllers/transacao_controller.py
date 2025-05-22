from flask import Blueprint, request, jsonify, Flask

from Database.conexao import conectar_financeiro
from Models.transacao_model import Transacao
from Utils.auth import token_required
import datetime
import Utils.validations as validator
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
transacao_bp = Blueprint('transacao', __name__)

# POST: Criar nova transação
@transacao_bp.route('/transacao', methods=['POST'])
@token_required
def criar_transacao(usuario_id):
    dados = request.get_json()

    descricao = dados.get('descricao')
    valor = dados.get('valor')
    data = dados.get('data')
    nome_banco = dados.get('nome_banco')
    nome_categoria = dados.get('nome_categoria')
    nome_tipo = dados.get('nome_tipo')

    if not all([descricao, valor, data, nome_banco, nome_categoria, nome_tipo]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    validator.valida_data(data)

    try:
        conn = conectar_financeiro()
        cursor = conn.cursor()

        # Buscar id da conta pelo nome_banco e usuario_id (para garantir que pertence ao usuário)
        cursor.execute(
            "SELECT id FROM conta WHERE nome_banco = %s AND fk_id_usuario = %s",
            (nome_banco, usuario_id)
        )
        conta = cursor.fetchone()
        if not conta:
            return jsonify({'erro': f'Conta com nome_banco "{nome_banco}" não encontrada para o usuário'}), 404
        fk_id_conta = conta[0]

        # Buscar id da categoria pelo nome_categoria
        cursor.execute(
            "SELECT id FROM categoria_transacao WHERE categoria = %s",
            (nome_categoria,)
        )
        categoria = cursor.fetchone()
        if not categoria:
            return jsonify({'erro': f'Categoria "{nome_categoria}" não encontrada'}), 404
        fk_id_categoria_transacao = categoria[0]

        # Buscar id do tipo pelo nome_tipo
        cursor.execute(
            "SELECT id FROM tipo_transacao WHERE tipo = %s",
            (nome_tipo,)
        )
        tipo = cursor.fetchone()
        if not tipo:
            return jsonify({'erro': f'Tipo "{nome_tipo}" não encontrado'}), 404
        fk_id_tipo_transacao = tipo[0]

        # Ajustar valor conforme tipo (1=Receita, 2=Despesa)
        if fk_id_tipo_transacao == 1:  # Receita
            valor = abs(valor)
        elif fk_id_tipo_transacao == 2:  # Despesa
            valor = -abs(valor)

        nova_transacao = Transacao(
            descricao,
            valor,
            data,
            usuario_id,
            fk_id_tipo_transacao,
            fk_id_conta,
            fk_id_categoria_transacao
        )

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

    finally:
        cursor.close()
        conn.close()

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

        transacao = Transacao.buscar_por_id(fk_id_transacao)

        if not transacao:
            return jsonify({'erro': 'Transação não encontrada'}), 404

        # Corrigido para acessar atributo do objeto
        if transacao.fk_id_usuario != usuario_id:
            return jsonify({'erro': 'Usuário não autorizado a alterar esta transação'}), 403

        # Permite esses campos do JSON, mapeando categoria e tipo para os ids
        permitidos = {'descricao', 'valor', 'data', 'categoria', 'tipo'}

        campos = {}
        for key in permitidos:
            if key in dados:
                campos[key] = dados[key]

        # Converte categoria e tipo de nome para id
        if 'categoria' in campos:
            id_categoria = Transacao.obter_id_categoria_por_nome(campos['categoria'])
            if id_categoria is None:
                return jsonify({'erro': 'Categoria não encontrada'}), 400
            campos['fk_id_categoria_transacao'] = id_categoria
            del campos['categoria']

        if 'tipo' in campos:
            id_tipo = Transacao.obter_id_tipo_por_nome(campos['tipo'])
            if id_tipo is None:
                return jsonify({'erro': 'Tipo não encontrado'}), 400
            campos['fk_id_tipo_transacao'] = id_tipo
            del campos['tipo']

        # Validar data se existir
        if 'data' in campos:
            validator.valida_data(campos['data'])

        if not campos:
            return jsonify({'erro': 'Nenhum dado enviado para atualização'}), 400

        atualizado = Transacao.atualizar(fk_id_transacao, campos)

        if atualizado:
            return jsonify({'mensagem': f'Transação {fk_id_transacao} atualizada com sucesso!'}), 200
        else:
            return jsonify({'erro': 'Erro ao atualizar no banco'}), 500

    except Exception as e:
        print(f"Erro ao atualizar transacao: {e}")
        return jsonify({'erro': 'Erro interno ao atualizar transação'}), 500


# DELETE: Deletar transação
@transacao_bp.route('/transacao/<int:id_transacao>', methods=['DELETE'])
@token_required
def deletar_transacao(usuario_id, id_transacao):
    try:
        transacao = Transacao.buscar_por_id(id_transacao)

        if not transacao:
            return jsonify({'erro': 'Transação não encontrada'}), 404

        # Corrigido aqui:
        if transacao.fk_id_usuario != usuario_id:
            return jsonify({'erro': 'Usuário não autorizado a excluir esta transação'}), 403

        deletado = Transacao.deletar(id_transacao)

        if deletado:
            return jsonify({'mensagem': f'Transação de id {id_transacao} excluída com sucesso!'}), 200
        else:
            return jsonify({'erro': 'Erro ao excluir transação'}), 500
    except Exception as e:
        print(f"Erro ao deletar transacao: {e}")
        return jsonify({'erro': 'Erro interno ao deletar transação'}), 500


