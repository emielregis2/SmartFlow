"""
Moduł obsługi bazy danych Supabase.
"""

from .database import (
    save_process,
    get_processes,
    get_process,
    update_process,
    delete_process
)

__all__ = [
    'save_process',
    'get_processes',
    'get_process',
    'update_process',
    'delete_process'
] 