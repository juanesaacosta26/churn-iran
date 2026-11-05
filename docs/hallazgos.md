# Hallazgos

# Hallazgos de la caracterización de clientes

La caracterización permitió comparar el comportamiento de los clientes que abandonaron el servicio con aquellos que permanecieron. Para ello, se analizaron variables relacionadas con la experiencia del cliente, el uso de los servicios, las condiciones de contratación y el valor registrado. Los resultados permiten identificar diferencias entre ambos grupos y reconocer cuáles características presentan una mayor asociación con el abandono.

## Hallazgo 1. Las quejas presentan una fuerte asociación con el abandono

La variable quejas muestra una de las diferencias más marcadas entre los clientes que abandonaron y los que permanecieron. Los resultados indican que los clientes que presentaron quejas registraron una tasa de abandono del 82,6 %, mientras que aquellos que no presentaron quejas tuvieron una tasa del 9,8 %. Esto representa una diferencia de aproximadamente 72,8 puntos porcentuales entre los dos grupos.

La prueba estadística también respalda esta diferencia, con un valor p de 1,27 × 10⁻¹⁸⁵, lo que indica una asociación estadísticamente significativa entre la presentación de quejas y la condición de abandono. En términos prácticos, este resultado muestra que las quejas constituyen una señal importante para diferenciar a los clientes que presentan mayor presencia de abandono dentro de los datos analizados.

Para el proyecto, este hallazgo es especialmente relevante porque las quejas podrían utilizarse como una característica para identificar clientes que requieren atención prioritaria. Sin embargo, la presencia de una queja no significa necesariamente que el cliente vaya a abandonar, por lo que debe analizarse junto con otras características de comportamiento.

**Figura:** caracterizacion_quejas.
![Tasa de abandono según quejas](../reports/figures/caracterizacion_quejas.png)

## Hallazgo 2. El estado del cliente presenta diferencias importantes en las tasas de abandono.

La variable estado también presenta una diferencia considerable entre sus categorías. Los clientes con estado no activo (nivel 2) registraron una tasa de abandono del 47,5 %, mientras que los clientes con estado activo (nivel 1) presentaron una tasa del 5,6 %. Esto representa una diferencia aproximada de 41,9 puntos porcentuales.

El valor p obtenido fue de 6,86 × 10⁻¹⁵², lo que evidencia una asociación estadísticamente significativa entre el estado del cliente y el abandono. Esta diferencia permite observar que la condición de actividad del cliente está estrechamente relacionada con su situación frente al servicio.

No obstante, este resultado debe interpretarse con precaución. El estado del cliente podría estar relacionado directamente con la condición de abandono que se busca estudiar, por lo que es necesario revisar su disponibilidad temporal antes de utilizarlo como variable predictora. Si el estado fue registrado después o al mismo tiempo que el abandono, podría generar fuga de información en los modelos.

Por esta razón, aunque es una variable útil para describir las diferencias entre los grupos, su utilización para anticipar el abandono debe evaluarse cuidadosamente.

**Figura:** caracterizacion_estado.
![Tasa de abandono según estado](../reports/figures/caracterizacion_estado.png)

## Hallazgo 3. Los clientes que abandonan presentan menores niveles de utilización del servicio.

La comparación de los segundos de uso muestra una diferencia importante entre los clientes que abandonaron y aquellos que permanecieron. La mediana de segundos de uso de los clientes que abandonaron fue de 1.256,5, mientras que para los clientes que permanecieron fue de 3.596,5. Esto significa que el nivel de uso registrado en el grupo que abandonó fue considerablemente menor.

Además, la prueba de Mann-Whitney arrojó un valor p de 1,84 × 10⁻⁸² y un delta de Cliff de -0,573, lo que refleja una diferencia estadísticamente significativa y un efecto de magnitud considerable entre ambos grupos. El signo negativo indica que los valores tienden a ser menores entre quienes abandonaron, de acuerdo con la orientación utilizada en el cálculo.

Este resultado permite identificar el nivel de utilización del servicio como una característica relevante para la caracterización del abandono. Una posible interpretación es que los clientes que reducen su utilización podrían estar mostrando un menor vínculo con los servicios de la empresa. Sin embargo, estos resultados corresponden a una comparación entre grupos y no permiten afirmar por sí solos que la reducción del uso sea la causa del abandono.

