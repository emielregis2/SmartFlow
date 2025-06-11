"""
Moduł formularzy dla SmartFlow.
"""
import streamlit as st
import time
from typing import Dict, Any, List
from ai.openai_service import OpenAIService
from database.supabase_client import update_process, get_user_processes, save_process

def validate_process_form(form_data: Dict[str, Any]) -> Dict[str, str]:
    """Waliduje dane formularza procesu."""
    errors = {}
    
    if not form_data.get('nazwa', '').strip():
        errors['nazwa'] = "Nazwa procesu jest wymagana"
    
    if not form_data.get('opis', '').strip():
        errors['opis'] = "Opis procesu jest wymagany"
    
    if not form_data.get('wielkosc_firmy'):
        errors['wielkosc_firmy'] = "Wielkość firmy jest wymagana"
    
    if not form_data.get('branza'):
        errors['branza'] = "Branża jest wymagana"
    
    if not form_data.get('budzet'):
        errors['budzet'] = "Budżet jest wymagany"
    
    if not form_data.get('czestotliwosc'):
        errors['czestotliwosc'] = "Częstotliwość jest wymagana"
    
    if not form_data.get('uczestnicy'):
        errors['uczestnicy'] = "Liczba uczestników jest wymagana"
    
    if not form_data.get('czas_godziny'):
        errors['czas_godziny'] = "Czas trwania jest wymagany"
    
    if not form_data.get('cel_usprawnienia'):
        errors['cel_usprawnienia'] = "Cel usprawnienia jest wymagany"
    
    return errors

