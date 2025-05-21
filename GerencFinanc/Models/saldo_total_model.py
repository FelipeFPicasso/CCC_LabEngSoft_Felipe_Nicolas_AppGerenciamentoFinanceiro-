from Database.conexao import conectar_financeiro

class SaldoTotal:
    @staticmethod
    def buscar_saldo_total_por_usuario(fk_id_usuario):
        conn = conectar_financeiro()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT SUM(saldo)
                FROM saldo_atual
                WHERE fk_id_usuario = %s
            """, (fk_id_usuario,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado[0] is not None else 0
        except Exception as e:
            print(f"Erro ao buscar saldo total: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
