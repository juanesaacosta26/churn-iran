# Diccionario de datos

Fuente: Iranian Churn Dataset, UCI Machine Learning Repository (2020).
https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset

Archivo: `data/raw/customer_churn.csv` (3150 filas × 14 columnas, separado por comas, sin faltantes).
Las variables corresponden a los **primeros 9 meses**; `churn` es el estado al **mes 12**.

| Columna original | Nombre en el código | Grupo | Tipo | Descripción |
|---|---|---|---|---|
| Call Failure | `fallas_llamada` | Servicio | Conteo | Número de llamadas fallidas |
| Complains | `quejas` | Servicio | Binaria | 0 = sin queja, 1 = con queja |
| Subscription Length | `meses_suscripcion` | Suscripción | Conteo | Meses totales de suscripción |
| Charge Amount | `nivel_cobro` | Suscripción | Ordinal 0–9 | Nivel de cobro (0 = más bajo, 9 = más alto) |
| Seconds of Use | `segundos_uso` | Uso | Continua | Segundos totales de llamadas |
| Frequency of use | `frecuencia_llamadas` | Uso | Conteo | Número total de llamadas |
| Frequency of SMS | `frecuencia_sms` | Uso | Conteo | Número total de mensajes de texto |
| Distinct Called Numbers | `numeros_distintos` | Uso | Conteo | Números distintos a los que llamó |
| Age Group | `grupo_edad` | Demografía | Ordinal 1–5 | 1 = más joven, 5 = mayor |
| Tariff Plan | `plan_tarifa` | Suscripción | Binaria | 1 = pago por uso, 2 = contrato |
| Status | `estado` | Suscripción | Binaria | 1 = activo, 2 = no activo |
| Age | `edad` | Demografía | Ordinal | Edad del cliente (solo toma 5 valores: 15, 25, 30, 45, 55) |
| Customer Value | `valor_cliente` | Suscripción | Continua | Valor calculado del cliente (lo calcula la empresa a partir del uso) |
| Churn | `churn` | Objetivo | Binaria | 1 = abandona, 0 = permanece |

## Datos rápidos (verificados al armar el repositorio)

- 3150 filas, **300 duplicadas exactas** → 2850 clientes únicos.
- Tasa de churn: 15.7 % en la base completa; 15.6 % (446 de 2850) sin duplicados.
- `edad` y `grupo_edad` son la misma información (cada grupo corresponde a una sola edad).
- 107 clientes únicos tienen `segundos_uso = 0`.
- `valor_cliente` se deriva del uso: revisar si aporta algo distinto (Juanes, Semana 1).
