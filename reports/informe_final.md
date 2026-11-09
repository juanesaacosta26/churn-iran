# Informe final
## Riesgo de abandono de clientes en una empresa de telecomunicaciones

**Integrantes:** Ianis Ramírez Cárdenas y Juan Esteban Acosta Morales  
**Asignatura:** Pensamiento Crítico II  
**Universidad:** Universidad Externado de Colombia  
**Fecha:** Noviembre de 2026

---

# 1. Planteamiento del problema, pregunta y objetivos

Las empresas de telecomunicaciones necesitan mantener relaciones estables con sus clientes, ya que el abandono del servicio puede representar una pérdida de ingresos y generar la necesidad de invertir recursos en la adquisición de nuevos usuarios. Por esta razón, identificar oportunamente a los clientes que presentan mayor riesgo de abandonar puede contribuir a organizar mejor las acciones de seguimiento y retención.

El problema que aborda este proyecto consiste en que una empresa puede disponer de información sobre el comportamiento de sus clientes, pero no necesariamente contar con criterios claros para reconocer cuáles presentan señales de un posible abandono. Si la identificación ocurre demasiado tarde, las oportunidades de contacto y retención pueden ser limitadas.

Para abordar esta situación se utiliza el Iranian Churn Dataset, publicado en el repositorio UCI Machine Learning Repository. El proyecto plantea un escenario en el que las características de uso, servicio y suscripción observadas durante los primeros nueve meses permiten estimar qué clientes presentan mayor riesgo de abandono al finalizar el mes doce. De esta manera, se considera una brecha de planificación de tres meses durante la cual la empresa podría organizar posibles acciones de retención.

### Pregunta de investigación

¿En qué medida las características de uso, servicio y suscripción observadas durante los primeros nueve meses permiten identificar y predecir qué clientes presentan mayor riesgo de abandono al finalizar los doce meses, para así apoyar la priorización de acciones de retención durante la brecha de planificación de tres meses?

### Objetivo general

Analizar la medida en que las características observadas de uso, servicios y suscripción de los clientes durante los primeros nueve meses permiten identificar cuáles presentan mayor riesgo de abandono al finalizar los doce meses, con el propósito de apoyar la priorización de clientes para posibles acciones de retención.

### Objetivos específicos

1. Identificar las características de comportamiento que presentan mayor relación con la condición de abandono de los clientes.
2. Caracterizar el comportamiento de los clientes según su condición final de abandono, reconociendo diferencias entre quienes abandonan y quienes permanecen.
3. Evaluar modelos de clasificación para estimar el riesgo de abandono y utilizar sus predicciones para ordenar a los clientes según su nivel de riesgo.

El alcance del proyecto es descriptivo, asociativo y predictivo. No busca demostrar que una característica cause el abandono ni comprobar que una estrategia de retención sea efectiva. Su propósito es aportar información para apoyar la toma de decisiones.

---

# 2. Datos y calidad de los datos

### 2.1 Fuente y unidad de análisis

La información utilizada proviene del **Iranian Churn Dataset**, disponible en UCI Machine Learning Repository. La unidad de análisis es cada cliente individual y la variable de interés es `churn`, que identifica si el cliente abandonó el servicio.

La base original contiene 3.150 registros y 14 variables. Para el análisis se realizó un proceso de depuración que permitió eliminar 300 registros duplicados exactos, conservando la primera aparición de cada registro. Como resultado, la base de trabajo quedó conformada por **2.850 clientes únicos y 14 variables**.

Esta decisión evita que un mismo registro tenga un peso repetido en la caracterización y reduce el riesgo de que copias de un mismo cliente queden distribuidas entre los conjuntos de entrenamiento y prueba.

### 2.2 Distribución de la variable objetivo

Después de la limpieza se identificaron 446 clientes que abandonaron el servicio, equivalentes al 15,6 % de la base, mientras que 2.404 clientes permanecieron, correspondientes al 84,4 %.

| Condición | Clientes | Porcentaje |
|---|---:|---:|
| Permanecieron (`churn = 0`) | 2.404 | 84,4 % |
| Abandonaron (`churn = 1`) | 446 | 15,6 % |
| **Total** | **2.850** | **100 %** |

Esta distribución evidencia un desbalance entre las dos categorías: los clientes que abandonaron representan una proporción menor. Por ello, la exactitud general no es suficiente para evaluar el desempeño de los modelos. También es necesario observar qué proporción de los abandonos reales logra identificar cada modelo.

