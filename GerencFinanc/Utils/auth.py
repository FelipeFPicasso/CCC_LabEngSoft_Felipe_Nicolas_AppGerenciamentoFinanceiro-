from functools import wraps
from flask import request, jsonify
import jwt

# Chave secreta usada para assinar o token (tem que ser a mesma do login)
SECRET_KEY = 'sua_chave_secreta'  # Troque para a mesma chave usada no seu login!

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Permite requisições OPTIONS passarem sem autenticação
        if request.method == 'OPTIONS':
            return '', 200

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'erro': 'Token é necessário'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": True})
            usuario_id = data['usuario_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'erro': 'Token inválido'}), 401

        return f(usuario_id, *args, **kwargs)

    return decorated

