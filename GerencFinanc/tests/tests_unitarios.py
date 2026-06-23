import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, date
import bcrypt

from Models.usuario_model import Usuario
from Models.login_model import Login
from Models.cartao_model import Cartao
from Models.limite_model import Limite


# ==================================================
# USUARIO MODEL
# ==================================================

def test_usuario_instancia():
    usuario = Usuario(
        "Felipe",
        "felipe@test.com",
        "123",
        "2000-01-01",
        "123"
    )

    assert usuario.nome == "Felipe"
    assert usuario.email == "felipe@test.com"


def test_usuario_to_dict():
    usuario = Usuario(
        "Felipe",
        "teste@test.com",
        "123",
        "2000-01-01",
        "123"
    )

    usuario.id = 10

    dados = usuario.to_dict()

    assert dados["id"] == 10
    assert dados["nome"] == "Felipe"


def test_usuario_to_dict_data_datetime():
    usuario = Usuario(
        "Teste",
        "teste@test.com",
        "123",
        datetime(2000, 1, 1),
        "123"
    )

    usuario.id = 1

    dados = usuario.to_dict()

    assert dados["data_nasc"] == datetime(2000, 1, 1)


def test_usuario_listar_todos():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchall.return_value = [
        [
            1,
            "Ana",
            "ana@test.com",
            "hash",
            date(2000, 1, 1),
            "123"
        ]
    ]

    conn.cursor.return_value = cursor

    with patch(
        "Models.usuario_model.conectar_financeiro",
        return_value=conn
    ):
        resultado = Usuario.listar_todos()

    assert len(resultado) == 1
    assert resultado[0]["nome"] == "Ana"


def test_usuario_listar_vazio():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchall.return_value = []

    conn.cursor.return_value = cursor

    with patch(
        "Models.usuario_model.conectar_financeiro",
        return_value=conn
    ):
        resultado = Usuario.listar_todos()

    assert resultado == []


def test_usuario_banco_erro():
    with patch(
        "Models.usuario_model.conectar_financeiro",
        side_effect=Exception()
    ):
        resultado = Usuario.listar_todos()

    assert resultado == []


def test_usuario_to_dict_completo():
    usuario = Usuario(
        "Teste",
        "teste@email.com",
        "123",
        datetime(2000, 1, 1),
        "123"
    )

    usuario.id = 10

    dados = usuario.to_dict()

    assert dados["id"] == 10
    assert dados["nome"] == "Teste"
    assert dados["email"] == "teste@email.com"
    assert dados["cpf"] == "123"


def test_usuario_listar_varios():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchall.return_value = [
        [
            1,
            "Ana",
            "ana@email.com",
            "hash",
            date(2000, 1, 1),
            "111"
        ],
        [
            2,
            "Bruno",
            "bruno@email.com",
            "hash",
            date(2001, 1, 1),
            "222"
        ]
    ]

    conn.cursor.return_value = cursor

    with patch(
        "Models.usuario_model.conectar_financeiro",
        return_value=conn
    ):
        resultado = Usuario.listar_todos()

    assert len(resultado) == 2
    assert resultado[0]["nome"] == "Ana"


# ==================================================
# LOGIN MODEL
# ==================================================

def test_login_buscar_usuario():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = [
        1,
        "Felipe",
        "felipe@test.com",
        "hash",
        "2000",
        "123"
    ]

    conn.cursor.return_value = cursor

    with patch(
        "Models.login_model.psycopg2.connect",
        return_value=conn
    ):
        usuario = Login.buscar_por_email("felipe@test.com")

    assert usuario["email"] == "felipe@test.com"


def test_login_usuario_nao_existe():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = None
    conn.cursor.return_value = cursor

    with patch(
        "Models.login_model.psycopg2.connect",
        return_value=conn
    ):
        resultado = Login.buscar_por_email("x@test.com")

    assert resultado is None