### 2.3 Variables utilizadas

Las variables disponibles representan características relacionadas con el uso del servicio, la experiencia del cliente y sus condiciones de suscripción. Entre ellas se encuentran las fallas de llamada, las quejas, los segundos de uso, la frecuencia de SMS, los números distintos contactados, los meses de suscripción, el nivel de cobro, el plan tarifario, el estado y la edad.

La variable `churn` se utiliza como resultado que se busca anticipar y no como predictor.

### 2.4 Calidad y depuración

La base procesada no presenta valores faltantes ni registros duplicados. Se revisaron las distribuciones, los valores mínimos y máximos, las medianas, los percentiles y los posibles valores atípicos mediante el criterio de 1,5 veces el rango intercuartílico (IQR).

Un resultado relevante corresponde a los clientes con cero segundos de uso: se identificaron 107 clientes en esta condición, de los cuales 56 abandonaron el servicio. Esto representa una tasa de abandono del 52,34 % dentro de ese grupo.

Este resultado muestra que la ausencia de uso registrado puede constituir una señal de riesgo, aunque no demuestra que la falta de utilización sea la causa del abandono.

También se revisó la redundancia entre variables. Se identificó que `grupo_edad` contiene la misma información que `edad`, por lo que se conservó la edad expresada en años. Además, se retiraron variables con información muy similar a otras características incluidas en el análisis, como se explica en la sección de metodología.

**Fuente de los resultados de calidad:** `docs/calidad_datos.md`.

---

# 3. Metodología

El desarrollo del proyecto se organizó en etapas de preparación de datos, análisis exploratorio, caracterización, selección de variables, entrenamiento y evaluación de modelos, interpretación y priorización.

### 3.1 Preparación de los datos

Se utilizó la base depurada de 2.850 clientes. La partición se realizó de manera estratificada, conservando aproximadamente la proporción de clientes que abandonaron y permanecieron en ambos conjuntos.

La distribución quedó de la siguiente manera:

| Conjunto | Clientes | Abandonos |
|---|---:|---:|
| Entrenamiento | 2.137 | 334 |
| Prueba | 713 | 112 |
| **Total** | **2.850** | **446** |

Se utilizó la semilla aleatoria 42 para mantener la reproducibilidad de los resultados.

### 3.2 Selección de variables

La selección se apoyó en el análisis de correlaciones, la revisión de redundancias y el factor de inflación de la varianza (VIF). Se buscó conservar variables que aportaran información útil sin incluir características que representaran prácticamente la misma información.

El conjunto final de predictores estuvo conformado por diez variables:

- Fallas de llamada.
- Quejas.
- Segundos de uso.
- Frecuencia de SMS.
- Números distintos contactados.
- Meses de suscripción.
- Nivel de cobro.
- Plan tarifario.
- Estado del cliente.
- Edad.

Se retiró `grupo_edad` porque representa la misma información que `edad`. También se excluyó `frecuencia_llamadas` debido a su alta correlación con `segundos_uso` (r = 0,95), y `valor_cliente`, porque presentó un VIF de 53 y las demás variables explicaban el 98 % de su variación.

Se conservaron `quejas` y `estado` en el modelo principal debido a su relación con el abandono y a que no presentaban redundancia estadística importante con los demás predictores. Sin embargo, su disponibilidad temporal debe revisarse, pues podrían contener información registrada cerca del momento del abandono.

### 3.3 Entrenamiento y comparación de modelos

Se compararon modelos de regresión logística, árbol de decisión, bosque aleatorio y boosting. La comparación se realizó mediante validación cruzada de cinco pliegues, utilizando únicamente el conjunto de entrenamiento para la selección del modelo.

Se consideraron principalmente las siguientes métricas:

- **AUC-ROC:** capacidad para distinguir entre clientes que abandonan y clientes que permanecen.
- **AUC-PR:** relación entre precisión y sensibilidad, especialmente útil cuando existe desbalance de clases.
- **Recall:** proporción de abandonos reales identificados.
- **Precisión:** proporción de clientes señalados como posibles abandonos que efectivamente abandonaron.
- **F1:** equilibrio entre precisión y recall.

La elección del modelo final consideró su desempeño en validación cruzada, su capacidad de identificar abandonos y su utilidad para ordenar a los clientes según el riesgo estimado.

