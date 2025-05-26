from Database.conexao import conectar_financeiro

class Limite:
    def __init__(self, id=None, titulo=None, valor=None, fk_id_recorrencia=None, fk_id_categoria_transacao=None, fk_id_usuario=None):
        self.id = id
        self.titulo = titulo
        self.valor = valor
        self.fk_id_recorrencia = fk_id_recorrencia
        self.fk_id_categoria_transacao = fk_id_categoria_transacao
        self.fk_id_usuario = fk_id_usuario

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'valor': self.valor,
            'fk_id_recorrencia': self.fk_id_recorrencia,
            'fk_id_categoria_transacao': self.fk_id_categoria_transacao,
            'fk_id_usuario': self.fk_id_usuario
        }

    @staticmethod
    def adicionar(limite):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO limite (titulo, valor, fk_id_usuario, fk_id_recorrencia, fk_id_categoria_transacao)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, titulo, valor, fk_id_usuario, fk_id_recorrencia, fk_id_categoria_transacao;
            """, (limite.titulo, limite.valor, limite.fk_id_usuario, limite.fk_id_recorrencia, limite.fk_id_categoria_transacao))

            resultado = cursor.fetchone()
            conn.commit()
            cursor.close()
            conn.close()

            if resultado:
                novo_limite = Limite(
                    id=resultado[0],
                    titulo=resultado[1],
                    valor=resultado[2],
                    fk_id_usuario=resultado[3],
                    fk_id_recorrencia=resultado[4],
                    fk_id_categoria_transacao=resultado[5]
                )
                return novo_limite
            else:
                return None

        except Exception as e:
            print(f"Erro ao adicionar limite: {e}")
            return None

    @staticmethod
    def listar_todos():
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("SELECT id, titulo, valor, fk_id_usuario, fk_id_recorrencia, fk_id_categoria_transacao FROM limite")
            resultados = cursor.fetchall()

            limites = []
            for resultado in resultados:
                limites.append(Limite(
                    id=resultado[0],
                    titulo=resultado[1],
                    valor=resultado[2],
                    fk_id_usuario=resultado[3],
                    fk_id_recorrencia=resultado[4],
                    fk_id_categoria_transacao=resultado[5]
                ))

            cursor.close()
            conn.close()
            return limites
        except Exception as e:
            print(f"Erro ao listar limites: {e}")
            return []

    @staticmethod
    def buscar_por_id(id_limite):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("SELECT id, titulo, valor, fk_id_usuario, fk_id_recorrencia, fk_id_categoria_transacao FROM limite WHERE id = %s", (id_limite,))
            resultado = cursor.fetchone()

            cursor.close()
            conn.close()

            if resultado:
                return Limite(
                    id=resultado[0],
                    titulo=resultado[1],
                    valor=resultado[2],
                    fk_id_usuario=resultado[3],
                    fk_id_recorrencia=resultado[4],
                    fk_id_categoria_transacao=resultado[5]
                )
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar limite por ID: {e}")
            return None

    @staticmethod
    def listar_por_usuario(id_usuario):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT id, titulo, valor, fk_id_usuario, fk_id_recorrencia, fk_id_categoria_transacao FROM limite WHERE fk_id_usuario = %s",
                (id_usuario,)
            )
            resultados = cursor.fetchall()

            limites = []
            for resultado in resultados:
                limites.append(Limite(
                    id=resultado[0],
                    titulo=resultado[1],
                    valor=resultado[2],
                    fk_id_usuario=resultado[3],
                    fk_id_recorrencia=resultado[4],
                    fk_id_categoria_transacao=resultado[5]
                ))

            cursor.close()
            conn.close()
            return limites
        except Exception as e:
            print(f"Erro ao listar limites por usuário: {e}")
            return []

    @staticmethod
    def deletar(id_limite):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM limite WHERE id = %s", (id_limite,))
            conn.commit()

            deletado = cursor.rowcount  # número de linhas afetadas
            cursor.close()
            conn.close()

            return deletado > 0
        except Exception as e:
            print(f"Erro ao deletar limite: {e}")
            return False

    @staticmethod
    def atualizar(id, titulo, valor, fk_id_categoria_transacao, fk_id_recorrencia):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("""
                           UPDATE limite
                           SET titulo                    = %s,
                               valor                     = %s,
                               fk_id_categoria_transacao = %s,
                               fk_id_recorrencia         = %s
                           WHERE id = %s
                           """, (titulo, valor, fk_id_categoria_transacao, fk_id_recorrencia, id))

            conn.commit()

            atualizado = cursor.rowcount > 0

            cursor.close()
            conn.close()

            return atualizado

        except Exception as e:
            print(f"Erro ao atualizar limite: {e}")
            return False

