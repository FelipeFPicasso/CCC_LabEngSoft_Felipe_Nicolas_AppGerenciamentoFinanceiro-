import psycopg2
from psycopg2 import sql
import bcrypt
from Database.conexao import conectar_financeiro

class Usuario:
    # Conexão com o banco de dados
    @staticmethod
    def _conectar():
        return conectar_financeiro()

    def __init__(self, nome, email, senha, data_nasc, cpf):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_nasc = data_nasc  # deve ser uma string no formato YYYY-MM-DD
        self.cpf = cpf

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'data_nasc': self.data_nasc,
            'cpf': self.cpf
        }

    @classmethod
    def adicionar(cls, usuario):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            # Gerar o hash da senha com o bcrypt
            hashed_senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            query = sql.SQL("""INSERT INTO usuario (nome, email, senha, data_nasc, cpf)
                               VALUES (%s, %s, %s, %s, %s) RETURNING id""")
            cursor.execute(query, (usuario.nome, usuario.email, hashed_senha, usuario.data_nasc, usuario.cpf))

            # Pegando o id gerado automaticamente após o insert
            usuario_id = cursor.fetchone()[0]
            conn.commit()

            cursor.close()
            conn.close()

            # Atualizando o objeto com o id gerado
            usuario.id = usuario_id
            usuario.senha = hashed_senha  # Armazenando a senha como string do hash
            return usuario
        except Exception as e:
            print(f"Erro ao adicionar usuário: {e}")
            return None

    @classmethod
    def listar_todos(cls):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("SELECT * FROM usuario")
            cursor.execute(query)

            usuarios = cursor.fetchall()

            cursor.close()
            conn.close()

            return [{'id': u[0], 'nome': u[1], 'email': u[2], 'senha': u[3], 'data_nasc': u[4].strftime('%Y-%m-%d'), 'cpf': u[5]} for u in usuarios]
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []

    @classmethod
    def buscar_por_email(cls, email):
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
                    'senha': usuario[3],  # A senha vai ser retornada com hash
                    'data_nasc': usuario[4],
                    'cpf': usuario[5]
                }
            return None
        except Exception as e:
            print(f"Erro ao buscar usuário por email: {e}")
            return None
        
    @classmethod
    def deletar(cls, id_usuario):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()
            query = sql.SQL("DELETE FROM usuario WHERE id = %s")
            cursor.execute(query, (id_usuario,))
            conn.commit()
            sucesso = cursor.rowcount > 0
            cursor.close()
            conn.close()
            return sucesso
        except Exception as e:
            print(f"Erro ao deletar usuário: {e}")
            return False

