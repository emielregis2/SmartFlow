"""
Implementacja funkcji autentykacji i autoryzacji.
"""

from typing import Optional, Dict
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Wczytanie zmiennych środowiskowych
load_dotenv()

# Inicjalizacja klienta Supabase
supabase: Client = create_client(
    os.getenv("SUPABASE_URL", ""),
    os.getenv("SUPABASE_KEY", "")
)

def login_user(email: str, password: str) -> Optional[Dict]:
    """
    Logowanie użytkownika.
    
    Args:
        email: Adres email użytkownika
        password: Hasło użytkownika
        
    Returns:
        Dict z danymi użytkownika lub None w przypadku błędu
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response.user
    except Exception as e:
        print(f"Błąd logowania: {e}")
        return None

def register_user(email: str, password: str) -> Optional[Dict]:
    """
    Rejestracja nowego użytkownika.
    
    Args:
        email: Adres email użytkownika
        password: Hasło użytkownika
        
    Returns:
        Dict z danymi użytkownika lub None w przypadku błędu
    """
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return response.user
    except Exception as e:
        print(f"Błąd rejestracji: {e}")
        return None

def logout_user() -> bool:
    """
    Wylogowanie użytkownika.
    
    Returns:
        True jeśli wylogowanie się powiodło, False w przeciwnym razie
    """
    try:
        supabase.auth.sign_out()
        return True
    except Exception as e:
        print(f"Błąd wylogowania: {e}")
        return False

def get_current_user() -> Optional[Dict]:
    """
    Pobranie danych aktualnie zalogowanego użytkownika.
    
    Returns:
        Dict z danymi użytkownika lub None jeśli nie ma zalogowanego użytkownika
    """
    try:
        user = supabase.auth.get_user()
        return user.user
    except Exception as e:
        print(f"Błąd pobierania danych użytkownika: {e}")
        return None 