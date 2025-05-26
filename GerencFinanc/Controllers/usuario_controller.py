from flask import Blueprint, request, jsonify
import datetime
from Models.usuario_model import Usuario
from Database.conexao import conectar_financeiro
from datetime import datetime
from datetime import datetime, timedelta
import Utils.validations as validator
from random import randint
from Utils.auth import token_required
from Utils.cod_recup_senha import gerar_codigo_recuperacao

usuario_bp = Blueprint('usuario', __name__)

#Busca por ID no banco
def busca_por_id(id_usuario):
    todos = Usuario.listar_todos()
    return next((u for u in todos if u['id'] == id_usuario), None)  

#POST: Cadastro do usuario
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
        validator.valida_todos(email, senha, data_nasc, is_data_nasc=True)

        novo_usuario = Usuario(nome, email, senha, data_nasc, cpf)
        Usuario.adicionar(novo_usuario)

        return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201

    except ValueError as ve:
        return jsonify({'erro': str(ve)}), 409

    except Exception as e:
        return jsonify({'erro': 'Erro ao criar usuário'}), 500

#GET: Busca por todos os usuarios cadastrados
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

#GET: retorna usuarios cadastrados por ID 
@usuario_bp.route('/usuario', methods=['GET'])
@token_required
def buscar_usuario_logado(id_usuario):
    usuario = busca_por_id(id_usuario)

    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    dados_usuario = {
        'id': usuario['id'],
        'nome': usuario['nome'],
        'email': usuario['email'],
        'cpf': usuario['cpf'],
        'data_nasc': usuario['data_nasc']
    }

    return jsonify(dados_usuario), 200

#PUT: Atualiza informacoes de cadastro do usuario
from datetime import datetime

@usuario_bp.route('/usuarios', methods=['PUT'])
@token_required
def atualizar_usuario(id_usuario):
    dados = request.get_json()

    if not busca_por_id(id_usuario):
        return jsonify({'erro': 'Usuário não encontrado'}), 404

    permitidos = {'nome', 'email', 'data_nasc'}

    campos = {
        key: value for key, value in dados.items()
        if key in permitidos
    }

    for campo, valor in list(campos.items()):
        if campo == 'email':
            validator.valida_email(valor)
        if campo == 'data_nasc':
            try:
                validator.valida_data(valor)
                valor_convertido = datetime.strptime(valor, '%d/%m/%Y').date()
                campos[campo] = valor_convertido.isoformat()
            except ValueError:
                return jsonify({'erro': 'Formato de data inválido. Use dd/mm/aaaa.'}), 400

    if not campos:
        return jsonify({'erro': 'Nenhum dado permitido enviado para atualização'}), 400

    if Usuario.atualizar(id_usuario, campos):
        return jsonify({'mensagem': 'Usuário atualizado com sucesso'}), 200
    else:
        return jsonify({'erro': 'Erro ao atualizar usuário'}), 500




@usuario_bp.route('/usuarios', methods=['DELETE'])
@token_required
def deletar_usuario(id_usuario):
    if Usuario.deletar(id_usuario):
        return jsonify({'mensagem': 'Usuário deletado com sucesso'}), 200
    else:
        return jsonify({'erro': 'Erro ao deletar usuário'}), 500

@usuario_bp.route('/usuarios/recuperar', methods=['POST'])
def recuperar_senha():
    dados = request.get_json()
    email = dados.get('email')

    if not email:
        return jsonify({'erro': 'E-mail é obrigatório'}), 400

    usuario = Usuario.buscar_por_email(email)

    if not usuario:
        return jsonify({'erro': 'E-mail não encontrado'}), 404

    # Geração de código de 6 dígitos
    codigo = str(randint(100000, 999999))

    # Expira em 15 minutos
    expiracao = datetime.utcnow() + timedelta(minutes=15)

    # Armazena o código e sua expiração no banco
    Usuario.armazenar_codigo_recuperacao(email, codigo, expiracao)

    # Aqui você enviaria o código por e-mail no mundo real
    print(f"Código de recuperação para {email}: {codigo}")  # Debug

    return jsonify({'mensagem': 'Código de recuperação enviado para o e-mail'}), 200


@usuario_bp.route('/usuarios/senha', methods=['PUT'])
def alterar_senha():
    dados = request.get_json()
    email = dados.get('email')
    nova_senha = dados.get('nova_senha')
    codigo_recuperacao = dados.get('codigo_recuperacao')

    # Verificação de parâmetros obrigatórios
    if not email or not nova_senha or not codigo_recuperacao:
        return jsonify({'erro': 'E-mail, nova senha e código de recuperação são obrigatórios'}), 400

    try:
        # Validação do código de recuperação
        Usuario.validar_codigo_recuperacao(email, codigo_recuperacao)

        # Alteração da senha
        Usuario.alterar_senha(email, nova_senha)

        return jsonify({'mensagem': 'Senha alterada com sucesso'}), 200
    except ValueError as ve:
        # Erros de validação (código inválido ou expirado)
        return jsonify({'erro': str(ve)}), 400
    except Exception as e:
        # Outros erros
        return jsonify({'erro': f'Erro ao atualizar a senha: {str(e)}'}), 500