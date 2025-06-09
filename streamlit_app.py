"""
SmartFlow - Aplikacja do analizy procesów biznesowych z wykorzystaniem AI.

Wymagania:
- Python 3.8+
- pip install -r requirements.txt

Użycie:
streamlit run streamlit_app.py

Autor: Dariusz Gąsior
"""

# ======================================
# 🧪 TRYB TESTOWY - Auto Login
# ======================================
# Ustaw na True aby pominąć logowanie podczas testowania
# PAMIĘTAJ: Zmień na False przed produkcją!
DEMO_AUTO_LOGIN = True  # ← Zmień na False żeby wrócić do normalnego logowania
TEST_USER_EMAIL = "test@smartflow.pl"
TEST_USER_PASSWORD = "test123456"
# ======================================

import streamlit as st
from components.auth import show_auth_page
from components.forms import show_profile_form, show_process_form
from components.visualizations import show_dashboard, show_user_processes, show_results
from database.supabase_client import init_supabase, get_user_processes
from ai.openai_service import analyze_process

# Konfiguracja strony
st.set_page_config(
    page_title="SmartFlow",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicjalizacja stanu sesji
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "auth"
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "process_data" not in st.session_state:
    st.session_state.process_data = None
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False

# Inicjalizacja klienta Supabase
try:
    supabase = init_supabase()
    st.session_state.demo_mode = False
except ValueError as e:
    st.session_state.demo_mode = True
    supabase = None

# ======================================
# 🧪 AUTO-LOGIN dla testowania
# ======================================
if DEMO_AUTO_LOGIN and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_data = {
        "id": "demo-user-12345",  # Mock ID dla testów
        "email": TEST_USER_EMAIL
    }
    # Dodaj informację o trybie testowym
    st.sidebar.info(f"🧪 **TRYB TESTOWY**\nAuto-login: {TEST_USER_EMAIL}")
# ======================================

# Routing aplikacji
if not st.session_state.authenticated:
    show_auth_page()
else:
    # Nawigacja
    st.sidebar.title("SmartFlow")
    
    # Sprawdź czy są wyniki analizy do wyświetlenia
    if st.session_state.get("current_analysis") and st.session_state.current_analysis.get("ai_analysis"):
        page = st.sidebar.radio(
            "Wybierz stronę",
            ["Dashboard", "Wyniki Analizy", "Nowa Analiza", "Moje Procesy", "Ustawienia"]
        )
    else:
        page = st.sidebar.radio(
            "Wybierz stronę",
            ["Dashboard", "Nowa Analiza", "Moje Procesy", "Ustawienia"]
        )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Wyniki Analizy":
        show_results()
    elif page == "Nowa Analiza":
        show_process_form()
    elif page == "Moje Procesy":
        show_user_processes()
    elif page == "Ustawienia":
        st.title("Ustawienia")
        if st.button("Wyloguj"):
            st.session_state.authenticated = False
            st.session_state.current_page = "auth"
            st.session_state.user_data = None
            st.rerun()