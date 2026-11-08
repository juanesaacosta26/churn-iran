"""Interpretación del modelo final (guía, bloque 3, sesión 1 de Juanes).

1. Importancia por permutación del bosque aleatorio (modelo final) en los 713 clientes de prueba:
   cuánto baja el AUC-PR si se desordena cada variable (30 repeticiones).
2. Árbol de decisión de profundidad 4 (el de la comparación) dibujado, como versión legible
   de las reglas que aprende un modelo basado en árboles.

Correr después de scripts/entrenar.py (usa particion.csv):
    python scripts/interpretar.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.inspection import permutation_importance  # noqa: E402
from sklearn.tree import plot_tree  # noqa: E402

from churn import config  # noqa: E402
from churn.datos import cargar_limpio  # noqa: E402
from churn.modelos import entrenar, separar  # noqa: E402

NOMBRES = {
    "fallas_llamada": "Fallas de llamada",
    "quejas": "Queja",
    "segundos_uso": "Segundos de uso",
    "frecuencia_sms": "SMS",
    "numeros_distintos": "Números distintos",
    "meses_suscripcion": "Meses de suscripción",
    "nivel_cobro": "Nivel de cobro",
    "plan_tarifa": "Plan (contrato)",
    "estado": "Estado (no activo)",
    "edad": "Edad",
}


def main():
    df = cargar_limpio()
    part = pd.read_csv(config.PARTICION)
    ent, pru = separar(df, part)
    X = config.VARIABLES_MODELO
    y_ent, y_pru = ent[config.OBJETIVO], pru[config.OBJETIVO]

    # 1. Importancia por permutación del bosque, medida en prueba -------------------
    bosque = entrenar("bosque", ent[X], y_ent)
    r = permutation_importance(bosque, pru[X], y_pru, scoring="average_precision",
                               n_repeats=30, random_state=config.SEMILLA, n_jobs=-1)
    imp = pd.DataFrame({
        "variable": X,
        "nombre": [NOMBRES[v] for v in X],
        "caida_auc_pr_media": r.importances_mean,
        "caida_auc_pr_desv": r.importances_std,
    }).sort_values("caida_auc_pr_media", ascending=False)
    imp.to_csv(config.TABLAS / "importancia_permutacion.csv", index=False)
    print(imp.round(3).to_string(index=False))

    orden = imp.iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 5))
    colores = ["#C2341F" if v in ("quejas", "estado") else "#5B3FD1" for v in orden["variable"]]
    ax.barh(orden["nombre"], orden["caida_auc_pr_media"], xerr=orden["caida_auc_pr_desv"],
            color=colores, ecolor="#4B4670", capsize=3)
    ax.set_xlabel("Caída del AUC-PR en prueba al desordenar la variable")
    ax.set_title("Importancia por permutación · bosque aleatorio (modelo final)")
    ax.axvline(0, color="#8C86AE", lw=1)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(config.FIGURAS / "importancia.png", dpi=150)
    plt.close(fig)

    # 2. Árbol de profundidad 4 -----------------------------------------------------
    arbol = entrenar("arbol", ent[X], y_ent)
    fig, ax = plt.subplots(figsize=(22, 10))
    plot_tree(arbol, feature_names=[NOMBRES[v] for v in X], class_names=["Permanece", "Abandona"],
              filled=True, rounded=True, impurity=False, proportion=True, fontsize=9, ax=ax)
    ax.set_title("Árbol de decisión (profundidad 4, mínimo 20 clientes por hoja), ajustado en entrenamiento")
    fig.tight_layout()
    fig.savefig(config.FIGURAS / "arbol.png", dpi=130)
    plt.close(fig)
    print("-> reports/figures/importancia.png, reports/figures/arbol.png, "
          "reports/tablas/importancia_permutacion.csv")


if __name__ == "__main__":
    main()
