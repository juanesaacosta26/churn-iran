"""Objetivo específico 2: caracterizar a quienes abandonan vs. quienes permanecen.

Dueña: Ianis (bloque 2). Firmas acordadas; no cambiarlas sin hablarlo en la reunión.
"""
import pandas as pd


def tabla_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """Por cada variable numérica: mediana, Q1 y Q3 en cada grupo de churn,
    p-valor de Mann-Whitney y tamaño del efecto (r o delta de Cliff).
    Una fila por variable, ordenada por tamaño del efecto.

    Columnas: variable, mediana_abandona, q1_abandona, q3_abandona,
    mediana_permanece, q1_permanece, q3_permanece, p_valor, efecto.
    Ordenar por |efecto| de mayor a menor.
    Referencia: segundos_uso 1256.5 vs 3596.5; frecuencia_llamadas 29 vs 64.
    """
    raise NotImplementedError


def tabla_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    """Por cada variable categórica y nivel: n, tasa de churn y p-valor de chi².

    Columnas: variable, nivel, n, tasa_churn, p_valor.
    Referencia: con queja 0.826 vs 0.098; no activo 0.475 vs activo 0.056;
    contrato 0.026 vs pago por uso 0.168.
    """
    raise NotImplementedError
