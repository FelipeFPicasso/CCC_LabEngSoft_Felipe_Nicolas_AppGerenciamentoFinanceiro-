from datetime import datetime
from Utils.auth import token_required
from flask import Blueprint, request, jsonify, Flask
from Models.cartao_model import Cartao
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cartao_bp = Blueprint('cartao_bp', __name__)

@cartao_bp.route('/cartoes', methods=['POST'])
@token_required
def criar_cartao(usuario_id):
    dados = request.json
    limite = dados.get('limite')
    venc_fatura = dados.get('venc_fatura')  # esperado formato dd/mm/yyyy
    fk_id_conta = dados.get('fk_id_conta')

    if limite is None or venc_fatura is None or fk_id_conta is None:
        return jsonify({'erro': 'limite, venc_fatura e fk_id_conta são obrigatórios'}), 400

    # Converter venc_fatura de dd/mm/yyyy para yyyy-mm-dd
    try:
        venc_fatura_us = datetime.strptime(venc_fatura, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return jsonify({'erro': 'Formato de data inválido para venc_fatura. Use dd/mm/yyyy'}), 400

    cartao = Cartao(limite, venc_fatura_us, fk_id_conta)

    cartao_adicionado = Cartao.adicionar(cartao)
    if cartao_adicionado is None:
        return jsonify({'erro': 'Falha ao adicionar cartão'}), 500

    # Aqui, se quiser retornar no formato BR para o cliente, pode converter novamente antes de retornar
    retorno = cartao_adicionado.to_dict()
    try:
        # converter de volta para dd/mm/yyyy para o front
        retorno['venc_fatura'] = datetime.strptime(retorno['venc_fatura'], '%Y-%m-%d').strftime('%d/%m/%Y')
    except Exception:
        pass

    return jsonify(retorno), 201

@cartao_bp.route('/cartoes', methods=['GET'])
def listar_todos_cartoes():
    cartoes = Cartao.listar_todos()
    lista = []
    for c in cartoes:
        d = c.to_dict()
        try:
            d['venc_fatura'] = datetime.strptime(d['venc_fatura'], '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception:
            pass
        lista.append(d)
    return jsonify(lista), 200


@cartao_bp.route('/cartoes/<int:id_cartao>', methods=['GET'])
def buscar_cartao(id_cartao):
    cartao = Cartao.buscar_por_id(id_cartao)
    if cartao is None:
        return jsonify({'erro': 'Cartão não encontrado'}), 404

    d = cartao.to_dict()
    try:
        d['venc_fatura'] = datetime.strptime(d['venc_fatura'], '%Y-%m-%d').strftime('%d/%m/%Y')
    except Exception:
        pass

    return jsonify(d), 200

@cartao_bp.route('/cartoes/usuario/<int:id_usuario>', methods=['GET'])
@token_required
def listar_cartoes_usuario(usuario_id_token, id_usuario):
    # Segurança: só permite listar os próprios cartões
    if usuario_id_token != id_usuario:
        return jsonify({'erro': 'Acesso não autorizado a cartões de outro usuário'}), 403

    cartoes = Cartao.listar_por_usuario(id_usuario)
    lista = []
    for c in cartoes:
        d = c.to_dict()
        try:
            d['venc_fatura'] = datetime.strptime(d['venc_fatura'], '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception:
            pass
        lista.append(d)
    return jsonify(lista), 200
