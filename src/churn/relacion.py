"""Objetivo específico 1: variables con mayor relación con el abandono.

Dueño: Juanes (bloque 1). Firmas acordadas.
"""
import pandas as pd


def correlacion_con_churn(df: pd.DataFrame) -> pd.DataFrame:
    """Correlación de cada predictor con churn (punto-biserial y Spearman),
    ordenada por valor absoluto. Columnas: variable, grupo, pearson_pb, spearman, p_valor.

    Una fila por predictor (sin `fila_original` ni `churn`). `grupo` sale de
    config.USO / SERVICIO / SUSCRIPCION / DEMOGRAFIA.
    Referencia (base cruda): quejas 0.53, estado 0.50, frecuencia_llamadas -0.30.
    """
    raise NotImplementedError


def tasa_por_categoria(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """Tasa de churn y n por cada nivel de `columna`.

    Columnas: nivel, n, tasa_churn. Referencia (base cruda): con queja 0.83, sin queja 0.10.
    """
    raise NotImplementedError


def redundancias(df: pd.DataFrame, umbral: float = 0.8) -> pd.DataFrame:
    """Pares de predictores con |correlación| >= umbral y VIF de cada predictor.

    Columnas: var_1, var_2, r, vif_1, vif_2 (una fila por par).
    Referencia (base limpia, sin grupo_edad): segundos_uso–frecuencia_llamadas r = 0.95
    y frecuencia_sms–valor_cliente r = 0.92.
    """
    raise NotImplementedError
