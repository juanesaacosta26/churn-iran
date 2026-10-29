# Contrato: archivo de predicciones

Es lo que Juanes (modelos) le entrega a Ianis (priorización). Formato fijo:
si hay que cambiarlo, se acuerda en la reunión y se actualiza `tests/test_modelos.py`.

Archivos y fechas límite:
- `data/processed/predicciones_base.csv` (logística): a más tardar el **miércoles 4 de noviembre** en la noche.
- `data/processed/predicciones_final.csv` (modelo elegido): a más tardar el **sábado 7 de noviembre** al mediodía.

Ejemplo para trabajar sin esperar: `data/processed/fixtures/predicciones_ejemplo.csv`
(713 clientes de prueba, 112 abandonan; modelo simple de 3 variables, **no usar sus cifras en el informe**).

| Columna | Tipo | Descripción |
|---|---|---|
| `fila_original` | int | Identificador del cliente (fila en el CSV original, 1..3150) |
| `conjunto` | str | `"prueba"` (solo se entregan clientes del conjunto de prueba) |
| `churn_real` | int | 0 / 1 |
| `prob_churn` | float | Probabilidad estimada de abandono, 0–1 |
| `modelo` | str | Nombre del modelo que la produjo |

`tests/test_modelos.py::test_predicciones_cumplen_contrato` comprueba estas columnas, las 713 filas, los 112 abandonos y que `prob_churn` esté entre 0 y 1.
