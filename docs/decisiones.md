# Bitácora de decisiones

Toda decisión que cambie cifras o variables se anota aquí **en la reunión semanal**,
con fecha, quién la propuso y por qué. El informe final cita esta bitácora en "Metodología".

| Fecha | Decisión | Por qué | Quién |
|---|---|---|---|
| 2026-10-11 | Se usa el CSV original de UCI (separado por comas) como única fuente en `data/raw/`. | El CSV del proyecto con `;` es la misma base exportada desde Excel. | Repositorio |
| _pendiente S1_ | ¿Quitar las 300 filas duplicadas? | Sugerido: sí, para que un mismo cliente no quede en entrenamiento y prueba. | Ianis |
| _pendiente S1_ | ¿`edad` o `grupo_edad`? | Son redundantes; usar solo una. | Ianis |
| _pendiente S1_ | ¿`estado` y `quejas` entran al modelo? | Son las más relacionadas con churn; discutir si son "tempranas" o casi el resultado. Se probará el modelo con y sin ellas (S3). | Juanes |
| _pendiente S1_ | ¿`valor_cliente` entra al modelo? | Es un cálculo a partir del uso: posible redundancia. | Juanes |
| _pendiente S2_ | Costo de un falso negativo vs. un falso positivo | Necesario para elegir el umbral de priorización. | Ianis + Juanes |
