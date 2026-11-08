"""Regresión logística bayesiana. Dueño: Juanes (estadística bayesiana, entrega del 6 de noviembre).

Modelo
------
    churn_i ~ Bernoulli(π_i),   logit(π_i) = α + Σ_j β_j · z_ij
    α   ~ Normal(0, 2.5)      (intercepto con las variables centradas)
    β_j ~ Normal(0, 2.5)      (por desviación estándar de la variable j)

Son las previas débilmente informativas por defecto de rstanarm::stan_glm, las mismas del
documento del curso (`prior = normal(location = 0, scale = 2.5)`): rstanarm las escala por la
desviación estándar de cada predictor, que es lo mismo que estandarizar aquí.
z_ij son las variables estandarizadas con la media y la desviación del ENTRENAMIENTO.
Los coeficientes se devuelven también en la escala ORIGINAL (por unidad de cada variable),
que es la que se interpreta como razón de momios OR = e^β.

Muestreo
--------
Monte Carlo hamiltoniano (HMC) programado aquí con numpy, sin dependencias nuevas:
- matriz de masa = covarianza de la aproximación de Laplace (precondicionamiento);
- paso ajustado en el calentamiento por promedio dual (Hoffman y Gelman, 2014) hacia
  una aceptación de 0.8; número de pasos de leapfrog aleatorio para evitar periodicidad;
- 4 cadenas que arrancan dispersas alrededor de la moda.

Diagnósticos
------------
R̂ con normalización por rangos y cadenas divididas, y tamaño efectivo de muestra (ESS)
de bulk y de cola (Vehtari et al., 2021), divergencias y tasa de aceptación.
El mismo modelo en R con rstanarm, como en el documento del curso: scripts/bayes_rstanarm.R.
"""
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import optimize, stats
from scipy.special import expit, log_expit

from churn import config

# ---------------------------------------------------------------------------
# Modelo


@dataclass
class Previa:
    mu_alfa: float = 0.0
    sd_alfa: float = 2.5
    sd_beta: object = 2.5      # número o vector (escala estandarizada)
    mu_beta: object = 0.0      # número o vector (escala estandarizada)


@dataclass
class Escalador:
    media: np.ndarray
    desv: np.ndarray

    @classmethod
    def ajustar(cls, X: pd.DataFrame):
        return cls(X.mean().to_numpy(float), X.std(ddof=0).to_numpy(float))

    def transformar(self, X: pd.DataFrame) -> np.ndarray:
        return (X.to_numpy(float) - self.media) / self.desv


def _diseno(Z: np.ndarray) -> np.ndarray:
    return np.column_stack([np.ones(len(Z)), Z])


def log_posterior(theta, A, y, previa: Previa):
    """log p(θ | datos) salvo constante, y su gradiente. A = [1, Z]."""
    eta = A @ theta
    loglik = np.sum(y * log_expit(eta) + (1 - y) * log_expit(-eta))
    k = len(theta) - 1
    sd = np.r_[previa.sd_alfa, np.broadcast_to(previa.sd_beta, k)]
    mu = np.r_[previa.mu_alfa, np.broadcast_to(previa.mu_beta, k)]
    logprior = -0.5 * np.sum(((theta - mu) / sd) ** 2)
    grad = A.T @ (y - expit(eta)) - (theta - mu) / sd**2
    return loglik + logprior, grad


def laplace(A, y, previa: Previa):
    """Moda posterior y covarianza (inversa del hessiano) de la aproximación normal."""
    f = lambda t: tuple(-v for v in log_posterior(t, A, y, previa))  # noqa: E731
    k = A.shape[1] - 1
    t0 = np.r_[previa.mu_alfa, np.broadcast_to(previa.mu_beta, k)]
    res = optimize.minimize(f, t0, jac=True, method="BFGS")
    p = expit(A @ res.x)
    sd = np.r_[previa.sd_alfa, np.broadcast_to(previa.sd_beta, k)]
    H = (A * (p * (1 - p))[:, None]).T @ A + np.diag(1 / sd**2)
    return res.x, np.linalg.inv(H)


