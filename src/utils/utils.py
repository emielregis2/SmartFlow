"""
Implementacja funkcji pomocniczych.
"""

import re
from typing import Optional

def validate_email(email: str) -> bool:
    """
    Walidacja adresu email.
    
    Args:
        email: Adres email do sprawdzenia
        
    Returns:
        True jeśli email jest poprawny, False w przeciwnym razie
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """
    Walidacja hasła.
    
    Args:
        password: Hasło do sprawdzenia
        
    Returns:
        Tuple (bool, str) - (czy hasło jest poprawne, komunikat błędu)
    """
    if len(password) < 8:
        return False, "Hasło musi mieć co najmniej 8 znaków"
    
    if not re.search(r'[A-Z]', password):
        return False, "Hasło musi zawierać wielką literę"
    
    if not re.search(r'[a-z]', password):
        return False, "Hasło musi zawierać małą literę"
    
    if not re.search(r'\d', password):
        return False, "Hasło musi zawierać cyfrę"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Hasło musi zawierać znak specjalny"
    
    return True, None

def format_currency(amount: float) -> str:
    """
    Formatowanie kwoty pieniężnej.
    
    Args:
        amount: Kwota do sformatowania
        
    Returns:
        Sformatowana kwota w PLN
    """
    return f"{amount:,.2f} zł".replace(",", " ")

def format_duration(hours: float) -> str:
    """
    Formatowanie czasu trwania.
    
    Args:
        hours: Liczba godzin
        
    Returns:
        Sformatowany czas trwania
    """
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} min"
    elif hours == int(hours):
        return f"{int(hours)} h"
    else:
        return f"{hours:.1f} h" 