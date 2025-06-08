"""
SmartFlow - Aplikacja do analizy procesów biznesowych z wykorzystaniem AI.
"""
import streamlit as st
from components import auth, forms, visualizations

# Konfiguracja strony
st.set_page_config(
    page_title="SmartFlow",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicjalizacja stanu sesji
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

# Główna logika routingu
def main():
    # Stylowanie
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Routing
    if st.session_state.page == 'login':
        auth.show_auth_page()
    
    elif st.session_state.page == 'profile':
        forms.show_profile_form()
    
    elif st.session_state.page == 'dashboard':
        visualizations.show_dashboard()
    
    elif st.session_state.page == 'new_process':
        forms.show_process_form()
    
    elif st.session_state.page == 'results':
        visualizations.show_results()

if __name__ == "__main__":
    main() 