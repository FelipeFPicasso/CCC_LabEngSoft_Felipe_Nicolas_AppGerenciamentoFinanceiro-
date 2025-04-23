import datetime

class Usuario:
    _usuarios = []
    _proximo_id = 1

    def __init__(self, nome, email, senha, data_nasc, cpf):
        self.id = Usuario._proximo_id
        Usuario._proximo_id += 1
        self.nome = nome
        self.email = email
        self.senha = senha
        self.data_nasc = data_nasc  # deve ser uma string no formato YYYY-MM-DD
        self.cpf = cpf

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'data_nasc': self.data_nasc,
            'cpf': self.cpf
        }

    @classmethod
    def adicionar(cls, usuario):
        cls._usuarios.append(usuario)

    @classmethod
    def listar_todos(cls):
        return [u.to_dict() for u in cls._usuarios]