def test_login_senha_correta():
    senha = "123456"

    hash_senha = bcrypt.hashpw(
        senha.encode(),
        bcrypt.gensalt()
    ).decode()

    assert Login.verificar_senha(
        senha,
        hash_senha
    )


def test_login_senha_errada():
    senha = "123"

    hash_senha = bcrypt.hashpw(
        b"456",
        bcrypt.gensalt()
    ).decode()

    assert not Login.verificar_senha(
        senha,
        hash_senha
    )


def test_login_hash_invalido():
    with pytest.raises(ValueError):
        Login.verificar_senha(
            "123",
            "hash_errado"
        )


def test_login_email_vazio():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = None
    conn.cursor.return_value = cursor

    with patch(
        "Models.login_model.psycopg2.connect",
        return_value=conn
    ):
        resultado = Login.buscar_por_email("")

    assert resultado is None


def test_login_banco_erro():
    with patch(
        "Models.login_model.psycopg2.connect",
        side_effect=Exception()
    ):
        resultado = Login.buscar_por_email("teste@email.com")

    assert resultado is None


# ==================================================
# CARTAO MODEL
# ==================================================

def test_cartao_instancia():
    cartao = Cartao(
        5000,
        "2026-01-10",
        1
    )

    assert cartao.limite == 5000


def test_cartao_to_dict_string():
    cartao = Cartao(
        5000,
        "2026-01-10",
        1
    )

    cartao.id = 1

    dados = cartao.to_dict()

    assert dados["id"] == 1
    assert dados["limite"] == 5000


def test_cartao_data_datetime():
    cartao = Cartao(
        100,
        datetime(2026, 1, 1),
        1
    )

    dados = cartao.to_dict()

    assert dados["venc_fatura"] == "01/01/2026"


def test_cartao_deletar():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.rowcount = 1
    conn.cursor.return_value = cursor

    with patch(
        "Models.cartao_model.Cartao._conectar",
        return_value=conn
    ):
        resultado = Cartao.deletar_por_id(1)

    assert resultado is True


def test_cartao_deletar_inexistente():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.rowcount = 0
    conn.cursor.return_value = cursor

    with patch(
        "Models.cartao_model.Cartao._conectar",
        return_value=conn
    ):
        resultado = Cartao.deletar_por_id(999)

    assert resultado is False


def test_cartao_adicionar():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = [5]
    conn.cursor.return_value = cursor

    cartao = Cartao(
        5000,
        "2026-01-01",
        1
    )

    with patch(
        "Models.cartao_model.Cartao._conectar",
        return_value=conn
    ):
        resultado = Cartao.adicionar(cartao)

    assert resultado.id == 5
    assert resultado.limite == 5000


def test_cartao_adicionar_erro():
    with patch(
        "Models.cartao_model.Cartao._conectar",
        side_effect=Exception()
    ):
        resultado = Cartao.adicionar(
            Cartao(
                100,
                "2026-01-01"
            )
        )

    assert resultado is None


def test_cartao_listar_todos():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchall.return_value = [
        [
            1,
            3000,
            "2026-01-01",
            2
        ]
    ]

    conn.cursor.return_value = cursor

    with patch(
        "Models.cartao_model.Cartao._conectar",
        return_value=conn
    ):
        resultado = Cartao.listar_todos()

    assert len(resultado) == 1
    assert resultado[0].limite == 3000


def test_cartao_buscar_por_id():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = [
        1,
        2000,
        "2026-01-01",
        3
    ]

    conn.__enter__.return_value = conn
    conn.cursor.return_value.__enter__.return_value = cursor

    with patch(
        "Models.cartao_model.Cartao._conectar",
        return_value=conn
    ):
        resultado = Cartao.buscar_por_id(1)

    assert resultado.id == 1
    assert resultado.limite == 2000
    assert resultado.fk_id_conta == 3