# ---------------------------------------------------------------------------
# HMC


@dataclass
class Muestras:
    draws: np.ndarray            # (cadenas, iteraciones, parámetros)
    nombres: list
    aceptacion: np.ndarray       # por cadena
    divergencias: np.ndarray     # por cadena
    paso: np.ndarray             # tamaño de paso final por cadena
    escalador: Escalador = None
    previa: Previa = field(default_factory=Previa)
    variables: list = None

    def planas(self) -> np.ndarray:
        return self.draws.reshape(-1, self.draws.shape[-1])


def _cadena(A, y, previa, theta0, cov, warmup, draws, rng, objetivo=0.8):
    L_chol = np.linalg.cholesky(cov)          # p = L^{-T} r  →  energía cinética r·r/2
    d = len(theta0)
    theta = theta0.copy()
    lp, g = log_posterior(theta, A, y, previa)
    # promedio dual
    eps, mu, log_eps_bar, h_bar, gamma, t0, kappa = 0.5, np.log(5 * 0.5), 0.0, 0.0, 0.05, 10, 0.75
    salida = np.empty((draws, d))
    acept, diverg = 0.0, 0
    for it in range(warmup + draws):
        n_pasos = rng.integers(5, 16)
        r = rng.standard_normal(d)                  # momento en el espacio blanqueado
        th, gr, lp_new = theta.copy(), g.copy(), lp
        h0 = -lp + 0.5 * r @ r
        r = r + 0.5 * eps * (L_chol.T @ gr)
        ok = True
        for k in range(n_pasos):
            th = th + eps * (L_chol @ r)
            lp_new, gr = log_posterior(th, A, y, previa)
            if not np.isfinite(lp_new):
                ok = False
                break
            if k < n_pasos - 1:
                r = r + eps * (L_chol.T @ gr)
        r = r + 0.5 * eps * (L_chol.T @ gr)
        h1 = -lp_new + 0.5 * r @ r if ok else np.inf
        dif = h0 - h1
        a = 1.0 if dif > 0 else float(np.exp(dif)) if np.isfinite(dif) else 0.0
        if rng.random() < a:
            theta, lp, g = th, lp_new, gr
        if it < warmup:
            m = it + 1
            h_bar = (1 - 1 / (m + t0)) * h_bar + (objetivo - a) / (m + t0)
            log_eps = mu - np.sqrt(m) / gamma * h_bar
            eps = float(np.exp(log_eps))
            log_eps_bar = m**-kappa * log_eps + (1 - m**-kappa) * log_eps_bar
            if it == warmup - 1:
                eps = float(np.exp(log_eps_bar))
        else:
            salida[it - warmup] = theta
            acept += a
            diverg += int((not np.isfinite(dif)) or (-dif > 1000))
    return salida, acept / draws, diverg, eps


def ajustar(X: pd.DataFrame, y: pd.Series, previa: Previa | None = None,
            cadenas: int = 4, calentamiento: int = 1000, iteraciones: int = 2000,
            semilla: int = config.SEMILLA) -> Muestras:
    """Ajusta la logística bayesiana con HMC y devuelve las muestras posteriores."""
    previa = previa or Previa()
    esc = Escalador.ajustar(X)
    A = _diseno(esc.transformar(X))
    yv = y.to_numpy(float)
    moda, cov = laplace(A, yv, previa)
    rng = np.random.default_rng(semilla)
    res = []
    for c in range(cadenas):
        inicio = moda + 2 * np.linalg.cholesky(cov) @ rng.standard_normal(len(moda))  # dispersas
        res.append(_cadena(A, yv, previa, inicio, cov, calentamiento, iteraciones,
                           np.random.default_rng(semilla + 100 + c)))
    return Muestras(
        draws=np.stack([r[0] for r in res]),
        nombres=["intercepto"] + list(X.columns),
        aceptacion=np.array([r[1] for r in res]),
        divergencias=np.array([r[2] for r in res]),
        paso=np.array([r[3] for r in res]),
        escalador=esc, previa=previa, variables=list(X.columns),
    )


