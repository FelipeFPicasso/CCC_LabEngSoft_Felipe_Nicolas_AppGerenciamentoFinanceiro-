from flask import Blueprint, jsonify
from Models.categoria_model import Categoria

categorias_bp = Blueprint('categorias', __name__)

@categorias_bp.route('/categorias', methods=['GET'])
def get_categorias():
    categorias = Categoria.listar_todas()
    return jsonify([
        {"id": cat.id, "nome": cat.nome} for cat in categorias
    ])
