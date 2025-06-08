"""
Testy logiki autoryzacji w components/auth.py
"""
import pytest
from components import auth

def test_show_auth_page_exists():
    assert hasattr(auth, 'show_auth_page')

def test_show_login_form_exists():
    assert hasattr(auth, 'show_login_form')

def test_show_registration_form_exists():
    assert hasattr(auth, 'show_registration_form') 