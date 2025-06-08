"""
Moduł formularzy dla SmartFlow.
"""
import streamlit as st
from typing import Dict, Any, List

def show_profile_form():
    """Formularz danych o firmie (jednorazowy)"""
    st.subheader("Informacje o Twojej firmie")
    st.write("Wypełnij podstawowe informacje o firmie, aby otrzymywać lepsze rekomendacje.")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_size = st.selectbox(
                "Wielkość firmy",
                ["5-10 osób", "11-25 osób", "26-50 osób"]
            )
            
            industry = st.selectbox(
                "Branża",
                ["Marketing", "Księgowość", "Handel", "Produkcja", "Usługi"]
            )
        
        with col2:
            budget_range = st.selectbox(
                "Budżet na usprawnienia",
                ["do 500 zł/miesiąc", "500-2000 zł/miesiąc", "powyżej 2000 zł/miesiąc"]
            )
        
        submitted = st.form_submit_button("Zapisz profil firmy", use_container_width=True)
        
        if submitted:
            profile_data = {
                "company_size": company_size,
                "industry": industry,
                "budget_range": budget_range
            }
            
            # TODO: Zapisz do Supabase
            st.session_state.user_profile = profile_data
            st.success("Profil firmy zapisany!")
            st.rerun()

def show_process_form():
    """Formularz analizy nowego procesu"""
    st.subheader("Przeanalizuj nowy proces")
    st.write("Opisz proces, który chcesz zoptymalizować, a AI wygeneruje rekomendacje.")
    
    with st.form("process_form"):
        # Podstawowe informacje o procesie
        col1, col2 = st.columns(2)
        
        with col1:
            process_name = st.text_input(
                "Nazwa procesu *",
                placeholder="np. Wystawianie faktur klientom"
            )
            
            frequency = st.selectbox(
                "Jak często wykonywany",
                ["codziennie", "raz w tygodniu", "raz w miesiącu"]
            )
            
            participants = st.selectbox(
                "Liczba uczestników",
                ["1 osoba", "2-3 osoby", "4 lub więcej"]
            )
        
        with col2:
            duration = st.number_input(
                "Czas trwania (godziny)",
                min_value=0.5,
                max_value=40.0,
                step=0.5,
                value=2.0
            )
            
            improvement_goals = st.multiselect(
                "Co chcesz poprawić?",
                ["szybkość", "mniej błędów", "mniej nudnej pracy", "oszczędność pieniędzy"],
                default=["szybkość"]
            )
        
        # Opis procesu
        description = st.text_area(
            "Szczegółowy opis procesu *",
            placeholder="Opisz krok po kroku jak obecnie wygląda ten proces...",
            height=150
        )
        
        # Przyciski
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.form_submit_button("Anuluj", use_container_width=True):
                st.rerun()
        
        with col2:
            submitted = st.form_submit_button("Przeanalizuj proces", use_container_width=True, type="primary")
        
        if submitted:
            if not process_name or not description:
                st.error("Wypełnij wszystkie pola oznaczone *")
            elif len(description) < 50:
                st.error("Opis procesu musi mieć co najmniej 50 znaków")
            else:
                # Przygotuj dane do analizy
                process_data = {
                    "title": process_name,
                    "description": description,
                    "form_data": {
                        "company": st.session_state.user_profile,
                        "process": {
                            "name": process_name,
                            "frequency": frequency,
                            "participants": participants,
                            "duration": duration,
                            "description": description
                        },
                        "improvement_goals": improvement_goals
                    }
                }
                
                # Zapisz do session state
                st.session_state.form_data = process_data
                st.rerun() 