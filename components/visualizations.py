"""
Moduł wizualizacji dla SmartFlow.
"""
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from database.supabase_client import delete_process, get_user_processes

def show_dashboard():
    """Dashboard z listą procesów użytkownika"""
    st.subheader("Twoje procesy")
    
    # Przycisk dodania nowego procesu
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write(f"Zarządzaj swoimi przeanalizowanymi procesami")
    
    with col3:
        if st.button("Nowy proces", use_container_width=True, type="primary"):
            st.session_state.page = "new_process"
            st.rerun()
    
    # Pobierz procesy z bazy danych (przykład)
    user_id = st.session_state.user_data["id"] if st.session_state.user_data else None
    supabase = st.session_state.get("supabase")
    if user_id and supabase:
        processes = get_user_processes(supabase, user_id)
    else:
        processes = []
    
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
    """Lista procesów w formie tabeli"""
    st.markdown("---")
    
    for process in processes:
        col1, col2, col3 = st.columns([4, 1, 1])
        with col1:
            st.write(f"**{process.get('title', 'Proces')}** | Ocena: {process.get('potential_score', '-')}/10 | Data: {process.get('created_at', '-')}")
        with col2:
            if st.button(f"Edytuj", key=f"edit_{process['id']}"):
                st.session_state.page = "edit_process"
                st.session_state.edit_process_id = process["id"]
                st.rerun()
        with col3:
            if st.button(f"Usuń", key=f"delete_{process['id']}"):
                user_id = st.session_state.user_data["id"] if st.session_state.user_data else None
                supabase = st.session_state.get("supabase")
                if user_id and supabase:
                    success = delete_process(supabase, process["id"], user_id)
                    if success:
                        st.success("Proces został usunięty.")
                        st.rerun()
                    else:
                        st.error("Nie udało się usunąć procesu.")

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