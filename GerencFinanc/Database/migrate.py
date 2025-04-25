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
            );"""
        ]

        for query in query_tabelas:
            cursor.execute(query)

        seed_registros_fixos(meu_banco)

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")