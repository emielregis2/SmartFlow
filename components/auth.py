"""
Moduł autentykacji dla SmartFlow.
"""
import streamlit as st
from typing import Optional, Dict, Any

def show_auth_page():
    """Wyświetla stronę logowania/rejestracji"""
    st.subheader("Logowanie do SmartFlow")
    
    # Tabs dla logowania i rejestracji
    tab1, tab2 = st.tabs(["Logowanie", "Rejestracja"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_registration_form()

def show_login_form():
    """Formularz logowania"""
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Hasło", type="password")
        submitted = st.form_submit_button("Zaloguj się")
        
        if submitted:
            if email and password:
                # TODO: Integracja z Supabase Auth
                st.session_state.user = {"email": email, "id": "mock-id"}
                st.success("Zalogowano pomyślnie!")
                st.rerun()
            else:
                st.error("Wypełnij wszystkie pola")

def show_registration_form():
    """Formularz rejestracji"""
    with st.form("registration_form"):
        email = st.text_input("Email")
        password = st.text_input("Hasło", type="password")
        confirm_password = st.text_input("Potwierdź hasło", type="password")
        submitted = st.form_submit_button("Zarejestruj się")
        
        if submitted:
            if not email or not password:
                st.error("Wypełnij wszystkie pola")
            elif password != confirm_password:
                st.error("Hasła nie są identyczne")
            elif len(password) < 6:
                st.error("Hasło musi mieć co najmniej 6 znaków")
            else:
                # TODO: Integracja z Supabase Auth
                st.session_state.user = {"email": email, "id": "mock-id"}
                st.success("Konto utworzone pomyślnie!")
                st.rerun() 