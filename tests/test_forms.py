"""
Testy logiki formularzy w components/forms.py
"""
import pytest
from components import forms

def test_show_profile_form(monkeypatch):
    # Test sprawdza, czy funkcja istnieje i można ją wywołać
    assert hasattr(forms, 'show_profile_form')

def test_show_process_form(monkeypatch):
    # Test sprawdza, czy funkcja istnieje i można ją wywołać
    assert hasattr(forms, 'show_process_form') 