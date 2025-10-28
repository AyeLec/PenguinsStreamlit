import streamlit as st
import pandas as pd
import seaborn as sns
import io
from utils import load_css

# ⚙ Config de la página: tiene que ir antes de cualquier output visual
st.set_page_config(page_title="ETL", layout="wide", initial_sidebar_state="expanded")

# 🎨 estilos globales
load_css()

st.title("🧹 ETL - Limpieza y preparación de datos")

st.markdown("""
En esta etapa realizamos el proceso **ETL (Extract, Transform, Load)**:

- **Extract:** se obtienen los datos del dataset `penguins` de Seaborn.
- **Transform:** se eliminan valores faltantes, se renombran columnas y se estandarizan formatos.
- **Load:** se genera un DataFrame listo para el análisis posterior.
""")

# --- EXTRACT ---
penguins = sns.load_dataset("penguins")

st.subheader("📥 Datos originales (primeras filas)")
st.dataframe(penguins.head(), use_container_width=True)

# --- TRANSFORM ---
penguins_clean = (
    penguins
    .dropna()
    .rename(columns=lambda x: x.strip().lower())
)

st.subheader("🧼 Datos limpios (primeras filas)")
st.dataframe(penguins_clean.head(), use_container_width=True)

# --- LOAD / RESUMEN DEL PROCESO ---
st.subheader("📦 Resumen del proceso ETL")
col_a, col_b = st.columns(2)
with col_a:
    st.metric("Filas originales", penguins.shape[0])
with col_b:
    st.metric("Filas después de limpieza", penguins_clean.shape[0])

st.success("Datos listos para el análisis exploratorio ✅")

# Guardamos el dataset limpio para que lo usen otras páginas
st.session_state["penguins_clean"] = penguins_clean

st.markdown("---")

# =========================
# 🧠 RESUMEN TÉCNICO DEL DATAFRAME LIMPIO
# =========================

st.subheader("🔍 Resumen técnico del dataset limpio")

# 1. info() (tipos de datos, nulos)
buffer = io.StringIO()
penguins_clean.info(buf=buffer)
info_str = buffer.getvalue()

st.markdown("**Estructura de columnas (`df.info()`)**")
st.code(info_str, language="text")

# 2. describe() (estadísticas numéricas)
st.markdown("**Estadísticas descriptivas numéricas (`df.describe()`)**")
st.dataframe(
    penguins_clean.describe().round(2),
    use_container_width=True
)

# 3. valores únicos en variables categóricas
st.markdown("**Distribución de variables categóricas**")

categorical_cols = ["species", "island", "sex"]
for col in categorical_cols:
    if col in penguins_clean.columns:
        st.markdown(f"- Columna: `{col}`")
        st.write(penguins_clean[col].value_counts(dropna=False))

st.caption("Este resumen es clave para entender con qué datos vamos a trabajar en el resto del análisis.")
