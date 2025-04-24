# Aplicativo para Gerenciamento de Finanças Pessoais.

## Descrição: 
 - O software permitirá o gerenciamento financeiro pessoal, incluindo registro, edição e exclusão de receitas e despesas. Será possível categorizar transações, acompanhar faturas de cartões, definir limites financeiros e visualizar informações em dashboards interativos. Ademais, poderá adicionar suas metas para investimentos e gerenciamento de carteira de investimentos manual.

## Tecnologias:
- Flask - Framework utilizado para o Back-End (API) | 3.1.0
- Python - Linguagem utilizada no Back-End | 3.13.2
- Flutter - Framework utilizado para o Front-End | 3.7.0
- Dart - Linguagem utilizado para o Front-End | 3.0.0
- PostgreSQL - Banco de Dados | 16.0 
- BrModelo - Programa utilizado para modelar o Banco de Dados | 3.3.2
- Xmind - Programa utilizado para criar o mapa da API | 2025
- Postman -  Utilizado para fazer a documentação da API e os testes dos EndPoints | 10.2.0

## Instalação:

- git clone https://github.com/FelipeFPicasso/AppGerenciamentoFinanceiro.git
- pip install flask
- pip install psycopg2-binary
- pip install sqlalchemy

## Estrutura dos EndPoints API:

- *URL*
  - localhost:8080
- *Public*
    - URL/login
        - POST: /
    - URL/cadastro
        - POST: /
    - URL/usuario
        - GET: /
        - GET: /{id}
        - PUT: /{id}
        - DELETE: /{id}
    - URL/transacao
        - GET: /
        - GET: /active
        - GET: /{id}
        - POST: /
        - PUT: /{id}
        - DELETE: /{id}


## Mapa da API:

- ![Image](https://github.com/user-attachments/assets/3e0414fd-f6f7-460f-8543-6a2b59261a47)    

## Desenvolvedores:

- Felipe Frantz Picasso - https://github.com/FelipeFPicasso

- Nícolas Comin Todero - https://github.com/NicolasComin
