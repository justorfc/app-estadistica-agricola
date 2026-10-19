# App de Estadística Aplicada con Python y R — Ingeniería Agrícola (Unisucre)

**Estudiante:** Justo Fuentes
**Código:** 6820995  ·  **Grupo:** 1
**Cultivo asignado:** Ñame  ·  **Municipio:** Sincelejo  ·  **Huella:** 287369BC
**Docente:** Justo Fuentes  ·  **Semestre:** 2026-2

## Descripción
App de Streamlit para el análisis estadístico de parcelas agrícolas.
Páginas: Inicio · Datos · EDA · Regresión (próximamente) · Series de tiempo (próximamente).

## Cómo ejecutarla
1. Abrir el repositorio en un Codespace.
2. `python -m venv .venv && .venv/bin/pip install -r requirements.txt`
3. `.venv/bin/streamlit run app.py`

## Hallazgos del EDA
Tamaño de la muestra: n = 10
¿Existe alg+un valopr atípico?
A simple vista la parcela P045 presenta un rendimiento de 29.77, considerablemente superior al resto cuyos rendimientos se encuentran entre 12.66 y 17.88

PREDICCIÓN: P045 popdría ser un atípico superior

CV 30.79
