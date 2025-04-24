import psycopg2
from psycopg2 import sql

class Usuario:
    # Conexão com o banco de dados
    @staticmethod
    def _conectar():
        return psycopg2.connect(
            host='localhost',
            database='financeiro',  # Conectar ao banco de dados 'financeiro'
            user='postgres',
            password='postgres',
            client_encoding='UTF8'
        )

    def __init__(self, nome, email, senha, data_nasc, cpf):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_nasc = data_nasc  # deve ser uma string no formato YYYY-MM-DD
        self.cpf = cpf

    def to_dict(self):
        return {
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

            query = sql.SQL("""
                INSERT INTO usuario (nome, email, senha, data_nasc, cpf)
                VALUES (%s, %s, %s, %s, %s) RETURNING id
            """)
            cursor.execute(query, (usuario.nome, usuario.email, usuario.senha, usuario.data_nasc, usuario.cpf))

            # Pegando o id gerado automaticamente após o insert
            usuario_id = cursor.fetchone()[0]
            conn.commit()

            cursor.close()
            conn.close()

            # Atualizando o objeto com o id gerado
            usuario.id = usuario_id
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

            return [{'id': u[0], 'nome': u[1], 'email': u[2], 'senha': u[3], 'data_nasc': u[4], 'cpf': u[5]} for u in usuarios]
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")
            return []


    @classmethod
    def buscar_por_id(cls, usuario_id):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("SELECT * FROM usuario WHERE id = %s")
            cursor.execute(query, [usuario_id])

            resultado = cursor.fetchone()

            cursor.close()
            conn.close()

            if resultado:
                return {
                    'id': resultado[0],
                    'nome': resultado[1],
                    'email': resultado[2],
                    'senha': resultado[3],
                    'data_nasc': resultado[4],
                    'cpf': resultado[5]
                }
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar usuário por ID: {e}")
            return None

