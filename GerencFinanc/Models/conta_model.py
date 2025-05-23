import psycopg2
from psycopg2 import sql
from Database.conexao import conectar_financeiro

class Conta:
    @staticmethod
    def _conectar():
        return conectar_financeiro()

    def __init__(self, nome_banco, saldo_inicial, fk_id_usuario):
        self.nome_banco = nome_banco
        self.saldo_inicial = saldo_inicial
        self.fk_id_usuario = fk_id_usuario

    def to_dict(self):
        return {
            'id': self.id,
            'nome_banco': self.nome_banco,
            'saldo_inicial': self.saldo_inicial,
            'fk_id_usuario': self.fk_id_usuario
        }

    @classmethod
    def adicionar(cls, conta):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("""
                INSERT INTO conta (nome_banco, saldo_inicial, fk_id_usuario)
                VALUES (%s, %s, %s) RETURNING id
            """)
            cursor.execute(query, (conta.nome_banco, conta.saldo_inicial, conta.fk_id_usuario))

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

            cursor.execute("SELECT * FROM conta")
            contas_data = cursor.fetchall()

            contas = []
            for c in contas_data:
                conta = Conta(c[1], c[2], c[3])
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

            cursor.execute("SELECT * FROM conta WHERE id = %s", (id_conta,))
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

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM conta WHERE fk_id_usuario = %s", (id_usuario,))
            contas_data = cursor.fetchall()

            contas = []
            for c in contas_data:
                conta = Conta(c[1], c[2], c[3])
                conta.id = c[0]
                contas.append(conta)

            cursor.close()
            conn.close()

            return contas
        except Exception as e:
            print(f"Erro ao listar contas por usuário: {e}")
            return []

    @classmethod
    def atualizar(cls, id_conta, campos):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            set_clause = ', '.join(f"{col} = %s" for col in campos.keys())
            valores = list(campos.values()) + [id_conta]

            query = f"UPDATE conta SET {set_clause} WHERE id = %s"
            cursor.execute(query, valores)
            success = cursor.rowcount

            conn.commit()
            cursor.close()
            conn.close()
            return success > 0
        except Exception as e:
            print(f"Erro ao atualizar conta: {e}")
            return False

    @classmethod
    def deletar_por_id(cls, id_conta):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            # 1. Buscar saldo da conta que será excluída
            cursor.execute("SELECT saldo_inicial FROM conta WHERE id = %s", (id_conta,))
            resultado = cursor.fetchone()
            if not resultado:
                cursor.close()
                conn.close()
                return False  # Conta não existe
            saldo_conta = resultado[0]

            # 2. Atualizar saldo_atual_total subtraindo o saldo da conta excluída
            cursor.execute("""
                           UPDATE saldo_atual_total
                           SET saldo = saldo - %s
                           WHERE fk_id_usuario = %s
                           """, (saldo_conta, id_conta))

            # 3. Deletar registros na saldo_atual que referenciam essa conta
            cursor.execute("DELETE FROM saldo_atual WHERE fk_id_conta = %s", (id_conta,))

            # 4. Deletar a conta
            cursor.execute("DELETE FROM conta WHERE id = %s", (id_conta,))
            sucesso = cursor.rowcount

            conn.commit()
            cursor.close()
            conn.close()

            return sucesso > 0
        except Exception as e:
            print(f"Erro ao deletar conta: {e}")
            return False