### 3.4 Evaluación e interpretación

Una vez seleccionado el modelo, se evaluó en el conjunto de prueba, que contiene 713 clientes y 112 abandonos. Este conjunto se utilizó para la evaluación final y no para seleccionar el modelo.

Adicionalmente, se realizó un análisis de sensibilidad para examinar cuánto dependían las predicciones de las variables `quejas` y `estado`. También se desarrolló una regresión logística bayesiana para interpretar las razones de momios y la incertidumbre de los coeficientes.

Finalmente, se utilizaron las probabilidades estimadas para ordenar a los clientes y analizar diferentes escenarios de capacidad de contacto y costos relativos de los errores.

Las decisiones sobre la selección de variables, la partición y los procedimientos de análisis se encuentran documentadas en `docs/decisiones.md`.

---

# 4. Caracterización de quienes abandonan frente a quienes permanecen

La caracterización permitió identificar diferencias entre los clientes que abandonaron el servicio y aquellos que permanecieron. Se analizaron variables relacionadas con la experiencia del cliente, la utilización del servicio, las condiciones de contratación y el valor registrado.

### 4.1 Quejas y estado del cliente

Las quejas presentan una de las diferencias más marcadas. Los clientes que registraron quejas tuvieron una tasa de abandono del 82,6 %, frente al 9,8 % de quienes no presentaron quejas. La diferencia es de aproximadamente 72,8 puntos porcentuales y la prueba estadística obtuvo un valor p de 1,27 × 10⁻¹⁸⁵.

El estado también mostró diferencias importantes. Los clientes con estado no activo registraron una tasa de abandono del 47,5 %, mientras que en los clientes activos fue del 5,6 %. La diferencia fue de 41,9 puntos porcentuales, con un valor p de 6,86 × 10⁻¹⁵².

Estos resultados indican que las quejas y el estado son características estrechamente relacionadas con la condición de abandono. No obstante, el estado requiere especial precaución porque podría estar registrado después o cerca del abandono y, por tanto, no necesariamente estar disponible para una predicción anticipada.

### 4.2 Utilización del servicio y valor del cliente

Los clientes que abandonaron presentaron una mediana de 1.256,5 segundos de uso, mientras que los clientes que permanecieron registraron una mediana de 3.596,5 segundos. La prueba de Mann-Whitney obtuvo un valor p de 1,84 × 10⁻⁸² y un delta de Cliff de −0,573.

También se observaron diferencias en el valor del cliente: la mediana del grupo que abandonó fue de 102,565, frente a 271,54 en el grupo que permaneció. La diferencia fue estadísticamente significativa (p = 1,59 × 10⁻⁷⁹), con un delta de Cliff de −0,562.

En conjunto, estos resultados muestran que quienes abandonaron presentaban menores niveles de utilización del servicio y un menor valor registrado como clientes.

### 4.3 Plan tarifario

Los clientes con plan de pago por uso presentaron una tasa de abandono del 16,8 %, mientras que los clientes con plan contractual registraron una tasa del 2,6 %. La diferencia fue de 14,2 puntos porcentuales y la prueba chi-cuadrado obtuvo un valor p de 2,64 × 10⁻⁸.

### 4.4 Resumen de los principales resultados

| Característica | Clientes que abandonaron | Clientes que permanecieron | Resultado |
|---|---:|---:|---|
| Quejas | 82,6 % con quejas | 9,8 % con quejas | Diferencia de 72,8 puntos porcentuales |
| Estado | 47,5 % no activos | 5,6 % no activos | Diferencia de 41,9 puntos porcentuales |
| Segundos de uso | Mediana: 1.256,5 | Mediana: 3.596,5 | p = 1,84 × 10⁻⁸² |
| Valor del cliente | Mediana: 102,565 | Mediana: 271,54 | p = 1,59 × 10⁻⁷⁹ |
| Plan tarifario | Pago por uso: 16,8 % | Contractual: 2,6 % | Diferencia de 14,2 puntos porcentuales |

También se encontraron diferencias estadísticamente significativas en la frecuencia de llamadas, los números distintos contactados y la frecuencia de SMS. En cambio, los meses de suscripción y las fallas de llamada no mostraron diferencias estadísticamente significativas en esta comparación.

