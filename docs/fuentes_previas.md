# Fuentes de las previas y de la elección del muestreo

Este documento sustenta las dos versiones (la de la literatura es la principal) de la logística bayesiana (`src/churn/bayes.py`,
`scripts/bayes.py`) y la elección del MCMC. Las cifras de los resultados están en
`reports/tablas/bayes_previas_*.csv`, `bayes_laplace_vs_mcmc.csv` y `bayes_eficiencia_mcmc.csv`.

## 1. Dos versiones del modelo

| Versión | Para qué | Previas |
|---|---|---|
| **Sustentada en la literatura** (principal) | Usar lo que ya se sabía del churn en telecomunicaciones antes de ver estos datos | Estado, queja y antigüedad centradas en efectos publicados; el intercepto y las otras 7 variables, débilmente informativas |
| **Débilmente informativa** (comparación) | Ver cuánto pesa la literatura: que los datos hablen casi solos, con una previa que solo descarta efectos absurdos | Intercepto y todos los β ~ Normal(0, 2.5) por desviación estándar de cada variable (Gelman et al., 2008; previas por defecto de `rstanarm`) |

**Regla:** ninguna previa sale de esta base ni de Keramati et al. (2014), que publica los mismos
3150 clientes. Si se usaran, la misma información entraría dos veces: en la previa y en la
verosimilitud.

## 2. ¿Hay registros históricos de churn del operador o de Irán?

No encontramos una tasa de churn publicada para el operador (Hamrah-e Aval, MCI) ni para el mercado
iraní.

- **Keramati et al. (2014)**, el artículo que publicó la base, describe 3150 clientes tomados al azar
  de la base de datos del centro de llamadas de un operador iraní durante 12 meses, con 495
  abandonos (15.7 %). Ubica las quejas entre las variables más influyentes. No da tasas de mercado.
- **Estudios con encuestas en Irán:** *A model for customer churn prediction in the Iranian
  telecommunication companies* (2016; 420 encuestados de un operador) y un estudio sobre clientes
  pospago de MCI en Zahedan (IAU). Identifican factores (calidad del servicio, insatisfacción,
  barreras de cambio, antigüedad de la SIM), pero no reportan efectos numéricos utilizables.

Lo que sí existe son **tasas del sector y efectos publicados en otros mercados**, y con eso se
construyen las previas.

## 3. Previas sustentadas en la literatura (modelo principal)

La desviación de cada previa se **ensancha** frente al error estándar publicado, porque la
evidencia viene de otro país, otra época y, en algunos casos, otra definición de la variable. Es un
"descuento" de la información externa, en la lógica de las *power priors* (Ibrahim y Chen, 2000).
La conversión a la escala del modelo es β* = β · s, donde s es la desviación estándar de la
variable en entrenamiento.

| Parámetro | Evidencia publicada | Previa (escala original) | Qué admite al 95 % |
|---|---|---|---|
| Estado no activo | Cliente "sin uso" frente a activo: β = 1.455 (EE 0.349), OR ≈ 4.3. Operador coreano, 5789 clientes (Ahn, Han y Lee, 2006) | β ~ Normal(1.46, 1.0) | OR entre 0.61 y 30.6 |
| Queja | Cada queja: β = 0.538 (EE 0.323), OR ≈ 1.7, p < 0.10 (Ahn, Han y Lee, 2006). Aquí la variable es "alguna queja" (0/1), no un conteo; por eso la desviación triplica el EE | β ~ Normal(0.54, 1.0) | OR entre 0.24 y 12.2 |
| Meses de suscripción | Cada mes de antigüedad: Exp(B) = 0.974, B = −0.027 (Wald 105.6, EE ≈ 0.003). Operador del Reino Unido (arXiv:1607.07792) | β ~ Normal(−0.027, 0.03) por mes | OR por 6 meses entre 0.60 y 1.21 |
| Intercepto | Las tasas del sector son promedios (ver sección 4), no el riesgo del cliente con variables promedio. No se transfiere | Normal(0, 2.5) | Riesgo entre 0.7 % y 99 % |
| Fallas, segundos, SMS, números distintos, nivel de cobro, plan, edad | Sin evidencia transferible: Ahn et al. miden la *tasa* de llamadas caídas (%), no el conteo; el estudio británico mide *cambios* de uso, no niveles | Normal(0, 2.5) por desviación estándar | Débilmente informativa |

