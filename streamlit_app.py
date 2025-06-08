"""
SmartFlow - Aplikacja do analizy procesów biznesowych z wykorzystaniem AI.

Wymagania:
- Python 3.8+
- pip install -r requirements.txt

Użycie:
streamlit run streamlit_app.py

Autor: Dariusz Gąsior
"""

import streamlit as st
from components.auth import show_auth_page
from components.forms import show_profile_form, show_process_form
from components.visualizations import show_dashboard, show_user_processes
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

# Inicjalizacja klienta Supabase
supabase = init_supabase()

# Routing aplikacji
if not st.session_state.authenticated:
    show_auth_page()
else:
    # Nawigacja
    st.sidebar.title("SmartFlow")
    page = st.sidebar.radio(
        "Wybierz stronę",
        ["Dashboard", "Nowa Analiza", "Moje Procesy", "Ustawienia"]
    )
    
    if page == "Dashboard":
        show_dashboard()
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