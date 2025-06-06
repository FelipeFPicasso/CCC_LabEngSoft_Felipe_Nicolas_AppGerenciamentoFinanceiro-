# relatorio_controller.py
from flask import Blueprint, jsonify, Flask, request
from Utils.auth import token_required
from Models.relatorio_model import RelatorioTransacao
from flask_cors import CORS
import Utils.validations as validator

app = Flask(__name__)
CORS(app)
relatorio_transacao_bp = Blueprint('relatorio_transacao_bp', __name__)

@relatorio_transacao_bp.route('/relatorio_transacao/transacao/<int:fk_id_transacao>', methods=['GET'])
@token_required
def get_relatorio_transacao(usuario_id, fk_id_transacao):
    try:
        relatorio = RelatorioTransacao.buscar_por_fk_id_transacao(fk_id_transacao)

        if relatorio:
            return jsonify(relatorio), 200
        else:
            return jsonify({"mensagem": "Relatório não encontrado para esse ID de transação"}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@relatorio_transacao_bp.route('/relatorio-transacao/usuario', methods=['GET'])
@token_required
def get_relatorios_transacoes_por_usuario(usuario_id):
    try:
        relatorios = RelatorioTransacao.buscar_por_id_usuario(usuario_id)

        if relatorios:
            return jsonify({"relatorios": relatorios}), 200
        else:
            return jsonify({"mensagem": "Nenhum relatório encontrado para o usuário."}), 404

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

#retorna transacoes baseado em filtros  
@relatorio_transacao_bp.route('/relatorio_transacao/filtro', methods=['GET'])
@token_required
def resumo_filtros(usuario_id):
    try:
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")
        categorias = request.args.getlist("categorias") 
        tipo = request.args.get("tipo")
        
        data_inicio = validator.valida_data(data_inicio)
        data_fim = validator.valida_data(data_fim)

        dados = RelatorioTransacao.filtro(usuario_id, data_inicio, data_fim, categorias, tipo)

        if dados is None:
            return jsonify({"erro": "Erro ao buscar dados"}), 500

        return jsonify(dados)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
#retorna transacoes baseado em filtros  
@relatorio_transacao_bp.route('/relatorio_transacao/resumo-por-categoria', methods=['GET'])
@token_required
def resumo_por_categoria(usuario_id):
    try:
        data_inicio = request.args.get("data_inicio")
        data_fim = request.args.get("data_fim")
        tipo = request.args.get("tipo")
        
        data_inicio = validator.valida_data(data_inicio)
        data_fim = validator.valida_data(data_fim)

        dados = RelatorioTransacao.resumoCategoria(usuario_id, data_inicio, data_fim, tipo)

        if dados is None:
            return jsonify({"erro": "Erro ao buscar dados"}), 500

        return jsonify(dados)

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    