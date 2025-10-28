import streamlit as st

st.set_page_config(page_title="Documentación", layout="wide")

st.title("📚 Documentación del proyecto")

st.markdown("""
### Sobre el dataset
El dataset de pingüinos de *Palmer Station* proviene de la Antártida e incluye medidas biométricas:
- Longitud y profundidad del pico
- Longitud de la aleta
- Masa corporal
- Sexo y especie

### Objetivo
Realizar un **análisis exploratorio de datos (EDA)** para:
- Explorar diferencias morfológicas entre especies.
- Analizar patrones según sexo.
- Practicar visualización y análisis estadístico con Python.

### Tecnologías utilizadas
- **Streamlit:** interfaz web interactiva
- **Plotly:** gráficos dinámicos
- **Seaborn / Pandas:** manejo y limpieza de datos

---
Desarrollado por **Ayelén Lecman**, abogada y analista de datos apasionada por el cruce entre derecho, ciencia y tecnología ⚖️💻
""")
