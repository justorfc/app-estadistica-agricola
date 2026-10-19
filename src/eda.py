"""Funciones de análisis exploratorio de datos (EDA) para la app."""
import json
from pathlib import Path

import pandas as pd
import streamlit as st

# Carpeta datos/ ubicada junto a la carpeta src/
CARPETA_DATOS = Path(__file__).resolve().parent.parent / "datos"


@st.cache_data
def cargar_datos(nombre_csv):
    """Lee un archivo CSV de la carpeta datos/ y devuelve un DataFrame.

    Parámetros: nombre_csv (str), por ejemplo "parcelas.csv".
    El resultado se guarda en caché para no releer el archivo en cada interacción.
    """
    return pd.read_csv(CARPETA_DATOS / nombre_csv)


def cargar_metadatos():
    """Lee datos/metadatos.json y devuelve un diccionario con la información del estudiante."""
    with open(CARPETA_DATOS / "metadatos.json", encoding="utf-8") as f:
        return json.load(f)


def resumen_numerico(serie):
    """Calcula estadísticos descriptivos de una serie numérica.

    Devuelve un pd.Series con: n, media, mediana, desviación estándar muestral
    (ddof=1), CV %, mínimo, Q1, Q3, máximo, RIC (Q3 - Q1) y asimetría.
    Los valores faltantes se ignoran.
    """
    s = pd.to_numeric(serie, errors="coerce").dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    media = s.mean()
    desv = s.std(ddof=1)  # ddof=1: desviación muestral
    return pd.Series({
        "n": int(s.count()),
        "media": media,
        "mediana": s.median(),
        "desviación estándar": desv,
        "CV (%)": desv / media * 100 if media != 0 else float("nan"),
        "mínimo": s.min(),
        "Q1": q1,
        "Q3": q3,
        "máximo": s.max(),
        "RIC": q3 - q1,
        "asimetría": s.skew(),
    })


def valores_faltantes(df):
    """Devuelve una tabla con la cantidad y el porcentaje de valores faltantes por columna."""
    faltan = df.isna().sum()
    return pd.DataFrame({
        "variable": df.columns,
        "faltantes": faltan.values,
        "porcentaje (%)": (faltan.values / len(df) * 100).round(2),
    })


def atipicos_iqr(serie):
    """Detecta atípicos con las vallas de Tukey (1.5·RIC).

    Devuelve (valla_inferior, valla_superior, atipicos), donde atipicos es la
    serie con los valores (y su índice) fuera de las vallas.
    """
    s = pd.to_numeric(serie, errors="coerce").dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    ric = q3 - q1
    inf, sup = q1 - 1.5 * ric, q3 + 1.5 * ric
    return inf, sup, s[(s < inf) | (s > sup)]
