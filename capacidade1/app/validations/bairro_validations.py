"""
Validation functions for Bairro module (C023T)
"""

from app.validations.common_validations import validar_campo_obrigatorio, validar_numerico

def validar_bairro(codigo_bairro, descricao):
    """
    Validate Bairro data
    
    Args:
        codigo_bairro: Code/ID for neighborhood
        descricao: Description of neighborhood
    
    Returns:
        tuple: (bool valid, str error_message or None)
    """
    errors = []
    
    if not codigo_bairro or not validar_numerico(codigo_bairro):
        errors.append("Neighborhood code must contain only numbers")
    
    if not descricao or not validar_campo_obrigatorio(descricao):
        errors.append("Neighborhood description is required")
    
    return len(errors) == 0, "; ".join(errors) if errors else None
