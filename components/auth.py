"""
Moduł autentykacji dla SmartFlow.
"""
import streamlit as st
from typing import Optional, Dict, Any
from database.supabase_client import init_supabase

def show_auth_page():
    """Wyświetla stronę logowania/rejestracji"""
    st.title("🚀 SmartFlow")
    st.subheader("Analiza procesów biznesowych z AI")
    
    # Tabs dla logowania i rejestracji
    tab1, tab2 = st.tabs(["Logowanie", "Rejestracja"])
    
    with tab1:
        show_login_form()
    
    with tab2:
        show_registration_form()

def show_login_form():
    """Formularz logowania"""
    st.info("💡 **Konto testowe:** test@smartflow.pl / test123456")
    
    with st.form("login_form"):
        email = st.text_input("Email", value="", placeholder="np. twój@email.pl")
        password = st.text_input("Hasło", type="password", value="", placeholder="Wprowadź hasło")
        submitted = st.form_submit_button("Zaloguj się")
        
        if submitted:
            if email and password and email.strip() and password.strip():
                try:
                    # Logowanie przez Supabase Auth
                    supabase = init_supabase()
                    response = supabase.auth.sign_in_with_password({
                        "email": email.strip(),
                        "password": password.strip()
                    })
                    
                    if response.user:
                        # Ustawienie session state
                        st.session_state.authenticated = True
                        st.session_state.user_data = {
                            "id": response.user.id,
                            "email": response.user.email
                        }
                        st.success("Zalogowano pomyślnie!")
                        st.rerun()
                    else:
                        st.error("Nieprawidłowe dane logowania")
                        
                except Exception as e:
                    st.error(f"Błąd logowania: {str(e)}")
            else:
                st.error("Wypełnij wszystkie pola")

def show_registration_form():
    """Formularz rejestracji"""
    with st.form("registration_form"):
        email = st.text_input("Email", placeholder="twój@email.pl")
        password = st.text_input("Hasło", type="password", placeholder="minimum 6 znaków")
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
                try:
                    # Rejestracja przez Supabase Auth
                    supabase = init_supabase()
                    response = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })
                    
                    if response.user:
                        st.success("Konto utworzone pomyślnie! Sprawdź email aby potwierdzić rejestrację.")
                    else:
                        st.error("Błąd podczas tworzenia konta")
                        
                except Exception as e:
                    st.error(f"Błąd rejestracji: {str(e)}") 