def test_cartao_buscar_inexistente():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = None

    conn.__enter__.return_value = conn
    conn.cursor.return_value.__enter__.return_value = cursor

    with patch(
        "Models.cartao_model.Cartao._conectar",
        return_value=conn
    ):
        resultado = Cartao.buscar_por_id(999)

    assert resultado is None


def test_cartao_atualizar_sem_campos():
    resultado = Cartao.atualizar(
        1,
        {}
    )

    assert resultado is False


def test_cartao_atualizar():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.rowcount = 1
    conn.cursor.return_value = cursor

    with patch(
        "Models.cartao_model.Cartao._conectar",
        return_value=conn
    ):
        resultado = Cartao.atualizar(
            1,
            {
                "limite": 5000
            }
        )

    assert resultado is True


# ==================================================
# LIMITE MODEL
# ==================================================

def test_limite_instancia():
    limite = Limite(
        id=1,
        titulo="Academia",
        valor=100,
        fk_id_recorrencia=1,
        fk_id_categoria_transacao=1,
        fk_id_usuario=1
    )

    assert limite.id == 1
    assert limite.titulo == "Academia"
    assert limite.valor == 100
    assert limite.fk_id_recorrencia == 1
    assert limite.fk_id_categoria_transacao == 1
    assert limite.fk_id_usuario == 1


def test_limite_adicionar():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = [
        1,
        "Academia",
        100,
        1,
        1,
        1
    ]

    conn.cursor.return_value = cursor

    with patch(
        "Models.limite_model.conectar_financeiro",
        return_value=conn
    ):
        resultado = Limite.adicionar(
            Limite(
                titulo="Academia",
                valor=100,
                fk_id_usuario=1,
                fk_id_recorrencia=1,
                fk_id_categoria_transacao=1
            )
        )

    assert resultado.id == 1


def test_limite_deletar():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.rowcount = 1
    conn.cursor.return_value = cursor

    with patch(
        "Models.limite_model.conectar_financeiro",
        return_value=conn
    ):
        assert Limite.deletar(1)


def test_limite_deletar_inexistente():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.rowcount = 0
    conn.cursor.return_value = cursor

    with patch(
        "Models.limite_model.conectar_financeiro",
        return_value=conn
    ):
        assert not Limite.deletar(99)


def test_limite_to_dict():
    limite = Limite(
        id=1,
        titulo="Casa",
        valor=500,
        fk_id_recorrencia=1,
        fk_id_categoria_transacao=1,
        fk_id_usuario=1
    )

    dados = limite.to_dict()

    assert dados["titulo"] == "Casa"
    assert dados["valor"] == 500


def test_limite_listar_todos():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchall.return_value = [
        [
            1,
            "Academia",
            100,
            1,
            1,
            1
        ]
    ]

    conn.cursor.return_value = cursor

    with patch(
        "Models.limite_model.conectar_financeiro",
        return_value=conn
    ):
        resultado = Limite.listar_todos()

    assert len(resultado) == 1
    assert resultado[0].titulo == "Academia"


def test_limite_buscar_por_id():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = [
        1,
        "Mercado",
        200,
        1,
        1,
        1
    ]

    conn.cursor.return_value = cursor

    with patch(
        "Models.limite_model.conectar_financeiro",
        return_value=conn
    ):
        resultado = Limite.buscar_por_id(1)

    assert resultado.titulo == "Mercado"


def test_limite_buscar_inexistente():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.fetchone.return_value = None
    conn.cursor.return_value = cursor

    with patch(
        "Models.limite_model.conectar_financeiro",
        return_value=conn
    ):
        resultado = Limite.buscar_por_id(99)

    assert resultado is None


def test_limite_atualizar():
    conn = MagicMock()
    cursor = MagicMock()

    cursor.rowcount = 1
    conn.cursor.return_value = cursor

    with patch(
        "Models.limite_model.conectar_financeiro",
        return_value=conn
    ):
        resultado = Limite.atualizar(
            1,
            "Novo",
            300,
            1,
            1
        )

    assert resultado is True