En general, la caracterización evidencia que el abandono se relaciona con diferencias en la experiencia y el comportamiento de los clientes. Estos resultados permiten reconocer perfiles distintos, pero no son suficientes por sí solos para anticipar qué clientes abandonarán.

**Figuras de caracterización:** se encuentran en `reports/figures/caracterizacion_*.png`.  
**Respaldo:** `docs/hallazgos.md` y las tablas de caracterización de `reports/tablas/`.

---

# 5. Variables más relacionadas y modelos predictivos

### 5.1 Relación entre las variables y el abandono

El análisis de relación identificó que las quejas y el estado no activo son las características con mayor asociación con el abandono. La correlación registrada fue de 0,55 para las quejas y 0,49 para el estado. En contraste, las fallas de llamada presentaron una correlación cercana a cero (r = 0,00).

También se identificaron relaciones elevadas entre algunos predictores. Por ejemplo, los segundos de uso y la frecuencia de llamadas presentaron una correlación de 0,95. Asimismo, la frecuencia de SMS y el valor del cliente mostraron una correlación de 0,92. Estas redundancias respaldaron la exclusión de algunas variables del modelo principal.

### 5.2 Comparación de modelos

Los resultados de validación cruzada mostraron que el bosque aleatorio obtuvo el mejor desempeño general entre los modelos comparados.

| Modelo | AUC-ROC promedio | AUC-PR promedio |
|---|---:|---:|
| Regresión logística | 0,929 | 0,741 |
| Árbol de decisión | 0,904 | 0,691 |
| Bosque aleatorio | **0,977** | **0,894** |
| Boosting | 0,974 | 0,890 |

El bosque aleatorio fue seleccionado como modelo final porque obtuvo el mayor AUC-PR promedio en validación cruzada y presentó un desempeño superior al de la regresión logística en la evaluación final.

En el conjunto de prueba, el bosque aleatorio alcanzó un AUC-PR de 0,907 y un AUC-ROC de 0,975. La regresión logística obtuvo un AUC-PR de 0,767 y un AUC-ROC de 0,930. Como referencia, la proporción de abandonos en el conjunto de prueba fue de aproximadamente 0,16, valor que sirve como referencia para interpretar el AUC-PR.

### 5.3 Capacidad predictiva y sensibilidad de las variables

Al evaluar la capacidad de identificación, el bosque aleatorio logró capturar el 91,1 % de los abandonos al seleccionar el 20 % de los clientes con mayor riesgo. La regresión logística alcanzó el 74,1 % bajo el mismo criterio.

Se realizó también un análisis de sensibilidad excluyendo las variables `quejas` y `estado`. En este escenario, el bosque aleatorio obtuvo un AUC-PR de 0,804 y capturó el 88,4 % de los abandonos al seleccionar el 20 % de mayor riesgo. La regresión logística, por su parte, obtuvo un AUC-PR de 0,461.

Este resultado muestra que el uso y las características de suscripción conservan información útil para identificar el abandono, incluso sin incluir las dos variables más relacionadas con el resultado. Sin embargo, el desempeño del modelo disminuye, por lo que la interpretación debe considerar la posible influencia temporal de las quejas y el estado.

### 5.4 Importancia de las variables

La importancia por permutación del bosque aleatorio mostró que las variables con mayor aporte al desempeño predictivo fueron:

| Variable | Caída del AUC-PR al desordenarla |
|---|---:|
| Quejas | 0,33 |
| Estado | 0,21 |
| Segundos de uso | 0,10 |
| Meses de suscripción | 0,07 |
| Plan tarifario | 0,00 |

Las quejas y el estado fueron las variables más importantes, seguidas por los segundos de uso y los meses de suscripción. El plan tarifario presentó un aporte prácticamente nulo según esta medida.

La importancia por permutación permite evaluar cuánto depende el desempeño del modelo de cada variable, pero no demuestra que una característica cause el abandono.

### 5.5 Regresión logística bayesiana

Como complemento interpretativo se estimó una regresión logística bayesiana con las mismas diez variables. Para la estimación se utilizaron cuatro cadenas de Monte Carlo, con 1.000 iteraciones de calentamiento y 2.000 muestras por cadena, para un total de 8.000 muestras posteriores.

Los diagnósticos indicaron una convergencia adecuada: el R̂ máximo fue de 1,003 y no se registraron divergencias.

Entre los resultados principales se encontró que:

