from email_validator import validate_email, EmailNotValidError
from flask import abort
import datetime
import json
import re

def valida_todos(email, senha, data_nasc, return_details=True, is_data_nasc:bool = True):
    valida_data(data_nasc)
    valida_email(email)
    valida_senha(senha, return_details)

def valida_email(email, return_details: bool = False, check_dns: bool = False):
    try:
        result = validate_email(email,check_deliverability=check_dns)
        if return_details:
            return {
                "valid": True,
                "normalized": result["email"],
                "local": result.local_part,
                "domain": result.domain,
            }
        return True
    
    except EmailNotValidError or Exception as e:
        if return_details:
            abort (400, description=f'Email invalido, erro encontrado: {str(e)}')
        abort (400, description=f'Email Invalido') 
    
def valida_senha(password: str, return_details=False) -> bool:
    error_pattern = "A senha deve conter:\n"
    errors = []

    if not (7 <= len(password) <= 50):
        errors.append("Entre 7 e 50 caracteres;")
    if not re.search(r"[A-Z]", password):
        errors.append("Ao menos 1 letra maiúscula;")
    if not re.search(r"[a-z]", password):
        errors.append("Ao menos 1 letra minúscula;")
    if not re.search(r"\d", password):
        errors.append("Ao menos 1 dígito;")
    if not re.search(r"[!@#$%^*()?]", password):
        errors.append("Ao menos 1 caracter especial: !@#$%^*()?")

    if errors:
        if return_details:
            abort(400, description=error_pattern + " ".join(errors))
        else:
            abort(400, description="Senha inválida")

    return True

def valida_data(data, is_data_nasc: bool = False ) -> bool:
    try:
        data = datetime.datetime.strptime(data, '%d/%m/%Y').date()
    except ValueError:
        abort(400, description='Data deve estar no formato DD/MM/YYYY')

    if not isinstance(data, datetime.date):
        abort(400, description='Data deve ser um objeto datetime.date')

    if is_data_nasc:
        hoje = datetime.date.today()
        idade = hoje.year - data.year - ((hoje.month, hoje.day) < (data.month, data.day))

        if idade < 18:
            abort(400, description='Usuário deve ter pelo menos 18 anos de idade')

    return True