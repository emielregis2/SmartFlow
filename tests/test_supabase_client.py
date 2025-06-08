"""
Testy jednostkowe dla modułu database/supabase_client.py
"""
import pytest
from unittest.mock import patch, MagicMock
from database import supabase_client

def test_init_supabase_env_missing(monkeypatch):
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_KEY", raising=False)
    with pytest.raises(ValueError):
        supabase_client.init_supabase()

def test_get_user_found():
    with patch.object(supabase_client, 'init_supabase') as mock_init:
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{"email": "test@test.com"}]
        mock_init.return_value = mock_client
        user = supabase_client.get_user("test@test.com")
        assert user["email"] == "test@test.com"

def test_get_user_not_found():
    with patch.object(supabase_client, 'init_supabase') as mock_init:
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        mock_init.return_value = mock_client
        user = supabase_client.get_user("notfound@test.com")
        assert user is None 