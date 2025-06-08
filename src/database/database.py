"""
Implementacja funkcji obsługi bazy danych Supabase.
"""

from typing import List, Dict, Optional
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

def save_process(user_id: str, process_data: Dict) -> Optional[Dict]:
    """
    Zapisanie nowego procesu do bazy danych.
    
    Args:
        user_id: ID użytkownika
        process_data: Dane procesu do zapisania
        
    Returns:
        Dict z danymi zapisanego procesu lub None w przypadku błędu
    """
    try:
        data = {
            "user_id": user_id,
            "name": process_data["process"]["name"],
            "description": process_data["process"]["description"],
            "form_data": process_data,
            "status": "new"
        }
        response = supabase.table("processes").insert(data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Błąd zapisywania procesu: {e}")
        return None

def get_processes(user_id: str) -> List[Dict]:
    """
    Pobranie wszystkich procesów użytkownika.
    
    Args:
        user_id: ID użytkownika
        
    Returns:
        Lista procesów użytkownika
    """
    try:
        response = supabase.table("processes")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
        return response.data
    except Exception as e:
        print(f"Błąd pobierania procesów: {e}")
        return []

def get_process(process_id: str) -> Optional[Dict]:
    """
    Pobranie pojedynczego procesu.
    
    Args:
        process_id: ID procesu
        
    Returns:
        Dict z danymi procesu lub None jeśli nie znaleziono
    """
    try:
        response = supabase.table("processes")\
            .select("*")\
            .eq("id", process_id)\
            .single()\
            .execute()
        return response.data
    except Exception as e:
        print(f"Błąd pobierania procesu: {e}")
        return None

def update_process(process_id: str, process_data: Dict) -> Optional[Dict]:
    """
    Aktualizacja procesu.
    
    Args:
        process_id: ID procesu
        process_data: Nowe dane procesu
        
    Returns:
        Dict z zaktualizowanymi danymi procesu lub None w przypadku błędu
    """
    try:
        response = supabase.table("processes")\
            .update(process_data)\
            .eq("id", process_id)\
            .execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Błąd aktualizacji procesu: {e}")
        return None

def delete_process(process_id: str) -> bool:
    """
    Usunięcie procesu.
    
    Args:
        process_id: ID procesu
        
    Returns:
        True jeśli usunięcie się powiodło, False w przeciwnym razie
    """
    try:
        response = supabase.table("processes")\
            .delete()\
            .eq("id", process_id)\
            .execute()
        return True
    except Exception as e:
        print(f"Błąd usuwania procesu: {e}")
        return False 