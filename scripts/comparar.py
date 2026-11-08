"""Comparación de modelos según el Avance 2 (paso 6) y la guía (bloque 2, sesiones 2 y 3 de Juanes).

1. Validación cruzada estratificada de 5 pliegues SOLO sobre entrenamiento:
   4 técnicas (logística, árbol, bosque, boosting) × 3 conjuntos de variables = 12 configuraciones.
2. Elección con el criterio fijado de antemano: mayor AUC-PR medio con las 10 variables; si la
   diferencia con la logística es menor de 0.02, gana la logística (más fácil de explicar).
3. Evaluación ÚNICA en los 713 clientes de prueba de las 12 configuraciones, de la logística
   bayesiana (data/processed/predicciones_bayes.csv, de scripts/bayes.py) y de las reglas R1 y R2.
4. Criterios C1–C4 del Avance 2, curvas ROC y precisión-recall y tabla de sensibilidad.

Correr después de scripts/entrenar.py y scripts/bayes.py:
    python scripts/comparar.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import precision_recall_curve, roc_curve  # noqa: E402

from churn import config  # noqa: E402
from churn.datos import cargar_limpio  # noqa: E402
from churn.evaluacion import metricas  # noqa: E402
from churn.modelos import comparar_modelos, entrenar, separar  # noqa: E402

TECNICAS = ["logistica", "arbol", "bosque", "boosting"]
CONJUNTOS = {
    "completo": config.VARIABLES_MODELO,
    "sin_estado_quejas": config.VARIABLES_SIN_ESTADO_QUEJAS,
    "solo_uso": config.VARIABLES_SOLO_USO,
}


def captura(y, prob, n):
    orden = np.argsort(-np.asarray(prob), kind="stable")[:n]
    return np.asarray(y)[orden].sum() / np.asarray(y).sum()


def main():
    df = cargar_limpio()
    part = pd.read_csv(config.PARTICION)
    ent, pru = separar(df, part)
    y_ent, y_pru = ent[config.OBJETIVO], pru[config.OBJETIVO]
    T, F = config.TABLAS, config.FIGURAS

    # 1. Validación cruzada (12 configuraciones) -----------------------------------
    cv = []
    for nombre_c, vars_ in CONJUNTOS.items():
        t = comparar_modelos(ent[vars_], y_ent, TECNICAS)
        t.insert(1, "conjunto", nombre_c)
        cv.append(t)
    cv = pd.concat(cv, ignore_index=True)
    cv.to_csv(T / "comparacion_modelos.csv", index=False)
    print(cv.round(3).to_string(index=False))

    # 2. Elección con el criterio previo ------------------------------------------
    comp = cv[cv["conjunto"] == "completo"].set_index("modelo")
    mejor = comp["auc_pr_media"].idxmax()
    dif = comp.loc[mejor, "auc_pr_media"] - comp.loc["logistica", "auc_pr_media"]
    elegido = "logistica" if dif < 0.02 else mejor
    print(f"\nMayor AUC-PR en CV: {mejor} ({comp.loc[mejor, 'auc_pr_media']:.3f}); "
          f"diferencia con la logística {dif:.3f} -> modelo propuesto: {elegido}")

    # 3. Evaluación única en prueba -----------------------------------------------
    r1 = (pru["quejas"] == 1).to_numpy()
    r2 = r1 | (pru["estado"] == 2).to_numpy()
    n1, n2 = int(r1.sum()), int(r2.sum())
    filas, probs = [], {}
    for nombre_c, vars_ in CONJUNTOS.items():
        for tec in TECNICAS:
            mod = entrenar(tec, ent[vars_], y_ent)
            pr = mod.predict_proba(pru[vars_])[:, 1]
            probs[(tec, nombre_c)] = pr
            m = metricas(y_pru, pr)
            filas.append({"modelo": tec, "conjunto": nombre_c, **m,
                          **{f"captura_{int(p * 100)}pct": captura(y_pru, pr, round(p * len(pru)))
                             for p in config.CAPACIDADES},
                          "captura_con_n_R1": captura(y_pru, pr, n1),
                          "captura_con_n_R2": captura(y_pru, pr, n2)})
    pb = pd.read_csv(config.RAIZ / "data" / "processed" / "predicciones_bayes.csv")
    pb = pb.set_index("fila_original").loc[pru["fila_original"], "prob_churn"].to_numpy()
    probs[("logistica_bayesiana", "completo")] = pb
    filas.append({"modelo": "logistica_bayesiana", "conjunto": "completo", **metricas(y_pru, pb),
                  **{f"captura_{int(p * 100)}pct": captura(y_pru, pb, round(p * len(pru))) for p in config.CAPACIDADES},
                  "captura_con_n_R1": captura(y_pru, pb, n1), "captura_con_n_R2": captura(y_pru, pb, n2)})
    prueba = pd.DataFrame(filas)
    prueba.to_csv(T / "metricas_prueba_todos.csv", index=False)
    print(prueba[["modelo", "conjunto", "auc_roc", "auc_pr", "captura_20pct", "captura_con_n_R2"]]
          .round(3).to_string(index=False))

    reglas = pd.DataFrame([
        {"regla": "R1: quejas", "contactados": n1, "pct": n1 / len(pru),
         "captura": y_pru.to_numpy()[r1].sum() / y_pru.sum(), "precision": y_pru.to_numpy()[r1].mean()},
        {"regla": "R2: quejas o no activo", "contactados": n2, "pct": n2 / len(pru),
         "captura": y_pru.to_numpy()[r2].sum() / y_pru.sum(), "precision": y_pru.to_numpy()[r2].mean()},
    ])
    reglas.to_csv(T / "reglas_referencia.csv", index=False)
    print(reglas.round(3).to_string(index=False))

    # 4. Sensibilidad ("¿en qué medida?"): mejor modelo y logística, 3 conjuntos ----
    sens = prueba[prueba["modelo"].isin({"logistica", mejor}) & (prueba["conjunto"].isin(CONJUNTOS))]
    sens = sens.merge(cv[["modelo", "conjunto", "auc_pr_media", "auc_pr_desv"]], on=["modelo", "conjunto"])
    sens[["modelo", "conjunto", "auc_pr_media", "auc_pr_desv", "auc_roc", "auc_pr", "captura_20pct"]].to_csv(
        T / "sensibilidad_variables.csv", index=False)

    # 5. Criterios del Avance 2 ---------------------------------------------------
    def fila(mod, conj="completo"):
        return prueba[(prueba["modelo"] == mod) & (prueba["conjunto"] == conj)].iloc[0]

    criterios = {}
    for mod in sorted({elegido, "logistica", "logistica_bayesiana"}):
        f = fila(mod)
        crit = {
            "C1_auc_pr_prueba": float(f["auc_pr"]), "C1_cumple": bool(f["auc_pr"] >= 0.50),
            "C2_ventaja_vs_R2_pp": float(100 * (f["captura_con_n_R2"] - reglas.loc[1, "captura"])),
            "C2_ventaja_vs_R1_pp": float(100 * (f["captura_con_n_R1"] - reglas.loc[0, "captura"])),
        }
        crit["C2_cumple"] = bool(crit["C2_ventaja_vs_R2_pp"] >= 3 and crit["C2_ventaja_vs_R1_pp"] >= 0)
        if mod in TECNICAS:
            sin = fila(mod, "sin_estado_quejas")
            crit.update({"C3_auc_pr_sin_estado_quejas": float(sin["auc_pr"]), "C3_cumple": bool(sin["auc_pr"] >= 0.31)})
            c = cv[(cv["modelo"] == mod) & (cv["conjunto"] == "completo")].iloc[0]
            crit.update({"C4_desv_pliegues": float(c["auc_pr_desv"]),
                         "C4_dif_cv_prueba": float(abs(c["auc_pr_media"] - f["auc_pr"])),
                         "C4_cumple": bool(c["auc_pr_desv"] <= 0.05 and abs(c["auc_pr_media"] - f["auc_pr"]) <= 0.05)})
        criterios[mod] = crit
    criterios["eleccion"] = {"mayor_auc_pr_cv": mejor, "diferencia_con_logistica": float(dif), "propuesto": elegido}
    (T / "criterios_avance2.json").write_text(json.dumps(criterios, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(criterios, indent=2, ensure_ascii=False))

    # 6. Curvas ROC y precisión-recall en prueba ------------------------------------
    fig, ejes = plt.subplots(1, 2, figsize=(12, 5))
    estilos = [(("bosque", "completo"), "Bosque aleatorio", "#2f855a", "-"),
               (("boosting", "completo"), "Boosting", "#805ad5", "-"),
               (("logistica", "completo"), "Logística clásica", "#2b6cb0", "-"),
               (("logistica_bayesiana", "completo"), "Logística bayesiana", "#c05621", "--"),
               (("arbol", "completo"), "Árbol (prof. 4)", "#718096", "-"),
               (("logistica", "sin_estado_quejas"), "Logística sin estado ni quejas", "#2b6cb0", ":")]
    for clave, etiqueta, color, ls in estilos:
        pr = probs[clave]
        fpr, tpr, _ = roc_curve(y_pru, pr)
        prec, rec, _ = precision_recall_curve(y_pru, pr)
        m = metricas(y_pru, pr)
        ejes[0].plot(fpr, tpr, color=color, ls=ls, label=f"{etiqueta} ({m['auc_roc']:.3f})")
        ejes[1].plot(rec, prec, color=color, ls=ls, label=f"{etiqueta} ({m['auc_pr']:.3f})")
    for regla, mask, mk in [("R1", r1, "o"), ("R2", r2, "s")]:
        yv = y_pru.to_numpy()
        tpr_r = yv[mask].sum() / yv.sum()
        fpr_r = ((~(yv == 1)) & mask).sum() / (yv == 0).sum()
        ejes[0].plot(fpr_r, tpr_r, mk, color="black", ms=8, label=f"Regla {regla}")
        ejes[1].plot(tpr_r, yv[mask].mean(), mk, color="black", ms=8, label=f"Regla {regla}")
    ejes[0].plot([0, 1], [0, 1], color="#cbd5e0", lw=1)
    ejes[1].axhline(y_pru.mean(), color="#cbd5e0", lw=1)
    ejes[0].set(xlabel="tasa de falsos positivos", ylabel="exhaustividad (recall)", title="Curva ROC · prueba")
    ejes[1].set(xlabel="exhaustividad (recall)", ylabel="precisión", title="Curva precisión-exhaustividad · prueba")
    for ax in ejes:
        ax.legend(fontsize=7.5, loc="lower right" if ax is ejes[0] else "lower left")
    fig.tight_layout()
    fig.savefig(F / "curvas_roc_pr.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
