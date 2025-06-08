# SmartFlow - Plan architektury UI

## Przegląd

Ten dokument opisuje architekturę interfejsu użytkownika dla aplikacji SmartFlow. Projekt został zoptymalizowany pod kątem prostoty MVP z wykorzystaniem podstawowych komponentów Streamlit.

## Architektura UI

### Główne założenia
- Single-page aplikacja w jednym pliku streamlit_app.py
- Linearne UI flow: Logowanie → Formularz → Wyniki → Dashboard
- Conditional rendering z wykorzystaniem session state
- Minimalne komponenty Streamlit dla szybkiej implementacji
- Desktop-first (bez optymalizacji mobile)

### Przepływ użytkownika
1. **Strona logowania** - email/hasło lub rejestracja
2. **Profil firmy** - jednorazowe wypełnienie danych o firmie
3. **Dashboard procesów** - lista przeanalizowanych procesów
4. **Formularz nowego procesu** - analiza nowego procesu
5. **Wyniki analizy** - prezentacja rekomendacji AI

## Struktura plików

```
smartflow/
├── streamlit_app.py           # Główna aplikacja (wszystko tutaj)
├── components/
│   ├── __init__.py
│   ├── auth.py               # Funkcje logowania/rejestracji
│   ├── forms.py              # Formularze i walidacja
│   ├── visualizations.py     # Podstawowe wykresy
│   └── utils.py              # Utility functions
├── database/
│   └── supabase_client.py    # Klient bazy danych
├── ai/
│   └── openai_service.py     # Serwis AI
└── requirements.txt
```

## Session State Management

### Struktura stanu aplikacji
```python
# Inicjalizacja session state
def initialize_session_state():
    """Inicjalizuje wszystkie zmienne stanu aplikacji"""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    if 'processes' not in st.session_state:
        st.session_state.processes = []
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    if 'page' not in st.session_state:
        st.session_state.page = 'auth'  # auth, profile, dashboard, new_process, results
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}

# Funkcje nawigacji
def go_to_page(page_name: str):
    """Przełącza na wybraną stronę"""
    st.session_state.page = page_name
    st.rerun()

def logout_user():
    """Wylogowuje użytkownika i resetuje stan"""
    st.session_state.user = None
    st.session_state.user_profile = None
    st.session_state.processes = []
    st.session_state.current_analysis = None
    st.session_state.page = 'auth'
    st.rerun()
```

## Layout głównej aplikacji

### Struktura streamlit_app.py
```python
import streamlit as st
import pandas as pd
from components.auth import show_auth_page
from components.forms import show_profile_form, show_process_form
from components.visualizations import show_dashboard, show_results
from database.supabase_client import SupabaseClient
from ai.openai_service import OpenAIService

# Konfiguracja strony
st.set_page_config(
    page_title="SmartFlow - Analiza Procesów Biznesowych",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    """Główna funkcja aplikacji"""
    initialize_session_state()
    
    # Header zawsze widoczny
    show_header()
    
    # Routing na podstawie stanu
    if st.session_state.page == 'auth':
        show_auth_page()
    elif st.session_state.page == 'profile':
        show_profile_form()
    elif st.session_state.page == 'dashboard':
        show_dashboard()
    elif st.session_state.page == 'new_process':
        show_process_form()
    elif st.session_state.page == 'results':
        show_results()
    else:
        st.error("Nieznana strona")
        go_to_page('dashboard')

def show_header():
    """Wyświetla nagłówek aplikacji"""
    st.title("SmartFlow - Analiza Procesów Biznesowych")
    
    # Navigation bar jeśli zalogowany
    if st.session_state.user:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.write(f"Zalogowany: {st.session_state.user['email']}")
        
        with col2:
            if st.button("Dashboard"):
                go_to_page('dashboard')
        
        with col3:
            if st.button("Nowy proces"):
                go_to_page('new_process')
        
        with col4:
            if st.button("Wyloguj"):
                logout_user()
    
    st.markdown("---")

if __name__ == "__main__":
    main()
```

## Komponenty UI

### 1. Strona autentykacji (auth.py)
```python
import streamlit as st
from database.supabase_client import SupabaseClient

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
                # user = supabase_client.login(email, password)
                # if user:
                
                # Tymczasowo - mock login
                st.session_state.user = {"email": email, "id": "mock-id"}
                
                # Sprawdź czy ma profil firmy
                # profile = supabase_client.get_user_profile(user_id)
                # if profile:
                #     st.session_state.user_profile = profile
                #     go_to_page('dashboard')
                # else:
                #     go_to_page('profile')
                
                # Tymczasowo
                go_to_page('dashboard')
                
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
                # user = supabase_client.register(email, password)
                
                # Tymczasowo - mock registration
                st.session_state.user = {"email": email, "id": "mock-id"}
                st.success("Konto utworzone pomyślnie!")
                go_to_page('profile')  # Nowy użytkownik → profil firmy
```

