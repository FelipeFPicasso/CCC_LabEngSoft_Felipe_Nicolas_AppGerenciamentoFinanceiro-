from flask import Blueprint, request, jsonify
import psycopg2
from psycopg2 import sql
from Database.seeder import seed_registros_fixos
from Database.conexao import conectar_postgres, conectar_financeiro

meu_banco = "financeiro"

def validar_estrutura_db():
    try:
        validar_database(meu_banco)
        criar_tabelas()
    except Exception as e:
        print(f"Erro ao validar estrutura do db: {e}")

def validar_database(meu_banco):
    try:
        conn = conectar_postgres()
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", [meu_banco])
        banco_existe = cursor.fetchone()

        cursor.close()
        conn.close()

        if banco_existe:
            print("Banco existe")
        else:
            criar_banco(meu_banco)
            print("Banco de dados criado com sucesso")

    except Exception as e:
        print(f"Erro ao verificar o banco de dados: {e}")

def criar_banco(meu_banco):
    try:
        conn = conectar_postgres()
        conn.autocommit = True
        cursor = conn.cursor()

        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(meu_banco)))

        cursor.close()
        conn.close()

        criar_tabelas()

    except Exception as e:
        print(f"Erro ao criar o banco '{meu_banco}': {e}")

def criar_tabelas():
    try:
        conn = conectar_financeiro()
        conn.autocommit = True
        cursor = conn.cursor()

        query_tabelas = [
            """CREATE TABLE IF NOT EXISTS usuario (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255),
                email VARCHAR(255),
                senha VARCHAR(255),
                data_nasc DATE,
                cpf VARCHAR(14)
            );""",
            """CREATE TABLE IF NOT EXISTS recorrencia (
                id SERIAL PRIMARY KEY,
                periodo VARCHAR(255)
            );""",
            """CREATE TABLE IF NOT EXISTS categoria_transacao (
                id SERIAL PRIMARY KEY,
                categoria VARCHAR(255)
            );""",
            """CREATE TABLE IF NOT EXISTS tipo_transacao (
                id SERIAL PRIMARY KEY,
                tipo VARCHAR(255)
            );""",
            """CREATE TABLE IF NOT EXISTS cartao (
                id SERIAL PRIMARY KEY,
                limite INT,
                venc_fatura DATE
            );""",
            """CREATE TABLE IF NOT EXISTS conta (
                id SERIAL PRIMARY KEY,
                nome_banco VARCHAR(255),
                saldo_inicial NUMERIC(10,2),
                fk_id_cartao INT,
                fk_id_usuario INT,
                CONSTRAINT fk_id_cartao FOREIGN KEY (fk_id_cartao) REFERENCES cartao(id),
                CONSTRAINT fk_id_usuario FOREIGN KEY (fk_id_usuario) REFERENCES usuario(id)
            );""",
            """CREATE TABLE IF NOT EXISTS limite (
                id SERIAL PRIMARY KEY,
                titulo VARCHAR(255),
                valor NUMERIC(7,2),
                fk_id_usuario INT,
                fk_id_recorrencia INT,
                fk_id_categoria_transacao INT,
                CONSTRAINT fk_id_categoria_transacao FOREIGN KEY (fk_id_categoria_transacao) REFERENCES categoria_transacao(id),
                CONSTRAINT fk_usuario FOREIGN KEY (fk_id_usuario) REFERENCES usuario(id)
            );""",
            """CREATE TABLE IF NOT EXISTS transacao (
                id SERIAL PRIMARY KEY,
                descricao VARCHAR(255),
                valor NUMERIC(7,2),
                data DATE,
                fk_id_usuario INT,
                fk_id_tipo_transacao INT,
                fk_id_conta INT,
                fk_id_categoria_transacao INT,
                CONSTRAINT fk_id_categoria_transacao_nessa FOREIGN KEY (fk_id_categoria_transacao) REFERENCES categoria_transacao(id),
                CONSTRAINT fk_id_tipo_transacao_nessa FOREIGN KEY (fk_id_tipo_transacao) REFERENCES tipo_transacao(id),
                CONSTRAINT fk_usuario_nessa FOREIGN KEY (fk_id_usuario) REFERENCES usuario(id),
                CONSTRAINT fk_id_conta_nessa FOREIGN KEY (fk_id_conta) REFERENCES conta(id)
            );""",
            """CREATE TABLE IF NOT EXISTS saldo_atual (
                id SERIAL PRIMARY KEY,
                fk_id_usuario INT,
                fk_id_conta INT,
                saldo NUMERIC(10,2) DEFAULT 0,
                CONSTRAINT fk_usuario_saldo FOREIGN KEY (fk_id_usuario) REFERENCES usuario(id),
                CONSTRAINT fk_conta_saldo FOREIGN KEY (fk_id_conta) REFERENCES conta(id),
                UNIQUE(fk_id_usuario, fk_id_conta)
            );""",
            """CREATE TABLE IF NOT EXISTS relatorio_transacao(
                id SERIAL PRIMARY KEY,
                fk_id_transacao INT,
                descricao VARCHAR(255),
                valor NUMERIC(7, 2),
                data DATE,
                fk_id_usuario INT,
                fk_id_tipo_transacao INT,
                fk_id_conta INT,
                fk_id_categoria_transacao INT,
                CONSTRAINT fk_relatorio_transacao FOREIGN KEY(fk_id_transacao) REFERENCES transacao(id),
                CONSTRAINT fk_rel_usuario FOREIGN KEY(fk_id_usuario) REFERENCES usuario(id),
                CONSTRAINT fk_rel_tipo FOREIGN KEY(fk_id_tipo_transacao) REFERENCES tipo_transacao(id),
                CONSTRAINT fk_rel_conta FOREIGN KEY(fk_id_conta) REFERENCES conta(id),
                CONSTRAINT fk_rel_categoria FOREIGN KEY(fk_id_categoria_transacao) REFERENCES categoria_transacao(id)
            );"""
        ]

        for query in query_tabelas:
            cursor.execute(query)

        seed_registros_fixos(meu_banco)

        criar_trigger_saldo_atual()

        criar_trigger_relatorio_transacao()

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")

