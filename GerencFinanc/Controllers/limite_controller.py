from flask import Blueprint, request, jsonify, Flask
from Models.limite_model import Limite
from Utils.auth import token_required
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
limite_bp = Blueprint('limite', __name__)

# POST: Criar um novo limite
@limite_bp.route('/limite', methods=['POST'])
@token_required
def criar_limite(usuario_id):
    dados = request.get_json()

    titulo = dados.get('titulo')
    valor = dados.get('valor')
    fk_id_recorrencia = dados.get('fk_id_recorrencia')
    fk_id_categoria_transacao = dados.get('fk_id_categoria_transacao')

    if not (titulo and valor and fk_id_recorrencia and fk_id_categoria_transacao):
        return jsonify({'erro': 'Campos obrigatórios: titulo, valor, fk_id_recorrencia, fk_id_categoria_transacao'}), 400

    novo_limite = Limite(
        titulo=titulo,
        valor=valor,
        fk_id_usuario=usuario_id,  # PEGANDO DIRETO DO TOKEN
        fk_id_recorrencia=fk_id_recorrencia,
        fk_id_categoria_transacao=fk_id_categoria_transacao
    )

    limite_criado = Limite.adicionar(novo_limite)

    if limite_criado:
        return jsonify({'mensagem': 'Limite criado com sucesso', 'limite': limite_criado.to_dict()}), 201
    else:
        return jsonify({'erro': 'Erro ao criar limite'}), 500


# GET: Listar todos os limites
@limite_bp.route('/limite', methods=['GET'])
def listar_limites():
    try:
        limites = Limite.listar_todos()
        return jsonify({'limites': [limite.to_dict() for limite in limites]}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar limites: {str(e)}'}), 500


# GET: Listar limite por ID
@limite_bp.route('/limite/<int:id_limite>', methods=['GET'])
def listar_limite_por_id(id_limite):
    try:
        limite = Limite.buscar_por_id(id_limite)
        if limite:
            return jsonify({'limite': limite.to_dict()}), 200
        else:
            return jsonify({'erro': 'Limite não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar limite: {str(e)}'}), 500


# GET: Listar limites do usuário pelo ID do usuário
@limite_bp.route('/limite/usuario', methods=['GET'])
@token_required
def listar_limites_por_usuario(usuario_id):
    try:
        limites = Limite.listar_por_usuario(usuario_id)
        if limites:
            return jsonify({'limites': [limite.to_dict() for limite in limites]}), 200
        else:
            return jsonify({'erro': 'Nenhum limite encontrado para este usuário'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar limites do usuário: {str(e)}'}), 500


@limite_bp.route('/limite/<int:id_limite>', methods=['DELETE'])
@token_required
def deletar_limite(usuario_id, id_limite):
    try:
        # Primeiro, buscar o limite para verificar se ele existe e pertence ao usuário
        limite = Limite.buscar_por_id(id_limite)
        if not limite:
            return jsonify({'erro': 'Limite não encontrado'}), 404

        # Opcional: Verificar se o limite pertence ao usuário que está tentando deletar
        if limite.fk_id_usuario != usuario_id:
            return jsonify({'erro': 'Acesso negado: limite não pertence ao usuário'}), 403

        sucesso = Limite.deletar(id_limite)
        if sucesso:
            return jsonify({'mensagem': 'Limite deletado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Erro ao deletar limite'}), 500
    except Exception as e:
        return jsonify({'erro': f'Erro ao deletar limite: {str(e)}'}), 500