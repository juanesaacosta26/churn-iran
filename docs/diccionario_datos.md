# Diccionario de datos

**Fuente:** Iranian Churn Dataset, UCI Machine Learning Repository (2020).  
https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset

**Archivo original:** `data/raw/customer_churn.csv` (3150 filas × 14 columnas, separado por comas, sin faltantes).

Las variables corresponden a los **primeros 9 meses**; `churn` es el estado al **mes 12**.

| Columna original | Nombre en el código | Grupo | Tipo | Rango observado | Descripción |
|---|---|---|---|---|---|
| Call Failure | `fallas_llamada` | Servicio | Conteo | 0–36 | Número de llamadas fallidas |
| Complains | `quejas` | Servicio | Binaria | 0–1 | 0 = sin queja, 1 = con queja |
| Subscription Length | `meses_suscripcion` | Suscripción | Conteo | 3–47 | Meses totales de suscripción |
| Charge Amount | `nivel_cobro` | Suscripción | Ordinal | 0–10 | Nivel de cobro (0 = más bajo, 10 = más alto) |
| Seconds of Use | `segundos_uso` | Uso | Continua | 0–17.090 | Segundos totales de llamadas |
| Frequency of use | `frecuencia_llamadas` | Uso | Conteo | 0–255 | Número total de llamadas |
| Frequency of SMS | `frecuencia_sms` | Uso | Conteo | 0–522 | Número total de mensajes de texto |
| Distinct Called Numbers | `numeros_distintos` | Uso | Conteo | 0–97 | Números distintos a los que llamó |
| Age Group | `grupo_edad` | Demografía | Ordinal | 1–5 | 1 = más joven, 5 = mayor |
| Tariff Plan | `plan_tarifa` | Suscripción | Binaria | 1–2 | 1 = pago por uso, 2 = contrato |
| Status | `estado` | Suscripción | Binaria | 1–2 | 1 = activo, 2 = no activo |
| Age | `edad` | Demografía | Ordinal | 15–55 | Edad del cliente (solo toma 5 valores: 15, 25, 30, 45, 55) |
| Customer Value | `valor_cliente` | Suscripción | Continua | 0–2.165,28 | Valor calculado del cliente (lo calcula la empresa a partir del uso) |
| Churn | `churn` | Objetivo | Binaria | 0–1 | 1 = abandona, 0 = permanece |

## Datos rápidos

- 3150 filas originales, **300 duplicadas exactas** → 2850 clientes únicos.
- Tasa de churn: 15.7 % en la base completa; 15.6 % (446 de 2850) sin duplicados.
- `edad` y `grupo_edad` contienen la misma información (cada grupo corresponde a una sola edad).
- 107 clientes únicos tienen `segundos_uso = 0`.
- `valor_cliente` se deriva del uso: revisar si aporta algo distinto (Juanes, bloque 1).

## Diferencia entre la base original y la base procesada

La base original contiene 3150 registros y 14 variables provenientes del conjunto de datos. Al cargarla mediante `cargar_crudo()`, se agrega la columna `fila_original`, que permite identificar la posición de cada registro.

Durante la preparación de los datos se eliminaron 300 registros duplicados, comparando las variables originales sin incluir `fila_original`. También se retiró `grupo_edad`, según la configuración del proyecto.

Como resultado, la base procesada contiene 2850 registros y 14 columnas, incluyendo `fila_original`. Esta es la versión que se utiliza para los análisis posteriores.

## Nota sobre los rangos observados

Los rangos observados corresponden a los valores mínimo y máximo encontrados en cada variable de la base procesada. Estos valores permiten describir los datos disponibles y deben distinguirse de los rangos teóricos definidos por el tipo de variable.
Dos ajustes importantes

## Importante para tener en cuenta:
1. En la descripción de nivel_cobro, cambia Ordinal 0–9 por Ordinal 0–10, porque encontramos valores hasta 10.
2. En la sección de diferencia entre bases, conserva que `grupo_edad` fue eliminada durante la preparación, aunque siga documentada aquí porque pertenece a la base original.
