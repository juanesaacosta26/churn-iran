# Bitácora de decisiones

Toda decisión que cambie cifras o variables se anota aquí **en la reunión de cierre de cada bloque**,
con fecha, quién la propuso y por qué. El informe final cita esta bitácora en "Metodología".

| Fecha | Decisión | Por qué | Quién |
|---|---|---|---|
| 2026-10-11 | Se usa el CSV original de UCI (separado por comas) como única fuente en `data/raw/`. | El CSV del proyecto con `;` es la misma base exportada desde Excel. | Repositorio |
| 2026-10-28 | Se ajusta el calendario: presentación el viernes 13 de noviembre; reuniones de PR el lunes 2, el sábado 7 y el martes 10 de noviembre. Las pruebas quedan escritas desde el inicio. | El trabajo en el repositorio no había empezado. | Ambos |
| _pendiente arranque (jue 29 oct)_ | ¿Quitar las 300 filas duplicadas? | Sugerido: sí, para que un mismo cliente no quede en entrenamiento y prueba. | Ianis |
| _pendiente arranque (jue 29 oct)_ | ¿`edad` o `grupo_edad`? | Son redundantes; usar solo una. Provisional en `config.py`: se quita `grupo_edad`. | Ianis |
| _pendiente reunión 1 (lun 2 nov)_ | ¿`estado` y `quejas` entran al modelo? | Son las más relacionadas con churn; discutir si son "tempranas" o casi el resultado. Se probará el modelo con y sin ellas (bloque 2). | Juanes |
| _pendiente reunión 1 (lun 2 nov)_ | ¿`valor_cliente` entra al modelo? | Es un cálculo a partir del uso: posible redundancia. | Juanes |
| _pendiente reunión 2 (sáb 7 nov)_ | Costo de un falso negativo vs. un falso positivo | Necesario para elegir el umbral de priorización. Sugerido: probar k = 2, 5 y 10. | Ianis + Juanes |
| _pendiente reunión 2 (sáb 7 nov)_ | Criterio para elegir el modelo final | Sugerido: AUC-PR y recall, desempatando por facilidad de explicar. | Juanes |