- La presencia de una queja se asoció con unas razones de momios de abandono 35,3 veces mayores que las de un cliente sin quejas, manteniendo constantes las demás variables (intervalo de credibilidad del 95 %: 20,36–62,34).
- El estado no activo presentó una razón de momios de 3,28 frente al estado activo (intervalo de credibilidad del 95 %: 2,11–5,09).
- Un aumento de 1.000 segundos de uso se asoció con una reducción de las razones de momios de abandono.
- Un aumento de seis meses de suscripción también se relacionó con menores razones de momios de abandono.
- Los intervalos de las variables edad y plan tarifario incluyeron el valor 1, por lo que no se encontró evidencia concluyente de una asociación diferente de cero para estos efectos en el modelo bayesiano.

La magnitud del efecto de las quejas fue considerablemente mayor que la esperada a partir de la evidencia externa utilizada para construir las distribuciones previas. Esto refuerza la necesidad de revisar cuándo se registran las quejas y si están disponibles realmente durante el periodo de anticipación.

En conjunto, los modelos muestran que el bosque aleatorio ofrece la mejor capacidad predictiva entre las alternativas evaluadas, mientras que la regresión logística bayesiana aporta una interpretación de los efectos y de su incertidumbre.

**Respaldo:** `reports/tablas/comparacion_modelos.csv`, `metricas_prueba_todos.csv`, `sensibilidad_variables.csv`, `importancia_permutacion.csv`, `criterios_avance2.json` y `docs/bayes_resultados.md`.

---

# 6. Priorización de clientes para el equipo de retención

La etapa de priorización utilizó las probabilidades estimadas por el bosque aleatorio para ordenar a los clientes desde el mayor hasta el menor riesgo de abandono. El propósito es que la empresa pueda concentrar sus recursos de contacto en los clientes con mayor probabilidad estimada de abandonar, teniendo en cuenta que la capacidad operativa puede ser limitada.

### 6.1 Distribución por deciles de riesgo

Los clientes del conjunto de prueba se ordenaron según su probabilidad estimada de abandono y se dividieron en diez grupos de tamaño similar. Los primeros deciles concentraron la mayor proporción de abandonos reales.

| Decil | Clientes | Abandonos | Tasa de abandono | Lift | Captura acumulada |
|---|---:|---:|---:|---:|---:|
| 1 | 72 | 67 | 93,06 % | 5,92 | 59,82 % |
| 2 | 71 | 35 | 49,30 % | 3,14 | 91,07 % |
| 3 | 71 | 6 | 8,45 % | 0,54 | 96,43 % |
| 4 | 72 | 2 | 2,78 % | 0,18 | 98,21 % |
| 5 | 71 | 1 | 1,41 % | 0,09 | 99,11 % |
| 6 | 71 | 1 | 1,41 % | 0,09 | 100,00 % |
| 7 | 72 | 0 | 0,00 % | 0,00 | 100,00 % |
| 8 | 71 | 0 | 0,00 % | 0,00 | 100,00 % |
| 9 | 71 | 0 | 0,00 % | 0,00 | 100,00 % |
| 10 | 71 | 0 | 0,00 % | 0,00 | 100,00 % |

El primer decil reunió 67 de los 112 abandonos del conjunto de prueba. Al acumular los dos primeros deciles se identificaron 102 abandonos, equivalentes al 91,1 % del total.

El lift compara la tasa de abandono de cada decil con la tasa general del conjunto de prueba. Un valor superior a 1 indica que el grupo presenta una concentración de abandonos mayor que la general. Los dos primeros deciles muestran los valores más altos, por lo que constituyen los grupos más relevantes para la priorización.

### 6.2 Escenarios de capacidad de contacto

También se evaluaron tres escenarios según la cantidad de clientes que la empresa podría contactar.

| Capacidad de contacto | Clientes contactados | Abandonos identificados | Abandonos capturados | Precisión |
|---|---:|---:|---:|---:|
| 10 % | 71 | 66 | 58,93 % | 92,96 % |
| 20 % | 143 | 102 | 91,07 % | 71,33 % |
| 30 % | 214 | 108 | 96,43 % | 50,47 % |

Los resultados muestran que contactar al 10 % de los clientes permite identificar el 58,93 % de los abandonos. Al aumentar la capacidad al 20 %, la cobertura alcanza el 91,07 %. Si se amplía al 30 %, se llega al 96,43 %, aunque la precisión disminuye porque se contacta a una mayor cantidad de clientes que finalmente permanecen.