# ---------------------------------------------------------------------------
# Diagnósticos (Vehtari, Gelman, Simpson, Carpenter y Bürkner, 2021)


def _dividir(x):                     # (cadenas, n) -> (2·cadenas, n/2)
    n = x.shape[1] // 2
    return np.concatenate([x[:, :n], x[:, n:2 * n]])


def _normalizar_rangos(x):
    r = stats.rankdata(x, method="average").reshape(x.shape)
    return stats.norm.ppf((r - 0.375) / (x.size + 0.25))


def _rhat_basico(x):
    m, n = x.shape
    B = n * x.mean(axis=1).var(ddof=1)
    W = x.var(axis=1, ddof=1).mean()
    return np.sqrt(((n - 1) / n * W + B / n) / W)


def _ess_basico(x):
    m, n = x.shape
    xc = x - x.mean(axis=1, keepdims=True)
    f = np.fft.rfft(xc, n=2 * n, axis=1)
    acov = np.fft.irfft(f * np.conj(f), axis=1)[:, :n] / n
    W = x.var(axis=1, ddof=1).mean()
    var_mas = (n - 1) / n * W + x.mean(axis=1).var(ddof=1)
    # forma de Stan: rho_t = 1 - (W - media de las autocovarianzas en t) / var_mas
    acov_media = acov.mean(axis=0)
    rho = 1 - (W - acov_media) / var_mas
    rho[0] = 1.0
    # secuencia inicial monótona de Geyer sobre pares
    pares = rho[:-1:2] + rho[1::2]
    k = np.argmax(pares < 0) if np.any(pares < 0) else len(pares)
    pares = np.minimum.accumulate(pares[:k])
    tau = -1 + 2 * pares.sum()
    return m * n / max(tau, 1 / np.log10(m * n))


def rhat(x):
    """R̂ por rangos con cadenas divididas: máx. entre bulk y versión 'doblada'."""
    s = _dividir(x)
    plegada = np.abs(s - np.median(s))
    return max(_rhat_basico(_normalizar_rangos(s)), _rhat_basico(_normalizar_rangos(plegada)))


def ess_bulk(x):
    return _ess_basico(_normalizar_rangos(_dividir(x)))


def ess_cola(x):
    s = _dividir(x)
    q05, q95 = np.quantile(s, [0.05, 0.95])
    return min(_ess_basico((s <= q05).astype(float)), _ess_basico((s <= q95).astype(float)))


def hdi(v, prob=0.95):
    """Intervalo de máxima densidad posterior (el más corto que contiene `prob`)."""
    v = np.sort(v)
    n = len(v)
    k = int(np.floor(prob * n))
    anchos = v[k:] - v[: n - k]
    i = int(np.argmin(anchos))
    return v[i], v[i + k]


def resumen(m: Muestras) -> pd.DataFrame:
    """Una fila por parámetro: media, desviación, HDI 95 %, P(β>0), razones de momios,
    R̂ y ESS."""
    filas = []
    plano = m.planas()
    for j, nombre in enumerate(m.nombres):
        v = plano[:, j]
        lo, hi = hdi(v)
        fila = {"parametro": nombre, "media": v.mean(), "desv": v.std(ddof=1),
                "hdi_2.5": lo, "hdi_97.5": hi, "prob_positivo": (v > 0).mean()}
        if j > 0:
            sd_x = m.escalador.desv[j - 1]
            fila["rm_1de"] = float(np.exp(np.median(v)))          # mediana posterior de exp(β)
            fila["rm_1de_hdi_2.5"], fila["rm_1de_hdi_97.5"] = np.exp(lo), np.exp(hi)
            fila["de_variable"] = sd_x
            fila["rm_por_unidad"] = float(np.exp(np.median(v) / sd_x))
            fila["rm_unidad_hdi_2.5"], fila["rm_unidad_hdi_97.5"] = np.exp(lo / sd_x), np.exp(hi / sd_x)
        fila["rhat"] = rhat(m.draws[:, :, j])
        fila["ess_bulk"] = ess_bulk(m.draws[:, :, j])
        fila["ess_cola"] = ess_cola(m.draws[:, :, j])
        filas.append(fila)
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# Predicción, chequeo predictivo y comparación de modelos


