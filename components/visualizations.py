"""
Moduł wizualizacji dla SmartFlow.
"""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import database.supabase_client as supabase_client
import json

def show_dashboard():
    """Dashboard z listą procesów użytkownika"""
    st.subheader("Twoje procesy")
    
    # Usunięto przycisk dodania nowego procesu
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"Zarządzaj swoimi przeanalizowanymi procesami")
    
    user = st.session_state.get("user") or st.session_state.get("user_data")
    if not user or not user.get("id"):
        st.warning("Brak informacji o użytkowniku. Zaloguj się ponownie.")
        return
    processes = supabase_client.get_user_processes(user["id"])
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
            st.session_state.page = "new_process"
            st.rerun()

def show_processes_list(processes: List[Dict[str, Any]]):
    """Lista procesów w formie tabeli z akcjami CRUD"""
    st.markdown("---")
    if not processes or len(processes) == 0:
        st.info("Brak procesów do wyświetlenia.")
        return

    # Konwersja do DataFrame
    df = pd.DataFrame(processes)

    # Dodaj skrócony opis do 500 znaków, nie tnąc wyrazów
    def short_desc(desc):
        if not desc:
            return ""
        if len(desc) <= 500:
            return desc
        cut = desc[:500].rsplit(' ', 1)[0]
        return cut + "…"
    df['OpisShort'] = df['description'].apply(short_desc)
    df['OpisLong'] = df['description']

    # Dodaj skróconą analizę AI (jako tekst JSON)
    def ai_short(ai):
        if not ai:
            return ""
        # Jeśli to string, spróbuj sparsować
        if isinstance(ai, str):
            try:
                ai_obj = json.loads(ai)
            except Exception:
                return ai[:500] + ("…" if len(ai) > 500 else "")
        else:
            ai_obj = ai
        text = json.dumps(ai_obj, ensure_ascii=False, indent=2)
        if len(text) <= 500:
            return text
        cut = text[:500].rsplit(' ', 1)[0]
        return cut + "…"
    def ai_long(ai):
        if not ai:
            return ""
        if isinstance(ai, str):
            try:
                ai_obj = json.loads(ai)
            except Exception:
                return ai
        else:
            ai_obj = ai
        return json.dumps(ai_obj, ensure_ascii=False, indent=2)
    df['AIShort'] = df['ai_analysis'].apply(ai_short)
    df['AILong'] = df['ai_analysis'].apply(ai_long)
    
    # Formatowanie kolumn
    df['Ocena'] = df['potential_score'].apply(lambda x: f"{x}/10")
    df['Data'] = pd.to_datetime(df['created_at']).dt.strftime('%d.%m.%Y')
    df['Status'] = df['status'].apply(lambda x: "Przeanalizowany" if x == "analyzed" else "Oczekuje")
    
    # Nagłówki w kolumnach (dodano 'Analiza AI')
    header_cols = st.columns([2, 3, 3, 1, 1, 1, 2])
    with header_cols[0]:
        st.markdown("<div style='text-align: center; font-weight: bold;'>Nazwa procesu</div>", unsafe_allow_html=True)
    with header_cols[1]:
        st.markdown("<div style='text-align: center; font-weight: bold;'>Opis</div>", unsafe_allow_html=True)
    with header_cols[2]:
        st.markdown("<div style='text-align: center; font-weight: bold;'>Analiza AI</div>", unsafe_allow_html=True)
    with header_cols[3]:
        st.markdown("<div style='text-align: center; font-weight: bold;'>Ocena</div>", unsafe_allow_html=True)
    with header_cols[4]:
        st.markdown("<div style='text-align: center; font-weight: bold;'>Data</div>", unsafe_allow_html=True)
    with header_cols[5]:
        st.markdown("<div style='text-align: center; font-weight: bold;'>Status</div>", unsafe_allow_html=True)
    with header_cols[6]:
        st.markdown("<div style='text-align: center; font-weight: bold;'>Akcje</div>", unsafe_allow_html=True)

    # Dodaj kolumnę Akcje (przyciski)
    for idx, row in df.iterrows():
        cols = st.columns([2, 3, 3, 1, 1, 1, 2])
        with cols[0]:
            st.markdown(f"<div style='text-align: left;'>{row['title']}</div>", unsafe_allow_html=True)
        with cols[1]:
            if row['OpisLong'] and len(row['OpisLong']) > 500:
                st.markdown(f"<div style='text-align: left;'>{row['OpisShort']}</div>", unsafe_allow_html=True)
                with st.expander("Pokaż więcej", expanded=False):
                    st.markdown(f"<div style='text-align: left;'>{row['OpisLong']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left;'>{row['OpisLong']}</div>", unsafe_allow_html=True)
        with cols[2]:
            if row['AILong'] and len(row['AILong']) > 500:
                st.markdown(f"<div style='text-align: left; white-space: pre-wrap;'>{row['AIShort']}</div>", unsafe_allow_html=True)
                with st.expander("Pokaż więcej", expanded=False):
                    st.markdown(f"<div style='text-align: left; white-space: pre-wrap;'>{row['AILong']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; white-space: pre-wrap;'>{row['AILong']}</div>", unsafe_allow_html=True)
        with cols[3]:
            st.markdown(f"<div style='text-align: center;'>{row['Ocena']}</div>", unsafe_allow_html=True)
        with cols[4]:
            st.markdown(f"<div style='text-align: center;'>{row['Data']}</div>", unsafe_allow_html=True)
        with cols[5]:
            st.markdown(f"<div style='text-align: center;'>{row['Status']}</div>", unsafe_allow_html=True)
        with cols[6]:
            colA, colB = st.columns(2)
            with colA:
                if st.button(f"Edytuj", key=f"edit_{row['id']}"):
                    st.session_state.current_process = processes[idx]
                    st.session_state.page = "edit_process"
                    st.rerun()
            with colB:
                if st.button(f"Usuń", key=f"delete_{row['id']}"):
                    supabase_client.soft_delete_process(row['id'])
                    st.success(f"Proces '{row['title']}' został usunięty.")
                    st.rerun()

def show_results():
    """Wyświetla wyniki analizy AI"""
    if not st.session_state.current_analysis:
        st.error("Brak danych analizy")
        if st.button("Powrót do dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        return
    
    analysis = st.session_state.current_analysis
    ai_results = analysis.get('ai_analysis', {})
    
    # Header z tytułem procesu
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader(f"Analiza: {analysis.get('title', 'Proces')}")
    
    with col2:
        if st.button("Powrót", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    
    st.markdown("---")
    
    # Główne metryki
    show_key_metrics(ai_results)
    
    # Rekomendacje
    show_recommendations(ai_results)
    
    # Plan wdrożenia  
    show_implementation_plan(ai_results)

def show_key_metrics(ai_results: Dict[str, Any]):
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

def show_recommendations(ai_results: Dict[str, Any]):
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

def show_implementation_plan(ai_results: Dict[str, Any]):
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

def show_user_processes():
    """Wyświetla procesy użytkownika - alias dla show_dashboard"""
    st.title("Moje Procesy")
    show_dashboard() 