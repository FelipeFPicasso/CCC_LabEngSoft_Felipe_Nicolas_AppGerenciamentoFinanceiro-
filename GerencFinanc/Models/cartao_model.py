import psycopg2
from psycopg2 import sql
from Database.conexao import conectar_financeiro

class Cartao:
    @staticmethod
    def _conectar():
        return conectar_financeiro()

    def __init__(self, limite, venc_fatura):
        self.limite = limite
        self.venc_fatura = venc_fatura  # string no formato YYYY-MM-DD

    def to_dict(self):
        return {
            'id': self.id,
            'limite': self.limite,
            'venc_fatura': self.venc_fatura
        }

    @classmethod
    def adicionar(cls, cartao, usuario_id=None):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            # Agora, o 'usuario_id' é associado de forma lógica
            query = sql.SQL("""
                INSERT INTO cartao (limite, venc_fatura)
                VALUES (%s, %s) RETURNING id
            """)
            cursor.execute(query, (cartao.limite, cartao.venc_fatura))

            cartao_id = cursor.fetchone()[0]
            conn.commit()

            cursor.close()
            conn.close()

            cartao.id = cartao_id
            return cartao
        except Exception as e:
            print(f"Erro ao adicionar cartão: {e}")
            return None

    @classmethod
    def listar_todos(cls):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM cartao")
            resultados = cursor.fetchall()

            cartoes = []
            for resultado in resultados:
                cartao = Cartao(resultado[1], resultado[2])  # Ajustado conforme a estrutura
                cartao.id = resultado[0]
                cartoes.append(cartao)

            cursor.close()
            conn.close()
            return cartoes
        except Exception as e:
            print(f"Erro ao listar cartões: {e}")
            return []

    @classmethod
    def buscar_por_id(cls, id_cartao):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM cartao WHERE id = %s", (id_cartao,))
            resultado = cursor.fetchone()

            cursor.close()
            conn.close()

            if resultado:
                cartao = Cartao(resultado[1], resultado[2])
                cartao.id = resultado[0]
                return cartao
            return None
        except Exception as e:
            print(f"Erro ao buscar cartão: {e}")
            return None

    @classmethod
    def buscar_por_usuario(cls, usuario_id):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM cartao WHERE fk_id_usuario = %s", (usuario_id,))
            resultados = cursor.fetchall()

            cartoes = []
            for resultado in resultados:
                cartao = Cartao(resultado[1], resultado[2])
                cartao.id = resultado[0]
                cartoes.append(cartao)

            cursor.close()
            conn.close()
            return cartoes
        except Exception as e:
            print(f"Erro ao buscar cartões do usuário: {e}")
            return []
        
    @classmethod
    def deletar_por_id(cls, id_cartao):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cartao WHERE id = %s", (id_cartao,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao buscar cartão: {e}")
            return False
