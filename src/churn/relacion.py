"""Objetivo específico 1: variables con mayor relación con el abandono.

Dueño: Juanes (Semana 1). Firmas acordadas.
"""
import pandas as pd


def correlacion_con_churn(df: pd.DataFrame) -> pd.DataFrame:
    """Correlación de cada predictor con churn (punto-biserial y Spearman),
    ordenada por valor absoluto. Columnas: variable, grupo, pearson_pb, spearman, p_valor."""
    raise NotImplementedError


def tasa_por_categoria(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """Tasa de churn y n por cada nivel de `columna`."""
    raise NotImplementedError


def redundancias(df: pd.DataFrame, umbral: float = 0.8) -> pd.DataFrame:
    """Pares de predictores con |correlación| >= umbral y VIF de cada predictor."""
    raise NotImplementedError