def criar_trigger_saldo_atual():
    try:
        conn = conectar_financeiro()
        cursor = conn.cursor()

        comando_sql = """
        CREATE OR REPLACE FUNCTION atualizar_saldo()
        RETURNS TRIGGER AS $$
        BEGIN
            -- Tenta atualizar o saldo existente
            UPDATE saldo_atual
            SET saldo = saldo + NEW.valor
            WHERE fk_id_usuario = NEW.fk_id_usuario AND fk_id_conta = NEW.fk_id_conta;

            -- Se nenhuma linha foi atualizada, insere um novo saldo
            IF NOT FOUND THEN
                INSERT INTO saldo_atual (fk_id_usuario, fk_id_conta, saldo)
                VALUES (NEW.fk_id_usuario, NEW.fk_id_conta, NEW.valor);
            END IF;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        DROP TRIGGER IF EXISTS trigger_atualizar_saldo ON transacao;

        CREATE TRIGGER trigger_atualizar_saldo
        AFTER INSERT ON transacao
        FOR EACH ROW
        EXECUTE FUNCTION atualizar_saldo();
        """

        cursor.execute(comando_sql)
        conn.commit()

        cursor.close()
        conn.close()

        print("Trigger de saldo_atual criada com sucesso")
    except Exception as e:
        print(f"Erro ao criar trigger de saldo_atual: {e}")

def criar_trigger_relatorio_transacao():
    try:
        conn = conectar_financeiro()
        cursor = conn.cursor()

        comando_sql = """
        -- Função para inserir no relatório
        CREATE OR REPLACE FUNCTION inserir_relatorio_transacao()
        RETURNS TRIGGER AS $$
        BEGIN
            INSERT INTO relatorio_transacao (
                fk_id_transacao,
                descricao,
                valor,
                data,
                fk_id_usuario,
                fk_id_tipo_transacao,
                fk_id_conta,
                fk_id_categoria_transacao
            )
            VALUES (
                NEW.id,
                NEW.descricao,
                NEW.valor,
                NEW.data,
                NEW.fk_id_usuario,
                NEW.fk_id_tipo_transacao,
                NEW.fk_id_conta,
                NEW.fk_id_categoria_transacao
            );
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        -- Trigger que chama a função após uma nova transação
        DROP TRIGGER IF EXISTS trigger_relatorio_transacao ON transacao;

        CREATE TRIGGER trigger_relatorio_transacao
        AFTER INSERT ON transacao
        FOR EACH ROW
        EXECUTE FUNCTION inserir_relatorio_transacao();
        """

        cursor.execute(comando_sql)
        conn.commit()
        cursor.close()
        conn.close()

        print("Trigger de relatorio_transacao criada com sucesso")
    except Exception as e:
        print(f"Erro ao criar trigger de relatorio_transacao: {e}")