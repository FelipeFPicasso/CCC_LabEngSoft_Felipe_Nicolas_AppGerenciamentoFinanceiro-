# Testes Automatizados

## Sobre a API

O GerencFinanc é uma API REST desenvolvida em Python utilizando Flask para gerenciamento financeiro pessoal.

A aplicação permite que usuários realizem o controle de suas finanças através de funcionalidades como:

* Cadastro e autenticação de usuários
* Gerenciamento de contas bancárias
* Cadastro de cartões
* Controle de limites financeiros
* Registro de transações de receita e despesa
* Consulta de saldos
* Emissão de relatórios financeiros

A comunicação é realizada através de endpoints REST e os dados são armazenados em um banco de dados PostgreSQL.

---

## Objetivo dos Testes

O principal objetivo dos testes é garantir que a aplicação funcione corretamente em diferentes níveis de validação.

Os testes permitem:

* Verificar se os métodos funcionam corretamente de forma isolada
* Validar a integração entre controllers, models e banco de dados
* Simular a utilização real da API por um usuário
* Detectar falhas antes que cheguem ao ambiente de produção
* Facilitar futuras manutenções e evoluções do sistema

Para atender aos requisitos da disciplina, foram implementados os três níveis de testes estudados em sala de aula:

* Testes Unitários
* Testes de Integração
* Testes de Sistema

---

# Estrutura dos Testes

```text
tests/
├── conftest.py
├── tests_unitarios.py
├── tests_integracao.py
└── tests_sistema.py
```

### Arquivos

| Arquivo               | Descrição                               |
| --------------------- | --------------------------------------- |
| `conftest.py`         | Fixtures e configurações compartilhadas |
| `tests_unitarios.py`  | Testes de classes e métodos isolados    |
| `tests_integracao.py` | Testes de integração entre camadas      |
| `tests_sistema.py`    | Simulação de uso da API por um usuário  |

---

# Testes Unitários

Os testes unitários verificam pequenas partes do sistema de forma isolada.

Foram testadas as seguintes classes:

* Usuario
* Login
* Cartao
* Limite

### Principais validações

#### Usuario

* Criação do objeto
* Conversão para dicionário
* Listagem de usuários
* Tratamento de retorno vazio
* Tratamento de erro de banco

#### Login

* Busca por e-mail
* Usuário inexistente
* Senha correta
* Senha incorreta
* Hash inválido

#### Cartao

* Instanciação
* Conversão de datas
* Inserção
* Busca por ID
* Atualização
* Exclusão

#### Limite

* Instanciação
* Conversão para dicionário
* Inserção
* Busca
* Atualização
* Exclusão

### Resultado

```text
36 testes unitários
```

---

# Testes de Integração

Os testes de integração verificam a comunicação entre diferentes camadas da aplicação.

Fluxo validado:

```text
Rota
 ↓
Controller
 ↓
Model
 ↓
Banco (Mock)
```

### Cenários testados

* Login com sucesso
* Login com usuário inexistente
* Cadastro de usuário
* Listagem de usuários
* Criação de conta
* Listagem de contas
* Criação de limite
* Listagem de limites
* Endpoint protegido sem token
* Fluxo financeiro completo

### Resultado

```text
10 testes de integração
```

---

# Testes de Sistema

Os testes de sistema simulam a utilização da API por um usuário real através do Flask Test Client.

### Cenários testados

* Cadastro de usuário
* Listagem de usuários
* Login
* Consulta de tipos de transação
* Consulta de contas
* Consulta de limites

### Resultado

```text
6 testes de sistema
```

---



# Instalação de bibliotecas e ferramentas

## Instale os requirements ou manualmente:

    pip install -r requirements.txt

## Manualmente:

    pip install flask 

    pip install pytest 

    pip install pytest-flask

    pip install pytest-cov

    pip install psycopg2

    pip install pyjwt

# Executando os Testes

## Executar todos

```bash
python -m pytest tests -v
```

## Executar testes unitários

```bash
python -m pytest tests/tests_unitarios.py -v
```

## Executar testes de integração

```bash
python -m pytest tests/tests_integracao.py -v
```

## Executar testes de sistema

```bash
python -m pytest tests/tests_sistema.py -v
```

---

# Quantidade Total

```text
36 Testes Unitários
10 Testes de Integração
 6 Testes de Sistema
---------------------
52 Testes Automatizados
```

---

# Conclusão

A implementação dos testes permitiu validar a aplicação em diferentes níveis de complexidade. Os testes unitários garantem o funcionamento correto dos modelos de negócio, os testes de integração verificam a comunicação entre as camadas da aplicação e os testes de sistema simulam o comportamento de um usuário real utilizando a API.

Com isso, a aplicação torna-se mais confiável, facilitando a identificação de erros, a manutenção do código e a evolução futura do sistema.