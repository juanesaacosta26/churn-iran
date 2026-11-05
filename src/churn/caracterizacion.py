"""Objetivo específico 2: caracterizar a quienes abandonan vs. quienes permanecen.

Dueña: Ianis (bloque 2). Firmas acordadas; no cambiarlas sin hablarlo en la reunión.
"""
import pandas as pd
import numpy as np
from scipy.stats import MonteCarloMethod



def tabla_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """Compara variables numéricas entre clientes que abandonan y permanecen."""

    from scipy.stats import mannwhitneyu

    objetivo = "churn"

    excluir = [
        objetivo,
        "estado",
        "quejas",
        "nivel_cobro",
        "plan_tarifa",
        "fila_original",
        "edad"
    ]

    numericas = [
        columna
        for columna in df.select_dtypes(include="number").columns
        if columna not in excluir
    ]

    abandonan = df[df[objetivo] == 1]
    permanecen = df[df[objetivo] == 0]

    resultados = []

    for variable in numericas:
        grupo_abandona = abandonan[variable].dropna()
        grupo_permanece = permanecen[variable].dropna()

        if len(grupo_abandona) == 0 or len(grupo_permanece) == 0:
            continue

        mediana_abandona = grupo_abandona.median()
        q1_abandona = grupo_abandona.quantile(0.25)
        q3_abandona = grupo_abandona.quantile(0.75)

        mediana_permanece = grupo_permanece.median()
        q1_permanece = grupo_permanece.quantile(0.25)
        q3_permanece = grupo_permanece.quantile(0.75)

        prueba = mannwhitneyu(
            grupo_abandona,
            grupo_permanece,
            alternative="two-sided"
        )

        n1 = len(grupo_abandona)
        n0 = len(grupo_permanece)

        # Delta de Cliff: diferencia entre las probabilidades
        # de que un grupo tenga valores mayores que el otro.
        delta_cliff = (
            2 * prueba.statistic / (n1 * n0) - 1
        )

        resultados.append({
            "variable": variable,
            "mediana_abandona": mediana_abandona,
            "q1_abandona": q1_abandona,
            "q3_abandona": q3_abandona,
            "mediana_permanece": mediana_permanece,
            "q1_permanece": q1_permanece,
            "q3_permanece": q3_permanece,
            "p_valor": prueba.pvalue,
            "efecto": delta_cliff
        })

    columnas = [
        "variable",
        "mediana_abandona",
        "q1_abandona",
        "q3_abandona",
        "mediana_permanece",
        "q1_permanece",
        "q3_permanece",
        "p_valor",
        "efecto"
    ]

    tabla = pd.DataFrame(resultados, columns=columnas)

    return (
        tabla.assign(magnitud=tabla["efecto"].abs())
        .sort_values("magnitud", ascending=False)
        .drop(columns="magnitud")
        .reset_index(drop=True)
    )




def tabla_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula la tasa de churn por categoría y su asociación con churn."""

    from scipy.stats import chi2_contingency

    objetivo = "churn"

    categoricas = [
        columna
        for columna in df.select_dtypes(include=["object", "category", "bool"]).columns
        if columna != objetivo
    ]

    # Incluir variables numéricas que representan categorías.
    posibles_categoricas = [
        "quejas",
        "nivel_cobro",
        "plan_tarifa",
        "estado",
        "edad"
    ]

    for columna in posibles_categoricas:
        if columna in df.columns and columna not in categoricas:
            categoricas.append(columna)

    resultados = []

    for variable in categoricas:
        datos = df[[variable, objetivo]].dropna()

        if datos.empty or datos[variable].nunique() < 2:
            continue

        tabla_cruzada = pd.crosstab(
            datos[variable],
            datos[objetivo]
        )

        if 0 not in tabla_cruzada.columns or 1 not in tabla_cruzada.columns:
            continue

        _, p_valor, _, esperadas = chi2_contingency(tabla_cruzada)

        if (esperadas < 5).any():
            _, p_valor, _, _ = chi2_contingency(
            tabla_cruzada,
            correction=False,
            method=MonteCarloMethod(n_resamples=10000, rng=np.random.default_rng(42))
            )

        for nivel, fila in tabla_cruzada.iterrows():
            total = int(fila.sum())
            abandonos = int(fila[1])

            resultados.append({
                "variable": variable,
                "nivel": nivel,
                "n": total,
                "tasa_churn": abandonos / total if total > 0 else 0,
                "p_valor": p_valor
            })

    columnas = ["variable", "nivel", "n", "tasa_churn", "p_valor"]

    return pd.DataFrame(resultados, columns=columnas)

def graficar_categoricas(tabla, carpeta="reports/figures"):
    """Genera gráficas de barras con porcentajes de abandono."""

    import matplotlib.pyplot as plt
    from pathlib import Path

    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)

    for variable in tabla["variable"].unique():
        datos = tabla[tabla["variable"] == variable]

        fig, ax = plt.subplots(figsize=(8, 5))

        barras = ax.bar(
            datos["nivel"].astype(str),
            datos["tasa_churn"]
        )

        ax.set_title(f"Tasa de abandono según {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Porcentaje de abandono")
        ax.set_ylim(0, 1)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f"{x:.0%}")
        )

        # Mostrar el porcentaje encima de cada barra
        ax.bar_label(
            barras,
            labels=[f"{valor:.1%}" for valor in datos["tasa_churn"]],
            padding=3
        )

        plt.tight_layout()

        fig.savefig(
            carpeta / f"caracterizacion_{variable}.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.show()
        plt.close(fig)

