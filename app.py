"""
SmartFlow - System analizy procesów biznesowych z wykorzystaniem AI

Wymagania:
- Python 3.8+
- pip install -r requirements.txt

Użycie:
streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional
import json

# Konfiguracja strony
st.set_page_config(
    page_title="SmartFlow - Analiza Procesów Biznesowych",
    page_icon="📊",
    layout="wide"
)

# Wczytanie zmiennych środowiskowych
load_dotenv()

def initialize_session_state():
    """Inicjalizacja stanu sesji"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'processes' not in st.session_state:
        st.session_state.processes = []
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}

def show_login_form():
    """Wyświetla formularz logowania"""
    with st.form("login_form"):
        st.subheader("Logowanie")
        email = st.text_input("Email")
        password = st.text_input("Hasło", type="password")
        submitted = st.form_submit_button("Zaloguj się")
        
        if submitted:
            # TODO: Implementacja logowania przez Supabase
            st.session_state.user = {"email": email}
            st.success("Zalogowano pomyślnie!")
            st.rerun()

def show_registration_form():
    """Wyświetla formularz rejestracji"""
    with st.form("registration_form"):
        st.subheader("Rejestracja")
        email = st.text_input("Email")
        password = st.text_input("Hasło", type="password")
        confirm_password = st.text_input("Potwierdź hasło", type="password")
        submitted = st.form_submit_button("Zarejestruj się")
        
        if submitted:
            if password != confirm_password:
                st.error("Hasła nie są identyczne!")
            else:
                # TODO: Implementacja rejestracji przez Supabase
                st.success("Zarejestrowano pomyślnie!")
                st.session_state.user = {"email": email}
                st.rerun()

def show_process_form():
    """Wyświetla formularz analizy procesu"""
    with st.form("process_form"):
        st.subheader("Analiza nowego procesu")
        
        # Dane o firmie
        st.write("### Informacje o firmie")
        company_size = st.selectbox(
            "Wielkość firmy",
            ["5-10 osób", "11-25 osób", "26-50 osób"]
        )
        industry = st.selectbox(
            "Branża",
            ["Marketing", "Księgowość", "Handel", "Produkcja", "Usługi"]
        )
        budget = st.selectbox(
            "Budżet na usprawnienia",
            ["do 500 zł/miesiąc", "500-2000 zł/miesiąc", "powyżej 2000 zł/miesiąc"]
        )
        
        # Dane o procesie
        st.write("### Informacje o procesie")
        process_name = st.text_input("Nazwa procesu")
        frequency = st.selectbox(
            "Częstotliwość",
            ["codziennie", "raz w tygodniu", "raz w miesiącu"]
        )
        participants = st.selectbox(
            "Liczba uczestników",
            ["1 osoba", "2-3 osoby", "4 lub więcej"]
        )
        duration = st.number_input("Czas trwania (godziny)", min_value=0.5, step=0.5)
        description = st.text_area("Opis procesu")
        
        # Cel usprawnienia
        st.write("### Cel usprawnienia")
        improvement_goal = st.multiselect(
            "Co chcesz poprawić?",
            ["szybkość", "mniej błędów", "mniej nudnej pracy", "oszczędność pieniędzy"]
        )
        
        submitted = st.form_submit_button("Przeanalizuj proces")
        
        if submitted:
            process_data = {
                "company": {
                    "size": company_size,
                    "industry": industry,
                    "budget": budget
                },
                "process": {
                    "name": process_name,
                    "frequency": frequency,
                    "participants": participants,
                    "duration": duration,
                    "description": description
                },
                "improvement_goal": improvement_goal
            }
            
            # TODO: Implementacja analizy AI
            st.session_state.analyzing = True
            st.rerun()

def show_analysis_results():
    """Wyświetla wyniki analizy"""
    st.subheader("Wyniki analizy")
    
    # Przykładowe wyniki (do zastąpienia przez prawdziwą analizę AI)
    results = {
        "ocena_potencjalu": 8,
        "mozliwe_oszczednosci": {
            "czas_godziny_miesiecznie": 16,
            "oszczednosci_pieniadze_miesiecznie": 2400
        },
        "rekomendacje": [
            {
                "narzedzie": "Zapier + InvoiceNinja",
                "czas_wdrozenia": "1 tydzień",
                "koszt_miesiecznie": 400,
                "opis": "Automatyczne tworzenie faktur z danych klientów"
            }
        ],
        "plan_wdrozenia": [
            "Tydzień 1: Konfiguracja InvoiceNinja",
            "Tydzień 2: Połączenie z systemem klientów przez Zapier"
        ]
    }
    
    # Wyświetlanie wyników
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Ocena potencjału",
            f"{results['ocena_potencjalu']}/10"
        )
        st.metric(
            "Możliwe oszczędności czasu",
            f"{results['mozliwe_oszczednosci']['czas_godziny_miesiecznie']}h/miesiąc"
        )
        st.metric(
            "Możliwe oszczędności pieniędzy",
            f"{results['mozliwe_oszczednosci']['oszczednosci_pieniadze_miesiecznie']} zł/miesiąc"
        )
    
    with col2:
        st.subheader("Rekomendowane narzędzia")
        for rec in results['rekomendacje']:
            with st.expander(f"🔧 {rec['narzedzie']}"):
                st.write(f"**Czas wdrożenia:** {rec['czas_wdrozenia']}")
                st.write(f"**Koszt miesięczny:** {rec['koszt_miesiecznie']} zł")
                st.write(f"**Opis:** {rec['opis']}")
    
    st.subheader("Plan wdrożenia")
    for i, step in enumerate(results['plan_wdrozenia'], 1):
        st.write(f"{i}. {step}")

def main():
    """Główna funkcja aplikacji"""
    initialize_session_state()
    
    # Nagłówek
    st.title("📊 SmartFlow - Analiza Procesów Biznesowych")
    st.markdown("---")
    
    # Logika logowania/rejestracji
    if not st.session_state.user:
        tab1, tab2 = st.tabs(["Logowanie", "Rejestracja"])
        with tab1:
            show_login_form()
        with tab2:
            show_registration_form()
    else:
        # Główny interfejs aplikacji
        st.sidebar.write(f"Zalogowany jako: {st.session_state.user['email']}")
        if st.sidebar.button("Wyloguj"):
            st.session_state.user = None
            st.rerun()
        
        # Formularz analizy procesu
        show_process_form()
        
        # Wyniki analizy
        if st.session_state.get('analyzing', False):
            show_analysis_results()

if __name__ == "__main__":
    main() 