def prob_posterior(m: Muestras, X: pd.DataFrame, max_draws: int | None = None) -> np.ndarray:
    """Matriz (muestras, clientes) con p_i para cada muestra posterior."""
    th = m.planas()
    if max_draws and len(th) > max_draws:
        th = th[np.linspace(0, len(th) - 1, max_draws).astype(int)]
    A = _diseno(m.escalador.transformar(X[m.variables]))
    return expit(A @ th.T).T


def log_lik(m: Muestras, X: pd.DataFrame, y: pd.Series, max_draws=4000) -> np.ndarray:
    th = m.planas()
    if len(th) > max_draws:
        th = th[np.linspace(0, len(th) - 1, max_draws).astype(int)]
    A = _diseno(m.escalador.transformar(X[m.variables]))
    eta = A @ th.T                                   # (clientes, muestras)
    yv = y.to_numpy(float)[:, None]
    return (yv * log_expit(eta) + (1 - yv) * log_expit(-eta)).T


def waic(ll: np.ndarray) -> dict:
    """WAIC (Watanabe, 2010) en escala elpd: más alto es mejor."""
    lppd_i = np.log(np.mean(np.exp(ll - ll.max(axis=0)), axis=0)) + ll.max(axis=0)
    p_i = ll.var(axis=0, ddof=1)
    elpd_i = lppd_i - p_i
    return {"elpd_waic": elpd_i.sum(), "se": np.sqrt(len(elpd_i) * elpd_i.var(ddof=1)),
            "p_waic": p_i.sum(), "puntual": elpd_i}


def elpd_prueba(ll: np.ndarray) -> dict:
    """Densidad predictiva logarítmica en los clientes de prueba (no vistos)."""
    mx = ll.max(axis=0)
    lpd_i = np.log(np.mean(np.exp(ll - mx), axis=0)) + mx
    return {"elpd_prueba": lpd_i.sum(), "se": np.sqrt(len(lpd_i) * lpd_i.var(ddof=1)), "puntual": lpd_i}


def chequeo_predictivo(m: Muestras, df: pd.DataFrame, grupos=("quejas", "estado", "plan_tarifa"),
                       semilla=config.SEMILLA, max_draws=4000) -> pd.DataFrame:
    """Simula bases replicadas y compara la tasa de abandono observada (total y por
    grupo) con su distribución predictiva posterior. p_predictivo cerca de 0 o 1 = mal ajuste."""
    rng = np.random.default_rng(semilla)
    P = prob_posterior(m, df, max_draws)
    yrep = rng.random(P.shape) < P
    y = df[config.OBJETIVO].to_numpy()
    filas = []

    def fila(nombre, mascara):
        sim = yrep[:, mascara].mean(axis=1)
        obs = y[mascara].mean()
        lo, hi = np.quantile(sim, [0.025, 0.975])
        filas.append({"grupo": nombre, "n": int(mascara.sum()), "tasa_observada": obs,
                      "tasa_simulada_media": sim.mean(), "sim_2.5": lo, "sim_97.5": hi,
                      "p_predictivo": (sim >= obs).mean()})

    fila("Total", np.ones(len(df), bool))
    for g in grupos:
        for nivel in sorted(df[g].unique()):
            etiqueta = config.ETIQUETAS.get(g, {}).get(nivel, nivel)
            fila(f"{g} = {etiqueta}", (df[g] == nivel).to_numpy())
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# Escala original, tabla del curso y logística clásica (máxima verosimilitud)

