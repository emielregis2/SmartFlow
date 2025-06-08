"""
Komponent nagłówka dla SmartFlow.
"""
import streamlit as st

def show_header():
    st.markdown("""
    <h1 style='text-align: left; color: #2B3A55;'>
        🚀 SmartFlow <span style='font-size: 0.6em; color: #4F8A8B;'>AI dla procesów biznesowych</span>
    </h1>
    """, unsafe_allow_html=True)
    st.markdown("---") 