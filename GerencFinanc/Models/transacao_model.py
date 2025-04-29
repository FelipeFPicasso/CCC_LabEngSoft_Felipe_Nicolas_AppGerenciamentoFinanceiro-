from Database.conexao import conectar_financeiro

class Transacao:
    def __init__(self, descricao, valor, data, fk_id_usuario, fk_id_tipo_transacao, fk_id_conta, fk_id_categoria_transacao):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.fk_id_usuario = fk_id_usuario
        self.fk_id_tipo_transacao = fk_id_tipo_transacao
        self.fk_id_conta = fk_id_conta
        self.fk_id_categoria_transacao = fk_id_categoria_transacao

    @classmethod
    def adicionar(cls, transacao):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            query = """
                INSERT INTO transacao (descricao, valor, data, fk_id_usuario, fk_id_tipo_transacao, fk_id_conta, fk_id_categoria_transacao)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, (
                transacao.descricao,
                transacao.valor,
                transacao.data,
                transacao.fk_id_usuario,
                transacao.fk_id_tipo_transacao,
                transacao.fk_id_conta,
                transacao.fk_id_categoria_transacao
            ))

            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao adicionar transação: {e}")
            return False
