import streamlit as st
import seaborn as sns
import pandas as pd
import plotly.express as px

from utils import load_css

load_css()

st.set_page_config(page_title="Estadísticas descriptivas", layout="wide")

st.title("📈 Estadísticas descriptivas")

penguins = sns.load_dataset("penguins").dropna()

st.markdown("### Resumen numérico por especie y sexo")
group_stats = (
    penguins
    .groupby(["species", "sex"])
    .agg({
        "bill_length_mm": ["mean", "std"],
        "bill_depth_mm": ["mean", "std"],
        "flipper_length_mm": ["mean", "std"],
        "body_mass_g": ["mean", "std"]
    })
    .round(2)
)
st.dataframe(group_stats, use_container_width=True)

st.markdown("### Boxplot de masa corporal por especie")
fig = px.box(penguins, x="species", y="body_mass_g", color="species",
             points="all", title="Comparación de masa corporal entre especies")
st.plotly_chart(fig, use_container_width=True)
