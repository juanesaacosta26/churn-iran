# Hallazgos

Cada hallazgo en una línea, **con su cifra** y la figura/tabla que lo respalda.
Ianis: hallazgos de caracterización (bloque 2) y priorización (bloques 2 y 3). Juanes: relación (bloque 1) y modelos (bloque 2).

| # | Hallazgo | Cifra | Respaldo | Autor |
|---|---|---|---|---|
| 1 | Quejarse y estar inactivo son las dos señales más ligadas al abandono; las fallas de llamada casi no se relacionan con él. | Con queja abandona el 83 % frente al 10 % sin queja (r = 0.53); inactivo, 47 % frente a 5 % (r = 0.50); fallas de llamada r = −0.01. Base cruda, 3150 filas. | `reports/tablas/relacion_churn.csv`, `reports/tablas/tasa_por_categoria.csv`, notebook 03 (figuras 1 y 2) | Juanes |
| 2 | Dos pares de variables repiten casi la misma información, así que una de cada par sobra en la regresión logística. | `segundos_uso`–`frecuencia_llamadas` r = 0.95; `frecuencia_sms`–`valor_cliente` r = 0.92; `valor_cliente` tiene VIF 56 (base cruda) y R² = 0.98 frente al resto. | `reports/figures/correlaciones.png`, `reports/tablas/redundancias.csv`, `reports/tablas/vif.csv` | Juanes |
