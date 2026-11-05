"""Priorización para el equipo de retención. Dueña: Ianis (bloques 2 y 3).

Recibe un archivo de predicciones con el formato de docs/contrato_predicciones.md.
Mientras no exista el de Juanes, usar data/processed/fixtures/predicciones_ejemplo.csv.
"""
import pandas as pd


def tabla_deciles(pred: pd.DataFrame) -> pd.DataFrame:
    """Ordena por prob_churn y parte en 10 deciles. Por decil: n, churn reales,
    tasa, lift y % acumulado de churners capturados.
    """
    columnas = [
        "decil", "n", "churn_reales",
        "tasa", "lift", "pct_acumulado"
    ]

    if pred.empty:
        return pd.DataFrame(columns=columnas)

    # Ordenar clientes desde el mayor hasta el menor riesgo.
    ordenado = pred.sort_values(
        "prob_churn",
        ascending=False
    ).reset_index(drop=True).copy()

    # Asignar los clientes a 10 deciles.
    total_clientes = len(ordenado)

    ordenado["decil"] = [
        (i * 10 // total_clientes) + 1
        for i in range(total_clientes)
    ]

    # Calcular clientes y abandonos reales por decil.
    tabla = (
        ordenado.groupby("decil")
        .agg(
            n=("churn_real", "size"),
            churn_reales=("churn_real", "sum")
        )
        .reindex(range(1, 11), fill_value=0)
    )

    tabla.index.name = "decil"
    tabla = tabla.reset_index()

    # Tasa de abandono de cada decil.
    tabla["tasa"] = (
        tabla["churn_reales"] / tabla["n"].replace(0, 1)
    )

    # Comparar cada decil con la tasa general de abandono.
    tasa_general = pred["churn_real"].mean()

    if tasa_general > 0:
        tabla["lift"] = tabla["tasa"] / tasa_general
    else:
        tabla["lift"] = 0

    # Porcentaje acumulado de abandonos capturados.
    total_churn = pred["churn_real"].sum()

    if total_churn > 0:
        tabla["pct_acumulado"] = (
            tabla["churn_reales"].cumsum() / total_churn * 100
        )
    else:
        tabla["pct_acumulado"] = 0

    return tabla[columnas]


def costo_por_umbral(pred: pd.DataFrame, costo_fn: float, costo_fp: float) -> pd.DataFrame:
    """Para umbrales de 0.05 a 0.95: FP, FN y costo total = FN*costo_fn + FP*costo_fp.

    Columnas: umbral, falsos_positivos, falsos_negativos, costo.
    Con k de config.K_COSTOS: costo_fn = k, costo_fp = 1.
    """
    raise NotImplementedError


def capacidad(pred: pd.DataFrame, porcentajes=(0.10, 0.20, 0.30)) -> pd.DataFrame:
    """Calcula cuántos abandonos captura el equipo al contactar
    a los clientes con mayor probabilidad de churn.
    """
    resultados = []

    # Ordenar clientes desde el mayor hasta el menor riesgo.
    ordenado = pred.sort_values(
        "prob_churn",
        ascending=False
    ).reset_index(drop=True)

    total_clientes = len(ordenado)
    total_churn = ordenado["churn_real"].sum()

    for p in porcentajes:

        # Calcular cuántos clientes puede contactar el equipo.
        contactados = round(p * total_clientes)

        # Seleccionar los clientes de mayor riesgo.
        seleccionados = ordenado.head(contactados)

        # Contar cuántos abandonaron realmente.
        churn_capturados = seleccionados["churn_real"].sum()

        # Porcentaje de abandonos identificados.
        if total_churn > 0:
            pct_capturado = churn_capturados / total_churn * 100
        else:
            pct_capturado = 0

        # Proporción de contactados que realmente abandonaron.
        if contactados > 0:
            precision = churn_capturados / contactados
        else:
            precision = 0

        resultados.append({
            "porcentaje": p,
            "contactados": contactados,
            "churn_capturados": churn_capturados,
            "pct_capturado": pct_capturado,
            "precision": precision
        })

    return pd.DataFrame(resultados)
