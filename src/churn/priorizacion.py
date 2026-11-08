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


def costo_por_umbral(
    pred: pd.DataFrame,
    costo_fn: float,
    costo_fp: float
) -> pd.DataFrame:
    """Calcula los falsos positivos, falsos negativos y costo total
    para umbrales entre 0.05 y 0.95.
    """
    resultados = []

    for umbral in [i / 100 for i in range(5, 100, 5)]:

        # Clasificar clientes según su probabilidad de abandono.
        predicho = pred["prob_churn"] >= umbral

        # Identificar los errores de clasificación.
        falsos_positivos = (
            (predicho) & (pred["churn_real"] == 0)
        ).sum()

        falsos_negativos = (
            (~predicho) & (pred["churn_real"] == 1)
        ).sum()

        # Calcular el costo total.
        costo = (
            falsos_negativos * costo_fn
            + falsos_positivos * costo_fp
        )

        resultados.append({
            "umbral": umbral,
            "falsos_positivos": falsos_positivos,
            "falsos_negativos": falsos_negativos,
            "costo": costo
        })

    return pd.DataFrame(resultados)


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



def comparar_grupo_prioritario(
    pred: pd.DataFrame,
    clientes: pd.DataFrame,
    proporcion: float = 0.20
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compara las características del grupo de mayor riesgo
    frente al resto de clientes.
    """

    from churn.caracterizacion import (
        tabla_numericas,
        tabla_categoricas
    )

    if not 0 < proporcion < 1:
        raise ValueError("La proporción debe estar entre 0 y 1.")

    # Ordenar clientes según su probabilidad de abandono.
    ordenado = pred.sort_values(
        "prob_churn",
        ascending=False
    ).reset_index(drop=True).copy()

    # Identificar el grupo de mayor riesgo.
    total = len(ordenado)
    cantidad_prioritaria = round(proporcion * total)

    ordenado["grupo_prioritario"] = 0
    ordenado.loc[:cantidad_prioritaria - 1, "grupo_prioritario"] = 1

    # Unir las predicciones con las características de los clientes.
    grupos = ordenado[
        ["fila_original", "grupo_prioritario"]
    ].merge(
        clientes,
        on="fila_original",
        how="inner",
        validate="one_to_one"
    )

    # Crear una copia y utilizar churn como indicador del grupo.
    # 1 = mayor riesgo; 0 = resto de clientes.
    perfil = grupos.drop(columns="grupo_prioritario").copy()
    perfil["churn"] = grupos["grupo_prioritario"].values

    # Comparar variables numéricas y categóricas.
    numericas = tabla_numericas(perfil)
    categoricas = tabla_categoricas(perfil)

    # Cambiar los nombres para reflejar que se comparan grupos de riesgo.
    numericas = numericas.rename(columns={
        "mediana_abandona": "mediana_alto_riesgo",
        "q1_abandona": "q1_alto_riesgo",
        "q3_abandona": "q3_alto_riesgo",
        "mediana_permanece": "mediana_restantes",
        "q1_permanece": "q1_restantes",
        "q3_permanece": "q3_restantes"
    })

    categoricas = categoricas.rename(columns={
        "tasa_churn": "proporcion_alto_riesgo"
    })

    return numericas, categoricas

