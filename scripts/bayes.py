"""Regresión logística bayesiana frente a la logística clásica (máxima verosimilitud).

Dueño: Juanes (entrega de estadística bayesiana, viernes 6 de noviembre).
Sigue los pasos del documento del curso "Modelo Bayesiano de Regresión Logística":
modelo, previas normal(0, 2.5), MCMC, resumen (media, DE, 2.5 %, 97.5 %), diagnósticos
(n_eff/N y R̂), densidades posteriores y razones de momios OR = e^β con su intervalo.

Correr con:
    python scripts/bayes.py            # completo (≈ 2–4 min)
    python scripts/bayes.py --rapido   # menos iteraciones, para probar

Ajusta dos versiones: previas sustentadas en la literatura (PRINCIPAL; docs/fuentes_previas.md)
y previa débilmente informativa Normal(0, 2.5) (comparación). Incluye la justificación del MCMC
(comparación con Laplace y con Metropolis de paseo aleatorio).

Usa la MISMA partición que los demás modelos (data/processed/particion.csv) y ajusta solo
con los 2137 clientes de entrenamiento. Escribe reports/tablas/bayes_*.csv,
reports/figures/bayes_*.png y data/processed/predicciones_bayes.csv (formato del contrato).
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import brier_score_loss, log_loss  # noqa: E402

from churn import bayes, config  # noqa: E402
from churn.datos import cargar_limpio  # noqa: E402
from churn.evaluacion import metricas  # noqa: E402
from churn.modelos import particion, separar  # noqa: E402

NOMBRES = {
    "intercepto": "Intercepto",
    "fallas_llamada": "Fallas de llamada (+1)",
    "quejas": "Queja (sí vs. no)",
    "segundos_uso": "Segundos de uso (+1000)",
    "frecuencia_sms": "SMS (+10)",
    "numeros_distintos": "Números distintos (+10)",
    "meses_suscripcion": "Meses de suscripción (+6)",
    "nivel_cobro": "Nivel de cobro (+1)",
    "plan_tarifa": "Contrato vs. pago por uso",
    "estado": "No activo vs. activo",
    "edad": "Edad (+10 años)",
}
AZUL, ROJO, GRIS = "#2b6cb0", "#c53030", "#718096"


# ---------------------------------------------------------------------------
# Figuras


def fig_densidades(m, ruta):
    """Equivalente a bayesplot::mcmc_areas(prob = 0.95), en escala OR por unidad."""
    orig = bayes.a_escala_original(m.planas(), m.escalador)
    vars_ = [v for v in m.variables]
    fig, ejes = plt.subplots(5, 2, figsize=(11, 12))
    for ax, v in zip(ejes.ravel(), vars_):
        j = m.nombres.index(v)
        u, _ = bayes.UNIDADES[v]
        orv = np.exp(u * orig[:, j])
        lo, hi = np.quantile(orv, [0.025, 0.975])
        dens, bordes, _ = ax.hist(orv, bins=80, density=True, color="#bee3f8", edgecolor="none")
        centro = (bordes[:-1] + bordes[1:]) / 2
        ax.fill_between(centro, dens, where=(centro >= lo) & (centro <= hi), color=AZUL, alpha=0.5, step="mid")
        ax.axvline(np.exp(u * orig[:, j].mean()), color="#1a365d", lw=1.5)
        ax.axvline(1, color=ROJO, ls="--", lw=1)
        ax.set_title(NOMBRES[v], fontsize=10)
        ax.set_yticks([])
    fig.suptitle("Distribución posterior de cada razón de momios (OR = e^β)\n"
                 "zona oscura = intervalo de credibilidad 95 % · línea roja = OR 1 (sin efecto)", fontsize=11)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def fig_trazas(m, ruta):
    claves = ["intercepto", "quejas", "estado", "frecuencia_sms", "segundos_uso", "edad"]
    orig = bayes.a_escala_original(m.planas(), m.escalador).reshape(m.draws.shape)
    fig, ejes = plt.subplots(len(claves), 2, figsize=(11, 2.0 * len(claves)))
    for f, k in enumerate(claves):
        j = m.nombres.index(k)
        for c in range(m.draws.shape[0]):
            ejes[f, 0].plot(orig[c, :, j], lw=0.3, alpha=0.8)
            ejes[f, 1].hist(orig[c, :, j], bins=50, histtype="step", density=True)
        ejes[f, 0].set_ylabel(k, fontsize=9)
    ejes[0, 0].set_title("Trazas de las 4 cadenas (β, escala original)")
    ejes[0, 1].set_title("Densidad posterior por cadena")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def fig_comparacion(comp, ruta):
    c = comp[comp["parametro"] != "intercepto"].sort_values("or_unidad_bayes").reset_index(drop=True)
    y = np.arange(len(c))
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.hlines(y + 0.15, c["or_unidad_bayes_q2.5"], c["or_unidad_bayes_q97.5"], color=AZUL, lw=3)
    ax.plot(c["or_unidad_bayes"], y + 0.15, "o", color=AZUL, label="Bayesiana (media, IC credibilidad 95 %)")
    ax.hlines(y - 0.15, c["or_unidad_mv_ic2.5"], c["or_unidad_mv_ic97.5"], color=GRIS, lw=3)
    ax.plot(c["or_unidad_mv"], y - 0.15, "s", color=GRIS, label="Clásica (estimación, IC confianza 95 %)")
    ax.axvline(1, color=ROJO, ls="--", lw=1)
    ax.set_xscale("log")
    ax.set_yticks(y, [NOMBRES[p] for p in c["parametro"]])
    ax.set_xlabel("razón de momios (escala logarítmica)")
    ax.set_title("Razones de momios: logística bayesiana frente a clásica")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def fig_ppc(ppc, sim_total, obs_total, ruta):
    fig, ejes = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [1, 1.6]})
    ejes[0].hist(sim_total, bins=40, color="#90cdf4", edgecolor="white")
    ejes[0].axvline(obs_total, color=ROJO, lw=2, label=f"observada {obs_total:.1%}")
    ejes[0].set_title("Tasa de abandono en 4000 bases simuladas")
    ejes[0].set_xlabel("tasa simulada (entrenamiento)")
    ejes[0].legend()
    g = ppc[ppc["grupo"] != "Total"].reset_index(drop=True)
    y = np.arange(len(g))
    ejes[1].hlines(y, g["sim_2.5"], g["sim_97.5"], color=AZUL, lw=4, alpha=0.6, label="predictiva 95 %")
    ejes[1].plot(g["tasa_observada"], y, "D", color=ROJO, label="observada")
    ejes[1].set_yticks(y, g["grupo"])
    ejes[1].set_xlabel("tasa de abandono")
    ejes[1].set_title("Chequeo predictivo posterior por grupo")
    ejes[1].legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def fig_previas(sens, ruta):
    s = sens[sens["parametro"] != "intercepto"]
    piv = s.pivot(index="parametro", columns="orden", values="or_unidad")
    piv = piv.loc[piv[1].sort_values().index]
    nombres = s.drop_duplicates("orden").set_index("orden")["previa"]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    y = np.arange(len(piv))
    marcas = ["s", "o", "^", "v", "x"]
    colores = ["#9c4221", "#c05621", "#dd6b20", "#f6ad55", AZUL]
    for k, o in enumerate(piv.columns):
        ax.plot(piv[o], y + (k - 2) * 0.13, marcas[k], color=colores[k], label=nombres[o])
    ax.axvline(1, color=ROJO, ls="--", lw=1)
    ax.set_xscale("log")
    ax.set_yticks(y, [NOMBRES[p] for p in piv.index])
    ax.set_xlabel("OR posterior (media) · escala logarítmica")
    ax.set_title("Sensibilidad a la previa: solo la queja depende de cuánto se confía en la literatura")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def fig_incertidumbre(inc, ruta):
    d = inc.sort_values("prob_media").reset_index(drop=True)
    x = np.arange(len(d))
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.fill_between(x, d["prob_q2.5"], d["prob_q97.5"], color="#bee3f8", label="IC credibilidad 95 %")
    ax.plot(x, d["prob_media"], color=AZUL, lw=1.2, label="probabilidad media posterior")
    ab = d["churn_real"] == 1
    ax.plot(x[ab], d.loc[ab, "prob_media"], "|", color=ROJO, ms=7, label="abandonó")
    ax.set_xlabel("713 clientes de prueba, ordenados por probabilidad")
    ax.set_ylabel("probabilidad de abandono")
    ax.set_title("Incertidumbre de la probabilidad de abandono de cada cliente")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


def fig_previa_posterior(m_debil, m_lit, ruta):
    """Previa de la literatura frente a las dos posteriores, en escala OR por unidad."""
    from scipy import stats as st
    claves = ["quejas", "estado", "meses_suscripcion"]
    od = bayes.a_escala_original(m_debil.planas(), m_debil.escalador)
    ol = bayes.a_escala_original(m_lit.planas(), m_lit.escalador)
    fig, ejes = plt.subplots(1, 4, figsize=(15, 3.8))
    for ax, v in zip(ejes[:3], claves):
        j = m_debil.nombres.index(v)
        u, _ = bayes.UNIDADES[v]
        mu, sd, _, _ = bayes.PREVIAS_LITERATURA[v]
        lx = np.linspace(u * (mu - 3.5 * sd), max(u * (mu + 3.5 * sd), u * od[:, j].max()), 400)
        ax.plot(np.exp(lx), st.norm.pdf(lx, u * mu, u * sd), color=GRIS, lw=2, label="previa (literatura)")
        for o, col, lab in [(od, AZUL, "posterior, previa débil (comparación)"), (ol, "#c05621", "posterior, previa literatura (principal)")]:
            lv = u * o[:, j]
            k = st.gaussian_kde(lv)
            ax.plot(np.exp(lx), k(lx), color=col, lw=2, label=lab)
        ax.axvline(1, color=ROJO, ls="--", lw=1)
        ax.set_xscale("log")
        ax.set_yticks([])
        ax.set_title(NOMBRES[v], fontsize=10)
        ax.set_xlabel("OR (escala log)")
    # tasa de abandono simulada frente a las tasas del sector (contraste, no previa)
    ax = ejes[3]
    rng = np.random.default_rng(2)
    for m_, col in [(m_debil, AZUL), (m_lit, "#c05621")]:
        P = bayes.prob_posterior(m_, m_.datos_ent, 2000)
        sim = (rng.random(P.shape) < P).mean(axis=1)
        ax.hist(sim, bins=30, density=True, histtype="step", color=col, lw=2)
    for lo, hi, txt, yy in [(0.169, 0.20, "Corea 17–20 %", 0.9), (0.215, 0.215, "pospago ≈ 22 %", 0.75),
                            (0.37, 0.80, "prepago 37–80 %", 0.6)]:
        ax.axvspan(lo, hi if hi > lo else lo + 0.004, color=GRIS, alpha=0.25)
        ax.text(lo, ax.get_ylim()[1] * yy, " " + txt, fontsize=7.5, color="#4a5568")
    ax.set_xlim(0.1, 0.85)
    ax.set_yticks([])
    ax.set_title("Tasa simulada vs. tasas anuales del sector", fontsize=10)
    ax.set_xlabel("tasa de abandono")
    ejes[0].legend(fontsize=7.5, loc="upper left")
    fig.suptitle("Previas de la literatura (gris) frente a las posteriores: los datos dominan; solo en la queja la previa baja el OR (47 → 35)", fontsize=10)
    fig.tight_layout()
    fig.savefig(ruta, dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Utilidades


def captura(y, puntaje, n):
    """Abandonos capturados si se contacta a los n de mayor puntaje."""
    orden = np.argsort(-np.asarray(puntaje), kind="stable")[:n]
    return int(np.asarray(y)[orden].sum())


def metricas_completas(nombre, y, prob):
    m = metricas(y, prob)
    m.update({"brier": brier_score_loss(y, prob), "log_loss": log_loss(y, prob)})
    for p in config.CAPACIDADES:
        n = round(p * len(y))
        c = captura(y, prob, n)
        m[f"captura_{int(p * 100)}pct"] = c / y.sum()
    return {"modelo": nombre, **m}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--rapido", action="store_true")
    args = a.parse_args()
    cal, it = (300, 500) if args.rapido else (1000, 2000)

    df = cargar_limpio()
    part = pd.read_csv(config.PARTICION) if config.PARTICION.exists() else particion(df, guardar=True)
    ent, pru = separar(df, part)
    y_ent, y_pru = ent[config.OBJETIVO], pru[config.OBJETIVO]
    X = config.VARIABLES_MODELO
    T, F = config.TABLAS, config.FIGURAS
    F.mkdir(parents=True, exist_ok=True)
    T.mkdir(parents=True, exist_ok=True)

    # 1. Logística bayesiana con previas de la literatura (principal) -----------
    def previa_lit(vars_, factor=1.0):
        return bayes.previa_literatura(bayes.Escalador.ajustar(ent[vars_]), vars_, factor)

    t0 = time.time()
    m = bayes.ajustar(ent[X], y_ent, previa=previa_lit(X), calentamiento=cal, iteraciones=it)
    seg = time.time() - t0
    res = bayes.tabla_curso(m)
    res.to_csv(T / "bayes_resumen.csv", index=False)
    diag = pd.DataFrame([{
        "cadenas": m.draws.shape[0], "calentamiento": cal, "iteraciones_por_cadena": it,
        "muestras_totales": m.draws.shape[0] * it,
        "rhat_max": res["rhat"].max(), "n_eff_min": res["n_eff"].min(),
        "n_eff_N_min": res["n_eff_N"].min(),
        "divergencias": int(m.divergencias.sum()), "aceptacion_media": m.aceptacion.mean(),
        "segundos": round(seg, 1),
    }])
    diag.to_csv(T / "bayes_diagnosticos.csv", index=False)
    print(f"Muestreo en {seg:.0f} s")
    print(diag.T.to_string(header=False))
    print(res[["parametro", "media", "de", "q2.5", "q97.5", "n_eff_N", "rhat", "or_unidad",
               "or_unidad_q2.5", "or_unidad_q97.5"]].round(4).to_string(index=False))
    fig_trazas(m, F / "bayes_trazas.png")
    fig_densidades(m, F / "bayes_densidades_or.png")

    # 2. Logística clásica y comparación de coeficientes ------------------------
    mv = bayes.logistica_mv(ent[X], y_ent)
    mv.to_csv(T / "logistica_mv.csv", index=False)
    comp = pd.DataFrame({
        "parametro": res["parametro"],
        "beta_bayes": res["media"], "de_bayes": res["de"],
        "beta_bayes_q2.5": res["q2.5"], "beta_bayes_q97.5": res["q97.5"],
        "beta_mv": mv["beta"], "ee_mv": mv["ee"], "beta_mv_ic2.5": mv["ic2.5"], "beta_mv_ic97.5": mv["ic97.5"],
        "p_valor_mv": mv["p_valor"], "prob_beta_pos_bayes": res["prob_beta_pos"],
    })
    comp["dif_beta"] = comp["beta_bayes"] - comp["beta_mv"]
    comp["dif_en_ee"] = comp["dif_beta"] / comp["ee_mv"]             # diferencia medida en errores estándar
    comp["razon_ancho_intervalo"] = (comp["beta_bayes_q97.5"] - comp["beta_bayes_q2.5"]) / (
        comp["beta_mv_ic97.5"] - comp["beta_mv_ic2.5"])
    for col in ["or_unidad", "or_unidad_q2.5", "or_unidad_q97.5"]:
        comp[col.replace("or_unidad", "or_unidad_bayes")] = res[col]
    for col in ["or_unidad", "or_unidad_ic2.5", "or_unidad_ic97.5"]:
        comp[col.replace("or_unidad", "or_unidad_mv")] = mv[col]
    comp["lectura"] = res["lectura"]
    excl0_b = (comp["beta_bayes_q2.5"] > 0) | (comp["beta_bayes_q97.5"] < 0)
    excl0_m = (comp["beta_mv_ic2.5"] > 0) | (comp["beta_mv_ic97.5"] < 0)
    comp["intervalo_excluye_0_bayes"] = excl0_b
    comp["intervalo_excluye_0_mv"] = excl0_m
    comp["misma_conclusion"] = excl0_b == excl0_m
    comp.to_csv(T / "bayes_vs_clasica_coeficientes.csv", index=False)
    print(comp[["parametro", "beta_bayes", "beta_mv", "dif_en_ee", "razon_ancho_intervalo",
                "or_unidad_bayes", "or_unidad_mv", "misma_conclusion"]].round(3).to_string(index=False))
    fig_comparacion(comp, F / "bayes_vs_clasica_or.png")

    # 3. Chequeo predictivo posterior ------------------------------------------
    ppc = bayes.chequeo_predictivo(m, ent)
    ppc.to_csv(T / "bayes_chequeo_predictivo.csv", index=False)
    P = bayes.prob_posterior(m, ent, 4000)
    sim_total = (np.random.default_rng(1).random(P.shape) < P).mean(axis=1)
    fig_ppc(ppc, sim_total, y_ent.mean(), F / "bayes_chequeo_predictivo.png")

    # 4. Prueba: desempeño de las dos logísticas y de las reglas -----------------
    Pp = bayes.prob_posterior(m, pru)
    prob_b = Pp.mean(axis=0)
    prob_m = bayes.prob_mv(mv, pru[X])
    q025, q975 = np.quantile(Pp, [0.025, 0.975], axis=0)
    inc = pd.DataFrame({"fila_original": pru["fila_original"].to_numpy(), "churn_real": y_pru.to_numpy(),
                        "quejas": pru["quejas"].to_numpy(), "estado": pru["estado"].to_numpy(),
                        "prob_media": prob_b, "prob_q2.5": q025, "prob_q97.5": q975,
                        "ancho_95": q975 - q025, "prob_clasica": prob_m})
    inc.to_csv(T / "bayes_incertidumbre_prueba.csv", index=False)
    fig_incertidumbre(inc, F / "bayes_incertidumbre_clientes.png")
    pd.DataFrame({
        "fila_original": pru["fila_original"].to_numpy(), "conjunto": "prueba",
        "churn_real": y_pru.astype(int).to_numpy(), "prob_churn": prob_b, "modelo": "logistica_bayesiana",
    }).to_csv(config.RAIZ / "data" / "processed" / "predicciones_bayes.csv", index=False)

    met = pd.DataFrame([metricas_completas("logistica_bayesiana", y_pru, prob_b),
                        metricas_completas("logistica_clasica", y_pru, prob_m)])
    met.to_csv(T / "bayes_vs_clasica_metricas.csv", index=False)
    print(met.round(4).T.to_string(header=False))

    # reglas de referencia del Avance 2 (R1: queja; R2: queja o no activo)
    r1 = (pru["quejas"] == 1).to_numpy()
    r2 = r1 | (pru["estado"] == 2).to_numpy()
    filas = []
    for nombre, regla in [("R1: quejas", r1), ("R2: quejas o no activo", r2)]:
        n = int(regla.sum())
        filas.append({"criterio": nombre, "contactados": n, "pct_contactados": n / len(pru),
                      "captura_regla": y_pru.to_numpy()[regla].sum() / y_pru.sum(),
                      "captura_bayes": captura(y_pru, prob_b, n) / y_pru.sum(),
                      "captura_clasica": captura(y_pru, prob_m, n) / y_pru.sum(),
                      "captura_azar": n / len(pru)})
    ref = pd.DataFrame(filas)
    ref["ventaja_bayes_pp"] = 100 * (ref["captura_bayes"] - ref["captura_regla"])
    ref.to_csv(T / "bayes_vs_reglas.csv", index=False)
    print(ref.round(3).to_string(index=False))

    # 5. ¿En qué medida? Variantes de variables (WAIC y elpd en prueba) ----------
    conjuntos = {
        "completo (10 variables)": X,
        "sin estado": [v for v in X if v != "estado"],
        "sin quejas": [v for v in X if v != "quejas"],
        "sin estado ni quejas": config.VARIABLES_SIN_ESTADO_QUEJAS,
        "solo uso y fallas": config.VARIABLES_SOLO_USO,
    }
    filas, refp = [], None
    for nombre, vars_ in conjuntos.items():
        mm = m if vars_ == X else bayes.ajustar(ent[vars_], y_ent, previa=previa_lit(vars_),
                                                calentamiento=cal, iteraciones=it // 2)
        w = bayes.waic(bayes.log_lik(mm, ent, y_ent))
        e = bayes.elpd_prueba(bayes.log_lik(mm, pru, y_pru))
        pr = bayes.prob_posterior(mm, pru).mean(axis=0)
        if refp is None:
            refp = (w["puntual"], e["puntual"])
        dw, de = w["puntual"] - refp[0], e["puntual"] - refp[1]
        mt = metricas(y_pru, pr)
        filas.append({"modelo": nombre, "n_variables": len(vars_),
                      "elpd_waic": w["elpd_waic"], "p_waic": w["p_waic"],
                      "dif_elpd_waic": dw.sum(), "se_dif_waic": np.sqrt(len(dw) * dw.var(ddof=1)),
                      "elpd_prueba": e["elpd_prueba"], "dif_elpd_prueba": de.sum(),
                      "se_dif_prueba": np.sqrt(len(de) * de.var(ddof=1)),
                      "auc_roc_prueba": mt["auc_roc"], "auc_pr_prueba": mt["auc_pr"],
                      "captura_20pct": captura(y_pru, pr, round(0.2 * len(pru))) / y_pru.sum()})
    var = pd.DataFrame(filas)
    var.to_csv(T / "bayes_variantes.csv", index=False)
    print(var.round(3).to_string(index=False))

    # 6. Sensibilidad a la previa: cuánto se descuenta la literatura, y previa débil ----
    escenarios = [("literatura, desviaciones × 0.5", 0.5), ("literatura (principal)", 1.0),
                  ("literatura, desviaciones × 2", 2.0), ("literatura, desviaciones × 4", 4.0),
                  ("débilmente informativa", None)]
    sens = []
    for orden, (nombre, fac) in enumerate(escenarios):
        if fac == 1.0:
            mm = m
        elif fac is None:
            mm = bayes.ajustar(ent[X], y_ent, calentamiento=cal, iteraciones=it // 2)
        else:
            mm = bayes.ajustar(ent[X], y_ent, previa=previa_lit(X, fac), calentamiento=cal, iteraciones=it // 2)
        r = bayes.tabla_curso(mm)
        r["previa"], r["orden"] = nombre, orden
        r["auc_roc_prueba"] = metricas(y_pru, bayes.prob_posterior(mm, pru).mean(axis=0))["auc_roc"]
        sens.append(r[["orden", "previa", "parametro", "media", "q2.5", "q97.5", "or_unidad",
                       "or_unidad_q2.5", "or_unidad_q97.5", "rhat", "auc_roc_prueba"]])
    sens = pd.concat(sens)
    sens.to_csv(T / "bayes_sensibilidad_previa.csv", index=False)
    fig_previas(sens, F / "bayes_sensibilidad_previa.png")
    print(sens.pivot(index="parametro", columns="orden", values="or_unidad").round(3))

    # 7. Probabilidades de interés para las conclusiones -------------------------
    orig = bayes.a_escala_original(m.planas(), m.escalador)
    j = {n: i for i, n in enumerate(m.nombres)}
    med = ent[X].median()

    def p_cliente(**cambios):
        x = med.copy()
        for k, v in cambios.items():
            x[k] = v
        return 1 / (1 + np.exp(-(orig[:, 0] + orig[:, 1:] @ x.to_numpy(float))))

    def r(v):
        lo_, hi_ = np.quantile(v, [0.025, 0.975])
        return {"media": round(float(v.mean()), 4), "q2.5": round(float(lo_), 4), "q97.5": round(float(hi_), 4)}

    p00 = p_cliente(quejas=0, estado=1)
    p10 = p_cliente(quejas=1, estado=1)
    p01 = p_cliente(quejas=0, estado=2)
    p11 = p_cliente(quejas=1, estado=2)
    extra = {
        "cliente_mediano": {k: float(v) for k, v in med.items()},
        "P(OR_quejas > 1)": float((orig[:, j["quejas"]] > 0).mean()),
        "P(OR_quejas > 10)": float((orig[:, j["quejas"]] > np.log(10)).mean()),
        "P(OR_estado > 1)": float((orig[:, j["estado"]] > 0).mean()),
        "P(OR_fallas > 1)": float((orig[:, j["fallas_llamada"]] > 0).mean()),
        "P(OR_plan < 1)": float((orig[:, j["plan_tarifa"]] < 0).mean()),
        "P(0.9 < OR_edad_10años < 1.1)": float((np.abs(10 * orig[:, j["edad"]]) < np.log(1.1)).mean()),
        "prob_activo_sin_queja": r(p00), "prob_activo_con_queja": r(p10),
        "prob_inactivo_sin_queja": r(p01), "prob_inactivo_con_queja": r(p11),
        "dif_queja_activo_pp": r(100 * (p10 - p00)),
        "prueba_ancho95_mediano": float(np.median(inc["ancho_95"])),
        "prueba_ancho95_p90": float(np.quantile(inc["ancho_95"], 0.9)),
        "prueba_dif_max_prob_bayes_vs_clasica": float(np.max(np.abs(prob_b - prob_m))),
    }
    (T / "bayes_probabilidades.json").write_text(json.dumps(extra, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(extra, indent=2, ensure_ascii=False))

    # 8. Comparación con la previa débilmente informativa -----------------------------
    bayes.tabla_previas_literatura(X).to_csv(T / "bayes_previas_literatura.csv", index=False)
    md = bayes.ajustar(ent[X], y_ent, calentamiento=cal, iteraciones=it)
    m.datos_ent = md.datos_ent = ent
    rd = bayes.tabla_curso(md)
    rd.to_csv(T / "bayes_resumen_debil.csv", index=False)
    cmp_ = pd.DataFrame({
        "parametro": res["parametro"], "lectura": res["lectura"],
        "or_literatura": res["or_unidad"], "or_literatura_q2.5": res["or_unidad_q2.5"],
        "or_literatura_q97.5": res["or_unidad_q97.5"],
        "or_debil": rd["or_unidad"], "or_debil_q2.5": rd["or_unidad_q2.5"], "or_debil_q97.5": rd["or_unidad_q97.5"],
        "rhat_debil": rd["rhat"],
        "previa_informada": res["parametro"].isin(list(bayes.PREVIAS_LITERATURA)),
    })
    cmp_.to_csv(T / "bayes_previas_comparacion.csv", index=False)
    prob_d = bayes.prob_posterior(md, pru).mean(axis=0)
    wl = bayes.waic(bayes.log_lik(m, ent, y_ent))
    wd = bayes.waic(bayes.log_lik(md, ent, y_ent))
    met_prev = pd.DataFrame([
        {"previa": "literatura (principal)", "elpd_waic": wl["elpd_waic"], **metricas_completas("", y_pru, prob_b)},
        {"previa": "debilmente_informativa", "elpd_waic": wd["elpd_waic"], **metricas_completas("", y_pru, prob_d)},
    ]).drop(columns="modelo")
    met_prev["rhat_max"] = [res["rhat"].max(), rd["rhat"].max()]
    met_prev["divergencias"] = [int(m.divergencias.sum()), int(md.divergencias.sum())]
    met_prev.to_csv(T / "bayes_previas_metricas.csv", index=False)
    print(cmp_.round(3).to_string(index=False))
    print(met_prev.round(4).T.to_string(header=False))
    fig_previa_posterior(md, m, F / "bayes_previa_vs_posterior.png")

    # 9. Justificación del MCMC: Laplace y Metropolis frente a HMC ---------------------
    from scipy import stats as st
    A = np.column_stack([np.ones(len(ent)), m.escalador.transformar(ent[X])])
    moda, cov = bayes.laplace(A, y_ent.to_numpy(float), previa_lit(X))
    Tm = bayes._matriz_t(m.escalador)
    th, se = Tm @ moda, np.sqrt(np.diag(Tm @ cov @ Tm.T))
    orig = bayes.a_escala_original(m.planas(), m.escalador)
    filas = []
    for v in ["quejas", "estado", "plan_tarifa"]:
        jj = m.nombres.index(v)
        lo, hi = np.quantile(orig[:, jj], [0.025, 0.975])
        filas.append({"parametro": v, "or_laplace": np.exp(th[jj]),
                      "or_laplace_2.5": np.exp(th[jj] - 1.96 * se[jj]), "or_laplace_97.5": np.exp(th[jj] + 1.96 * se[jj]),
                      "or_mcmc": np.exp(orig[:, jj].mean()), "or_mcmc_2.5": np.exp(lo), "or_mcmc_97.5": np.exp(hi),
                      "asimetria_or_mcmc": st.skew(np.exp(orig[:, jj]))})
    t0 = time.time()
    rw = bayes.metropolis(ent[X], y_ent, previa=previa_lit(X), calentamiento=cal, iteraciones=it)
    seg_rw = time.time() - t0
    neff_rw = min(bayes.ess_bulk(rw[:, :, k]) for k in range(rw.shape[2])) / rw[:, :, 0].size
    just = pd.DataFrame(filas)
    just.to_csv(T / "bayes_laplace_vs_mcmc.csv", index=False)
    efic = pd.DataFrame([
        {"metodo": "HMC (usado)", "n_eff_N_min": res["n_eff_N"].min(), "rhat_max": res["rhat"].max(), "segundos": round(seg, 1)},
        {"metodo": "Metropolis de paseo aleatorio", "n_eff_N_min": neff_rw,
         "rhat_max": max(bayes.rhat(rw[:, :, k]) for k in range(rw.shape[2])), "segundos": round(seg_rw, 1)},
    ])
    efic.to_csv(T / "bayes_eficiencia_mcmc.csv", index=False)
    print(just.round(3).to_string(index=False))
    print(efic.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