El escenario del 20 % representa una alternativa relevante porque permite identificar una proporción alta de los abandonos sin contactar a toda la base. La diferencia entre los 72 clientes del primer decil y los 71 del escenario de capacidad del 10 % se debe a que ambos cortes se calculan de manera independiente sobre el conjunto de prueba.

### 6.3 Perfil de los clientes de mayor riesgo

Al comparar el 20 % de clientes con mayor riesgo frente al resto, se encontraron diferencias en varias características de uso.

| Variable | Mediana del 20 % de mayor riesgo | Mediana del resto |
|---|---:|---:|
| Segundos de uso | 1.260 | 3.794 |
| Valor del cliente | 113,805 | 280,6275 |
| Frecuencia de llamadas | 31 | 68,5 |
| Números distintos contactados | 10 | 24 |
| Frecuencia de SMS | 16 | 28 |
| Meses de suscripción | 35 | 34,5 |
| Fallas de llamada | 7 | 7 |

Las diferencias en segundos de uso, valor del cliente, frecuencia de llamadas, números distintos contactados y frecuencia de SMS fueron estadísticamente significativas (p < 0,001). Por el contrario, los meses de suscripción (p = 0,160) y las fallas de llamada (p = 0,516) no mostraron diferencias significativas.

En las variables categóricas también se observó una mayor proporción de clientes de alto riesgo entre quienes presentaron quejas y quienes tenían estado no activo. Por ejemplo, el 89,1 % de los clientes con quejas fue clasificado como de alto riesgo, frente al 13,3 % de quienes no presentaron quejas. Para el estado, la proporción fue del 68,5 % entre los no activos y del 5,1 % entre los activos.

Estos porcentajes representan la proporción de clientes clasificados con alto riesgo dentro de cada categoría, no la distribución de categorías dentro del grupo de alto riesgo.

### 6.4 Costos relativos de los errores

Finalmente, se evaluaron diferentes umbrales de decisión teniendo en cuenta que no identificar a un cliente que abandona puede representar una pérdida mayor que contactar a un cliente que finalmente permanece.

Se utilizó la función:

**Costo = FP + k × FN**

Donde FP representa los falsos positivos, FN los falsos negativos y k el peso asignado a los falsos negativos.

| k | Umbral | Falsos positivos | Falsos negativos | Costo mínimo |
|---:|---:|---:|---:|---:|
| 2 | 0,35 | 26 | 14 | 54 |
| 5 | 0,20 | 54 | 6 | 84 |
| 10 | 0,20 | 54 | 6 | 114 |

Al aumentar el peso de los falsos negativos, el umbral de 0,20 permite reducir su cantidad de 14 a 6, aunque aumenta la cantidad de falsos positivos. La elección del umbral depende de la capacidad de contacto y del costo relativo que la empresa asigne a cada tipo de error.

Los valores de esta tabla son unidades relativas de penalización y no representan costos monetarios reales.

En conclusión, la priorización permite transformar las probabilidades del modelo en un orden de atención. El escenario de contacto del 20 % constituye una alternativa útil para orientar los recursos hacia los clientes con mayor riesgo estimado.

**Respaldo:** `reports/tablas/priorizacion_deciles.csv`, `priorizacion_capacidad.csv`, `priorizacion_costos.csv` y `docs/hallazgos.md`.

---

# 7. Riesgos: falsos positivos, falsos negativos y privacidad

La utilización de un modelo predictivo para priorizar clientes implica riesgos que deben considerarse antes de aplicar sus resultados en un contexto empresarial.

### 7.1 Falsos positivos

Un falso positivo ocurre cuando el modelo identifica a un cliente como posible abandono, pero este finalmente permanece en el servicio. En este caso, la empresa podría destinar recursos de contacto o retención a una persona que no iba a abandonar.

En el conjunto de prueba, el bosque aleatorio registró ocho falsos positivos. Su precisión fue de aproximadamente 91,5 %, lo que significa que una proporción alta de los clientes señalados como posibles abandonos efectivamente pertenecía a la clase de abandono.

### 7.2 Falsos negativos

Un falso negativo ocurre cuando el modelo no identifica a un cliente que finalmente abandona. Este error puede ser especialmente importante porque la empresa pierde la oportunidad de considerar a ese cliente dentro de sus acciones de seguimiento.

