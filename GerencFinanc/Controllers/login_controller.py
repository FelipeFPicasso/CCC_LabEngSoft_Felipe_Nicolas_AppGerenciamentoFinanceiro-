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

    if not (email and senha):
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

    usuario = Usuario.buscar_por_email(email)

    if usuario and verificar_senha(senha, usuario['senha']):
        # Gerar o token JWT
        payload = {
            'user_id': usuario['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'token': token}), 200
    else:
        return jsonify({'erro': 'Email ou senha inválidos'}), 401


def verificar_senha(senha_fornecida, hash_armazenado):
    """Verifica se a senha fornecida corresponde ao hash armazenado"""
    return bcrypt.checkpw(senha_fornecida.encode('utf-8'), hash_armazenado.encode('utf-8'))