def show_process_form():
    """Wyświetla formularz dodawania/edycji procesu."""
    st.header("Przeanalizuj nowy proces")

    # Inicjalizacja session state dla walidacji
    if 'validation_errors' not in st.session_state:
        st.session_state.validation_errors = {}
    if 'validation_timestamp' not in st.session_state:
        st.session_state.validation_timestamp = 0
    if 'validation_auto_clear' not in st.session_state:
        st.session_state.validation_auto_clear = False

    # Automatyczne czyszczenie błędów po 5 sekundach
    current_time = time.time()
    if (st.session_state.validation_timestamp > 0 and 
        current_time - st.session_state.validation_timestamp >= 5.0):
        st.session_state.validation_errors = {}
        st.session_state.validation_timestamp = 0
        st.session_state.validation_auto_clear = False
        st.rerun()

    # CSS dla czerwonych ramek
    if st.session_state.validation_errors:
        st.markdown("""
        <style>
        .stTextInput > div > div > input[aria-invalid="true"] {
            border: 2px solid #ff4444 !important;
            border-radius: 4px !important;
        }
        .stTextArea > div > div > textarea[aria-invalid="true"] {
            border: 2px solid #ff4444 !important;
            border-radius: 4px !important;
        }
        .validation-error {
            color: #ff4444;
            font-size: 0.8em;
            margin-top: 2px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Informacje o firmie
    st.subheader("Informacje o firmie")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wielkosc_firmy = st.selectbox(
            "Wielkość firmy",
            ["", "5-10 osób", "11-25 osób", "26-50 osób", "Powyżej 50 osób"],
            key="wielkosc_firmy"
        )
        if 'wielkosc_firmy' in st.session_state.validation_errors:
            st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["wielkosc_firmy"]}</div>', unsafe_allow_html=True)
    
    with col2:
        branza = st.selectbox(
            "Branża",
            ["", "Handel", "Usługi", "Produkcja", "IT", "Marketing", "Księgowość", 
             "Medycyna", "Edukacja", "Gastronomia", "Inna"],
            key="branza"
        )
        if 'branza' in st.session_state.validation_errors:
            st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["branza"]}</div>', unsafe_allow_html=True)

    budzet = st.selectbox(
        "Miesięczny budżet na usprawnienia",
        ["", "Do 500 zł", "500-2000 zł", "2000-5000 zł", "Powyżej 5000 zł"],
        key="budzet"
    )
    if 'budzet' in st.session_state.validation_errors:
        st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["budzet"]}</div>', unsafe_allow_html=True)

    # Szczegóły procesu
    st.subheader("Szczegóły procesu")
    
    nazwa = st.text_input(
        "Nazwa procesu",
        placeholder="np. Wystawianie faktur",
        key="nazwa"
    )
    if st.session_state.validation_errors.get('nazwa'):
        st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["nazwa"]}</div>', unsafe_allow_html=True)

    opis = st.text_area(
        "Opis procesu",
        placeholder="Opisz dokładnie jak wygląda ten proces - krok po kroku",
        height=150,
        key="opis"
    )
    if st.session_state.validation_errors.get('opis'):
        st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["opis"]}</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        czestotliwosc = st.selectbox(
            "Jak często wykonywany",
            ["", "Codziennie", "Kilka razy w tygodniu", "Raz w tygodniu", 
             "Kilka razy w miesiącu", "Raz w miesiącu", "Rzadziej"],
            key="czestotliwosc"
        )
        if 'czestotliwosc' in st.session_state.validation_errors:
            st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["czestotliwosc"]}</div>', unsafe_allow_html=True)
    
    with col2:
        uczestnicy = st.selectbox(
            "Liczba osób zaangażowanych",
            ["", "1 osoba", "2-3 osoby", "4-5 osób", "6-10 osób", "Powyżej 10 osób"],
            key="uczestnicy"
        )
        if 'uczestnicy' in st.session_state.validation_errors:
            st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["uczestnicy"]}</div>', unsafe_allow_html=True)

    czas_godziny = st.number_input(
        "Ile godzin zajmuje (za każdym razem)",
        min_value=0.0,
        max_value=100.0,
        step=0.5,
        key="czas_godziny"
    )
    if 'czas_godziny' in st.session_state.validation_errors:
        st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["czas_godziny"]}</div>', unsafe_allow_html=True)

    # Cel usprawnienia
    st.subheader("Cel usprawnienia")
    
    cel_usprawnienia = st.multiselect(
        "Co chcesz poprawić? (możesz wybrać kilka opcji)",
        ["Szybkość wykonania", "Mniej błędów", "Mniej nudnej pracy", 
         "Oszczędność pieniędzy", "Lepsza jakość", "Automatyzacja"],
        key="cel_usprawnienia"
    )
    if 'cel_usprawnienia' in st.session_state.validation_errors:
        st.markdown(f'<div class="validation-error">{st.session_state.validation_errors["cel_usprawnienia"]}</div>', unsafe_allow_html=True)

    # Przycisk analizy
    if st.button("🔍 Przeanalizuj proces", type="primary", use_container_width=True):
        # Zbierz dane z formularza
        form_data = {
            'nazwa': nazwa,
            'opis': opis,
            'wielkosc_firmy': wielkosc_firmy,
            'branza': branza,
            'budzet': budzet,
            'czestotliwosc': czestotliwosc,
            'uczestnicy': uczestnicy,
            'czas_godziny': czas_godziny,
            'cel_usprawnienia': cel_usprawnienia
        }
        
        # Walidacja
        validation_errors = validate_process_form(form_data)
        
        if validation_errors:
            # Zapisz błędy i timestamp
            st.session_state.validation_errors = validation_errors
            st.session_state.validation_timestamp = time.time()
            st.session_state.validation_auto_clear = True
            
            # Pokaż główny komunikat błędu
            st.error("❌ Wypełnij wszystkie obowiązkowe pola!")
            
            # Odśwież stronę aby pokazać czerwone ramki
            st.rerun()
            
        else:
            # Wyczyść błędy jeśli wszystko jest OK
            st.session_state.validation_errors = {}
            st.session_state.validation_timestamp = 0
            
            # Analiza AI
            with st.spinner("Analizuję proces..."):
                try:
                    user = st.session_state.user
                    openai_service = OpenAIService()
                    
                    # Wywołaj analizę AI
                    analiza = openai_service.analyze_process(form_data)
                    
                    # Zapisz proces
                    process_data = {
                        **form_data,
                        'analiza_ai': analiza,
                        'ocena_potencjalu': analiza.get('ocena_potencjalu', 5),
                        'status': 'nowy'
                    }
                    
                    result = save_process(user["id"], process_data)
                    
                    if result:
                        st.success("✅ Proces został przeanalizowany i zapisany!")
                        st.balloons()
                        
                        # Pokaż wyniki
                        st.subheader("📊 Wyniki analizy")
                        st.json(analiza)
                        
                        # Wyczyść formularz
                        for key in form_data.keys():
                            if key in st.session_state:
                                del st.session_state[key]
                        
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Błąd podczas zapisywania procesu")
                        
                except Exception as e:
                    st.error(f"❌ Błąd podczas analizy: {str(e)}")

    # Pasek boczny z informacjami o walidacji
    if st.session_state.validation_errors and st.session_state.validation_timestamp > 0:
        time_left = max(0, 5.0 - (time.time() - st.session_state.validation_timestamp))
        if time_left > 0:
            with st.sidebar:
                st.warning(f"⏰ Błędy znikną za {time_left:.1f}s")
                
                # Auto-refresh co sekundę
                if st.session_state.validation_auto_clear:
                    time.sleep(0.1)
                    st.rerun()

def edit_process_form():
    st.subheader("Edytuj proces")
    user_id = st.session_state.user_data["id"] if st.session_state.user_data else None
    process_id = st.session_state.get("edit_process_id")
    if not (user_id and process_id):
        st.error("Brak danych do edycji procesu.")
        return
    # Pobierz dane procesu
    processes = get_user_processes(user_id)
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