import psycopg2

def conectar_postgres():
    return psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='postgres',
        client_encoding='UTF8'
    )

def conectar_financeiro():
    return psycopg2.connect(
        host='localhost',
        database='financeiro',
        user='postgres',
        password='postgres',
        client_encoding='UTF8'
    )
