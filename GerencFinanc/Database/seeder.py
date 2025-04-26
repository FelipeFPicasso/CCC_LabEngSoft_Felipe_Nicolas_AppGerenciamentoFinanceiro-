import psycopg2

from Database.conexao import conectar_financeiro


def seed_registros_fixos(meu_banco):
    try:
        conn = conectar_financeiro()
        conn.autocommit = True
        cursor = conn.cursor()

        # Recorrência
        cursor.execute("SELECT COUNT(*) FROM recorrencia;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO recorrencia (periodo) VALUES 
                ('Diário'), ('Semanal'), ('Mensal'),
                ('Semestral'), ('Anual');
            """)

        # Categoria de transação
        cursor.execute("SELECT COUNT(*) FROM categoria_transacao;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO categoria_transacao (categoria) VALUES
                ('Alimentação'), ('Transporte'), ('Lazer'), ('Saúde'),
                ('Educação'), ('Moradia'), ('Investimentos'),
                ('Assinaturas'), ('Compras');
            """)

        # Tipo de transação
        cursor.execute("SELECT COUNT(*) FROM tipo_transacao;")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO tipo_transacao (tipo) VALUES
                ('Receita'), ('Despesa');
            """)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao executar o seeder: {e}")
