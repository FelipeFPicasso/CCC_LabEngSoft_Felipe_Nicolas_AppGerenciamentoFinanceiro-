from unittest.mock import MagicMock, patch


# =========================================================
# 1 - Login com usuário válido
# =========================================================

def test_integracao_login_sucesso(client):
    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor

    cursor.fetchone.return_value = [
        1,
        "Felipe",
        "felipe@email.com",
        "hash",
        "2000-01-01",
        "123"
    ]

    with patch(
        "Models.login_model.psycopg2.connect",
        return_value=conn
    ), patch(
        "Models.login_model.bcrypt.checkpw",
        return_value=True
    ):
        resposta = client.post(
            "/login",
            json={
                "email": "felipe@email.com",
                "senha": "123"
            }
        )

    assert resposta.status_code == 200
    assert "token" in resposta.get_json()


# =========================================================
# 2 - Login usuário inexistente
# =========================================================

def test_integracao_login_usuario_inexistente(client):
    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = None

    with patch(
        "Models.login_model.psycopg2.connect",
        return_value=conn
    ):
        resposta = client.post(
            "/login",
            json={
                "email": "naoexiste@email.com",
                "senha": "123"
            }
        )

    assert resposta.status_code == 401


# =========================================================
# 3 - Criar usuário
# =========================================================

def test_integracao_cadastrar_usuario(client):
    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = [1]

    with patch(
        "Models.usuario_model.conectar_financeiro",
        return_value=conn
    ):
        resposta = client.post(
            "/usuarios",
            json={
                "nome": "Teste",
                "email": "teste@email.com",
                "senha": "Senha@123",
                "data_nasc": "01/01/2000",
                "cpf": "123456789"
            }
        )

    assert resposta.status_code in [201, 409]


# =========================================================
# 4 - Listar usuários
# =========================================================

def test_integracao_listar_usuarios(client):
    resposta = client.get("/usuarios")

    assert resposta.status_code == 200
    assert isinstance(resposta.get_json(), list)


# =========================================================
# 5 - Criar conta autenticada
# =========================================================

def test_integracao_criar_conta(client):
    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor
    cursor.fetchone.return_value = [10]

    with patch(
        "Models.conta_model.conectar_financeiro",
        return_value=conn
    ):
        resposta = client.post(
            "/conta",
            headers={
                "Authorization": "Bearer token"
            },
            json={
                "nome_banco": "Nubank",
                "saldo_inicial": 500
            }
        )

    assert resposta.status_code in [201, 401]


# =========================================================
# 6 - Listar contas
# =========================================================

def test_integracao_listar_contas(client):
    resposta = client.get("/conta")

    assert resposta.status_code == 200
    assert "contas" in resposta.get_json()


# =========================================================
# 7 - Criar limite
# =========================================================

def test_integracao_criar_limite(client):
    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor

    cursor.fetchone.return_value = [
        1,
        "Academia",
        200,
        1,
        1,
        1
    ]

    with patch(
        "Models.limite_model.conectar_financeiro",
        return_value=conn
    ):
        resposta = client.post(
            "/limite",
            headers={
                "Authorization": "Bearer token"
            },
            json={
                "titulo": "Academia",
                "valor": 200,
                "fk_id_recorrencia": 1,
                "fk_id_categoria_transacao": 1
            }
        )

    assert resposta.status_code in [201, 401]


# =========================================================
# 8 - Listar limites
# =========================================================

def test_integracao_listar_limites(client):
    resposta = client.get("/limite")

    assert resposta.status_code == 200
    assert "limites" in resposta.get_json()


# =========================================================
# 9 - Endpoint protegido sem token
# =========================================================

def test_integracao_sem_token(client):
    resposta = client.post(
        "/limite",
        json={
            "titulo": "Teste",
            "valor": 100
        }
    )

    assert resposta.status_code in [401, 403]


# =========================================================
# 10 - Fluxo completo financeiro
# =========================================================

def test_integracao_fluxo_completo(client):
    conn = MagicMock()
    cursor = MagicMock()

    conn.cursor.return_value = cursor

    cursor.fetchone.side_effect = [
        [
            1,
            "Felipe",
            "felipe@email.com",
            "hash",
            "2000-01-01",
            "123"
        ],
        [10],
        [
            5,
            "Academia",
            200,
            1,
            1,
            1
        ]
    ]

    with patch(
        "Models.login_model.psycopg2.connect",
        return_value=conn
    ), patch(
        "Models.login_model.bcrypt.checkpw",
        return_value=True
    ):
        login = client.post(
            "/login",
            json={
                "email": "felipe@email.com",
                "senha": "123"
            }
        )

    assert login.status_code == 200

    token = login.get_json()["token"]

    with patch(
        "Models.conta_model.conectar_financeiro",
        return_value=conn
    ):
        conta = client.post(
            "/conta",
            headers={
                "Authorization": token
            },
            json={
                "nome_banco": "Nubank",
                "saldo_inicial": 1000
            }
        )

    assert conta.status_code == 201