# Unidad en que se lee cada razón de momios (el curso lee "por cada año de edad").
UNIDADES = {
    "fallas_llamada": (1, "por cada falla de llamada adicional"),
    "quejas": (1, "con queja frente a sin queja"),
    "segundos_uso": (1000, "por cada 1000 segundos (≈ 17 min) más de uso"),
    "frecuencia_sms": (10, "por cada 10 SMS más"),
    "numeros_distintos": (10, "por cada 10 números distintos más"),
    "meses_suscripcion": (6, "por cada 6 meses más de suscripción"),
    "nivel_cobro": (1, "por cada nivel de cobro más"),
    "plan_tarifa": (1, "contrato frente a pago por uso"),
    "estado": (1, "no activo frente a activo"),
    "edad": (10, "por cada 10 años más de edad"),
}


def a_escala_original(theta_std: np.ndarray, esc: Escalador) -> np.ndarray:
    """Convierte (…, 1+k) coeficientes estandarizados a la escala original:
    β_j = β*_j / s_j,   α = α* − Σ β*_j · m_j / s_j."""
    th = np.atleast_2d(theta_std)
    b = th[:, 1:] / esc.desv
    a = th[:, 0] - b @ esc.media
    out = np.column_stack([a, b])
    return out if np.ndim(theta_std) > 1 else out[0]


def _matriz_t(esc: Escalador) -> np.ndarray:
    k = len(esc.desv)
    T = np.zeros((k + 1, k + 1))
    T[0, 0] = 1
    T[0, 1:] = -esc.media / esc.desv
    T[1:, 1:] = np.diag(1 / esc.desv)
    return T


def tabla_curso(m: Muestras) -> pd.DataFrame:
    """Resumen como en el documento del curso (salida de summary() de rstanarm), en la
    escala original: media, DE, cuantiles 2.5/50/97.5, n_eff, n_eff/N y R̂; y la tabla de
    razones de momios OR = e^β con su intervalo de credibilidad del 95 %, por unidad y por
    la unidad de interpretación de UNIDADES."""
    orig = a_escala_original(m.planas(), m.escalador)
    cad = orig.reshape(m.draws.shape)
    N = orig.shape[0]
    filas = []
    for j, nombre in enumerate(m.nombres):
        v = orig[:, j]
        q025, q50, q975 = np.quantile(v, [0.025, 0.5, 0.975])
        neff = ess_bulk(cad[:, :, j])
        fila = {"parametro": nombre, "media": v.mean(), "de": v.std(ddof=1),
                "q2.5": q025, "q50": q50, "q97.5": q975,
                "n_eff": neff, "n_eff_N": neff / N, "rhat": rhat(cad[:, :, j]),
                "prob_beta_pos": (v > 0).mean(),
                "or": np.exp(v.mean()), "or_q2.5": np.exp(q025), "or_q97.5": np.exp(q975)}
        if nombre in UNIDADES:
            u, txt = UNIDADES[nombre]
            fila.update({"unidad": u, "lectura": txt, "or_unidad": np.exp(u * v.mean()),
                         "or_unidad_q2.5": np.exp(u * q025), "or_unidad_q97.5": np.exp(u * q975)})
        filas.append(fila)
    return pd.DataFrame(filas)


def logistica_mv(X: pd.DataFrame, y: pd.Series) -> pd.DataFrame:
    """Regresión logística clásica por máxima verosimilitud, sin penalización (equivale a
    glm(family = binomial) en R o a statsmodels.Logit). Errores estándar de Wald desde la
    matriz de información; IC del 95 % y p-valores. Escala original."""
    esc = Escalador.ajustar(X)
    A = _diseno(esc.transformar(X))
    yv = y.to_numpy(float)

    def f(t):
        eta = A @ t
        ll = np.sum(yv * log_expit(eta) + (1 - yv) * log_expit(-eta))
        return -ll, -(A.T @ (yv - expit(eta)))

    res = optimize.minimize(f, np.zeros(A.shape[1]), jac=True, method="BFGS",
                            options={"gtol": 1e-8, "maxiter": 5000})
    p = expit(A @ res.x)
    cov_std = np.linalg.inv((A * (p * (1 - p))[:, None]).T @ A)
    T = _matriz_t(esc)
    th = T @ res.x
    se = np.sqrt(np.diag(T @ cov_std @ T.T))
    z = th / se
    filas = []
    for j, nombre in enumerate(["intercepto"] + list(X.columns)):
        lo, hi = th[j] - 1.959964 * se[j], th[j] + 1.959964 * se[j]
        fila = {"parametro": nombre, "beta": th[j], "ee": se[j], "ic2.5": lo, "ic97.5": hi,
                "z": z[j], "p_valor": 2 * stats.norm.sf(abs(z[j])),
                "or": np.exp(th[j]), "or_ic2.5": np.exp(lo), "or_ic97.5": np.exp(hi)}
        if nombre in UNIDADES:
            u, _ = UNIDADES[nombre]
            fila.update({"or_unidad": np.exp(u * th[j]), "or_unidad_ic2.5": np.exp(u * lo),
                         "or_unidad_ic97.5": np.exp(u * hi)})
        filas.append(fila)
    tabla = pd.DataFrame(filas)
    tabla.attrs["escalador"] = esc
    tabla.attrs["theta_std"] = res.x
    return tabla


