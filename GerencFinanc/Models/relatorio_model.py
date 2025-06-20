# relatorio_model.py
import psycopg2
from Database.conexao import conectar_financeiro

class RelatorioTransacao:
    @staticmethod
    def buscar_por_fk_id_transacao(fk_id_transacao):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            query = """
                SELECT 
                    r.fk_id_transacao,
                    t.descricao,
                    t.valor,
                    t.data,
                    u.nome AS nome_usuario,
                    tt.tipo AS tipo_transacao,
                    c.nome_banco AS nome_conta,
                    cat.categoria AS nome_categoria
                FROM relatorio_transacao r
                JOIN transacao t ON t.id = r.fk_id_transacao
                JOIN usuario u ON t.fk_id_usuario = u.id
                JOIN tipo_transacao tt ON t.fk_id_tipo_transacao = tt.id
                JOIN conta c ON t.fk_id_conta = c.id
                JOIN categoria_transacao cat ON t.fk_id_categoria_transacao = cat.id
                WHERE r.fk_id_transacao = %s;
            """

            cursor.execute(query, (fk_id_transacao,))
            row = cursor.fetchone()

            cursor.close()
            conn.close()

            if row:
                relatorio = {
                    "fk_id_transacao": row[0],
                    "descricao": row[1],
                    "valor": float(row[2]),
                    "data": row[3].isoformat(),
                    "nome_usuario": row[4],
                    "tipo_transacao": row[5],
                    "nome_conta": row[6],
                    "nome_categoria": row[7]
                }
                return relatorio
            else:
                return None

        except Exception as e:
            raise Exception(f"Erro ao buscar relatório: {str(e)}")

    @staticmethod
    def buscar_por_id_usuario(id_usuario):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            query = """
                    SELECT r.fk_id_transacao, \
                           t.descricao, \
                           t.valor, \
                           t.data, \
                           u.nome        AS nome_usuario, \
                           tt.tipo       AS tipo_transacao, \
                           c.nome_banco  AS nome_conta, \
                           cat.categoria AS nome_categoria
                    FROM relatorio_transacao r
                             JOIN transacao t ON t.id = r.fk_id_transacao
                             JOIN usuario u ON t.fk_id_usuario = u.id
                             JOIN tipo_transacao tt ON t.fk_id_tipo_transacao = tt.id
                             JOIN conta c ON t.fk_id_conta = c.id
                             JOIN categoria_transacao cat ON t.fk_id_categoria_transacao = cat.id
                    WHERE t.fk_id_usuario = %s
                    ORDER BY t.data DESC; \
                    """

            cursor.execute(query, (id_usuario,))
            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            relatorios = []
            for row in rows:
                relatorios.append({
                    "fk_id_transacao": row[0],
                    "descricao": row[1],
                    "valor": float(row[2]),
                    "data": row[3].isoformat(),
                    "nome_usuario": row[4],
                    "tipo_transacao": row[5],
                    "nome_conta": row[6],
                    "nome_categoria": row[7]
                })

            return relatorios

        except Exception as e:
            raise Exception(f"Erro ao buscar relatórios do usuário: {str(e)}")
        
    @staticmethod
    def filtro(usuario_id, data_inicio=None, data_fim=None, categorias=None, tipo=None):
        try:
            conn = conectar_financeiro()
            cur = conn.cursor()

            query = """
                SELECT c.categoria AS categoria, tp.tipo AS tipo, data, SUM(t.valor)
                FROM transacao t
                JOIN categoria_transacao c ON c.id = t.fk_id_categoria_transacao
                JOIN tipo_transacao tp ON tp.id = t.fk_id_tipo_transacao
                WHERE t.fk_id_usuario = %s
            """
            params = [usuario_id]

            if tipo and tipo.capitalize() in ['Receita','Despesa']:
                query += " AND tp.tipo = %s"
                params.append(tipo.capitalize())

            if data_inicio:
                query += " AND data >= %s"
                params.append(data_inicio)

            if data_fim:
                query += " AND data <= %s"
                params.append(data_fim)

            if categorias and len(categorias) > 0:
                query += " AND c.categoria = ANY(%s)"
                params.append(categorias)
                
            query += " GROUP BY categoria, tipo, data ORDER BY SUM(valor) DESC"

            cur.execute(query, params)
            resultados = cur.fetchall()

            cur.close()
            conn.close()

            return [{"categoria": r[0], "tipo": r[1], "data": r[2], "total": float(r[3])} for r in resultados]

        except Exception as e:
            print(f"Erro ao buscar gastos por categoria: {e}")
            return None
        
    @staticmethod
    def resumoCategoria(usuario_id, data_inicio=None, data_fim=None, tipo=None, categorias=None):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            query = """
                SELECT c.categoria AS categoria, SUM(t.valor) AS total
                FROM transacao t
                JOIN categoria_transacao c ON c.id = t.fk_id_categoria_transacao
                JOIN tipo_transacao tp ON tp.id = t.fk_id_tipo_transacao
                WHERE t.fk_id_usuario = %s
            """
            params = [usuario_id]

            if data_inicio:
                query += " AND t.data >= %s"
                params.append(data_inicio)

            if data_fim:
                query += " AND t.data <= %s"
                params.append(data_fim)

            if tipo and tipo.capitalize() in ['Receita', 'Despesa']:
                query += " AND tp.tipo = %s"
                params.append(tipo.capitalize())

            if categorias:
                query += " AND c.categoria IN %s"
                params.append(tuple(categorias))

            query += " GROUP BY c.categoria ORDER BY total DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            cursor.close()
            conn.close()

            return [
                {"categoria": row[0], "total": float(row[1])}
                for row in rows
            ]
        except Exception as e:
            print(f"Erro ao buscar resumo por categoria: {e}")
            return None


        
