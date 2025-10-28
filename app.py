import streamlit as st
from utils import load_css

st.set_page_config(
    page_title="Análisis de Pingüinos 🐧",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

st.title("Análisis de Pingüinos 🐧")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## Bienvenidos!
    Esta aplicación realiza un **análisis completo del dataset de pingüinos de Palmer Station**.
    Incluye todas las etapas de un flujo de datos:
    1. **Documentación:** explicación del dataset y objetivos del análisis.
                
    2. **ETL:** limpieza y preparación de datos.
                
    3. **EDA:** análisis exploratorio con gráficos interactivos.
                
    4. **Simulación Montecarlo:** estimaciones de probabilidad mediante simulación.
                
    Elegí una sección en el menú lateral para comenzar 👈
    """)

with col2:
    st.image("assets/penguinGIF.gif", width=300)


# --- Footer ---
st.markdown(
    """
    <div style="margin-top:150px;"> 
        <hr style="border:none; border-top:1px solid #444; margin-bottom:30px;"> 
        <div style="text-align:center; font-size:15px; margin-bottom:20px;">
            Desarrollado con ❤️ por <b>Ayelen Lecman</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# centrado de botones usando columnas
col1, col2, col3 = st.columns([3, 2, 3])

with col2:
    # fila horizontal centrada
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/ayelecman", use_container_width=True)
    with btn_col2:
        st.link_button("GitHub", "https://github.com/AyeLec", use_container_width=True)