def prob_mv(tabla: pd.DataFrame, X: pd.DataFrame) -> np.ndarray:
    th = tabla["beta"].to_numpy()
    return expit(th[0] + X.to_numpy(float) @ th[1:])


# ---------------------------------------------------------------------------
# Previas sustentadas en la literatura (ver docs/fuentes_previas.md)
#
# Cada entrada: (media, desviación) de β en la escala ORIGINAL (por unidad de la variable),
# la evidencia y la fuente. La desviación se ensancha frente al error estándar publicado
# ("descuento", en la lógica de las power priors de Ibrahim y Chen, 2000) porque la evidencia
# viene de otro país, otra época y otra definición de la variable. Las variables sin evidencia
# transferible conservan la previa débilmente informativa Normal(0, 2.5) por desviación estándar.
# Ninguna previa sale de esta base ni de Keramati et al. (2014), que usa los mismos datos.

PREVIA_INTERCEPTO_LITERATURA = {
    # Las tasas de churn del sector describen el PROMEDIO de abandono (marginal), mientras que el
    # intercepto es el log-momio del cliente con todas las variables en su promedio (condicional);
    # en esta base ese cliente tiene ≈ 3 % de riesgo aunque la tasa promedio sea 15.6 %, porque el
    # abandono se concentra en quienes se quejan o están inactivos. Por eso el intercepto conserva la
    # previa débil y las tasas del sector se usan como CONTRASTE de la tasa simulada (chequeo predictivo).
    "media": 0.0, "desv": 2.5,
    "evidencia": "No se transfiere: las tasas del sector (17–20 %/año en Corea; ≈ 22 %/año pospago; "
                 "37–80 %/año prepago emergente) son promedios, no el riesgo del cliente promedio. "
                 "Se usan como contraste de la tasa simulada por el modelo.",
    "fuente": "Ahn, Han y Lee (2006); Ovum vía RCR Wireless (2014); Strategy Analytics vía Capacity",
}

PREVIAS_LITERATURA = {
    "estado": (1.46, 1.0,
               "Estado 'sin uso' frente a activo: β = 1.455 (EE 0.349), OR ≈ 4.3, operador coreano.",
               "Ahn, Han y Lee (2006), tabla de la logística con estado"),
    "quejas": (0.54, 1.0,
               "Cada queja: β = 0.538 (EE 0.323), OR ≈ 1.7 (p < 0.10), operador coreano. Aquí la variable "
               "es 'alguna queja' (0/1), no un conteo; por eso la desviación triplica el EE.",
               "Ahn, Han y Lee (2006)"),
    "meses_suscripcion": (-0.027, 0.03,
                          "Cada mes de antigüedad: B = −0.027, Exp(B) = 0.974 (Wald 105.6, EE ≈ 0.003), "
                          "operador del Reino Unido. Desviación ≈ 10 veces el EE.",
                          "Customer Churn in Mobile Markets: A Comparison of Techniques (arXiv:1607.07792)"),
}


