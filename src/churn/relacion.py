"""Objetivo específico 1: variables con mayor relación con el abandono.

Dueño: Juanes (bloque 1). Firmas acordadas.
"""
import numpy as np
import pandas as pd
from scipy import stats

from churn import config

# Columnas que nunca son predictores: el identificador y el objetivo.
_NO_PREDICTORES = ("fila_original", config.OBJETIVO)


def _grupo_de(variable: str) -> str:
    """Devuelve el grupo de la pregunta (uso, servicio, suscripcion, demografia) de una variable."""
    for nombre, miembros in (
        ("uso", config.USO),
        ("servicio", config.SERVICIO),
        ("suscripcion", config.SUSCRIPCION),
        ("demografia", config.DEMOGRAFIA),
    ):
        if variable in miembros:
            return nombre
    return "otro"


def _predictores(df: pd.DataFrame) -> list:
    """Columnas del DataFrame que son predictores (todo menos fila_original y churn)."""
    return [c for c in df.columns if c not in _NO_PREDICTORES]


def correlacion_con_churn(df: pd.DataFrame) -> pd.DataFrame:
    """Correlación de cada predictor con churn (punto-biserial y Spearman),
    ordenada por valor absoluto. Columnas: variable, grupo, pearson_pb, spearman, p_valor.

    Una fila por predictor (sin `fila_original` ni `churn`). `grupo` sale de
    config.USO / SERVICIO / SUSCRIPCION / DEMOGRAFIA.
    Referencia (base cruda): quejas 0.53, estado 0.50, frecuencia_llamadas -0.30.
    """
    if config.OBJETIVO not in df.columns:
        raise KeyError(f"El DataFrame no tiene la columna objetivo '{config.OBJETIVO}'")
    y = df[config.OBJETIVO].astype(float)

    filas = []
    for var in _predictores(df):
        x = df[var].astype(float)
        if x.nunique() < 2:  # una columna constante no tiene correlación definida
            r_pb = rho = p = np.nan
        else:
            # Punto-biserial = Pearson entre una variable continua y una binaria (0/1).
            r_pb, p = stats.pointbiserialr(y, x)
            # Spearman = Pearson sobre rangos: robusta a colas largas y atípicos.
            rho, _ = stats.spearmanr(y, x)
        filas.append({
            "variable": var,
            "grupo": _grupo_de(var),
            "pearson_pb": float(r_pb),
            "spearman": float(rho),
            "p_valor": float(p),
        })

    tabla = pd.DataFrame(filas, columns=["variable", "grupo", "pearson_pb", "spearman", "p_valor"])
    orden = tabla["pearson_pb"].abs().sort_values(ascending=False, na_position="last").index
    return tabla.loc[orden].reset_index(drop=True)


def tasa_por_categoria(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """Tasa de churn y n por cada nivel de `columna`.

    Columnas: nivel, n, tasa_churn. Referencia (base cruda): con queja 0.83, sin queja 0.10.
    """
    if columna not in df.columns:
        raise KeyError(f"La columna '{columna}' no está en el DataFrame")
    if columna in _NO_PREDICTORES:
        raise ValueError(f"'{columna}' no es un predictor: no tiene sentido calcular su tasa de churn")

    tabla = (
        df.groupby(columna, dropna=False)[config.OBJETIVO]
        .agg(n="size", tasa_churn="mean")
        .reset_index()
        .rename(columns={columna: "nivel"})
        .sort_values("nivel")
        .reset_index(drop=True)
    )
    tabla["n"] = tabla["n"].astype(int)
    return tabla[["nivel", "n", "tasa_churn"]]


def redundancias(df: pd.DataFrame, umbral: float = 0.8) -> pd.DataFrame:
    """Pares de predictores con |correlación| >= umbral y VIF de cada predictor.

    Columnas: var_1, var_2, r, vif_1, vif_2 (una fila por par).
    Referencia (base limpia, sin grupo_edad): segundos_uso–frecuencia_llamadas r = 0.95
    y frecuencia_sms–valor_cliente r = 0.92.
    """
    raise NotImplementedError
