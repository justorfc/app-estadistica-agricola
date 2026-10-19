# verificar_muestra.R — Fase 2 del Lápiz y Algoritmo (verificación con R)
# En Posit Cloud: sube datos/muestra10.csv al proyecto y ejecuta este script.
m <- read.csv("muestra10.csv")              # 1. Leer las 10 parcelas asignadas
y <- m$rendimiento                           # 2. Variable de interés (t/ha)

media    <- mean(y)                          # 3. Media
mediana  <- median(y)                        # 4. Mediana
varianza <- var(y)                           # 5. Varianza muestral (n-1)
de       <- sd(y)                            # 6. Desviación estándar
cv       <- 100 * de / media                 # 7. CV (%)
q        <- quantile(y, c(0.25, 0.75), type = 7)  # 8. Cuartiles tipo 7
ric      <- q[2] - q[1]                      # 9. Rango intercuartílico
li <- q[1] - 1.5 * ric; ls <- q[2] + 1.5 * ric   # 10. Vallas de Tukey

cat("n =", length(y), " media =", round(media, 3), " mediana =", round(mediana, 3), "\n")
cat("varianza =", round(varianza, 4), " desv. est. =", round(de, 4), " CV =", round(cv, 2), "%\n")
cat("Q1 =", round(q[1], 4), " Q3 =", round(q[2], 4), " RIC =", round(ric, 4), "\n")
cat("Lím. inf. =", round(li, 4), " Lím. sup. =", round(ls, 4), "\n")
cat("Atípicos:", m$parcela[y < li | y > ls], "\n")
print(tapply(y, m$riego, mean))              # 11. Media por riego
boxplot(y, horizontal = TRUE, main = "Rendimiento (t/ha) - muestra de 10 parcelas")