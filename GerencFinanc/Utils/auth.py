from functools import wraps
from flask import request, jsonify
import jwt

# Chave secreta usada para assinar o token (tem que ser a mesma do login)
SECRET_KEY = 'sua_chave_secreta'  # Troque para a mesma chave usada no seu login!

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Verifica se o cabeçalho Authorization está presente
        if 'Authorization' in request.headers:
            # Pega o token após "Bearer"
            token = request.headers['Authorization'].split(" ")[1]  # Pega a segunda parte após "Bearer"

        if not token:
            return jsonify({'erro': 'Token é necessário'}), 401

        try:
            # Aqui decodificamos o token para extrair o usuario_id
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})
            usuario_id = data['usuario_id']  # Usando 'usuario_id' no lugar de 'user_id'
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401

        return f(usuario_id, *args, **kwargs)

    return decorated
