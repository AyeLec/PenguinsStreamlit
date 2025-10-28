import streamlit as st
import seaborn as sns
import numpy as np
import pandas as pd

st.set_page_config(page_title="Simulación Monte Carlo", layout="wide")

st.title("🎲 Simulación de Monte Carlo")

st.markdown("""
Este módulo te permite ingresar una **especie de pingüino** y una **característica específica**
(como la longitud del pico, la profundidad del pico, la longitud de la aleta o la masa corporal)
junto con un **valor objetivo**.

Luego, se realizan simulaciones de Monte Carlo para estimar la probabilidad de encontrar
un pingüino de esa especie con una característica cercana a ese valor en el conjunto de datos.
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

# Nos quedamos solo con columnas numéricas relevantes
feature_map = {
    "Longitud del pico (mm)": "bill_length_mm",
    "Profundidad del pico (mm)": "bill_depth_mm",
    "Longitud de la aleta (mm)": "flipper_length_mm",
    "Masa corporal (g)": "body_mass_g"
}

st.sidebar.header("Parámetros de simulación")

# elegir especie
species = st.sidebar.selectbox(
    "Elegí la especie",
    sorted(penguins["species"].unique())
)

# elegir variable / característica
feature_label = st.sidebar.selectbox(
    "Elegí la característica a evaluar",
    list(feature_map.keys())
)

feature_col = feature_map[feature_label]

# filtrar por especie
df_species = penguins[penguins["species"] == species]

# rango sugerido para el valor objetivo
col_min = float(df_species[feature_col].min())
col_max = float(df_species[feature_col].max())

valor_objetivo = st.sidebar.number_input(
    f"Valor objetivo para {feature_label}",
    min_value=col_min,
    max_value=col_max,
    value=float(df_species[feature_col].mean()),
    step=0.1
)

# tolerancia: qué tan cerca consideramos "cumple"
tolerancia = st.sidebar.number_input(
    "Tolerancia (±)",
    min_value=0.1,
    max_value=(col_max - col_min),
    value=1.0,
    step=0.1,
    help="Ej: si valor objetivo=45 y tolerancia=1, contamos valores entre 44 y 46."
)

# cantidad de simulaciones Monte Carlo
n_sim = st.sidebar.number_input(
    "Número de simulaciones",
    min_value=100,
    max_value=100000,
    value=5000,
    step=1000
)

st.sidebar.caption("Apretá el botón para correr la simulación 👇")
run = st.sidebar.button("Simular")

st.subheader("Descripción del experimento")
st.write(f"""
Queremos estimar:  
> ¿Cuál es la probabilidad de que un pingüino **{species}** tenga  
> **{feature_label} ≈ {valor_objetivo:.2f}** (± {tolerancia})?

Para eso:
1. Tomamos la distribución real de `{feature_label}` para la especie elegida.
2. Hacemos {n_sim} muestreos aleatorios con reemplazo (Monte Carlo).
3. Medimos en qué proporción de simulaciones el valor cae dentro del rango permitido.
""")

if run:
    # =============================================================================
    # MONTE CARLO
    # =============================================================================

    # tomamos la serie numérica real de esa característica en esa especie
    data = df_species[feature_col].values

    # simulamos n_sim valores sacados de esa distribución empírica
    simulaciones = np.random.choice(data, size=int(n_sim), replace=True)

    # chequeamos cuántos caen dentro del rango objetivo ± tolerancia
    lower = valor_objetivo - tolerancia
    upper = valor_objetivo + tolerancia
    cumple = ((simulaciones >= lower) & (simulaciones <= upper)).mean()

    prob_pct = cumple * 100.0

    st.markdown("---")
    st.subheader("📌 Resultado")
    st.write(
        f"La probabilidad estimada de observar un pingüino **{species}** "
        f"con `{feature_label}` entre **{lower:.2f} y {upper:.2f}** "
        f"es aproximadamente **{prob_pct:.2f}%**."
    )

    st.markdown("### Distribución simulada vs rango objetivo")
    st.caption("Te mostramos la distribución de los valores simulados para que veas dónde cae tu objetivo.")

    # histograma usando st.pyplot rápido
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.hist(simulaciones, bins=30, edgecolor="white")
    ax.axvspan(lower, upper, color="red", alpha=0.2, label="Rango objetivo")
    ax.set_xlabel(feature_label)
    ax.set_ylabel("Frecuencia (simulada)")
    ax.legend()
    st.pyplot(fig)

    st.markdown("### Datos de referencia (muestra real de la especie seleccionada)")
    st.dataframe(
        df_species[
            ["species", "sex", "bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]
        ],
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Elegí los parámetros en la barra lateral y apretá **Simular**.")
