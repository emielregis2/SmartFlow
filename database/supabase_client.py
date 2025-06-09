"""
Moduł konfiguracji klienta Supabase dla SmartFlow.
"""
import os
from typing import Dict, Any, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Wczytanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja klienta Supabase
supabase: Optional[Client] = None

def init_supabase() -> Client:
    """Inicjalizacja klienta Supabase"""
    global supabase
    
    if supabase is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError("Brak wymaganych zmiennych środowiskowych SUPABASE_URL i SUPABASE_ANON_KEY")
        
        supabase = create_client(url, key)
    
    return supabase

def get_user(email: str) -> Optional[Dict[str, Any]]:
    """Pobieranie użytkownika po emailu"""
    client = init_supabase()
    
    response = client.table("users").select("*").eq("email", email).execute()
    
    if response.data:
        return response.data[0]
    return None

def create_user(email: str, password: str) -> Dict[str, Any]:
    """Tworzenie nowego użytkownika"""
    client = init_supabase()
    
    # Rejestracja w Supabase Auth
    auth_response = client.auth.sign_up({
        "email": email,
        "password": password
    })
    
    if not auth_response.user:
        raise ValueError("Błąd podczas tworzenia użytkownika")
    
    # Tworzenie profilu użytkownika
    profile_data = {
        "id": auth_response.user.id,
        "email": email,
        "created_at": auth_response.user.created_at
    }
    
    response = client.table("users").insert(profile_data).execute()
    
    if not response.data:
        raise ValueError("Błąd podczas tworzenia profilu użytkownika")
    
    return response.data[0]

def update_user_profile(user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Aktualizacja profilu użytkownika"""
    client = init_supabase()
    
    response = client.table("users").update(profile_data).eq("id", user_id).execute()
    
    if not response.data:
        raise ValueError("Błąd podczas aktualizacji profilu użytkownika")
    
    return response.data[0]

def create_process(user_id: str, process_data: Dict[str, Any]) -> Dict[str, Any]:
    """Tworzenie nowego procesu"""
    client = init_supabase()
    
    # Dodanie user_id do danych procesu
    process_data["user_id"] = user_id
    
    response = client.table("processes").insert(process_data).execute()
    
    if not response.data:
        raise ValueError("Błąd podczas tworzenia procesu")
    
    return response.data[0]

def get_user_processes(user_id: str) -> list[Dict[str, Any]]:
    """Pobieranie procesów użytkownika"""
    client = init_supabase()
    
    response = client.table("processes").select("*").eq("user_id", user_id).execute()
    
    return response.data

def update_process(process_id: str, process_data: Dict[str, Any]) -> Dict[str, Any]:
    """Aktualizacja procesu"""
    client = init_supabase()
    
    response = client.table("processes").update(process_data).eq("id", process_id).execute()
    
    if not response.data:
        raise ValueError("Błąd podczas aktualizacji procesu")
    
    return response.data[0] 