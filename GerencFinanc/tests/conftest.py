import pytest
import sys
import os
from datetime import datetime

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from main import app
from Database.conexao import conectar_financeiro
from Models.usuario_model import Usuario


@pytest.fixture(scope="session")
def flask_app():
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(flask_app):
    return flask_app.test_client()


@pytest.fixture
def limpar_banco():
    conn = conectar_financeiro()
    cursor = conn.cursor()

    try:
        tabelas = [
            "transacao",
            "limite",
            "cartao",
            "conta",
            "usuario"
        ]

        for tabela in tabelas:
            cursor.execute(f"DELETE FROM {tabela}")

        conn.commit()

        yield

    finally:
        for tabela in tabelas:
            cursor.execute(f"DELETE FROM {tabela}")

        conn.commit()
        cursor.close()
        conn.close()


@pytest.fixture
def usuario_valido(limpar_banco):
    return {
        "nome": "Felipe Teste",
        "email": "felipe@test.com",
        "senha": "Senha@123",
        "data_nasc": "01/01/2000",
        "cpf": "12345678901"
    }


@pytest.fixture
def usuario_invalido():
    return {
        "nome": "",
        "email": "emailerrado",
        "senha": "123"
    }


@pytest.fixture
def usuario_modelo_valido():
    return Usuario(
        nome="Teste",
        email="modelo@test.com",
        senha="Senha@123",
        data_nasc=datetime(2000, 1, 1),
        cpf="11111111111"
    )


@pytest.fixture
def usuario_logado(client, usuario_valido):
    client.post(
        "/usuarios",
        json=usuario_valido
    )

    resposta = client.post(
        "/login",
        json={
            "email": usuario_valido["email"],
            "senha": usuario_valido["senha"]
        }
    )

    return resposta.get_json()["token"]