En el conjunto de prueba, el bosque aleatorio registró 26 falsos negativos y un recall de aproximadamente 76,8 %. Esto significa que identificó cerca de tres cuartas partes de los abandonos reales, pero dejó sin identificar a los restantes.

La comparación entre ambos errores muestra que el umbral de clasificación debe responder a las necesidades de la empresa. Si se busca reducir los falsos negativos, puede ser conveniente ampliar el grupo de clientes contactados, siempre que exista capacidad operativa suficiente.

### 7.3 Riesgo de fuga de información

Uno de los principales riesgos metodológicos corresponde a las variables `quejas` y `estado`. Ambas presentan una relación muy marcada con el abandono y tienen un peso elevado en las predicciones.

Sin embargo, si estas características se registraron cerca del momento del abandono o después de que el cliente tomó la decisión de retirarse, podrían contener información que no estaría disponible durante los primeros nueve meses. En ese caso, el desempeño del modelo podría ser más alto de lo que sería posible conseguir en una aplicación anticipada real.

El análisis de sensibilidad mostró que, al excluir estas dos variables, el bosque aleatorio mantiene un AUC-PR de 0,804 y captura el 88,4 % de los abandonos al seleccionar el 20 % de mayor riesgo. Esto demuestra que las demás características conservan información predictiva, aunque el desempeño disminuye.

Antes de implementar el modelo, sería necesario verificar las fechas exactas de registro de las quejas y del estado del cliente, y confirmar que ambas variables estén disponibles antes del momento en que se tomaría la decisión de contacto.

### 7.4 Privacidad y uso responsable

La información de los clientes debe utilizarse únicamente para los fines autorizados del análisis y de acuerdo con las políticas de protección de datos aplicables. En una implementación real se deberían establecer controles de acceso, limitar la información disponible a los usuarios que la necesitan y evitar divulgar identificadores o información individual en informes y presentaciones.

Las predicciones tampoco deberían utilizarse como una decisión automática sobre la continuidad del servicio, las condiciones comerciales o el acceso a beneficios. Su finalidad es apoyar la identificación de clientes que podrían requerir atención, manteniendo la revisión humana y la posibilidad de evaluar cada situación de manera individual.

Por tanto, el modelo debe entenderse como una herramienta de apoyo a la decisión y no como un mecanismo definitivo para determinar el comportamiento de una persona.

---

# 8. Conclusiones: respuesta a la pregunta de investigación

El proyecto permitió identificar que las características de uso, experiencia y suscripción contienen información útil para reconocer diferencias entre los clientes que abandonan y quienes permanecen. Las quejas y el estado del cliente mostraron las asociaciones más marcadas, mientras que los segundos de uso y el valor registrado del cliente presentaron diferencias importantes entre ambos grupos.

En cuanto a la capacidad predictiva, el bosque aleatorio fue el modelo con mejor desempeño entre las alternativas evaluadas. En el conjunto de prueba obtuvo un AUC-PR de 0,907, frente a 0,767 de la regresión logística. Además, al seleccionar el 20 % de los clientes con mayor riesgo estimado, logró identificar el 91,1 % de los abandonos registrados.

Estos resultados permiten responder que las características analizadas sí ofrecen información relevante para identificar y ordenar clientes según su riesgo de abandono. En particular, el modelo permite concentrar una proporción importante de los abandonos en un grupo reducido de clientes, lo que puede apoyar la distribución de los recursos de contacto durante una etapa de planificación.

No obstante, el desempeño debe interpretarse considerando la posible fuga de información asociada con las variables `quejas` y `estado`. Al excluirlas, el bosque aleatorio conserva un AUC-PR de 0,804 y captura el 88,4 % de los abandonos al seleccionar el 20 % de mayor riesgo. Esto indica que las variables relacionadas con el uso y la suscripción también aportan información para anticipar el abandono.

En relación con los objetivos específicos, se identificaron las características con mayor asociación con el abandono, se describieron las diferencias entre quienes abandonaron y permanecieron, y se evaluó la capacidad de los modelos para estimar y ordenar el riesgo.

En consecuencia, el proyecto ofrece una base analítica para apoyar la priorización de posibles acciones de retención. Sin embargo, no demuestra que contactar a los clientes identificados evite efectivamente el abandono; esa efectividad tendría que evaluarse mediante una intervención posterior.

---

# 9. Limitaciones y trabajo futuro