Las tres previas informadas admiten el "sin efecto" (OR = 1) dentro de su rango del 95 %. Orientan
la dirección y el tamaño esperado, pero dejan que los datos contradigan a la literatura si es el
caso.

**Sensibilidad al descuento.** Como el "cuánto descontar" es una decisión, se repitió el modelo
multiplicando las tres desviaciones por 0.5, 2 y 4, y con la previa débil
(`bayes_sensibilidad_previa.csv`). Solo el OR de la queja depende de esa elección (de 21 a 47), y
siempre queda muy lejos de 1.

## 4. Tasas de churn del sector (contraste, no previa)

| Fuente | Tasa | Mercado |
|---|---|---|
| Ahn, Han y Lee (2006) | 16.9 % (2003) y 20.0 % (2004) al año; 11.3 % en su muestra de 8 meses | Corea, telefonía móvil |
| Ovum, citado en RCR Wireless (2014) | Pospago: < 2 % mensual se considera aceptable (≈ 22 % al año). Prepago: < 5 % mensual (≈ 2/3 al año) | Mundial |
| Strategy Analytics para Juvo, citado en Capacity | Prepago: 37 % a 80 % al año | 7 mercados emergentes |

**Por qué no sirven como previa del intercepto.** Una tasa de mercado es el promedio de abandono
(una cantidad marginal). El intercepto del modelo es el log-momio del cliente con **todas las
variables en su promedio** (una cantidad condicional). En esta base ese cliente tiene ≈ 3 % de
riesgo, aunque la tasa promedio sea 15.6 %, porque el abandono se concentra en quienes se quejan o
están inactivos. Las dos cantidades no son la misma, y forzar 20 % en el intercepto contradice a
los datos sin que haya evidencia de por medio.

**Para qué sí sirven.** Como contraste del modelo: en el chequeo predictivo, la tasa simulada
(15.7 %, entre 14.1 % y 17.3 %) queda algo por debajo del rango coreano (17–20 %) y muy por debajo
del prepago emergente (37–80 %). Es coherente con un sesgo de supervivencia: la base solo incluye
clientes con al menos 3 meses de antigüedad y activos durante los 9 meses observados (Avance 2,
paso 5).

## 5. ¿Por qué muestreo Monte Carlo (MCMC) y por qué HMC?

**La posterior no tiene fórmula cerrada.** La verosimilitud logística no tiene una previa conjugada,
así que P(β | datos) se conoce solo salvo una constante: una integral en 11 dimensiones.

| Alternativa | Qué pasa con estos datos |
|---|---|
| Cuadrícula | 100 valores por parámetro dan 100¹¹ evaluaciones: inviable |
| Aproximación de Laplace (normal en la moda) | Supone simetría. El OR de la queja es asimétrico (sesgo 1.06) y el del plan aún más (2.53). Laplace da para la queja 33.2 (19.2–57.4) y MCMC 35.3 (20.4–62.3): recorta la cola derecha. Para el plan da 0.93 (0.23–3.83) frente a 0.82 (0.17–3.24) |
| Inferencia variacional | Rápida, pero tiende a subestimar la varianza posterior (Blei et al., 2017), que es justo lo que se quiere reportar |
| **MCMC** | Converge a la posterior exacta. Con las muestras se calcula cualquier cosa: OR, P(OR > 10), la probabilidad de cada cliente, el chequeo predictivo. Además trae diagnósticos de convergencia (R̂, n_eff) |

**Dentro de MCMC, ¿por qué Monte Carlo hamiltoniano (HMC)?**

- **Gibbs** necesita las distribuciones condicionales completas. En la logística no son estándar sin
  aumentar los datos (Pólya-Gamma; Polson et al., 2013).
- **Metropolis de paseo aleatorio** sirve, pero con 11 parámetros correlacionados avanza a pasos
  cortos. Se corrió con la misma covarianza de Laplace y la escala óptima 2.38/√d (Gelman, Roberts y
  Gilks, 1996), 4 × 2000 muestras:

