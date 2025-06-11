"""
Moduł formularzy dla SmartFlow.
"""
import streamlit as st
import time
from typing import Dict, Any, List
from ai.openai_service import OpenAIService
from database.supabase_client import update_process, get_user_processes, save_process

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

    # Inicjalizacja stanu błędów walidacji
    if "validation_errors" not in st.session_state:
        st.session_state.validation_errors = {}
    if "validation_timestamp" not in st.session_state:
        st.session_state.validation_timestamp = 0

    # Sprawdź czy minęło 5 sekund i wyczyść błędy
    current_time = time.time()
    if st.session_state.validation_errors and (current_time - st.session_state.validation_timestamp) > 5:
        st.session_state.validation_errors = {}
        st.rerun()

    
    with st.form("process_form"):
        # Podstawowe informacje o procesie
        col1, col2 = st.columns(2)
        
        with col1:
            # Pole nazwa procesu z walidacją
            name_error = st.session_state.validation_errors.get("process_name", False)
            name_help = "To pole jest wymagane" if name_error else None
            
            process_name = st.text_input(
                "Nazwa procesu *",
                placeholder="np. Wystawianie faktur klientom",
                help=name_help
            )
            
            # Czerwony komunikat błędu pod polem
            if name_error:
                st.markdown("<p style='color: red; font-size: 0.8em; margin-top: -10px;'>Wypełnij nazwę procesu</p>", unsafe_allow_html=True)
            
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
        
        # Opis procesu z walidacją
        desc_error = st.session_state.validation_errors.get("description", False)
        
        st.markdown("**Szczegółowy opis procesu** *")
        st.caption("Opisz krok po kroku jak obecnie wygląda ten proces. Maksymalnie 3000 znaków.")
        st.caption("**Skróty klawiszowe:** Ctrl+V (wklej), Ctrl+A (zaznacz wszystko), Ctrl+Z (cofnij)")
        
        # CSS dla podświetlenia błędów - nazwa procesu
        if st.session_state.validation_errors.get("process_name"):
            st.markdown("""
            <style>
            .stTextInput input {
                border: 2px solid #ff4b4b !important;
                border-radius: 0.25rem !important;
                box-shadow: 0 0 0 0.2rem rgba(255, 75, 75, 0.25) !important;
            }
            </style>
            """, unsafe_allow_html=True)

        # CSS dla podświetlenia błędów - opis procesu  
        if desc_error:
            st.markdown("""
            <style>
            .stTextArea textarea {
                border: 2px solid #ff4b4b !important;
                border-radius: 0.25rem !important;
                box-shadow: 0 0 0 0.2rem rgba(255, 75, 75, 0.25) !important;
            }
            </style>
            """, unsafe_allow_html=True)

        description = st.text_area(
            label="Opis procesu",
            label_visibility="collapsed",
            placeholder="Przykład opisu procesu:\n\n1. Otrzymuję zamówienie przez email\n2. Sprawdzam dostępność produktu w systemie Excel\n3. Tworzę fakturę ręcznie w programie\n4. Wysyłam fakturę do klienta mailem\n5. Archywizuję dokumenty w folderze\n\nUWAGA: Możesz wkleić tekst ze schowka używając Ctrl+V",
            height=220,
            max_chars=3000,
            help="Pole obsługuje standardowe skróty klawiszowe: Ctrl+V (wklej), Ctrl+C (kopiuj), Ctrl+A (zaznacz wszystko)"
        )
        
        # Czerwony komunikat błędu pod polem opisu
        if desc_error:
            st.markdown("<p style='color: red; font-size: 0.8em; margin-top: -10px;'>Wypełnij opis procesu (min. 50 znaków)</p>", unsafe_allow_html=True)
        
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
            # Walidacja pól z podświetlaniem na 5 sekund
            validation_errors = {}
            
            if not process_name or process_name.strip() == "":
                validation_errors["process_name"] = True
                
            if not description or description.strip() == "":
                validation_errors["description"] = True
            elif len(description.strip()) < 50:
                validation_errors["description"] = True
            
            if validation_errors:
                # Ustaw błędy walidacji w session state
                st.session_state.validation_errors = validation_errors
                st.session_state.validation_timestamp = time.time()
                
                # Wyświetl ogólny komunikat błędu
                if validation_errors.get("process_name") and validation_errors.get("description"):
                    st.error("Wypełnij pola: nazwę procesu i opis procesu (min. 50 znaków)")
                elif validation_errors.get("process_name"):
                    st.error("Wypełnij nazwę procesu")
                elif validation_errors.get("description"):
                    if not description or description.strip() == "":
                        st.error("Wypełnij opis procesu")
                    else:
                        st.error("Opis procesu musi mieć co najmniej 50 znaków")
                
                # Przeładuj formularz aby pokazać błędy i ustaw timer
                st.rerun()
            else:
                # Wyczyść błędy walidacji
                st.session_state.validation_errors = {}
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
                        ai_service = OpenAIService()
                        ai_results = ai_service.analyze_process(process_data)
                        st.session_state.current_analysis["ai_analysis"] = ai_results
                        st.session_state.current_analysis["potential_score"] = ai_results["ocena_potencjalu"]
                        # Zapisz proces do bazy
                        user_id = st.session_state.user_data["id"] if st.session_state.user_data else None
                        if user_id:
                            try:
                                process_id = save_process(user_id, st.session_state.current_analysis)
                                st.success("Proces został zapisany!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Błąd zapisu procesu: {str(e)}")
                        else:
                            st.warning("Brak użytkownika. Proces nie został zapisany.")
                    except Exception as e:
                        st.error(f"Błąd podczas analizy: {str(e)}")
                
                st.rerun()

    # Pasek boczny z informacjami o walidacji
    if st.session_state.validation_errors and st.session_state.validation_timestamp > 0:
        time_left = max(0, 5.0 - (time.time() - st.session_state.validation_timestamp))
        if time_left > 0:
            with st.sidebar:
                st.warning(f"Błędy znikną za {time_left:.1f}s")
                
                # Auto-refresh co sekundę
                time.sleep(0.1)
                st.rerun()

def edit_process_form():
    st.subheader("Edytuj proces")
    supabase = st.session_state.get("supabase")
    user_id = st.session_state.user_data["id"] if st.session_state.user_data else None
    process_id = st.session_state.get("edit_process_id")
    if not (supabase and user_id and process_id):
        st.error("Brak danych do edycji procesu.")
        return
    # Pobierz dane procesu
    processes = get_user_processes(supabase, user_id)
    process = next((p for p in processes if p["id"] == process_id), None)
    if not process:
        st.error("Nie znaleziono procesu do edycji.")
        return
    # Formularz edycji
    with st.form("edit_process_form"):
        new_title = st.text_input("Nazwa procesu", value=process.get("title", ""))
        new_description = st.text_area("Opis procesu", value=process.get("description", ""), height=150)
        new_goals = st.text_input("Cele usprawnienia (przecinek)", value=", ".join(process.get("form_data", {}).get("improvement_goals", [])))
        submitted = st.form_submit_button("Zapisz zmiany", use_container_width=True)
        if submitted:
            updated_data = {
                "title": new_title,
                "description": new_description,
                "form_data": process.get("form_data", {})
            }
            # Aktualizuj cele usprawnienia
            updated_data["form_data"]["improvement_goals"] = [g.strip() for g in new_goals.split(",") if g.strip()]
            try:
                update_process(process_id, updated_data)
                st.success("Proces został zaktualizowany.")
                st.session_state.page = "dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"Błąd podczas aktualizacji: {str(e)}") 