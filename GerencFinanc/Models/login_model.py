import psycopg2
from psycopg2 import sql
import bcrypt

class Login:
    @staticmethod
    def _conectar():
        return psycopg2.connect(
            host='localhost',
            database='financeiro',
            user='postgres',
            password='postgres',
            client_encoding='UTF8'
        )

    @classmethod
    def buscar_por_email(cls, email):
        """Busca um usuário pelo email para a autenticação"""
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("SELECT * FROM usuario WHERE email = %s")
            cursor.execute(query, (email,))

            usuario = cursor.fetchone()

            cursor.close()
            conn.close()

            if usuario:
                return {
                    'id': usuario[0],
                    'nome': usuario[1],
                    'email': usuario[2],
                    'senha': usuario[3],  # A senha retornada é com hash
                    'data_nasc': usuario[4],
                    'cpf': usuario[5]
                }
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por email: {e}")
            return None

    @classmethod
    def verificar_senha(cls, senha_fornecida, hash_armazenado):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return bcrypt.checkpw(senha_fornecida.encode('utf-8'), hash_armazenado.encode('utf-8'))
