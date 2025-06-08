"""
Komponent listy procesów dla SmartFlow.
"""
import streamlit as st
from typing import List, Dict, Any

def show_process_list(processes: List[Dict[str, Any]]):
    st.subheader("Lista procesów")
    if not processes:
        st.info("Brak procesów do wyświetlenia.")
        return
    for process in processes:
        st.markdown(f"**{process.get('title', 'Proces')}** - {process.get('status', 'brak statusu')}") 