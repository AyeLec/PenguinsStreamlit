import streamlit as st
from utils import load_css

st.set_page_config(
    page_title="Análisis de Pingüinos 🐧",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

st.title("Análisis de Pingüinos 🐧")
st.markdown(
    """
    ## Bienvenida

    Esta aplicación realiza un **análisis completo del dataset de pingüinos de Palmer Station**.
    Incluye todas las etapas de un flujo de datos:

    1. **ETL (Extract, Transform, Load):** limpieza y preparación de datos.  
    2. **EDA (Exploratory Data Analysis):** análisis exploratorio con gráficos interactivos.  
    3. **Estadísticas descriptivas:** métricas resumen por especie y sexo.  
    4. **Documentación:** explicación del dataset y objetivos del análisis.

    Elegí una sección en el menú lateral para comenzar 👈
    """
)
