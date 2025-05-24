from datetime import datetime, date

import psycopg2
from psycopg2 import sql
from Database.conexao import conectar_financeiro

class Cartao:

    @staticmethod
    def _conectar():
        return conectar_financeiro()

    def __init__(self, limite, venc_fatura, fk_id_conta=None):
        self.id = None
        self.limite = limite
        self.venc_fatura = venc_fatura  # string no formato YYYY-MM-DD
        self.fk_id_conta = fk_id_conta  # ID da conta associada ao cartão
        self.nome_conta = None  # novo atributo

    def to_dict(self):
        venc = self.venc_fatura
        if isinstance(venc, (datetime, date)):
            venc_formatado = venc.strftime('%d/%m/%Y')
        else:
            # Caso seja string, tenta parsear para datetime para formatar, senão retorna como está
            try:
                dt = datetime.strptime(venc, '%Y-%m-%d')
                venc_formatado = dt.strftime('%d/%m/%Y')
            except Exception:
                venc_formatado = venc  # mantém o que veio, pode ser None ou string já formatada

        return {
            'id': self.id,
            'limite': self.limite,
            'venc_fatura': venc_formatado,
            'fk_id_conta': self.fk_id_conta,
            'nome_conta': self.nome_conta
        }

    @classmethod
    def adicionar(cls, cartao):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = sql.SQL("""
                INSERT INTO cartao (limite, venc_fatura, fk_id_conta)
                VALUES (%s, %s, %s) RETURNING id
            """)
            cursor.execute(query, (cartao.limite, cartao.venc_fatura, cartao.fk_id_conta))

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

            cursor.execute("SELECT id, limite, venc_fatura, fk_id_conta FROM cartao")
            resultados = cursor.fetchall()

            cartoes = []
            for resultado in resultados:
                cartao = Cartao(resultado[1], resultado[2], resultado[3])
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

            cursor.execute("SELECT id, limite, venc_fatura, fk_id_conta FROM cartao WHERE id = %s", (id_cartao,))
            resultado = cursor.fetchone()

            cursor.close()
            conn.close()

            if resultado:
                cartao = Cartao(resultado[1], resultado[2], resultado[3])
                cartao.id = resultado[0]
                return cartao
            return None
        except Exception as e:
            print(f"Erro ao buscar cartão: {e}")
            return None

    @classmethod
    def atualizar(cls, id_cartao, campos):
        """
        Atualiza os campos do cartão com id=id_cartao.
        campos: dict com as colunas e seus novos valores.
        Retorna True se atualizado com sucesso, False caso contrário.
        """
        if not campos:
            return False

        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            # Monta a cláusula SET dinamicamente para a query SQL
            set_clause = ', '.join(f"{col} = %s" for col in campos.keys())
            valores = list(campos.values()) + [id_cartao]

            query = f"UPDATE cartao SET {set_clause} WHERE id = %s"
            cursor.execute(query, valores)
            success = cursor.rowcount > 0

            conn.commit()
            cursor.close()
            conn.close()

            return success
        except Exception as e:
            print(f"Erro ao atualizar cartão: {e}")
            return False

    @classmethod
    def deletar_por_id(cls, id_cartao):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM cartao WHERE id = %s", (id_cartao,))
            success = cursor.rowcount

            conn.commit()
            cursor.close()
            conn.close()
            return success > 0
        except Exception as e:
            print(f"Erro ao deletar cartão: {e}")
            return False

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            query = """
                    SELECT cartao.id, cartao.limite, cartao.venc_fatura, cartao.fk_id_conta, conta.nome_banco
                    FROM cartao
                             INNER JOIN conta ON cartao.fk_id_conta = conta.id
                    WHERE conta.fk_id_usuario = %s \
                    """
            cursor.execute(query, (usuario_id,))
            resultados = cursor.fetchall()

            cartoes = []
            for resultado in resultados:
                cartao = Cartao(resultado[1], resultado[2], resultado[3])
                cartao.id = resultado[0]
                # Adiciona o nome da conta para o retorno
                cartao.nome_conta = resultado[4]
                cartoes.append(cartao)

            cursor.close()
            conn.close()
            return cartoes
        except Exception as e:
            print(f"Erro ao listar cartões por usuário: {e}")
            return []

    @classmethod
    def deletar_por_id(cls, id_cartao):
        try:
            conn = cls._conectar()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM cartao WHERE id = %s", (id_cartao,))
            sucesso = cursor.rowcount

            conn.commit()
            cursor.close()
            conn.close()

            return sucesso > 0
        except Exception as e:
            print(f"Erro ao deletar cartão: {e}")
            return False

