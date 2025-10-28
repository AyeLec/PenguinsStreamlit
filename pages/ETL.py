import streamlit as st
import pandas as pd
import seaborn as sns

st.set_page_config(page_title="ETL", layout="wide")

st.title("🧹 ETL - Limpieza y preparación de datos")

st.markdown("""
En esta etapa realizamos el proceso **ETL (Extract, Transform, Load)**:
- **Extract:** se obtienen los datos del dataset `penguins` de Seaborn.
- **Transform:** se eliminan valores faltantes, se renombran columnas y se estandarizan formatos.
- **Load:** se genera un DataFrame listo para el análisis.
""")

# --- Extract
penguins = sns.load_dataset("penguins")
st.subheader("Datos originales (primeras filas)")
st.dataframe(penguins.head())

# --- Transform
penguins_clean = (
    penguins
    .dropna()
    .rename(columns=lambda x: x.strip().lower())
)
st.subheader("Datos limpios (primeras filas)")
st.dataframe(penguins_clean.head())

# --- Load
st.subheader("Resumen del proceso ETL")
st.write(f"Filas originales: {penguins.shape[0]}")
st.write(f"Filas después de limpieza: {penguins_clean.shape[0]}")

st.success("Datos listos para el análisis exploratorio ✅")

st.session_state["penguins_clean"] = penguins_clean