### 2. Formularz profilu firmy (forms.py)
```python
import streamlit as st

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
            # supabase_client.save_user_profile(st.session_state.user['id'], profile_data)
            
            st.session_state.user_profile = profile_data
            st.success("Profil firmy zapisany!")
            
            # Przekieruj do dashboard
            go_to_page('dashboard')

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
                go_to_page('dashboard')
        
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
                
                # Rozpocznij analizę AI
                start_ai_analysis(process_data)

def start_ai_analysis(process_data):
    """Rozpoczyna analizę AI i wyświetla wyniki"""
    with st.spinner("Analizuję proces za pomocą AI... To może potrwać do 60 sekund."):
        try:
            # TODO: Integracja z OpenAI Service
            # from ai.openai_service import OpenAIService, ProcessAnalysisRequest
            # ai_service = OpenAIService(api_key=st.secrets["OPENAI_API_KEY"])
            # result = ai_service.analyze_process(request)
            
            # Tymczasowo - mock wyniki
            result = {
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
                    "Tydzień 2: Połączenie przez Zapier"
                ],
                "uwagi": ["Wymaga zgodę klientów na automatyczne faktury"]
            }
            
            # TODO: Zapisz proces i analizę do bazy danych
            # process_id = supabase_client.save_process(user_id, process_data, result)
            
            # Zapisz do session state
            st.session_state.current_analysis = {
                **process_data,
                "analysis": result,
                "id": "mock-process-id"
            }
            
            st.success("Analiza zakończona pomyślnie!")
            go_to_page('results')
            
        except Exception as e:
            st.error(f"Błąd podczas analizy: {str(e)}")
```

