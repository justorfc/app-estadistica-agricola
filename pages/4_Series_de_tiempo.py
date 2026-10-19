"""Página 4: series de tiempo (en construcción)."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from src.eda import cargar_datos

st.set_page_config(page_title="Series de tiempo", page_icon="🕒")
st.title("Series de tiempo")
st.info("🚧 Página en construcción. Próximamente encontrarás aquí:")
st.markdown(
    "- Componentes de una serie\n- Descomposición\n- Promedios móviles\n- Pronóstico"
)

# Vista previa: precipitación mensual
st.subheader("Vista previa: precipitación mensual")
clima = cargar_datos("clima_mensual.csv")
clima["fecha"] = pd.to_datetime(clima["fecha"])
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=clima, x="fecha", y="precipitacion_mm", ax=ax)
ax.set_xlabel("Fecha (mes)")
ax.set_ylabel("Precipitación (mm/mes)")
st.pyplot(fig)
