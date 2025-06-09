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
        st.markdown("**Szczegółowy opis procesu** *")
        st.caption("💡 Opisz krok po kroku jak obecnie wygląda ten proces. Maksymalnie 3000 znaków.")
        st.caption("📋 **Tip:** Możesz wkleić tekst ze schowka używając **Ctrl+V**")
        
        description = st.text_area(
            label="Szczegółowy opis procesu",
            placeholder="Przykład: 1. Otrzymuję zamówienie mailem\n2. Sprawdzam dostępność produktu w excelu\n3. Tworzę fakturę ręcznie\n4. Wysyłam fakturę do klienta...\n\n💡 Możesz wkleić tutaj gotowy tekst z dokumentu używając Ctrl+V",
            height=200,
            max_chars=3000,
            label_visibility="collapsed",
            key="process_description"
        )
        
        # Licznik znaków
        char_count = len(description) if description else 0
        col_counter1, col_counter2 = st.columns([3, 1])
        with col_counter2:
            color = "red" if char_count > 3000 else "orange" if char_count > 2500 else "green"
            st.markdown(f"<p style='text-align: right; color: {color}; font-size: 0.8em;'>{char_count}/3000 znaków</p>", unsafe_allow_html=True)
        
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
                        "company": st.session_state.get("user_profile", {}),
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
                st.session_state.current_analysis = process_data
                
                # Wyświetl status analizy
                with st.spinner("Analizuję proces..."):
                    try:
                        # TODO: Tu będzie integracja z OpenAI
                        # Na razie generujemy mock wyniki
                        import time
                        time.sleep(2)  # Symulacja analizy
                        
                        # Mock wyników analizy AI
                        mock_ai_results = {
                            "ocena_potencjalu": 7,
                            "mozliwe_oszczednosci": {
                                "czas_godziny_miesiecznie": int(duration * 4),
                                "oszczednosci_pieniadze_miesiecznie": int(duration * 4 * 150)
                            },
                            "rekomendacje": [
                                {
                                    "narzedzie": "Zapier + Standardowe rozwiązanie",
                                    "czas_wdrozenia": "1-2 tygodnie",
                                    "koszt_miesiecznie": 200,
                                    "opis": f"Automatyzacja procesu: {process_name}"
                                }
                            ],
                            "plan_wdrozenia": [
                                "Tydzień 1: Analiza obecnego procesu",
                                "Tydzień 2: Konfiguracja narzędzi",
                                "Tydzień 3: Testowanie i wdrożenie"
                            ],
                            "uwagi": [
                                "Proces ma dobry potencjał automatyzacji",
                                "Zalecane stopniowe wdrażanie"
                            ]
                        }
                        
                        # Dodaj wyniki do danych procesu
                        st.session_state.current_analysis["ai_analysis"] = mock_ai_results
                        st.session_state.current_analysis["potential_score"] = mock_ai_results["ocena_potencjalu"]
                        
                        st.success("✅ Analiza zakończona! Przejdź do wyników.")
                        
                        # TODO: Zapisz do bazy danych Supabase
                        
                    except Exception as e:
                        st.error(f"Błąd podczas analizy: {str(e)}")
                
                st.rerun() 