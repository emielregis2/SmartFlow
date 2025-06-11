"""
Moduł konfiguracji klienta Supabase dla SmartFlow.
"""
import os
from typing import Dict, Any, Optional, List
from supabase import create_client, Client
from dotenv import load_dotenv

# Wczytanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja klienta Supabase
supabase: Optional[Client] = None

def init_supabase() -> Client:
    """Inicjalizuje klienta Supabase"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        raise ValueError("Brak konfiguracji Supabase w zmiennych środowiskowych")
    
    return create_client(url, key)

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

def get_user_processes(user_id: str) -> List[Dict]:
    """Pobiera procesy użytkownika"""
    try:
        client = init_supabase()
        result = client.table("processes").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return result.data
    except Exception as e:
        print(f"Błąd pobierania procesów: {str(e)}")
        return []

def update_process(process_id: str, process_data: Dict[str, Any]) -> Dict[str, Any]:
    """Aktualizacja procesu"""
    client = init_supabase()
    
    response = client.table("processes").update(process_data).eq("id", process_id).execute()
    
    if not response.data:
        raise ValueError("Błąd podczas aktualizacji procesu")
    
    return response.data[0]

def save_process(user_id: str, process_data: Dict) -> str:
    """Zapisuje proces do bazy danych"""
    try:
        client = init_supabase()
        result = client.table("processes").insert({
            "user_id": user_id,
            "title": process_data.get("title"),
            "description": process_data.get("description"),
            "form_data": process_data.get("form_data"),
            "ai_analysis": process_data.get("ai_analysis"),
            "potential_score": process_data.get("ai_analysis", {}).get("ocena_potencjalu"),
            "status": "analyzed"
        }).execute()
        
        return result.data[0]["id"]
    except Exception as e:
        raise Exception(f"Błąd zapisywania procesu: {str(e)}")

def delete_process(process_id: str, user_id: str) -> bool:
    """Usuwa proces (soft delete)"""
    try:
        client = init_supabase()
        result = client.table("processes").update({
            "deleted_at": "now()"
        }).eq("id", process_id).eq("user_id", user_id).execute()
        
        return len(result.data) > 0
    except Exception as e:
        print(f"Błąd usuwania procesu: {str(e)}")
        return False

def soft_delete_process(process_id: str) -> bool:
    """Usuwa proces (soft delete) - uproszczona wersja"""
    try:
        client = init_supabase()
        result = client.table("processes").update({
            "deleted_at": "now()"
        }).eq("id", process_id).execute()
        
        return len(result.data) > 0
    except Exception as e:
        print(f"Błąd usuwania procesu: {str(e)}")
        return False 