### 3. Dashboard procesów (visualizations.py)
```python
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def show_dashboard():
    """Dashboard z listą procesów użytkownika"""
    st.subheader("Twoje procesy")
    
    # Przycisk dodania nowego procesu
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"Zarządzaj swoimi przeanalizowanymi procesami")
    
    with col3:
        if st.button("Nowy proces", use_container_width=True, type="primary"):
            go_to_page('new_process')
    
    # TODO: Pobierz procesy z bazy danych
    # processes = supabase_client.get_user_processes(st.session_state.user['id'])
    
    # Tymczasowo - mock data
    processes = [
        {
            "id": "1",
            "title": "Wystawianie faktur",
            "potential_score": 8,
            "created_at": "2025-06-07",
            "status": "analyzed"
        },
        {
            "id": "2", 
            "title": "Rekrutacja pracowników",
            "potential_score": 6,
            "created_at": "2025-06-06",
            "status": "analyzed"
        }
    ]
    
    if not processes:
        show_empty_dashboard()
    else:
        show_processes_list(processes)

def show_empty_dashboard():
    """Dashboard gdy brak procesów"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info(
            "**Nie masz jeszcze żadnych przeanalizowanych procesów**\n\n"
            "Kliknij 'Nowy proces' aby rozpocząć analizę swojego pierwszego procesu biznesowego."
        )
        
        if st.button("Rozpocznij analizę", use_container_width=True, type="primary"):
            go_to_page('new_process')

def show_processes_list(processes):
    """Lista procesów w formie tabeli"""
    st.markdown("---")
    
    # Konwersja do DataFrame
    df = pd.DataFrame(processes)
    
    # Formatowanie kolumn
    df['Ocena'] = df['potential_score'].apply(lambda x: f"{x}/10")
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d.%m.%Y')
    df['Status'] = df['status'].apply(lambda x: "Przeanalizowany" if x == "analyzed" else "Oczekuje")
    
    # Wyświetl tabelę
    display_df = df[['title', 'Ocena', 'Data', 'Status']].copy()
    display_df.columns = ['Nazwa procesu', 'Ocena potencjału', 'Data utworzenia', 'Status']
    
    # Tabela z selection
    event = st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row"
    )
    
    # Obsługa kliknięcia w wiersz
    if event.selection.rows:
        selected_idx = event.selection.rows[0]
        selected_process = processes[selected_idx]
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("Zobacz szczegóły"):
                # TODO: Załaduj szczegóły procesu
                st.session_state.current_analysis = selected_process
                go_to_page('results')
        
        with col2:
            if st.button("Edytuj"):
                st.info("Funkcja edycji będzie dostępna wkrótce")
        
        with col3:
            if st.button("Usuń", type="secondary"):
                # TODO: Soft delete w bazie danych
                st.success(f"Proces '{selected_process['title']}' został usunięty")
                st.rerun()

def show_results():
    """Wyświetla wyniki analizy AI"""
    if not st.session_state.current_analysis:
        st.error("Brak danych analizy")
        if st.button("Powrót do dashboard"):
            go_to_page('dashboard')
        return
    
    analysis = st.session_state.current_analysis
    ai_results = analysis.get('analysis', {})
    
    # Header z tytułem procesu
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"Analiza: {analysis.get('title', 'Proces')}")
    
    with col2:
        if st.button("Powrót", use_container_width=True):
            go_to_page('dashboard')
    
    st.markdown("---")
    
    # Główne metryki
    show_key_metrics(ai_results)
    
    # Rekomendacje
    show_recommendations(ai_results)
    
    # Plan wdrożenia  
    show_implementation_plan(ai_results)
    
    # Akcje
    show_result_actions(analysis)

def show_key_metrics(ai_results):
    """Wyświetla kluczowe metryki analizy"""
    st.subheader("Podsumowanie analizy")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        score = ai_results.get('ocena_potencjalu', 0)
        st.metric(
            "Ocena potencjału",
            f"{score}/10",
            delta=f"{'Wysoki' if score >= 7 else 'Średni' if score >= 4 else 'Niski'} potencjał"
        )
    
    with col2:
        time_savings = ai_results.get('mozliwe_oszczednosci', {}).get('czas_godziny_miesiecznie', 0)
        st.metric(
            "Oszczędność czasu",
            f"{time_savings}h/miesiąc",
            delta=f"{time_savings * 12}h/rok"
        )
    
    with col3:
        cost_savings = ai_results.get('mozliwe_oszczednosci', {}).get('oszczednosci_pieniadze_miesiecznie', 0)
        st.metric(
            "Oszczędność kosztów",
            f"{cost_savings:,.0f} zł/miesiąc",
            delta=f"{cost_savings * 12:,.0f} zł/rok"
        )

def show_recommendations(ai_results):
    """Wyświetla rekomendacje narzędzi"""
    st.subheader("Rekomendowane rozwiązania")
    
    recommendations = ai_results.get('rekomendacje', [])
    
    for i, rec in enumerate(recommendations, 1):
        with st.expander(f"{i}. {rec.get('narzedzie', 'Nieznane narzędzie')}", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Opis:** {rec.get('opis', 'Brak opisu')}")
            
            with col2:
                st.write(f"**Czas wdrożenia:** {rec.get('czas_wdrozenia', 'Nieznany')}")
                st.write(f"**Koszt:** {rec.get('koszt_miesiecznie', 0)} zł/miesiąc")

def show_implementation_plan(ai_results):
    """Wyświetla plan wdrożenia"""
    st.subheader("Plan wdrożenia")
    
    plan = ai_results.get('plan_wdrozenia', [])
    
    for i, step in enumerate(plan, 1):
        st.write(f"**{i}.** {step}")
    
    # Uwagi
    uwagi = ai_results.get('uwagi', [])
    if uwagi:
        st.subheader("Ważne uwagi")
        for uwaga in uwagi:
            st.warning(uwaga)

def show_result_actions(analysis):
    """Akcje dostępne dla wyników"""
    st.markdown("---")
    st.subheader("Co dalej?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Eksportuj raport", use_container_width=True):
            st.info("Funkcja eksportu będzie dostępna wkrótce")
    
    with col2:
        if st.button("Analizuj ponownie", use_container_width=True):
            # Wróć do formularza z wypełnionymi danymi
            go_to_page('new_process')
    
    with col3:
        if st.button("Nowy proces", use_container_width=True, type="primary"):
            st.session_state.current_analysis = None
            go_to_page('new_process')
```

## Styling i UX

### CSS customization
```python
# W streamlit_app.py - dodaj na początku
def apply_custom_styles():
    """Stosuje niestandardowe style CSS"""
    st.markdown("""
    <style>
    /* Główny container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Przyciski */
    .stButton > button {
        border-radius: 6px;
        border: none;
        font-weight: 500;
    }
    
    /* Formularze */
    .stForm {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    /* Metryki */
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 6px;
        border: 1px solid #e9ecef;
    }
    
    /* Tabela */
    .stDataFrame {
        border: 1px solid #e9ecef;
        border-radius: 6px;
    }
    
    /* Ukryj menu Streamlit */
    #MainMenu {visibility: hidden;}
    
    /* Ukryj footer */
    footer {visibility: hidden;}
    
    /* Ukryj header */
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Wywołaj na początku main()
def main():
    apply_custom_styles()
    # ... reszta kodu
```

