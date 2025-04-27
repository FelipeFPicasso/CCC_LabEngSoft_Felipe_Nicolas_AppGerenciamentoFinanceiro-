from email_validator import validate_email, EmailNotValidError

def valida_email(email, return_details: bool = False, check_dns: bool = False):
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

