from Database.conexao import conectar_financeiro

class Categoria:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @staticmethod
    def listar_todas():
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM categoria_transacao")
            categorias_data = cursor.fetchall()

            categorias = []
            for c in categorias_data:
                categorias.append(Categoria(c[0], c[1]))

            cursor.close()
            conn.close()

            return categorias
        except Exception as e:
            print(f"Erro ao listar categorias: {e}")
            return []
