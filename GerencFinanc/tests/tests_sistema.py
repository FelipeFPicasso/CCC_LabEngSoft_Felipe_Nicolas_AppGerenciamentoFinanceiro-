import pytest
from unittest.mock import MagicMock, patch


# ----------------------------
# Sistema Cadastro Usuário
# ----------------------------

def test_cadastrar_usuario(client):

    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = (1,)

    conn.commit.return_value = None
    cursor.execute.return_value = None

    with patch(
        "Models.usuario_model.conectar_financeiro",
        return_value=conn
    ), patch(
        "Models.usuario_model.bcrypt.hashpw",
        return_value=b"hash_fake"
    ):

        resposta = client.post(
            "/usuarios",
            json={
                "nome": "Felipe",
                "email": "felipe@test.com",
                "senha": "Felipe@123",
                "data_nasc": "01/01/2000",
                "cpf": "123456789"
            }
        )

    assert resposta.status_code in [201, 409]


# ----------------------------
# Sistema Listagem Usuários
# ----------------------------

def test_listar_usuarios(client):

    resposta = client.get("/usuarios")

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert isinstance(dados, list)


# ----------------------------
# Sistema Login
# ----------------------------

def test_login_usuario(client):

    resposta = client.post(
        "/login",
        json={
            "email": "felipe@test.com",
            "senha": "123456"
        }
    )

    assert resposta.status_code in [200, 401]


# ----------------------------
# Sistema Dados Fixos
# ----------------------------

def test_listar_tipos_transacao(client):

    resposta = client.get(
        "/tipos-transacao",
        headers={
            "Authorization": "Bearer teste"
        }
    )

    assert resposta.status_code in [200, 401]


# ----------------------------
# Sistema Listar Contas
# ----------------------------

def test_listar_contas(client):

    resposta = client.get("/conta")

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert "contas" in dados


# ----------------------------
# Sistema Listar Limites
# ----------------------------

def test_listar_limites(client):

    resposta = client.get("/limite")

    assert resposta.status_code == 200

    dados = resposta.get_json()

    assert "limites" in dados