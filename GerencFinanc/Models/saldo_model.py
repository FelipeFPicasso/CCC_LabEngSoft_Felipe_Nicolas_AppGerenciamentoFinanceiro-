from Database.conexao import conectar_financeiro

class Saldo:
    def __init__(self, fk_id_usuario, fk_id_conta, saldo):
        self.fk_id_usuario = fk_id_usuario
        self.fk_id_conta = fk_id_conta
        self.saldo = saldo

    def to_dict(self):
        return {
            'fk_id_usuario': self.fk_id_usuario,
            'fk_id_conta': self.fk_id_conta,
            'saldo': float(self.saldo)
        }

    @staticmethod
    def buscar_por_usuario_e_conta(fk_id_usuario, fk_id_conta):
        try:
            conn = conectar_financeiro()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT fk_id_usuario, fk_id_conta, saldo
                FROM saldo_atual
                WHERE fk_id_usuario = %s AND fk_id_conta = %s;
            """, (fk_id_usuario, fk_id_conta))

            resultado = cursor.fetchone()
            cursor.close()
            conn.close()

            if resultado:
                return Saldo(*resultado)
            return None
        except Exception as e:
            print(f"Erro ao buscar saldo: {e}")
            return None


