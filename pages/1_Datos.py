"""Página 1: vista general de los datos."""
import pandas as pd
import streamlit as st

from src.eda import cargar_datos, valores_faltantes

st.set_page_config(page_title="Datos", page_icon="📋", layout="wide")
st.title("Datos de las parcelas")

df = cargar_datos("parcelas.csv")

# Dimensiones de la tabla
c1, c2 = st.columns(2)
c1.metric("Filas (parcelas)", df.shape[0])
c2.metric("Columnas (variables)", df.shape[1])

st.subheader("Tabla de parcelas")
st.dataframe(df, width="stretch")

# Clasificación: texto -> cualitativa; números -> cuantitativa
st.subheader("Tipo de cada variable")
tipos = pd.DataFrame({
    "variable": df.columns,
    "tipo": ["Cuantitativa" if pd.api.types.is_numeric_dtype(df[c]) else "Cualitativa"
             for c in df.columns],
    "tipo de dato": [str(t) for t in df.dtypes],
})
st.dataframe(tipos, width="stretch", hide_index=True)

st.subheader("Valores faltantes")
st.dataframe(valores_faltantes(df), width="stretch", hide_index=True)

st.download_button(
    "Descargar parcelas.csv",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="parcelas.csv",
    mime="text/csv",
)
