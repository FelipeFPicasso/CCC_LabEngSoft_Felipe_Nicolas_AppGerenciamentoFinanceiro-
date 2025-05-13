import random
import string

def gerar_codigo_recuperacao(tamanho=6):
    """
    Gera um código de recuperação aleatório contendo letras e números.
    Exemplo: 'A9B3C1'
    """
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choices(caracteres, k=tamanho))