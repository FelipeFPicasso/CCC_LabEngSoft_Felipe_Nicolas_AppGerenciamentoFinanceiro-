import psycopg2
from psycopg2 import errors
from psycopg2 import sql
import bcrypt
from Database.conexao import conectar_financeiro
from datetime import datetime, timedelta


class Usuario:
    # Conexão com o banco de dados
    @staticmethod
    def _conectar():
        return conectar_financeiro()

    def __init__(self, nome, email, senha, data_nasc, cpf):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_nasc = data_nasc
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
        conn = None
        cursor = None
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            hashed_senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            query = sql.SQL("""INSERT INTO usuario (nome, email, senha, data_nasc, cpf)
                               VALUES (%s, %s, %s, %s, %s) RETURNING id""")
            cursor.execute(query, (usuario.nome, usuario.email, hashed_senha, usuario.data_nasc, usuario.cpf))

            usuario_id = cursor.fetchone()[0]
            conn.commit()

            usuario.id = usuario_id
            usuario.senha = hashed_senha
            return usuario

        except psycopg2.IntegrityError as e:
            if conn:
                conn.rollback()
            if hasattr(e, 'pgcode') and e.pgcode == '23505':  # Código de erro para violação de unicidade
                raise ValueError("Email ou CPF já cadastrados")
            raise

        except Exception as e:
            if conn:
                conn.rollback()
            raise

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

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
    def atualizar(cls, id_usuario, campos):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            set_clause = ', '.join(f"{col} = %s" for col in campos.keys())
            valores = list(campos.values()) + [id_usuario]

            query = f"UPDATE usuario SET {set_clause} WHERE id = %s"
            cursor.execute(query, valores)
            success = cursor.rowcount

            conn.commit()
            cursor.close()
            conn.close()
            return success > 0
        except Exception as e:
            print(f"Erro ao atualizar usuário: {e}")
            return False

    @classmethod
    def deletar(cls, id_usuario):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            # Primeiro, deletar registros da relatorio_transacao que usam transações do usuário
            cursor.execute("""
                           DELETE
                           FROM relatorio_transacao
                           WHERE fk_id_transacao IN (SELECT id
                                                            FROM transacao
                                                            WHERE fk_id_usuario = %s)
                           """, (id_usuario,))

            # Depois, deletar os registros em cascata manual
            cursor.execute("DELETE FROM transacao WHERE fk_id_usuario = %s", (id_usuario,))
            cursor.execute("DELETE FROM saldo_atual WHERE fk_id_usuario = %s", (id_usuario,))
            cursor.execute("DELETE FROM limite WHERE fk_id_usuario = %s", (id_usuario,))
            cursor.execute("DELETE FROM conta WHERE fk_id_usuario = %s", (id_usuario,))
            cursor.execute("DELETE FROM saldo_atual_total WHERE fk_id_usuario = %s", (id_usuario,))


            # Por fim, deletar o usuário
            cursor.execute("DELETE FROM usuario WHERE id = %s", (id_usuario,))
            success = cursor.rowcount

            conn.commit()
            cursor.close()
            conn.close()
            return success > 0
        except Exception as e:
            print(f"Erro ao deletar usuário e dados relacionados: {e}")
            return False

    @classmethod
    def armazenar_codigo_recuperacao(cls, email, codigo, expiracao):
        conn = conectar_financeiro()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE usuario
                       SET codigo_recuperacao = %s,
                           codigo_expira_em   = %s
                       WHERE email = %s
                       """, (codigo, expiracao, email))
        conn.commit()

        # Verificação para garantir que a atualização foi feita
        cursor.execute("SELECT codigo_recuperacao FROM usuario WHERE email = %s", (email,))
        resultado = cursor.fetchone()
        if resultado and resultado[0] == codigo:
            print(f"Código de recuperação para {email} atualizado com sucesso.")
        else:
            print(f"Falha ao atualizar código de recuperação para {email}.")

        cursor.close()
        conn.close()

    @classmethod
    def alterar_senha(cls, email, nova_senha):
        # Criptografa a nova senha
        hashed_senha = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Atualiza a senha no banco
        conn = cls._conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                           UPDATE usuario
                           SET senha = %s
                           WHERE email = %s
                           """, (hashed_senha, email))

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Erro ao alterar a senha: {e}")
            raise
        return True

    @classmethod
    def validar_codigo_recuperacao(cls, email, codigo):
        conn = conectar_financeiro()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT codigo_recuperacao, codigo_expira_em
                       FROM usuario
                       WHERE email = %s
                       """, (email,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        if not resultado:
            raise ValueError("E-mail não encontrado")

        codigo_armazenado, expiracao = resultado
        print(f"Código armazenado: {codigo_armazenado}, Expiração: {expiracao}")

        if codigo != codigo_armazenado:
            raise ValueError("Código inválido")

        # Verificação de expiração
        if expiracao and datetime.utcnow() > expiracao:
            raise ValueError("Código expirado")

        return True