"""Página 2: análisis exploratorio de datos."""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from src.eda import atipicos_iqr, cargar_datos, resumen_numerico

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")
st.title("Análisis exploratorio de datos (EDA)")

df = cargar_datos("parcelas.csv")

# Etiquetas con unidades para los ejes
UNIDADES = {
    "dosis_N": "Dosis de N (kg/ha)",
    "lamina_riego": "Lámina de riego (mm)",
    "materia_organica": "Materia orgánica (%)",
    "ph": "pH",
    "rendimiento": "Rendimiento (t/ha)",
}
numericas = list(UNIDADES)

# --- Filtros en la barra lateral ---
st.sidebar.header("Filtros")
suelos = st.sidebar.multiselect("Suelo", sorted(df["suelo"].unique()),
                                default=sorted(df["suelo"].unique()))
riegos = st.sidebar.multiselect("Riego", sorted(df["riego"].unique()),
                                default=sorted(df["riego"].unique()))
dff = df[df["suelo"].isin(suelos) & df["riego"].isin(riegos)]
st.sidebar.caption(f"Parcelas seleccionadas: {len(dff)}")

if dff.empty:
    st.warning("No hay parcelas con los filtros seleccionados.")
    st.stop()

tab_uni, tab_cual, tab_biv, tab_m10 = st.tabs(
    ["Univariado", "Cualitativo", "Bivariado",
     "Muestra de 10 parcelas (verificación del cálculo a mano)"])

# --- a) Univariado ---
with tab_uni:
    var = st.selectbox("Variable numérica", numericas,
                       format_func=lambda v: UNIDADES[v])
    st.dataframe(resumen_numerico(dff[var]).to_frame("valor").round(3))

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        sns.histplot(dff[var].dropna(), kde=True, ax=ax)  # histograma + densidad
        ax.set_xlabel(UNIDADES[var])
        ax.set_ylabel("Frecuencia (n.º de parcelas)")
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        sns.boxplot(y=dff[var], ax=ax)
        ax.set_ylabel(UNIDADES[var])
        st.pyplot(fig)

    inf, sup, atip = atipicos_iqr(dff[var])
    st.markdown(f"**Vallas de Tukey:** [{inf:.3f}, {sup:.3f}]")
    if atip.empty:
        st.success("No hay parcelas atípicas en esta variable.")
    else:
        tabla = dff.loc[atip.index, ["parcela", var]]
        st.write(f"Parcelas atípicas ({len(tabla)}):")
        st.dataframe(tabla, hide_index=True)

# --- b) Cualitativo ---
with tab_cual:
    for var in ["suelo", "riego"]:
        st.subheader(var.capitalize())
        abs_ = dff[var].value_counts()
        tabla = pd.DataFrame({
            var: abs_.index,
            "frecuencia absoluta": abs_.values,
            "frecuencia relativa (%)": (abs_.values / abs_.sum() * 100).round(2),
        })
        c1, c2 = st.columns(2)
        c1.dataframe(tabla, hide_index=True)
        fig, ax = plt.subplots()
        sns.barplot(x=abs_.index, y=abs_.values, ax=ax)
        ax.set_xlabel(var.capitalize())
        ax.set_ylabel("Número de parcelas")
        c2.pyplot(fig)

# --- c) Bivariado ---
with tab_biv:
    c1, c2 = st.columns(2)
    for col, var in zip([c1, c2], ["suelo", "riego"]):
        fig, ax = plt.subplots()
        sns.boxplot(data=dff, x=var, y="rendimiento", ax=ax)
        ax.set_xlabel(var.capitalize())
        ax.set_ylabel(UNIDADES["rendimiento"])
        col.pyplot(fig)

    x = st.selectbox("Variable X", [v for v in numericas if v != "rendimiento"],
                     format_func=lambda v: UNIDADES[v])
    fig, ax = plt.subplots()
    sns.scatterplot(data=dff, x=x, y="rendimiento", hue="riego", ax=ax)
    ax.set_xlabel(UNIDADES[x])
    ax.set_ylabel(UNIDADES["rendimiento"])
    st.pyplot(fig)

    st.subheader("Correlación de Pearson")
    corr = dff[numericas].corr(method="pearson")
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)

# --- d) Muestra de 10 parcelas ---
with tab_m10:
    m10 = cargar_datos("muestra10.csv")
    st.dataframe(m10, hide_index=True)
    st.markdown("**Resumen del rendimiento (t/ha)**")
    st.dataframe(resumen_numerico(m10["rendimiento"]).to_frame("valor").round(3))
    inf, sup, atip = atipicos_iqr(m10["rendimiento"])
    st.markdown(f"**Vallas de Tukey:** inferior = {inf:.3f}, superior = {sup:.3f}")
    if atip.empty:
        st.success("No hay atípicos en la muestra.")
    else:
        st.dataframe(m10.loc[atip.index], hide_index=True)
    st.markdown("**Media del rendimiento (t/ha) por riego**")
    st.dataframe(m10.groupby("riego")["rendimiento"].mean().round(3)
                 .rename("media (t/ha)").to_frame())
