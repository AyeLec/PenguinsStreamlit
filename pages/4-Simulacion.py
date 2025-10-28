import streamlit as st
import seaborn as sns
import numpy as np
import plotly.graph_objects as go
from utils import load_css

# --- CONFIG PÁGINA ---
st.set_page_config(
    page_title="Simulación Monte Carlo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS GLOBAL ---
load_css()

st.title("Simulación Monte Carlo")

st.markdown("""
Esta herramienta estima, de manera empírica, **qué tan probable es observar un pingüino con determinadas características físicas**.

1. Elegí una especie.
2. Elegí una variable morfológica (pico, aleta, peso).
3. Definí un valor objetivo y una tolerancia.
4. Calculamos por remuestreo (Monte Carlo) qué tan frecuente es ver algo así en esa especie.
""")

st.markdown("---")

# ======================
# Datos base
# ======================
if "penguins_clean" in st.session_state:
    penguins = st.session_state["penguins_clean"].copy()
else:
    penguins = sns.load_dataset("penguins").dropna().copy()
    penguins.columns = penguins.columns.str.lower().str.strip()

# Map de nombres lindos -> columnas reales
feature_map = {
    "Longitud del pico (mm)": "bill_length_mm",
    "Profundidad del pico (mm)": "bill_depth_mm",
    "Longitud de la aleta (mm)": "flipper_length_mm",
    "Masa corporal (g)": "body_mass_g",
}

# ----------------------
# Sidebar (parámetros)
# ----------------------
st.sidebar.header("Parámetros de simulación")

species = st.sidebar.selectbox(
    "Especie",
    sorted(penguins["species"].unique())
)

feature_label = st.sidebar.selectbox(
    "Variable a evaluar",
    list(feature_map.keys())
)
feature_col = feature_map[feature_label]

df_species = penguins[penguins["species"] == species]

col_min = float(df_species[feature_col].min())
col_max = float(df_species[feature_col].max())
col_mean = float(df_species[feature_col].mean())

valor_objetivo = st.sidebar.number_input(
    f"Valor objetivo para {feature_label}",
    min_value=col_min,
    max_value=col_max,
    value=col_mean,
    step=0.1,
)

# Mostrar rango permitido
st.sidebar.caption(
    f"📏 Rango válido para {feature_label} en {species}: "
    f"**{col_min:.2f} – {col_max:.2f}**"
)

tolerancia = st.sidebar.number_input(
    "Tolerancia (±)",
    min_value=0.1,
    max_value=(col_max - col_min),
    value=1.0 if feature_col != "body_mass_g" else 50.0,
    step=0.1,
    help=(
        "Ejemplo: si el valor objetivo es 45 y la tolerancia es 1, "
        "el rango evaluado va de 44 a 46."
    ),
)

n_sim = st.sidebar.number_input(
    "Número de simulaciones",
    min_value=100,
    max_value=100000,
    value=5000,
    step=1000,
    help="Más simulaciones = estimación más estable, pero más lenta."
)

run = st.sidebar.button("Calcular probabilidad")

# ======================
# Descripción rápida
# ======================
st.subheader("Planteo del experimento")

lower = valor_objetivo - tolerancia
upper = valor_objetivo + tolerancia

st.markdown(
    f"""        
    **¿Qué probabilidad hay de observar un pingüino `{species}` con `{feature_label}` entre `{lower:.2f}` y `{upper:.2f}`?**
    
    Donde:
    - Valor objetivo: **{valor_objetivo:.2f}**
    - Tolerancia: **± {tolerancia:.2f}**
    - Rango evaluado: **[{lower:.2f}, {upper:.2f}]**
    - Simulaciones Monte Carlo: **{n_sim:.0f}**
    """
)

# ======================
# Simulación
# ======================
if run:
    data = df_species[feature_col].values

    # Monte Carlo: remuestreo con reemplazo
    simulaciones = np.random.choice(data, size=int(n_sim), replace=True)

    cumple_mask = (simulaciones >= lower) & (simulaciones <= upper)
    prob_pct = cumple_mask.mean() * 100.0

    st.markdown("---")
    st.subheader("Resultado")

    st.metric(
        label="Probabilidad estimada",
        value=f"{prob_pct:.2f} %",
        help="Porcentaje de simulaciones que caen en el rango definido."
    )

    # Histograma interactivo con banda de rango objetivo
    fig = go.Figure()

    # Histograma de las simulaciones
    fig.add_trace(go.Histogram(
        x=simulaciones,
        nbinsx=30,
        name="Simulaciones",
        opacity=0.8
    ))

    # Banda vertical para el rango objetivo
    fig.add_vrect(
        x0=lower,
        x1=upper,
        fillcolor="red",
        opacity=0.2,
        layer="below",
        line_width=0,
        annotation_text="Rango objetivo",
        annotation_position="top left"
    )

    fig.update_layout(
        title=f"Distribución simulada de {feature_label} en {species}",
        xaxis_title=feature_label,
        yaxis_title="Frecuencia simulada",
        barmode="overlay",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Nota interpretativa
    st.caption(
        "El histograma muestra valores simulados tomando como referencia la distribución real de esa especie. "
        "La banda roja marca el rango que definiste como 'aceptable'. "
        "La métrica indica qué tan común es ver pingüinos en ese rango."
    )

else:
    st.info("Elegí los parámetros en la barra lateral y apretá **Calcular probabilidad** para correr la simulación.")