def previa_literatura(esc: Escalador, variables: list, factor: float = 1.0) -> Previa:
    """Previa PRINCIPAL: media y desviación por coeficiente según la literatura donde la hay,
    Normal(0, 2.5) por desviación estándar en el resto. Convierte de escala original a
    estandarizada: β* = β · s_j  →  Normal(m · s_j, d · s_j). `factor` multiplica las desviaciones
    de las previas informadas (sensibilidad al descuento: < 1 confía más en la literatura)."""
    mu = np.zeros(len(variables))
    sd = np.full(len(variables), 2.5)
    for i, v in enumerate(variables):
        if v in PREVIAS_LITERATURA:
            m, d, _, _ = PREVIAS_LITERATURA[v]
            mu[i], sd[i] = m * esc.desv[i], factor * d * esc.desv[i]
    return Previa(mu_alfa=PREVIA_INTERCEPTO_LITERATURA["media"], sd_alfa=PREVIA_INTERCEPTO_LITERATURA["desv"],
                  mu_beta=mu, sd_beta=sd)


def tabla_previas_literatura(variables: list) -> pd.DataFrame:
    """Tabla de las previas usadas: media y desviación de β, OR implícito y su rango al 95 %."""
    filas = [{"parametro": "intercepto (cliente con variables en su promedio)",
              "media_beta": PREVIA_INTERCEPTO_LITERATURA["media"], "desv_beta": PREVIA_INTERCEPTO_LITERATURA["desv"],
              "implica_95": "débilmente informativa: Normal(0, 2.5); riesgo entre {:.1%} y {:.1%}".format(
                  *expit(PREVIA_INTERCEPTO_LITERATURA["media"] + np.array([-1.96, 1.96]) * PREVIA_INTERCEPTO_LITERATURA["desv"])),
              "evidencia": PREVIA_INTERCEPTO_LITERATURA["evidencia"], "fuente": PREVIA_INTERCEPTO_LITERATURA["fuente"]}]
    for v in variables:
        if v in PREVIAS_LITERATURA:
            m, d, ev, fu = PREVIAS_LITERATURA[v]
            u, txt = UNIDADES[v]
            lo, hi = np.exp(u * (m + np.array([-1.96, 1.96]) * d))
            filas.append({"parametro": v, "media_beta": m, "desv_beta": d,
                          "implica_95": f"OR {txt}: {np.exp(u * m):.2f} ({lo:.2f} a {hi:.2f})",
                          "evidencia": ev, "fuente": fu})
        else:
            filas.append({"parametro": v, "media_beta": 0.0, "desv_beta": np.nan,
                          "implica_95": "débilmente informativa: Normal(0, 2.5) por desviación estándar",
                          "evidencia": "Sin evidencia transferible (otras unidades o variables).",
                          "fuente": "Gelman et al. (2008)"})
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# Justificación del MCMC: Laplace y Metropolis de paseo aleatorio como alternativas


def metropolis(X: pd.DataFrame, y: pd.Series, previa: Previa | None = None, cadenas=4,
               calentamiento=1000, iteraciones=2000, semilla=config.SEMILLA) -> np.ndarray:
    """Metropolis de paseo aleatorio con propuesta normal de covarianza de Laplace y escala
    óptima 2.38/√d (Gelman, Roberts y Gilks, 1996). Solo para comparar eficiencia con HMC."""
    previa = previa or Previa()
    esc = Escalador.ajustar(X)
    A = _diseno(esc.transformar(X))
    yv = y.to_numpy(float)
    moda, cov = laplace(A, yv, previa)
    L = np.linalg.cholesky(cov)
    d = len(moda)
    rng = np.random.default_rng(semilla)
    salida = np.empty((cadenas, iteraciones, d))
    for c in range(cadenas):
        th = moda + 2 * L @ rng.standard_normal(d)
        lp = log_posterior(th, A, yv, previa)[0]
        for t in range(calentamiento + iteraciones):
            prop = th + 2.38 / np.sqrt(d) * L @ rng.standard_normal(d)
            lpn = log_posterior(prop, A, yv, previa)[0]
            if np.log(rng.random()) < lpn - lp:
                th, lp = prop, lpn
            if t >= calentamiento:
                salida[c, t - calentamiento] = th
    return salida
