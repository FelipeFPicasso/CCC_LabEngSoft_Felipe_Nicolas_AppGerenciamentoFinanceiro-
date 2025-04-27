from flask import Blueprint, request, jsonify
from Models.cartao_model import Cartao
from Utils.auth import token_required  # Importando o decorator de autenticação

cartao_bp = Blueprint('cartao', __name__)

# POST: Criar um novo cartão
@cartao_bp.route('/cartao', methods=['POST'])
@token_required
def criar_cartao(usuario_id):  # <-- recebe o ID do usuário autenticado
    dados = request.get_json()
    limite = dados.get('limite')
    venc_fatura = dados.get('venc_fatura')

    if not (limite and venc_fatura):
        return jsonify({'erro': 'limite e venc_fatura são obrigatórios'}), 400

    novo_cartao = Cartao(limite, venc_fatura)

    # O usuário já está associado ao cartão por meio do token
    cartao_adicionado = Cartao.adicionar(novo_cartao, usuario_id)

    if cartao_adicionado:
        return jsonify({'mensagem': 'Cartão criado com sucesso', 'cartao': cartao_adicionado.to_dict()}), 201
    else:
        return jsonify({'erro': 'Erro ao criar cartão'}), 500

# GET: Listar todos os cartões
@cartao_bp.route('/cartao', methods=['GET'])
@token_required
def listar_cartoes(usuario_id):
    try:
        cartoes = Cartao.listar_todos()
        return jsonify({'cartoes': [cartao.to_dict() for cartao in cartoes]}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar cartões: {str(e)}'}), 500

# GET: Buscar cartão por ID
@cartao_bp.route('/cartao/<int:id_cartao>', methods=['GET'])
@token_required
def buscar_cartao_por_id(id_cartao):
    try:
        cartao = Cartao.buscar_por_id(id_cartao)
        if cartao:
            return jsonify({'cartao': cartao.to_dict()}), 200
        else:
            return jsonify({'erro': 'Cartão não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar cartão: {str(e)}'}), 500

# GET: Buscar cartões do usuário
#@cartao_bp.route('/cartao/usuario/<int:id_usuario>', methods=['GET'])
#@token_required
#def listar_cartoes_usuario(usuario_id, id_usuario):
#    try:
#        # Verifica se o ID do usuário do token corresponde ao ID passado na URL
#        if usuario_id != id_usuario:
 #           return jsonify({'erro': 'Você não tem permissão para acessar os cartões deste usuário'}), 403
#
 #       # Se os IDs baterem, buscamos os cartões desse usuário
  #      cartoes = Cartao.buscar_por_usuario(id_usuario)
#        if cartoes:
#            return jsonify({'cartoes': [cartao.to_dict() for cartao in cartoes]}), 200
#        else:
#            return jsonify({'erro': 'Nenhum cartão encontrado para este usuário'}), 404
#    except Exception as e:
 #       return jsonify({'erro': f'Erro ao listar cartões do usuário: {str(e)}'}), 500

#DELETE: deleta cartao por ID 
@token_required
@cartao_bp.route('/cartao/<int:id_cartao>', methods=['DELETE'])
def deletar_cartao_por_id(id_cartao):
    try:
        if  Cartao.deletar_por_id(id_cartao):
            return jsonify(f"Cartão de id {id_cartao} excluído com sucesso!"), 200
        else:
            return jsonify({'erro': 'Cartão não encontrado'}), 404
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar cartão: {str(e)}'}), 500