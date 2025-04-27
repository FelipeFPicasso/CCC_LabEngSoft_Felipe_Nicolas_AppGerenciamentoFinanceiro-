import psycopg2
from psycopg2 import sql
from Database.conexao import conectar_financeiro

class Conta:
    @staticmethod
    def _conectar():
        return conectar_financeiro()

    def __init__(self, nome_banco, saldo_inicial, usuario_id):
        self.nome_banco = nome_banco
        self.saldo_inicial = saldo_inicial
        self.usuario_id = usuario_id

    def to_dict(self):
        return {
            'id': self.id,
            'nome_banco': self.nome_banco,
            'saldo_inicial': self.saldo_inicial,
            'usuario_id': self.usuario_id
        }

    @classmethod
    def adicionar(cls, conta):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("""INSERT INTO conta (nome_banco, saldo_inicial, usuario_id)
                               VALUES (%s, %s, %s) RETURNING id""")
            cursor.execute(query, (conta.nome_banco, conta.saldo_inicial, conta.usuario_id))

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
                conta = Conta(c[1], c[2], c[3])
                conta.id = c[0]
                return conta
            return None
        except Exception as e:
            print(f"Erro ao buscar conta: {e}")
            return None
