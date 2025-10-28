import streamlit as st
import seaborn as sns
import plotly.express as px
from utils import load_css

# --- CONFIG PÁGINA ---
st.set_page_config(
    page_title="EDA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS GLOBAL ---
load_css()

st.title("📊 Análisis Exploratorio de Datos (EDA)")

# ======================
# CARGA DEL DATASET
# ======================
if "penguins_clean" in st.session_state:
    penguins = st.session_state["penguins_clean"].copy()
else:
    penguins = (
        sns.load_dataset("penguins")
        .dropna()
        .rename(columns=lambda c: c.strip().lower())
    )

penguins.columns = penguins.columns.str.strip().str.lower()

st.markdown("### Panorama general (todas las especies)")
st.caption("Distribuciones y relaciones morfológicas entre especies de pingüinos.")

# ======================
# SECCIÓN A1: Masa corporal por especie (boxplot)
# ======================
fig_box_all = px.box(
    penguins,
    x="species",
    y="body_mass_g",
    color="species",
    points="all",
    title="Masa corporal por especie",
    labels={
        "species": "Especie",
        "body_mass_g": "Masa corporal (g)"
    }
)
st.plotly_chart(fig_box_all, use_container_width=True)

# ======================
# SECCIÓN A2: Longitud de aleta vs masa corporal
# ======================
fig_scatter_flipper_mass = px.scatter(
    penguins,
    x="flipper_length_mm",
    y="body_mass_g",
    color="species",
    symbol="sex",
    hover_data=["island"],
    title="Aleta vs Masa corporal",
    labels={
        "flipper_length_mm": "Longitud de aleta (mm)",
        "body_mass_g": "Masa corporal (g)",
        "species": "Especie",
        "sex": "Sexo"
    }
)
st.plotly_chart(fig_scatter_flipper_mass, use_container_width=True)

# ======================
# SECCIÓN A3: Longitud de pico vs masa corporal
# ======================
fig_scatter_bill_mass = px.scatter(
    penguins,
    x="bill_length_mm",
    y="body_mass_g",
    color="species",
    symbol="sex",
    hover_data=["bill_depth_mm", "island"],
    title="Longitud de pico vs Masa corporal",
    labels={
        "bill_length_mm": "Longitud de pico (mm)",
        "body_mass_g": "Masa corporal (g)",
        "species": "Especie",
        "sex": "Sexo"
    }
)
st.plotly_chart(fig_scatter_bill_mass, use_container_width=True)

# ======================
# SECCIÓN A4: Matriz de correlación
# ======================

corr = penguins.select_dtypes("number").corr().round(2)

fig_corr = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Matriz de correlación entre variables numéricas",
    labels=dict(color="Correlación"),
)

st.plotly_chart(fig_corr, use_container_width=True)

st.caption(
    "Una correlación positiva (rojo) indica que las variables aumentan juntas; "
    "una correlación negativa (azul) indica que cuando una aumenta, la otra disminuye."
)

# ─────────────────────────────────
st.markdown("---")
# ─────────────────────────────────

# ======================
# SECCIÓN B: Exploración por especie
# ======================
st.markdown("### Zoom por especie")
st.caption("Elegí una especie para ver su distribución interna y diferencias por sexo.")

# Sidebar: solo para esta parte
st.sidebar.header("Filtro especie")
species = st.sidebar.selectbox(
    "Especie a analizar",
    sorted(penguins["species"].unique())
)

df_species = penguins[penguins["species"] == species]

# Layout con dos gráficos lado a lado
col_b1, col_b2 = st.columns(2)

# B1: Pico vs masa (dentro de la especie seleccionada)
with col_b1:
    fig_species_bill_mass = px.scatter(
        df_species,
        x="bill_length_mm",
        y="body_mass_g",
        color="sex",
        hover_data=["bill_depth_mm", "flipper_length_mm", "island"],
        title=f"Longitud de pico vs Masa corporal ({species})",
        labels={
            "bill_length_mm": "Longitud de pico (mm)",
            "body_mass_g": "Masa corporal (g)",
            "sex": "Sexo"
        }
    )
    st.plotly_chart(fig_species_bill_mass, use_container_width=True)

# B2: Aleta vs masa (dentro de la especie seleccionada)
with col_b2:
    fig_species_flipper_mass = px.scatter(
        df_species,
        x="flipper_length_mm",
        y="body_mass_g",
        color="sex",
        hover_data=["bill_length_mm", "bill_depth_mm", "island"],
        title=f"Aleta vs Masa corporal ({species})",
        labels={
            "flipper_length_mm": "Longitud de aleta (mm)",
            "body_mass_g": "Masa corporal (g)",
            "sex": "Sexo"
        }
    )
    st.plotly_chart(fig_species_flipper_mass, use_container_width=True)

# Histograma de masa corporal por sexo en esa especie
fig_hist_species = px.histogram(
    df_species,
    x="body_mass_g",
    color="sex",
    nbins=20,
    title=f"Distribución de masa corporal ({species})",
    labels={
        "body_mass_g": "Masa corporal (g)",
        "sex": "Sexo"
    }
)
st.plotly_chart(fig_hist_species, use_container_width=True)
