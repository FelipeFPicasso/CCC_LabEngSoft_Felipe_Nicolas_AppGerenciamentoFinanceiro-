from email_validator import validate_email, EmailNotValidError
import re

def valida_email(email, return_details: bool = False, check_dns: bool = False) -> bool:
    try:
        result = validate_email(email,check_deliverability=check_dns)
        if return_details:
            return {
                "valid": True,
                "normalized": result["email"],
                "local": result.get("local"),
                "domain": result.get("domain"),
                "domain_info": result.get("domain_info")
            }
        return True
    except EmailNotValidError as e:
        if return_details:
            return {"valid": False, "error": str(e)}
        return False
    except Exception as e:
        if return_details:
            return {"valid": False, "error": "Unknown error: " + str(e)}
        return False
    
def valida_senha(password: str, return_details = False) -> bool:

    error_pattern = "A senha deve conter: \n"

    errors = []

    if not (7 <= len(password) <= 50):
        errors.append("Entre 7 e 50 caracteres.")
    if not re.search(r"[A-Z]", password):
        errors.append("Ao menos 1 letra maiúscula.")
    if not re.search(r"[a-z]", password):
        errors.append("Ao menos 1 letra minúscula.")
    if not re.search(r"\d", password):
        errors.append("Ao menos 1 dígito.")
    if not re.search(r"[!@#$%^&*()?]", password):
        errors.append("Ao menos 1 caracter especial: !@#$%^&*()?")
    
    valid = len(errors) == 0

    if return_details:
        if not valid:
            return {
                "valid": valid,
                "message": error_pattern,
                "errors": errors
            }

    return valid

def valida_data_nasc(data_nasc) -> bool:
    