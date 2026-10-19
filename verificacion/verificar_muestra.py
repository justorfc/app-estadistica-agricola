# verificar_muestra.py — Fase 2 del Lápiz y Algoritmo (verificación con Python)
# Ejecuta desde la raíz del repositorio:  .venv/bin/python verificacion/verificar_muestra.py
import pandas as pd

m = pd.read_csv("datos/muestra10.csv")      # 1. Leer las 10 parcelas asignadas
y = m["rendimiento"]                         # 2. Variable de interés (t/ha)

media = y.mean()                             # 3. Media aritmética
mediana = y.median()                         # 4. Mediana
var = y.var(ddof=1)                          # 5. Varianza muestral (divide entre n-1)
de = y.std(ddof=1)                           # 6. Desviación estándar muestral
cv = 100 * de / media                        # 7. Coeficiente de variación (%)
q1, q3 = y.quantile([0.25, 0.75])            # 8. Cuartiles (método tipo 7, igual que R)
ric = q3 - q1                                # 9. Rango intercuartílico
li, ls = q1 - 1.5 * ric, q3 + 1.5 * ric      # 10. Límites (vallas) de Tukey
atipicos = m.loc[(y < li) | (y > ls), "parcela"].tolist()

print(f"n = {len(y)}  media = {media:.3f}  mediana = {mediana:.3f}")
print(f"varianza = {var:.4f}  desv. est. = {de:.4f}  CV = {cv:.2f} %")
print(f"Q1 = {q1:.4f}  Q3 = {q3:.4f}  RIC = {ric:.4f}")
print(f"Límite inferior = {li:.4f}  Límite superior = {ls:.4f}  Atípicos: {atipicos}")
print("\nMedia por riego:")
print(m.groupby("riego")["rendimiento"].mean().round(3))   # 11. Media por grupo