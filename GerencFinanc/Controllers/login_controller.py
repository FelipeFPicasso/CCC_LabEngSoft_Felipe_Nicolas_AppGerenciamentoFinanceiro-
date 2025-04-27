from flask import Blueprint, request, jsonify
import datetime
from Models.usuario_model import Usuario
from Models.login_model import Login
import bcrypt
import jwt

login_bp = Blueprint('login', __name__)

# Configuração da chave secreta para o JWT
SECRET_KEY = 'sua_chave_secreta'

@login_bp.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    # Verifica se o email e a senha foram fornecidos
    if not (email and senha):
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

    # Busca o usuário pelo email
    usuario = Usuario.buscar_por_email(email)

    # Verifica se o usuário existe e se a senha está correta
    if usuario and verificar_senha(senha, usuario['senha']):
        # Gerar o token JWT com o usuario_id e data de expiração
        payload = {
            'usuario_id': usuario['id'],  # Alterado para 'usuario_id' para ser consistente com o token
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(weeks=1)  # Token expira em 7 dias
        }

        # Codifica o token para uma string
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # Exemplo de resposta com o token para o cliente
        bearer_token = f"Bearer {token}"

        return jsonify({'token': bearer_token}), 200

    else:
        return jsonify({'erro': 'Email ou senha inválidos'}), 401

def verificar_senha(senha_fornecida, hash_armazenado):
    """Verifica se a senha fornecida corresponde ao hash armazenado"""
    return bcrypt.checkpw(senha_fornecida.encode('utf-8'), hash_armazenado.encode('utf-8'))
