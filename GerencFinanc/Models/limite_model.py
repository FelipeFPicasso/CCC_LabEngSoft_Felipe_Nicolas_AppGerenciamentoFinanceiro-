from Database.conexao import conectar_financeiro

class Limite:
    def __init__(self, titulo, valor, fk_id_recorrencia, fk_id_categoria_transacao, fk_id_usuario):
        self.titulo = titulo
        self.valor = valor
        self.fk_id_recorrencia = fk_id_recorrencia
        self.fk_id_categoria_transacao = fk_id_categoria_transacao
        self.fk_id_usuario = fk_id_usuario

    def to_dict(self):
        return {
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
                # AQUI, instanciamos o objeto Limite com os valores do banco
                novo_limite = Limite(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
                return novo_limite
            else:
                return None

        except Exception as e:
            print(f"Erro ao adicionar limite: {e}")
            return None

    # METODO PARA LISTAR TODOS OS LIMITES
    @staticmethod
    def listar_todos():
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("SELECT id, titulo, valor, fk_id_usuario, fk_id_recorrencia, fk_id_categoria_transacao FROM limite")
            resultados = cursor.fetchall()

            limites = []
            for resultado in resultados:
                limites.append(Limite(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5]))

            cursor.close()
            conn.close()
            return limites
        except Exception as e:
            print(f"Erro ao listar limites: {e}")
            return []

    # METODO PARA BUSCAR LIMITE PELO ID
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
                return Limite(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar limite por ID: {e}")
            return None

    # METODO PARA LISTAR LIMITES POR USUÁRIO
    @staticmethod
    def listar_por_usuario(id_usuario):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("SELECT id, titulo, valor, fk_id_usuario, fk_id_recorrencia, fk_id_categoria_transacao FROM limite WHERE fk_id_usuario = %s", (id_usuario,))
            resultados = cursor.fetchall()

            limites = []
            for resultado in resultados:
                limites.append(Limite(resultado[1], resultado[2], resultado[3], resultado[4], resultado[5]))

            cursor.close()
            conn.close()
            return limites
        except Exception as e:
            print(f"Erro ao listar limites por usuário: {e}")
            return []
