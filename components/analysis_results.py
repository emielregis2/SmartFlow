"""
Komponent wyświetlania wyników analizy AI dla SmartFlow.
"""
import streamlit as st
from typing import Dict, Any

def show_analysis_results(results: Dict[str, Any]):
    st.subheader("Wyniki analizy AI")
    if not results:
        st.warning("Brak wyników do wyświetlenia.")
        return
    st.json(results) 