from flask import Blueprint, request, jsonify
import datetime
from Models.usuario_model import Usuario
from Database.conexao import conectar_financeiro


usuario_bp = Blueprint('usuario', __name__)

def busca_por_id(id_usuario):
    todos = Usuario.listar_todos()
    return next((u for u in todos if u['id'] == id_usuario), None)  

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.get_json()
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    data_nasc = dados.get('data_nasc')
    cpf = dados.get('cpf')

    if not (nome and email and senha and data_nasc and cpf):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    try:
        datetime.datetime.strptime(data_nasc, '%Y-%m-%d')
    except ValueError:
        return jsonify({'erro': 'data_nasc deve estar no formato YYYY-MM-DD'}), 400

    novo_usuario = Usuario(nome, email, senha, data_nasc, cpf)
    resultado = Usuario.adicionar(novo_usuario)

    if resultado == 'unique_violation':
        return jsonify({'erro': 'Email ou CPF já cadastrados'}), 409  # 409 Conflict
    elif resultado:
        return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201
    else:
        return jsonify({'erro': 'Erro ao criar usuário'}), 500

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    nome = request.args.get('nome')
    email = request.args.get('email')

    usuarios = Usuario.listar_todos()

    # Aplicar filtro se nome ou email forem fornecidos
    if nome:
        usuarios = [u for u in usuarios if nome.lower() in u['nome'].lower()]
    if email:
        usuarios = [u for u in usuarios if email.lower() in u['email'].lower()]

    return jsonify(usuarios), 200

@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
def buscar_usuario_por_id(id_usuario):
    usuario = busca_por_id(id_usuario)

    if usuario:
        return jsonify(usuario), 200
    return jsonify({'erro': 'Usuário não encontrado'}), 404

@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    dados = request.get_json()

    if not busca_por_id(id_usuario):
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    permitidos = {'nome', 'email', 'senha', 'data_nasc'}

    campos = {
        key: value for key, value in dados.items() 
        if key in permitidos
    }

    if not campos:
        return jsonify({'erro': 'Nenhum dado enviado para atualização'}), 400
    
    if Usuario.atualizar(id_usuario, campos):
        return jsonify({'mensagem': 'Usuário atualizado com sucesso'}), 200
    else:
        return jsonify({'erro': 'Erro ao atualizar usuário'}), 500


@classmethod
def deletar(cls, id_transacao):
    try:
        conn = conectar_financeiro()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM transacao WHERE id = %s", (id_transacao,))
        success = cursor.rowcount

        conn.commit()
        conn.close()
        cursor.close()
        return success > 0
    except Exception as e:
        print(f"Erro ao buscar transacao: {e}")
        return False
