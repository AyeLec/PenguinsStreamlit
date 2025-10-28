from pathlib import Path
import streamlit as st

def load_css():
    """
    Inyecta el CSS global styles.css en la página actual de Streamlit.
    Llamar a esta función al inicio de cada page.
    """
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.sidebar.warning("⚠️ styles.css no encontrado")