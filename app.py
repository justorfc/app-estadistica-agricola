"""Página de inicio de la app."""
import streamlit as st

from src.eda import cargar_metadatos

st.set_page_config(page_title="Estadística Agrícola", page_icon="🌱", layout="wide")

st.title("Estadística Aplicada con Python y R — Ingeniería Agrícola, Unisucre")

# Datos del estudiante y del conjunto de datos asignado
meta = cargar_metadatos()
with st.container(border=True):
    st.subheader("Ficha del estudiante")
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**Nombre:** {meta['nombre']}")
    c1.markdown(f"**Código:** {meta['codigo']}")
    c2.markdown(f"**Cultivo:** {meta['cultivo']}")
    c2.markdown(f"**Municipio:** {meta['municipio']}")
    c3.markdown(f"**N.º de parcelas:** {meta['n_parcelas']}")
    c3.markdown(f"**Huella:** `{meta['huella']}`")

st.markdown(
    "Esta aplicación permite explorar, de forma interactiva, los datos de un ensayo "
    "agrícola (parcelas, manejo del suelo y riego, rendimiento) y el clima mensual de la zona."
)
st.subheader("Páginas")
st.markdown(
    "- **Datos:** tabla de parcelas, tipos de variables, valores faltantes y descarga del CSV.\n"
    "- **EDA:** análisis exploratorio univariado, cualitativo y bivariado, con filtros.\n"
    "- **Regresión:** correlación y modelos de regresión (en construcción).\n"
    "- **Series de tiempo:** análisis del clima mensual (en construcción)."
)
