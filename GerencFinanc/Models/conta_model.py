import psycopg2
from psycopg2 import sql
from Database.conexao import conectar_financeiro

class Conta:
    @staticmethod
    def _conectar():
        return conectar_financeiro()

    def __init__(self, nome_banco, saldo_inicial, fk_id_usuario, fk_id_cartao):
        self.nome_banco = nome_banco
        self.saldo_inicial = saldo_inicial
        self.fk_id_usuario = fk_id_usuario  # Nome alterado para fk_id_usuario
        self.fk_id_cartao = fk_id_cartao  # Nome alterado para fk_id_cartao

    def to_dict(self):
        return {
            'id': self.id,
            'nome_banco': self.nome_banco,
            'saldo_inicial': self.saldo_inicial,
            'fk_id_usuario': self.fk_id_usuario,  # Retorna o campo com o nome correto no banco
            'fk_id_cartao': self.fk_id_cartao  # Retorna o campo com o nome correto no banco
        }

    @classmethod
    def adicionar(cls, conta):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("""
                INSERT INTO conta (nome_banco, saldo_inicial, fk_id_usuario, fk_id_cartao)
                VALUES (%s, %s, %s, %s) RETURNING id
            """)
            cursor.execute(query, (conta.nome_banco, conta.saldo_inicial, conta.fk_id_usuario, conta.fk_id_cartao))

            conta_id = cursor.fetchone()[0]
            conn.commit()

            cursor.close()
            conn.close()

            conta.id = conta_id
            return conta
        except Exception as e:
            print(f"Erro ao adicionar conta: {e}")
            return None

    @classmethod
    def listar_todas(cls):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = "SELECT * FROM conta"
            cursor.execute(query)
            contas_data = cursor.fetchall()

            contas = []
            for c in contas_data:
                conta = Conta(c[1], c[2], c[3], c[4])  # Ajustado para usar fk_id_usuario e fk_id_cartao
                conta.id = c[0]
                contas.append(conta)

            cursor.close()
            conn.close()

            return contas
        except Exception as e:
            print(f"Erro ao listar todas as contas: {e}")
            return []

    @classmethod
    def buscar_por_id(cls, id_conta):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("SELECT * FROM conta WHERE id = %s")
            cursor.execute(query, (id_conta,))
            c = cursor.fetchone()

            cursor.close()
            conn.close()

            if c:
                conta = Conta(c[1], c[2], c[3], c[4])  # Ajustado para usar fk_id_usuario e fk_id_cartao
                conta.id = c[0]
                return conta
            return None
        except Exception as e:
            print(f"Erro ao buscar conta: {e}")
            return None

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("SELECT * FROM conta WHERE fk_id_usuario = %s")
            cursor.execute(query, (id_usuario,))
            contas_data = cursor.fetchall()

            contas = []
            for c in contas_data:
                conta = Conta(c[1], c[2], c[3], c[4])  # Ajustado para usar fk_id_usuario e fk_id_cartao
                conta.id = c[0]
                contas.append(conta)

            cursor.close()
            conn.close()

            return contas
        except Exception as e:
            print(f"Erro ao listar contas por usuário: {e}")
            return []
