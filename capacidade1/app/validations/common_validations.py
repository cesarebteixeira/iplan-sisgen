"""
Common validation functions for Capacity 1
"""

from datetime import datetime

def validar_campo_obrigatorio(campo):
    """
    Validate that a field is not empty
    
    Args:
        campo: Field value (string or any type)
    
    Returns:
        bool: True if valid, False otherwise
    """
    if isinstance(campo, str):
        return len(campo.strip()) > 0
    return campo is not None

def validar_numerico(valor):
    """
    Validate that a value is numeric (integer)
    
    Args:
        valor: Value to validate
    
    Returns:
        bool: True if numeric, False otherwise
    """
    if isinstance(valor, (int, float)):
        return True
    if isinstance(valor, str):
        try:
            int(valor)
            return True
        except (ValueError, TypeError):
            return False
    return False

def validar_data(data_str):
    """
    Validate and parse a date string in YYYY-MM-DD format
    
    Args:
        data_str: Date string to validate
    
    Returns:
        tuple: (bool valid, datetime.date or None)
    """
    if not data_str:
        return False, None
    try:
        data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
        return True, data_obj
    except (ValueError, TypeError):
        return False, None

def validar_intervalo_datas(data_inicio_str, data_fim_str):
    """
    Validate that data_inicio <= data_fim
    
    Args:
        data_inicio_str: Start date string (YYYY-MM-DD)
        data_fim_str: End date string (YYYY-MM-DD)
    
    Returns:
        tuple: (bool valid, message)
    """
    if not data_inicio_str or not data_fim_str:
        return True, None
    
    valid_inicio, data_inicio = validar_data(data_inicio_str)
    valid_fim, data_fim = validar_data(data_fim_str)
    
    if not (valid_inicio and valid_fim):
        return False, "Invalid date format"
    
    if data_inicio > data_fim:
        return False, "Start date must be less than or equal to end date"
    
    return True, None

def validar_sn(valor):
    """
    Validate that value is 'S' or 'N'
    
    Args:
        valor: Value to validate
    
    Returns:
        bool: True if 'S' or 'N' (case-insensitive), False otherwise
    """
    if not valor:
        return True  # Optional field
    if isinstance(valor, str):
        return valor.upper() in ['S', 'N']
    return False

def validar_ano(ano):
    """
    Validate year range (1900-2100)
    
    Args:
        ano: Year value
    
    Returns:
        bool: True if valid year, False otherwise
    """
    if not isinstance(ano, (int, str)):
        return False
    try:
        ano_int = int(ano)
        return 1900 <= ano_int <= 2100
    except (ValueError, TypeError):
        return False

def validar_mes(mes):
    """
    Validate month range (1-12)
    
    Args:
        mes: Month value
    
    Returns:
        bool: True if valid month, False otherwise
    """
    if not isinstance(mes, (int, str)):
        return False
    try:
        mes_int = int(mes)
        return 1 <= mes_int <= 12
    except (ValueError, TypeError):
        return False