Los resultados deben interpretarse teniendo en cuenta varias limitaciones.

En primer lugar, el análisis utiliza una base pública correspondiente a un operador de telecomunicaciones de Irán. Por tanto, los patrones identificados no necesariamente representan el comportamiento de los clientes de otras empresas, países o mercados. La aplicación del modelo en otro contexto requeriría contar con información propia y realizar una nueva evaluación.

En segundo lugar, aunque el proyecto plantea utilizar características de los primeros nueve meses para anticipar el abandono al finalizar el mes doce, es necesario verificar con mayor detalle el momento exacto en que se registraron algunas variables. En particular, las quejas y el estado del cliente podrían contener información cercana al resultado que se busca anticipar. Esta situación puede producir una estimación optimista del desempeño si no se confirma su disponibilidad temporal.

En tercer lugar, la base presenta un desbalance entre clientes que abandonan y clientes que permanecen. Aunque se utilizaron métricas como AUC-PR, recall y precisión para evaluar los modelos, los resultados pueden cambiar si se modifica la proporción de abandono en una población diferente.

Además, la evaluación se realizó sobre una partición específica de entrenamiento y prueba. Aunque se utilizó validación cruzada durante la selección de modelos, sería conveniente realizar una validación temporal y comprobar el desempeño con datos nuevos de la empresa antes de implementar el modelo.

Otra limitación corresponde a los costos de los errores. La función utilizada asigna penalizaciones relativas a falsos positivos y falsos negativos, pero no incorpora costos monetarios reales de contacto, descuentos, beneficios de retención ni pérdidas económicas por abandono. Por esta razón, los umbrales evaluados no deben interpretarse como una política financiera definitiva.

Finalmente, el proyecto no evalúa directamente la efectividad de las estrategias de retención. Identificar clientes con mayor riesgo no significa que una llamada, una oferta o un beneficio vaya a impedir su abandono.

Como trabajo futuro se propone:

1. Verificar la fecha de registro de cada variable y asegurar que los predictores estén disponibles antes del momento de decisión.
2. Evaluar el modelo con datos nuevos y de diferentes periodos para comprobar su estabilidad.
3. Incorporar información sobre los costos reales de contacto y de abandono para definir umbrales de decisión más cercanos a las necesidades de la empresa.
4. Diseñar una prueba piloto de acciones de retención que permita medir si el contacto con los clientes priorizados reduce efectivamente el abandono.
5. Revisar periódicamente el desempeño del modelo y posibles diferencias entre grupos de clientes para evitar que sus predicciones pierdan utilidad con el tiempo.

En conclusión, el proyecto constituye una herramienta de análisis y priorización, pero su implementación debe acompañarse de validación temporal, revisión de la calidad de los datos y evaluación de las acciones que se decida realizar.

---

# Referencias

Ahn, J.-H., Han, S.-P., & Lee, Y.-S. (2006). Customer churn analysis: Churn determinants and mediation effects of partial defection in the Korean mobile telecommunications service industry. *Telecommunications Policy, 30*(10–11), 552–568. https://pages.stern.nyu.edu/~shan2/customerchurn.pdf

Arai, K., Fujikawa, I., Nakagawa, Y., Momozaki, R., & Ogawa, S. (2023). Churn customer estimation method based on LightGBM for improving sales. *International Journal of Advanced Computer Science and Applications, 14*(2), 119–125.

Gelman, A., Jakulin, A., Pittau, M. G., & Su, Y.-S. (2008). A weakly informative default prior distribution for logistic and other regression models. *The Annals of Applied Statistics, 2*(4), 1360–1383.

Hoffman, M. D., & Gelman, A. (2014). The No-U-Turn sampler: Adaptively setting path lengths in Hamiltonian Monte Carlo. *Journal of Machine Learning Research, 15*, 1593–1623.

Ibrahim, J. G., & Chen, M.-H. (2000). Power prior distributions for regression models. *Statistical Science, 15*(1), 46–60. https://doi.org/10.1214/ss/1009212673

Iranian Churn [Dataset]. (2020). *UCI Machine Learning Repository*. https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset

Keramati, A., Jafari-Marandi, R., Aliannejadi, M., Ahmadian, I., Mozaffari, M., & Abbasi, U. (2014). Improved churn prediction in telecommunication industry using data mining techniques. *Applied Soft Computing, 24*, 994–1012.