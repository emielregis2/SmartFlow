"""
Komponent bocznego paska nawigacji dla SmartFlow.
"""
import streamlit as st

def show_sidebar():
    st.sidebar.title("SmartFlow")
    st.sidebar.markdown("---")
    st.sidebar.write("Witaj w aplikacji do analizy procesów biznesowych!")
    st.sidebar.markdown("---")
    st.sidebar.write("Wersja MVP") 