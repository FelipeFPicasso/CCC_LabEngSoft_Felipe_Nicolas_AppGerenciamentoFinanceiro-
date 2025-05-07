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
