from flask import Blueprint, request, jsonify
from Models.cartao_model import Cartao

cartao_bp = Blueprint('cartao', __name__)

@cartao_bp.route('/cartao', methods=['POST'])
def criar_cartao():
    #return jsonify({'SUCCESS': 'CRIADO COM SUCESSO'}), 200

    dados = request.get_json()
    limite = dados.get('limite')
    venc_fatura = dados.get('venc_fatura')
    print(dados)

    if not (limite and venc_fatura):
        return jsonify({'erro': 'limite e venc_fatura são obrigatórios'}), 400

    novo_cartao = Cartao(limite, venc_fatura)

    cartao_adicionado = Cartao.adicionar(novo_cartao)

    if cartao_adicionado:
        return jsonify({'mensagem': 'Cartao criado com sucesso', 'cartao': cartao_adicionado.to_dict()}), 201
    else:
        return jsonify({'erro': 'Erro ao criar cartao'}), 500