### Loading states
```python
def show_loading_spinner(message: str = "Ładowanie..."):
    """Wyświetla spinner z custom message"""
    return st.spinner(message)

def show_progress_bar(progress: float, message: str = ""):
    """Wyświetla progress bar"""
    progress_bar = st.progress(progress)
    if message:
        st.text(message)
    return progress_bar
```

## Error Handling

### Error boundaries
```python
def safe_component(component_func):
    """Decorator dla bezpiecznego wyświetlania komponentów"""
    def wrapper(*args, **kwargs):
        try:
            return component_func(*args, **kwargs)
        except Exception as e:
            st.error(f"Błąd w komponencie: {str(e)}")
            st.info("Odśwież stronę lub skontaktuj się z pomocą techniczną")
            
            # Log błędu
            import logging
            logging.error(f"Component error in {component_func.__name__}: {str(e)}")
            
            return None
    return wrapper

# Użycie
@safe_component
def show_dashboard():
    # ... kod dashboard
```

### Validation helpers
```python
def validate_email(email: str) -> bool:
    """Waliduje format emaila"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_process_form(data: dict) -> list:
    """Waliduje dane formularza procesu"""
    errors = []
    
    if not data.get('title'):
        errors.append("Nazwa procesu jest wymagana")
    elif len(data['title']) < 3:
        errors.append("Nazwa procesu musi mieć co najmniej 3 znaki")
    
    if not data.get('description'):
        errors.append("Opis procesu jest wymagany")
    elif len(data['description']) < 50:
        errors.append("Opis procesu musi mieć co najmniej 50 znaków")
    
    return errors
```

## Testing UI

### Testy komponentów
```python
import pytest
import streamlit as st
from unittest.mock import patch, MagicMock

def test_auth_page():
    """Test strony logowania"""
    with patch('streamlit.form') as mock_form:
        with patch('streamlit.text_input') as mock_input:
            mock_input.return_value = "test@example.com"
            
            show_auth_page()
            
            # Sprawdź czy formularz został utworzony
            mock_form.assert_called()

def test_process_form_validation():
    """Test walidacji formularza procesu"""
    data = {
        'title': 'Te',  # Za krótkie
        'description': 'Krótki opis'  # Za krótki
    }
    
    errors = validate_process_form(data)
    
    assert len(errors) == 2
    assert "co najmniej 3 znaki" in errors[0]
    assert "co najmniej 50 znaków" in errors[1]

def test_session_state_initialization():
    """Test inicjalizacji session state"""
    # Mock session_state
    st.session_state = {}
    
    initialize_session_state()
    
    assert 'user' in st.session_state
    assert 'page' in st.session_state
    assert st.session_state.page == 'auth'
```

## Deployment considerations

### Environment-specific UI
```python
import os

def get_app_config():
    """Zwraca konfigurację UI dla środowiska"""
    env = os.getenv('ENVIRONMENT', 'development')
    
    if env == 'production':
        return {
            'debug_mode': False,
            'show_mock_data': False,
            'page_title': "SmartFlow",
        }
    else:
        return {
            'debug_mode': True,
            'show_mock_data': True,
            'page_title': "SmartFlow (DEV)",
        }

# Debug panel dla developmentu
def show_debug_panel():
    """Panel debugowy (tylko development)"""
    config = get_app_config()
    
    if config['debug_mode']:
        with st.expander("Debug Panel"):
            st.json(dict(st.session_state))
            
            if st.button("Reset Session State"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
```

## Harmonogram implementacji

### Faza 1: Podstawowa struktura (2-3 godziny)
1. Struktura plików i session state management
2. Routing między stronami
3. Podstawowe komponenty auth i formularzy
4. Mock data dla testowania

### Faza 2: Integracja (2-3 godziny)
1. Połączenie z Supabase (auth, database)
2. Integracja z OpenAI service
3. Obsługa błędów i walidacja
4. Podstawowe style CSS

### Faza 3: Finalizacja (1-2 godziny)
1. Dashboard z prawdziwymi danymi
2. Polish UI/UX
3. Testy komponentów
4. Deployment considerations

## Metryki UX

### KPI interfejsu
- **Task completion rate:** > 90% użytkowników kończy analizę procesu
- **Time to first value:** < 5 minut od rejestracji do pierwszej analizy
- **Error rate:** < 5% błędów w formularzach
- **User satisfaction:** > 4/5 w ankiecie UX

### A/B testing możliwości
- Formularz jednoetapowy vs wizard
- Tabela vs karty dla listy procesów
- Różne prompty w AI analysis
- Pozycja CTA buttons

---

**Autor:** Sesja planistyczna z AI (10xDevs)  
**Data:** 8 czerwca 2025  
**Status:** Gotowy do implementacji