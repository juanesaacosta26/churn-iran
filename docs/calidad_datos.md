# Calidad de los datos

## Resumen de la base procesada

- Total de clientes: 2850.
- Total de variables: 14.
- Valores faltantes: 0.
- Registros duplicados: 0.

## Estadísticas por variable numérica

Los valores atípicos se identificaron utilizando el criterio de 1.5 × IQR.

| Variable            |   Mínimo |   Percentil 5 |   Mediana |   Percentil 95 |   Máximo |   Cantidad de ceros |   Valores atípicos |
|:--------------------|---------:|--------------:|----------:|---------------:|---------:|--------------------:|-------------------:|
| fallas_llamada      |        0 |        0      |      6    |          23    |    36    |                 609 |                 44 |
| quejas              |        0 |        0      |      0    |           1    |     1    |                2620 |                230 |
| meses_suscripcion   |        3 |       13      |     35    |          42    |    47    |                   0 |                208 |
| nivel_cobro         |        0 |        0      |      0    |           4    |    10    |                1575 |                 62 |
| segundos_uso        |        0 |      267.5    |   3041    |       15044.2  | 17090    |                 107 |                189 |
| frecuencia_llamadas |        0 |        4      |     54.5  |         185    |   255    |                 107 |                118 |
| frecuencia_sms      |        0 |        0      |     22    |         356    |   522    |                 522 |                333 |
| numeros_distintos   |        0 |        2      |     21    |          52    |    97    |                 107 |                 82 |
| plan_tarifa         |        1 |        1      |      1    |           2    |     2    |                   0 |                229 |
| estado              |        1 |        1      |      1    |           2    |     2    |                   0 |                684 |
| edad                |       15 |       25      |     30    |          55    |    55    |                   0 |                633 |
| valor_cliente       |        0 |       17.7345 |    232.52 |        1592.48 |  2165.28 |                  85 |                104 |
| churn               |        0 |        0      |      0    |           1    |     1    |                2404 |                446 |

## Clientes con cero segundos de uso

- Clientes con segundos_uso = 0: 107.
- De ellos, clientes que abandonaron: 56.
- Porcentaje de abandono en este grupo: 52.34%.

## Interpretación

De los 107 clientes que no registraron segundos de uso, 56 abandonaron el servicio, lo que representa el 52.34% de este grupo. Esto indica que más de la mitad de los clientes sin uso registrado terminaron abandonando. Por esta razón, la variable `segundos_uso` puede ser una señal importante para identificar clientes que podrían estar en riesgo de abandono. Sin embargo, este resultado muestra una relación entre las variables y no significa que la falta de uso sea necesariamente la causa del abandono.
