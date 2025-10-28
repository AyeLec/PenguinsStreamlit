import streamlit as st
import plotly.express as px
import seaborn as sns

from utils import load_css

load_css()

st.set_page_config(page_title="EDA", layout="wide")

st.title("📊 Análisis Exploratorio de Datos (EDA)")

if "penguins_clean" in st.session_state:
    penguins = st.session_state["penguins_clean"]
else:
    penguins = sns.load_dataset("penguins").dropna()

st.sidebar.header("Filtros")
species = st.sidebar.selectbox("Elegí la especie", sorted(penguins["species"].unique()))
df = penguins[penguins["species"] == species]

chart_type = st.sidebar.radio(
    "Tipo de gráfico",
    ["Dispersión pico vs masa", "Histograma de masa", "Boxplot por sexo"]
)

if chart_type == "Dispersión pico vs masa":
    fig = px.scatter(df, x="bill_length_mm", y="body_mass_g", color="sex",
                     title=f"Longitud del pico vs masa corporal ({species})")
elif chart_type == "Histograma de masa":
    fig = px.histogram(df, x="body_mass_g", color="sex", nbins=20,
                       title=f"Distribución de masa corporal ({species})")
else:
    fig = px.box(df, x="sex", y="body_mass_g", points="all",
                 title=f"Masa corporal por sexo ({species})")

st.plotly_chart(fig, use_container_width=True)
st.dataframe(df.head(), use_container_width=True)
