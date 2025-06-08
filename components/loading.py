"""
Komponent ekranu ładowania/progressu dla SmartFlow.
"""
import streamlit as st

def show_loading(message: str = "Analizuję proces..."):
    with st.spinner(message):
        st.write(":hourglass_flowing_sand: Proszę czekać...") 