| Método | n_eff/N mínimo | R̂ máximo | Tiempo |
|---|---|---|---|
| **HMC (usado)** | **0.56** | **1.003** | 16 s |
| Metropolis de paseo aleatorio | 0.020 | 1.028 (no cumple < 1.01) | 1.6 s |

HMC da unas **28 veces más muestras efectivas por iteración**, y unas 3 veces más por segundo. Con
el mismo número de muestras, Metropolis no alcanza la convergencia exigida. HMC usa el gradiente de
la log-posterior para proponer saltos largos que igual se aceptan (Neal, 2011; Hoffman y Gelman,
2014). Es el algoritmo de Stan, `rstanarm` y PyMC.

## Referencias

Ahn, J.-H., Han, S.-P., & Lee, Y.-S. (2006). Customer churn analysis: Churn determinants and
mediation effects of partial defection in the Korean mobile telecommunications service industry.
*Telecommunications Policy, 30*(10–11), 552–568. https://pages.stern.nyu.edu/~shan2/customerchurn.pdf

Blei, D. M., Kucukelbir, A., & McAuliffe, J. D. (2017). Variational inference: A review for
statisticians. *Journal of the American Statistical Association, 112*(518), 859–877.

Capacity Media. (s. f.). *Operators spend 90% of subscriber acquisition budget on countering churn*
[informe de Strategy Analytics para Juvo].
https://capacitymedia.com/articles/3823134/operators-spend-90-of-subscriber-acquisition-budget-on-countering-churn

Customer churn in mobile markets: A comparison of techniques. (2016). arXiv:1607.07792.
https://arxiv.org/pdf/1607.07792

Gelman, A., Jakulin, A., Pittau, M. G., & Su, Y.-S. (2008). A weakly informative default prior
distribution for logistic and other regression models. *The Annals of Applied Statistics, 2*(4),
1360–1383.

Gelman, A., Roberts, G. O., & Gilks, W. R. (1996). Efficient Metropolis jumping rules. En
*Bayesian Statistics 5* (pp. 599–607). Oxford University Press.

Hoffman, M. D., & Gelman, A. (2014). The No-U-Turn sampler: Adaptively setting path lengths in
Hamiltonian Monte Carlo. *Journal of Machine Learning Research, 15*, 1593–1623.

Ibrahim, J. G., & Chen, M.-H. (2000). Power prior distributions for regression models.
*Statistical Science, 15*(1), 46–60.
https://projecteuclid.org/journals/statistical-science/volume-15/issue-1/Power-prior-distributions-for-regression-models/10.1214/ss/1009212673.pdf

Keramati, A., Jafari-Marandi, R., Aliannejadi, M., Ahmadian, I., Mozaffari, M., & Abbasi, U. (2014).
Improved churn prediction in telecommunication industry using data mining techniques.
*Applied Soft Computing, 24*, 994–1012.
https://adiwijaya.staff.telkomuniversity.ac.id/files/2014/02/keramati2014-Improved-churn-prediction-in-telecommunication-industry-using-data-mining-techniques.pdf

Meyer, D. (2014, 6 de noviembre). Ovum: Churn remains hurdle for mobile operators worldwide.
*RCR Wireless News*.
https://rcrwireless.com/20141106/big-data-analytics/ovum-churn-remains-hurdle-for-mobile-operators-worldwide-tag2

A model for customer churn prediction in the Iranian telecommunication companies. (2016).
*Journal of Management and Development Process, 29*(2), 99–116.
https://www.magiran.com/paper/1683603?lang=en

Neal, R. M. (2011). MCMC using Hamiltonian dynamics. En S. Brooks, A. Gelman, G. Jones y X.-L. Meng
(Eds.), *Handbook of Markov Chain Monte Carlo* (pp. 113–162). Chapman & Hall/CRC.

Polson, N. G., Scott, J. G., & Windle, J. (2013). Bayesian inference for logistic models using
Pólya-Gamma latent variables. *Journal of the American Statistical Association, 108*(504), 1339–1349.

Study affective variables in mobile customers churn. (s. f.). Islamic Azad University.
https://sanad.iau.ir/en/Article/950010
