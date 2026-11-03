# Calidad de los datos

## 1. Descripción de la base de datos

El proyecto utiliza el conjunto de datos *Iranian Churn Dataset*, disponible en el repositorio UCI Machine Learning Repository. La base contiene información de 3150 clientes de una empresa de telecomunicaciones iraní y permite analizar las características relacionadas con el abandono del servicio.

La unidad de análisis es el cliente y la variable objetivo es `churn`, que identifica si el cliente abandonó el servicio (1) o permaneció activo (0).

## 2. Revisión inicial

La base original contiene 3150 registros y 15 columnas, incluyendo `fila_original`, que se utiliza para identificar la posición de cada registro en el archivo original.

Durante la revisión se verificó la estructura de los datos, los nombres de las columnas, la presencia de valores faltantes y los valores de la variable objetivo.

## 3. Proceso de limpieza

Para preparar los datos se realizaron las siguientes operaciones:

- **Identificación de duplicados:** se encontraron 300 registros duplicados. Para identificarlos, se compararon todas las columnas excepto `fila_original`, ya que esta última funciona como identificador de la posición original.
- **Eliminación de duplicados:** se conservaron los primeros registros y se eliminaron las repeticiones.
- **Eliminación de `grupo_edad`:** se retiró esta columna de acuerdo con la configuración definida para el proyecto. Esto debido a que tanto `edad` como `grupo_edad` contienen misma información del mismo contexto.
- **Conservación de los registros restantes:** después de la limpieza quedaron 2850 clientes.

## 4. Resultado de la limpieza

| Indicador | Resultado |
|---|---:|
| Registros originales | 3150 |
| Registros duplicados eliminados | 300 |
| Registros finales | 2850 |
| Columna eliminada | `grupo_edad` |

La base limpia se guarda en `data/processed/clientes.csv` y se carga mediante la función `cargar_limpio()` del módulo `src/churn/datos.py`.

## 5. Consideraciones

La columna `fila_original` se conserva como identificador del registro y no representa una característica de comportamiento del cliente.

La limpieza busca disponer de una base consistente para los análisis posteriores. No implica que las relaciones encontradas entre las variables y el abandono sean causales.