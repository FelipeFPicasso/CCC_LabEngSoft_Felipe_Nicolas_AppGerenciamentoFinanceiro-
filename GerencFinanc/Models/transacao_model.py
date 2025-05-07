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

    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'valor': self.valor,
            'data': self.data,
            'fk_id_usuario': self.fk_id_usuario,
            'fk_id_tipo_transacao': self.fk_id_tipo_transacao,
            'fk_id_conta': self.fk_id_conta,
            'fk_id_categoria_transacao': self.fk_id_categoria_transacao
        }

    @classmethod
    def adicionar(cls, transacao):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO transacao (descricao, valor, data, fk_id_usuario, fk_id_tipo_transacao,
                                                  fk_id_conta, fk_id_categoria_transacao)
                           VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
                           """, (
                               transacao.descricao,
                               transacao.valor,
                               transacao.data,
                               transacao.fk_id_usuario,
                               transacao.fk_id_tipo_transacao,
                               transacao.fk_id_conta,
                               transacao.fk_id_categoria_transacao
                           ))
            id_inserido = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return id_inserido
        except Exception as e:
            print(
                f"Erro ao inserir transação. Descrição: {transacao.descricao}, Valor: {transacao.valor}, Erro: {str(e)}")
            return None

    @classmethod
    def listar_todas(cls):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM transacao')
            data = cursor.fetchall()

            transacoes = []
            for c in data:
                transacao = Transacao(c[1],c[2],c[3],c[4],c[5],c[6],c[7])
                transacao.id = c[0]
                transacoes.append(transacao)

            cursor.close()
            conn.close()
            return transacoes
        except Exception as e:
            print(f"Erro ao listar todas as transacoes: {e}")
            return []

    @classmethod
    def listar_por_usuario(cls, id_usuario):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            query = 'SELECT * FROM transacao WHERE fk_id_usuario = %s'
            cursor.execute(query, (id_usuario,))
            data = cursor.fetchall()

            transacoes = []
            for c in data:
                transacao = Transacao(c[1],c[2],c[3],c[4],c[5],c[6],c[7])
                transacao.id = c[0]
                transacoes.append(transacao)

            conn.close()
            cursor.close()
            return transacoes
        except Exception as e:
            print(f"Erro ao buscar transacao: {e}")
            return []

    @classmethod
    def buscar_por_id(cls, id_transacao):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM transacao WHERE id = %s', (id_transacao,))
            data = cursor.fetchone()

            transacao = Transacao(data[1],data[2],data[3],data[4],data[5],data[6],data[7])
            transacao.id = data[0]

            cursor.close()
            conn.close()
            return transacao
        except Exception as e:
            print(f"Erro ao buscar transacao: {e}")
            return []

    @classmethod
    def atualizar(cls, fk_id_transacao, campos):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            set_clause = ', '.join(f"{col} = %s" for col in campos.keys())
            valores = list(campos.values()) + [fk_id_transacao]

            cursor.execute(f"UPDATE transacao SET {set_clause} WHERE id = %s", valores)
            success = cursor.rowcount

            conn.commit()
            conn.close()
            cursor.close()
            return success > 0
        except Exception as e:
            print(f"Erro ao atualizar transacao: {e}")
            return False

    @classmethod
    def deletar(cls, id_transacao):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            # Verifica se há vínculos na tabela relatorio_transacao
            cursor.execute("SELECT COUNT(*) FROM relatorio_transacao WHERE fk_id_transacao = %s", (id_transacao,))
            if cursor.fetchone()[0] > 0:
                print(f"Transação {id_transacao} está vinculada a um relatório.")
                cursor.close()
                conn.close()
                return False

            cursor.execute("DELETE FROM transacao WHERE id = %s", (id_transacao,))
            success = cursor.rowcount

            conn.commit()
            cursor.close()
            conn.close()
            return success > 0
        except Exception as e:
            print(f"Erro ao deletar transacao: {e}")
            return False