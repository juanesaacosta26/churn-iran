# Bitácora de decisiones

Toda decisión que cambie cifras o variables se anota aquí **en la reunión de cierre de cada bloque**,
con fecha, quién la propuso y por qué. El informe final cita esta bitácora en "Metodología".

| Fecha | Decisión | Por qué | Quién |
|---|---|---|---|
| 2026-10-11 | Se usa el CSV original de UCI (separado por comas) como única fuente en `data/raw/`. | El CSV del proyecto con `;` es la misma base exportada desde Excel. | Repositorio |
| 2026-10-28 | Se ajusta el calendario: presentación el viernes 13 de noviembre; reuniones de PR el lunes 2, el sábado 7 y el martes 10 de noviembre. Las pruebas quedan escritas desde el inicio. | El trabajo en el repositorio no había empezado. | Ambos |
| 2026-10-29 | Se quitan las **300 filas duplicadas exactas** (iguales en las 14 columnas), conservando la primera aparición. La base de trabajo queda en **2850 clientes, 446 abandonos (15.6 %)**. | Las 300 copias vienen de 165 registros repetidos de 2 a 6 veces. Si se dejan, un mismo cliente podría quedar en entrenamiento y en prueba y el modelo parecería mejor de lo que es; además pesarían doble en las tablas de caracterización. La tasa de abandono casi no cambia (15.7 % → 15.6 %). | Ianis (propuesta), ambos |
| 2026-10-29 | Se usa `edad` y se quita `grupo_edad` (`config.COLUMNA_EDAD_A_QUITAR = "grupo_edad"`). | Cada grupo corresponde exactamente a una edad (1→15, 2→25, 3→30, 4→45, 5→55): son la misma información y meter las dos duplica la variable en el modelo. Se conserva `edad` porque se lee en años. | Ianis (propuesta), ambos |
| _pendiente reunión 1 (lun 2 nov)_ | ¿`estado` y `quejas` entran al modelo? | Son las más relacionadas con churn; discutir si son "tempranas" o casi el resultado. Se probará el modelo con y sin ellas (bloque 2). | Juanes |
| _pendiente reunión 1 (lun 2 nov)_ | ¿`valor_cliente` entra al modelo? | Es un cálculo a partir del uso: posible redundancia. | Juanes |
| _pendiente reunión 2 (sáb 7 nov)_ | Costo de un falso negativo vs. un falso positivo | Necesario para elegir el umbral de priorización. Sugerido: probar k = 2, 5 y 10. | Ianis + Juanes |
| _pendiente reunión 2 (sáb 7 nov)_ | Criterio para elegir el modelo final | Sugerido: AUC-PR y recall, desempatando por facilidad de explicar. | Juanes |

**Nota para la sesión 2 de Ianis (calidad):** después de quitar duplicados quedan 14 pares de clientes con las mismas características y distinto `churn` (28 filas, casi todos con `segundos_uso = 0`). Sugerido: no quitarlos (son clientes distintos que ningún modelo puede separar) y documentarlos en `docs/calidad_datos.md`.