Para el proyecto, los segundos de uso representan una señal de comportamiento que podría contribuir a identificar clientes con menor actividad y complementar otras variables en la identificación anticipada del riesgo.

**Figura:** caracterizacion_segundos_uso.
![Distribución de segundos de uso](../reports/figures/caracterizacion_segundos_uso.png)

## Hallazgo 4. Los clientes que abandonan presentan un menor valor registrado como cliente

La variable valor_cliente también presenta una diferencia marcada entre los dos grupos. Los clientes que abandonaron registraron una mediana de 102,565, mientras que aquellos que permanecieron alcanzaron una mediana de 271,54. Esto indica que el valor registrado de los clientes que abandonaron fue considerablemente inferior al de quienes continuaron utilizando el servicio.

La prueba de Mann-Whitney obtuvo un valor p de 1,59 × 10⁻⁷⁹ y un delta de Cliff de -0,562, lo que evidencia una diferencia estadísticamente significativa y un efecto de magnitud considerable. Al igual que en los segundos de uso, el signo negativo indica que los valores tienden a ser menores en el grupo que abandonó.

Este resultado sugiere que el valor del cliente puede aportar información para diferenciar los perfiles de quienes abandonan y quienes permanecen. Además, al analizarlo junto con los segundos de uso, se observa que los clientes que abandonaron no solo registraron una menor utilización del servicio, sino también un menor valor en esta variable.

Para la empresa, esta característica puede ser útil al momento de analizar qué clientes presentan diferentes perfiles de comportamiento y cómo distribuir los esfuerzos de retención. Sin embargo, un menor valor del cliente no debe interpretarse automáticamente como una mayor probabilidad de abandono, sino como una característica que debe evaluarse junto con otras señales.

**Figura:** caracterizacion_valor_cliente.
![Distribución del valor del cliente](../reports/figures/caracterizacion_valor_cliente.png)

## Hallazgo 5. El plan de tarifa presenta diferencias en la proporción de clientes que abandonan.

Los resultados muestran diferencias entre los clientes según el tipo de plan tarifario. Los clientes con plan de pago por uso (nivel 1) registraron una tasa de abandono del 16,8 %, mientras que aquellos con plan contractual (nivel 2) presentaron una tasa del 2,6 %. La diferencia entre ambos grupos es de aproximadamente 14,2 puntos porcentuales.

La prueba chi-cuadrado obtuvo un valor p de 2,64 × 10⁻⁸, lo que indica que existe una asociación estadísticamente significativa entre el plan tarifario y la condición de abandono. En los datos analizados, los clientes con plan de pago por uso presentan una mayor proporción de abandono que aquellos con plan contractual.

Este resultado permite reconocer que las condiciones de contratación también pueden estar relacionadas con el comportamiento de los clientes. Por lo tanto, el tipo de plan puede complementar la información obtenida de las variables de uso y de experiencia del servicio para caracterizar diferentes perfiles de abandono.

Para el proyecto, esta diferencia puede ser útil al momento de identificar grupos de clientes que requieren un análisis más detallado y evaluar si las estrategias de retención deberían considerar las condiciones de contratación.

**Figura:** caracterizacion_plan_tarifa.
![Tasa de abandono según plan de tarifa](../reports/figures/caracterizacion_plan_tarifa.png)

## Conclusión general.

En conclusión, los resultados muestran que el abandono está asociado con diferencias en la experiencia del cliente, la utilización del servicio, el valor registrado y las condiciones de contratación. Las quejas y el estado del cliente presentan las diferencias más marcadas en las variables categóricas, mientras que los segundos de uso y el valor del cliente destacan entre las variables numéricas por sus diferencias entre grupos y la magnitud de sus efectos.

También se encontró que la frecuencia de llamadas, los números distintos contactados y la frecuencia de SMS presentan diferencias estadísticamente significativas entre quienes abandonan y quienes permanecen, a diferencia de los meses de suscripción y las fallas en llamadas que no mostraron diferencias estadísticamente significativas en esta comparación.

Estos resultados permiten reconocer características que podrían aportar información para identificar clientes con mayor riesgo de abandono. Sin embargo, la caracterización por sí sola no permite establecer qué clientes abandonarán en el futuro. Por ello, estos hallazgos servirán como base para la siguiente etapa del proyecto: evaluar la capacidad de los modelos predictivos para identificar y priorizar anticipadamente a los clientes que requieren acciones de retención.