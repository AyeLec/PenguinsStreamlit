import streamlit as st
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Pingüinos 🐧", layout="wide")

# Dataset
penguins = sns.load_dataset("penguins").dropna(subset=["species", "bill_length_mm", "body_mass_g", "sex"])

st.title("Explorador de pingüinos 🐧")
st.write("Visualización interactiva de medidas corporales por especie.")

# Sidebar
st.sidebar.header("Filtros")
species = st.sidebar.selectbox("Elegí la especie", penguins["species"].unique())
df = penguins[penguins["species"] == species]

chart_type = st.sidebar.radio(
    "Tipo de gráfico",
    ["Dispersión pico vs masa", "Histograma de masa", "Boxplot de masa por sexo"]
)

# Main panel
if chart_type == "Dispersión pico vs masa":
    fig = px.scatter(
        df,
        x="bill_length_mm",
        y="body_mass_g",
        color="sex",
        title=f"Pico vs Masa corporal ({species})",
        labels={
            "bill_length_mm": "Longitud pico (mm)",
            "body_mass_g": "Masa corporal (g)",
            "sex": "Sexo"
        }
    )

elif chart_type == "Histograma de masa":
    fig = px.histogram(
        df,
        x="body_mass_g",
        nbins=20,
        color="sex",
        title=f"Distribución de masa corporal ({species})",
        labels={
            "body_mass_g": "Masa corporal (g)"
        }
    )

else:  # Boxplot
    fig = px.box(
        df,
        x="sex",
        y="body_mass_g",
        title=f"Masa corporal por sexo ({species})",
        labels={
            "sex": "Sexo",
            "body_mass_g": "Masa corporal (g)"
        },
        points="all"
    )

st.plotly_chart(fig, use_container_width=True)

st.subheader("Datos filtrados")
st.dataframe(df[["species","sex","bill_length_mm","bill_depth_mm","flipper_length_mm","body_mass_g"]])

