"""Objetivo específico 2: caracterizar a quienes abandonan vs. quienes permanecen.

Dueña: Ianis (Semana 2). Firmas acordadas; no cambiarlas sin hablarlo en la reunión.
"""
import pandas as pd


def tabla_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """Por cada variable numérica: mediana, Q1 y Q3 en cada grupo de churn,
    p-valor de Mann-Whitney y tamaño del efecto (r o delta de Cliff).
    Una fila por variable, ordenada por tamaño del efecto."""
    raise NotImplementedError


def tabla_categoricas(df: pd.DataFrame) -> pd.DataFrame:
    """Por cada variable categórica y nivel: n, tasa de churn y p-valor de chi²."""
    raise NotImplementedError
