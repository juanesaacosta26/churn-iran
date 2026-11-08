# Regresión logística bayesiana con rstanarm, siguiendo el documento del curso
# ("Modelo Bayesiano de Regresión Logística", ejemplo del Titanic).
#
# Es el mismo modelo que scripts/bayes.py (Python): mismas 10 variables, misma partición
# (data/processed/particion.csv), previas de la literatura (principal) y normal(0, 2.5) (comparación). Sirve para contrastar las cifras con
# Stan. Correr desde la raíz del repositorio, DESPUÉS de python scripts/entrenar.py:
#     Rscript scripts/bayes_rstanarm.R
#
# install.packages(c("rstanarm", "bayesplot", "dplyr"))

library(rstanarm)
library(bayesplot)
library(dplyr)

clientes  <- read.csv("data/processed/clientes.csv")
particion <- read.csv("data/processed/particion.csv")
datos <- clientes %>% inner_join(particion, by = "fila_original")
ent <- datos %>% filter(conjunto == "entrenamiento")   # 2137 clientes
pru <- datos %>% filter(conjunto == "prueba")          # 713 clientes

formula <- churn ~ fallas_llamada + quejas + segundos_uso + frecuencia_sms +
  numeros_distintos + meses_suscripcion + nivel_cobro + plan_tarifa + estado + edad

# 1. Logística clásica (máxima verosimilitud) ---------------------------------
modelo_clasico <- glm(formula, data = ent, family = binomial(link = "logit"))
print(summary(modelo_clasico))
print(round(exp(cbind(OR = coef(modelo_clasico), confint.default(modelo_clasico))), 4))

# 2. Logística bayesiana ---------------------------------------------------------
# PRINCIPAL: previas sustentadas en la literatura (docs/fuentes_previas.md), en escala ORIGINAL
# (autoscale = FALSE). Estado N(1.46, 1) y queja N(0.54, 1): Ahn, Han y Lee (2006);
# meses N(-0.027, 0.03): operador del Reino Unido (arXiv:1607.07792). Las demás variables,
# N(0, 2.5 / sd(x)), que equivale a Normal(0, 2.5) por desviación estándar.
vars <- c("fallas_llamada", "quejas", "segundos_uso", "frecuencia_sms", "numeros_distintos",
          "meses_suscripcion", "nivel_cobro", "plan_tarifa", "estado", "edad")
s_x <- sapply(ent[vars], function(v) sqrt(mean((v - mean(v))^2)))   # desviación como en Python
loc <- setNames(rep(0, length(vars)), vars)
esc <- 2.5 / s_x
loc["estado"] <- 1.46;              esc["estado"] <- 1.0
loc["quejas"] <- 0.54;              esc["quejas"] <- 1.0
loc["meses_suscripcion"] <- -0.027; esc["meses_suscripcion"] <- 0.03

modelo_bayesiano <- stan_glm(
  formula,
  data = ent,
  family = binomial(link = "logit"),
  prior = normal(location = unname(loc), scale = unname(esc), autoscale = FALSE),
  prior_intercept = normal(location = 0, scale = 2.5),
  chains = 4, iter = 3000, warmup = 1000,   # 4 x 2000 = 8000 muestras posteriores
  seed = 42
)
prior_summary(modelo_bayesiano)

# COMPARACIÓN: previa débilmente informativa (por defecto de rstanarm, autoscale = TRUE)
modelo_debil <- stan_glm(
  formula, data = ent, family = binomial(link = "logit"),
  prior = normal(location = 0, scale = 2.5),
  prior_intercept = normal(location = 0, scale = 2.5),
  chains = 4, iter = 3000, warmup = 1000, seed = 42
)
print(round(exp(cbind(literatura = coef(modelo_bayesiano), debil = coef(modelo_debil))), 3))

# Resumen: media, DE, cuantiles 2.5 % y 97.5 %, n_eff y Rhat
print(summary(modelo_bayesiano, probs = c(0.025, 0.975), digits = 4))

# Razones de momios OR = e^beta con su intervalo de credibilidad del 95 %
post <- as.matrix(modelo_bayesiano)
tabla_or <- data.frame(
  media_beta = colMeans(post),
  OR         = exp(colMeans(post)),
  OR_2.5     = exp(apply(post, 2, quantile, 0.025)),
  OR_97.5    = exp(apply(post, 2, quantile, 0.975)),
  P_beta_pos = colMeans(post > 0)
)
print(round(tabla_or, 4))

# Densidades posteriores (como mcmc_areas del documento)
p <- mcmc_areas(modelo_bayesiano,
                pars = c("quejas", "estado", "fallas_llamada", "nivel_cobro", "plan_tarifa", "edad"),
                prob = 0.95)
ggplot2::ggsave("reports/figures/bayes_mcmc_areas_R.png", p, width = 8, height = 6, dpi = 150)

# Diagnósticos y chequeo predictivo posterior
print(max(summary(modelo_bayesiano)[, "Rhat"]))
pp <- pp_check(modelo_bayesiano, plotfun = "stat", stat = "mean")
ggplot2::ggsave("reports/figures/bayes_pp_check_R.png", pp, width = 6, height = 4, dpi = 150)

# 3. Comparación en los 713 clientes de prueba ----------------------------------
prob_bayes   <- colMeans(posterior_epred(modelo_bayesiano, newdata = pru))
prob_clasica <- predict(modelo_clasico, newdata = pru, type = "response")
print(summary(abs(prob_bayes - prob_clasica)))

# 4. ¿En qué medida? Modelo sin estado ni quejas, comparado con LOO
sin <- setdiff(vars, c("estado", "quejas"))
modelo_sin <- update(modelo_bayesiano, formula = . ~ . - estado - quejas,
                     prior = normal(location = unname(loc[sin]), scale = unname(esc[sin]), autoscale = FALSE))
print(loo_compare(loo(modelo_bayesiano), loo(modelo_sin)))
